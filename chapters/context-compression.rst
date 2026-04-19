.. _chapter-context-compression:

上下文压缩：当对话超出 Token 限制
========================================================

.. contents::
   :depth: 3
   :local:

为什么需要上下文压缩
------------------------

Token 限制的现实
~~~~~~~~~~~~~~~~~~

任何大型语言模型都有一个不可逾越的物理边界——**上下文窗口长度（context length）** 。
无论是 GPT-4 的 128K、Claude 的 200K，还是开源模型的 8K~32K，
当对话历史不断累积，发送给模型的 ``prompt_tokens`` 终将触及这个上限。
此时 API 调用会返回错误（通常是 ``context_length_exceeded`` 或 HTTP 400），
对话将无法继续。

对于一个长时间运行的 Agent（如 Hermes）来说，这几乎是必然事件。
在一次典型的编程会话中，Agent 会反复读写文件、搜索代码、执行终端命令，
每个工具调用的输入和输出都会被追加到消息历史中。
一个中等复杂度的重构任务很容易产生超过 50K token 的对话历史，
而长时间的调试会话可能超过 200K token。

成本和延迟的影响
~~~~~~~~~~~~~~~~~~

即使在上下文窗口之内，过长的对话历史也会带来两个严重问题：

**成本线性增长。** 大多数 LLM 提供商按 token 计费，``prompt_tokens`` 包含
完整的对话历史。如果一个 100 轮的对话历史占用了 80K token，
那么每发送一条新消息都要为这 80K token 付费——即使其中大部分内容
（例如早期的文件读取结果）已经不再相关。

**延迟线性增长。** 模型处理输入的时间与 token 数量成正比。
在 200K token 的对话历史中，每条新消息的响应延迟可能是 5K token 时的 10 倍以上。

因此，**上下文压缩不仅是避免错误的手段，更是控制成本和延迟的核心机制。**

简单截断 vs. 结构化压缩
~~~~~~~~~~~~~~~~~~~~~~~~~

最简单的方案是"删掉旧消息"。但这会带来严重的信息丢失：

- 用户早期提出的约束条件（"不要使用 pandas，只用标准库"）被遗忘
- 已完成的工作被重复执行（Agent 不知道某个 bug 已经修复）
- 上下文中的关键决策（"我们决定用 Redis 而不是 Memcached"）丢失

Hermes 选择了**结构化压缩（structured compression）** 方案：
用一个 LLM 生成结构化摘要，保留关键信息，同时大幅缩减 token 数量。
这是唯一能在"保留信息"和"缩减 token"之间取得合理平衡的方法。

.. note::

   术语说明：在 Hermes 代码库中，"压缩"和"compaction"是同义词。
   配置项使用 ``threshold_percent`` ，内部类名使用 ``ContextCompressor`` 。
   本文中交替使用这两个术语。

压缩引擎抽象（ContextEngine ABC）
-------------------------------------

设计理念
~~~~~~~~~~

Hermes 的上下文压缩不是硬编码在主循环中，而是通过一个抽象基类
``ContextEngine`` 来实现的。这个设计允许第三方插件（如 LCM、RAG）
替换默认的压缩行为，而无需修改核心代码。

ContextEngine 定义在 ``agent/context_engine.py`` 中，约 185 行，
是整个压缩子系统的接口契约：

.. code-block:: python

    class ContextEngine(ABC):
        """Base class all context engines must implement."""

        @property
        @abstractmethod
        def name(self) -> str:
            """Short identifier (e.g. 'compressor', 'lcm')."""

        @abstractmethod
        def update_from_response(self, usage: Dict[str, Any]) -> None:
            """Update tracked token usage from an API response."""

        @abstractmethod
        def should_compress(self, prompt_tokens: int = None) -> bool:
            """Return True if compaction should fire this turn."""

        @abstractmethod
        def compress(
            self,
            messages: List[Dict[str, Any]],
            current_tokens: int = None,
        ) -> List[Dict[str, Any]]:
            """Compact the message list and return the new message list."""

核心接口
~~~~~~~~~~

ContextEngine 的接口可以分为四个层次：

**身份标识层：** ``name`` 属性返回引擎的唯一标识符。
内置的 ``ContextCompressor`` 返回 ``"compressor"`` 。
插件系统通过 ``context.engine`` 配置项选择引擎。

**Token 状态层：** 引擎必须维护以下状态变量，
``run_agent.py`` 在每轮迭代后直接读取它们：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 变量名
     - 含义
   * - ``last_prompt_tokens``
     - 最近一次 API 调用的 prompt token 数
   * - ``last_completion_tokens``
     - 最近一次 API 调用的 completion token 数
   * - ``last_total_tokens``
     - 总 token 数
   * - ``threshold_tokens``
     - 触发压缩的阈值
   * - ``context_length``
     - 模型的上下文窗口长度
   * - ``compression_count``
     - 本次会话中已执行的压缩次数

**决策层：** ``should_compress()`` 决定是否触发压缩。
``should_compress_preflight()`` 是可选的快速估算（默认返回 False），
用于在发送 API 请求之前进行粗略检查。

**执行层：** ``compress()`` 是核心方法，接收完整的消息列表，
返回压缩后的消息列表。

可选扩展
~~~~~~~~~~

ContextEngine 还提供了多个可选的 hook 方法：

.. code-block:: python

    # 会话生命周期
    def on_session_start(self, session_id, **kwargs): ...
    def on_session_end(self, session_id, messages): ...
    def on_session_reset(self): ...

    # 引擎提供的工具（如 LCM 的 lcm_grep）
    def get_tool_schemas(self) -> List[Dict]: ...
    def handle_tool_call(self, name, args, **kwargs) -> str: ...

    # 状态显示
    def get_status(self) -> Dict[str, Any]: ...

    # 模型切换
    def update_model(self, model, context_length, ...): ...

引擎的生命周期遵循严格的顺序：

1. 引擎被实例化并注册（插件 ``register()`` 或默认创建）
2. ``on_session_start()`` 在新对话开始时调用
3. ``update_from_response()`` 在每次 API 响应后调用
4. ``should_compress()`` 在每轮迭代后检查
5. ``compress()`` 在 ``should_compress()`` 返回 True 时调用
6. ``on_session_end()`` 在会话真正结束时调用（CLI 退出、``/reset`` 、网关超时）

插件选择机制
~~~~~~~~~~~~~~

引擎通过配置文件选择。在 ``config.yaml`` 中：

.. code-block:: yaml

    context:
      engine: "compressor"    # 默认值

Hermes 会在 ``plugins/context_engine/<name>/`` 目录下查找对应的引擎实现。
如果配置项为空或未设置，则使用内置的 ``ContextCompressor`` 。

触发条件与阈值设计
------------------------

基础阈值：threshold_percent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ContextCompressor`` 的构造函数接受一个 ``threshold_percent`` 参数，
默认值为 **0.50（50%）** 。这意味着当 ``prompt_tokens`` 达到模型上下文窗口的
50% 时，压缩就会被触发：

.. code-block:: python

    self.threshold_tokens = max(
        int(self.context_length * threshold_percent),
        MINIMUM_CONTEXT_LENGTH,
    )

这里有一个关键的 ``max()`` 保护：阈值不会低于 ``MINIMUM_CONTEXT_LENGTH`` 。
这防止了在大上下文模型（如 200K token）上过早触发压缩——
50% 的 200K 是 100K，已经足够触发，但 50% 的 8K 只有 4K，
可能太早了。

.. note::

   为什么是 50% 而不是 80% 或 90%？因为压缩本身需要时间：
   LLM 生成摘要可能需要 5-15 秒，在此期间对话无法继续。
   50% 的阈值给系统留出了足够的余量，避免在极端情况下
   API 在压缩完成之前就拒绝请求。

反抖动保护（Anti-Thrashing）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果压缩效果不好——例如只删除了很少的消息——下一次迭代又会立即触发压缩，
形成无限循环。为了防止这种情况，``ContextCompressor`` 实现了反抖动机制：

.. code-block:: python

    def should_compress(self, prompt_tokens=None) -> bool:
        tokens = prompt_tokens or self.last_prompt_tokens
        if tokens < self.threshold_tokens:
            return False
        # Anti-thrashing: back off if recent compressions were ineffective
        if self._ineffective_compression_count >= 2:
            logger.warning(
                "Compression skipped — last %d compressions saved <10%% each.",
                self._ineffective_compression_count,
            )
            return False
        return True

逻辑很简单：如果连续两次压缩的节省比例都低于 10%，
就停止压缩并建议用户使用 ``/new`` 开始新会话。

在 ``compress()`` 方法的末尾，压缩效果被记录：

.. code-block:: python

    savings_pct = (saved_estimate / display_tokens * 100)
    self._last_compression_savings_pct = savings_pct
    if savings_pct < 10:
        self._ineffective_compression_count += 1
    else:
        self._ineffective_compression_count = 0

完整的触发决策流程如下：

.. mermaid::

   flowchart TD
       A["API 响应返回<br/>update_from_response()"] --> B{"prompt_tokens >=<br/>threshold_tokens?"}
       B -- 否 --> Z["正常继续"]
       B -- 是 --> C{"连续 2 次压缩<br/>节省 < 10%?"}
       C -- 是 --> D["跳过压缩<br/>建议 /new"]
       C -- 否 --> E["触发 compress()"]
       E --> F["Phase 1: 工具结果修剪"]
       F --> G["Phase 2: 边界确定"]
       G --> H["Phase 3: LLM 摘要生成"]
       H --> I["Phase 4: 消息组装"]
       I --> J["Phase 5: Tool 对清理"]
       J --> K["计算节省比例"]
       K --> L{"节省 < 10%?"}
       L -- 是 --> M["_ineffective_count += 1"]
       L -- 否 --> N["_ineffective_count = 0"]
       M --> Z
       N --> Z

Phase 1: 工具结果修剪（_prune_old_tool_results）
---------------------------------------------------

为什么先修剪工具结果？
~~~~~~~~~~~~~~~~~~~~~~~~

LLM 摘要生成是压缩流程中**最昂贵的操作**——它需要一次额外的 API 调用。
如果对话历史中充满了大量重复或冗余的工具输出
（例如同一个文件被读取了 5 次，或一个终端命令输出了 3000 行日志），
直接将所有这些内容发送给摘要模型既浪费 token 又浪费时间。

因此，Phase 1 是一个**廉价的预处理步骤** ，不涉及 LLM 调用，
只做简单的字符串操作来缩减消息体积。

Hash 去重
~~~~~~~~~~~

第一步是**内容哈希去重** 。Agent 经常多次读取同一个文件
（例如修改后重新读取来验证结果）。``_prune_old_tool_results`` 使用
MD5 哈希的前 12 个字符作为指纹：

.. code-block:: python

    content_hashes: dict = {}  # hash -> (index, tool_call_id)
    for i in range(len(result) - 1, -1, -1):
        msg = result[i]
        if msg.get("role") != "tool":
            continue
        content = msg.get("content") or ""
        if isinstance(content, list):
            continue  # 跳过多模态内容
        if len(content) < 200:
            continue  # 短内容不值得去重
        h = hashlib.md5(content.encode("utf-8", errors="replace")).hexdigest()[:12]
        if h in content_hashes:
            result[i] = {**msg, "content":
                "[Duplicate tool output — same content as a more recent call]"}
        else:
            content_hashes[h] = (i, msg.get("tool_call_id", "?"))

关键细节：

- **从后向前遍历** ：保留最新的完整副本，替换较旧的重复
- **跳过小于 200 字符的内容** ：去重的收益不值得哈希计算的开销
- **跳过多模态内容** （list 类型的 content）：无法简单地哈希
- 去重发生在修剪之前，所以被标记为重复的内容后续不会再被摘要化

28 种工具摘要器
~~~~~~~~~~~~~~~~~

去重之后，``_prune_old_tool_results`` 对边界之外的旧工具结果生成信息性摘要。
``_summarize_tool_result()`` 函数为 28 种不同的工具名称提供了专门的摘要格式：

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 工具名
     - 摘要格式示例
   * - ``terminal``
     - ``[terminal] ran \`npm test\` -> exit 0, 47 lines output``
   * - ``read_file``
     - ``[read_file] read config.py from line 1 (1,200 chars)``
   * - ``write_file``
     - ``[write_file] wrote to config.py (15 lines)``
   * - ``search_files``
     - ``[search_files] content search for 'compress' in agent/ -> 12 matches``
   * - ``patch``
     - ``[patch] replace in config.py (3,400 chars result)``
   * - ``web_search``
     - ``[web_search] query='hermes agent' (8,500 chars result)``
   * - ``browser_navigate``
     - ``[browser_navigate] https://example.com (12,000 chars)``
   * - ``delegate_task``
     - ``[delegate_task] 'fix the auth bug' (2,300 chars result)``
   * - ``execute_code``
     - ``[execute_code] \`import os; print(os.getcwd())\` (3 lines output)``
   * - ``vision_analyze``
     - ``[vision_analyze] 'describe the layout' (4,200 chars)``
   * - ``memory``
     - ``[memory] store on preferences``
   * - 其他
     - ``[tool_name] arg1=val1 arg2=val2 (N chars result)``

每个专门的摘要器都从工具参数中提取关键信息（命令、路径、模式等），
以及从结果内容中提取状态信息（退出码、匹配数、字符数等）。

工具参数 JSON 截断
~~~~~~~~~~~~~~~~~~~~

除了工具结果，Phase 1 还会截断**工具调用的参数** 。
一个 ``write_file`` 调用可能包含 50KB 的文件内容作为参数，
这些参数在对话历史中占据大量 token。

截断使用 ``_truncate_tool_call_args_json()`` 函数，
它会**解析 JSON、递归截断长字符串值、然后重新序列化** ：

.. code-block:: python

    def _shrink(obj):
        if isinstance(obj, str):
            if len(obj) > head_chars:  # head_chars = 200
                return obj[:head_chars] + "...[truncated]"
            return obj
        if isinstance(obj, dict):
            return {k: _shrink(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_shrink(v) for v in obj]
        return obj

为什么需要保持 JSON 有效性？因为一些模型提供者
（如 MiniMax）会严格验证 ``function.arguments`` 字段的 JSON 格式。
如果只是简单地从某个位置截断字符串并追加 ``...[truncated]`` ，
会产生无效的 JSON（例如未终止的字符串、缺少的闭合括号），
导致提供者返回 HTTP 400 错误，**整个会话卡死** 。
这是一个实际遇到过的 bug（issue #11762）。

修剪边界确定
~~~~~~~~~~~~~~

修剪操作只影响**尾部保护区域之外** 的消息。
尾部保护通过 token 预算实现：

.. code-block:: python

    # 从消息列表末尾向前遍历，累积 token 数
    for i in range(len(result) - 1, -1, -1):
        ...
        if accumulated + msg_tokens > protect_tail_tokens and (len(result) - i) >= min_protect:
            boundary = i
            break
        accumulated += msg_tokens

``protect_tail_tokens`` 默认等于 ``tail_token_budget`` ，
由 ``summary_target_ratio * threshold_tokens`` 计算，
对于典型的 128K 模型大约为 12-15K token。

完整的工具结果修剪流程：

.. mermaid::

   flowchart TD
       A["输入: 消息列表 +<br/>尾部保护预算"] --> B["构建索引:<br/>tool_call_id → (name, args)"]
       B --> C["确定修剪边界<br/>(token 预算向后累积)"]
       C --> D["Pass 1: Hash 去重<br/>(MD5, 保留最新副本)"]
       D --> E{"边界外有<br/>工具结果?"}
       E -- 否 --> G
       E -- 是 --> F["Pass 2: 替换为<br/>信息性摘要"]
       F --> G{"边界外有<br/>工具调用参数?"}
       G -- 否 --> H["返回 (修剪后的列表, 修剪计数)"]
       G -- 是 --> I["Pass 3: JSON 截断<br/>(保持有效性)"]
       I --> H

Phase 2: 边界确定
-------------------

三段式分割
~~~~~~~~~~~~

压缩的本质是将消息列表分为三段：

1. **头部（Head）** ：系统提示 + 最初的几轮对话，直接保留
2. **中间（Middle）** ：需要被压缩/摘要化的部分
3. **尾部（Tail）** ：最近的对话，直接保留

.. mermaid::

   flowchart LR
       subgraph Head["头部 (直接保留)"]
           direction TB
           H1["System Prompt"]
           H2["User Message #1"]
           H3["Assistant Reply #1"]
       end
       subgraph Middle["中间 (摘要化)"]
           direction TB
           M1["... 50+ 消息 ..."]
           M2["工具调用与结果"]
           M3["用户请求与回复"]
       end
       subgraph Tail["尾部 (直接保留)"]
           direction TB
           T1["最近 ~20K token"]
           T2["最新用户消息"]
           T3["最新助手回复"]
       end
       Head --> Middle --> Tail

头部保护：protect_first_n=3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

头部始终保护前 ``protect_first_n`` 条消息（默认 3 条）。
这通常包含：

1. 系统提示（system prompt）—— 包含 Agent 的身份、能力和约束
2. 第一条用户消息—— 通常包含用户的初始请求
3. 第一条助手回复—— 包含 Agent 对请求的理解和初步行动

这些消息是不可压缩的——系统提示定义了 Agent 的行为规则，
第一条用户消息定义了对话的起点。

尾部保护：Token 预算而非固定消息数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

早期版本使用固定消息数（如 "保留最后 20 条消息"）来保护尾部，
但这种方法在不同模型和不同使用模式下效果差异很大。

当前版本使用 **token 预算** 来保护尾部：

.. code-block:: python

    def _find_tail_cut_by_tokens(self, messages, head_end, token_budget=None):
        if token_budget is None:
            token_budget = self.tail_token_budget
        soft_ceiling = int(token_budget * 1.5)
        accumulated = 0
        cut_idx = n

        for i in range(n - 1, head_end - 1, -1):
            msg_tokens = len(content) // 4 + 10  # 粗略估算
            if accumulated + msg_tokens > soft_ceiling and (n - i) >= min_tail:
                break
            accumulated += msg_tokens
            cut_idx = i

``tail_token_budget`` 的计算公式：

.. math::

   \text{tail\_budget} = \text{threshold\_tokens} \times \text{summary\_target\_ratio}

其中 ``summary_target_ratio`` 默认为 0.20，即阈值 token 的 20%。
对于 128K 模型（阈值 64K），尾部预算约为 12.8K token。

**软上限（soft_ceiling）** 是预算的 1.5 倍，允许在遇到超大消息时
（如一个巨大的文件读取结果）稍微超出预算，避免在消息中间截断。

边界对齐：避免拆分工具调用组
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenAI API 要求消息列表中的工具调用和工具结果严格配对。
如果压缩边界恰好落在工具调用组的中间——例如保留了助手消息中的工具调用，
但删除了对应的工具结果——API 会返回错误。

因此有两个对齐函数：

**前向对齐（_align_boundary_forward）：** 如果压缩起始位置落在
工具结果上，向前滑动到第一个非工具消息。

.. code-block:: python

    def _align_boundary_forward(self, messages, idx):
        while idx < len(messages) and messages[idx].get("role") == "tool":
            idx += 1
        return idx

**后向对齐（_align_boundary_backward）：** 如果压缩结束位置落在
连续的工具结果中间，向后回退到父助手消息之前，
让整个"助手消息 + 工具结果"组一起进入摘要区域。

.. code-block:: python

    def _align_boundary_backward(self, messages, idx):
        check = idx - 1
        while check >= 0 and messages[check].get("role") == "tool":
            check -= 1
        if check >= 0 and messages[check].get("role") == "assistant" \
                and messages[check].get("tool_calls"):
            idx = check
        return idx

**最新用户消息保护：** 这是一个关键的安全措施（修复 issue #10896）。
如果最新的用户消息被错误地放入了中间区域（摘要化的部分），
LLM 摘要器会将它标记为"Pending User Asks"，但摘要前缀告诉下一个模型
只响应摘要之后的消息——导致用户的最新请求被"遗忘"。
``_ensure_last_user_message_in_tail()`` 确保最新的用户消息始终在尾部。

边界对齐流程：

.. mermaid::

   flowchart TD
       A["protect_first_n = 3<br/>初始 compress_start"] --> B["前向对齐<br/>跳过工具结果"]
       B --> C["_find_tail_cut_by_tokens()<br/>从末尾向前累积 token"]
       C --> D["后向对齐<br/>避免拆分工具组"]
       D --> E{"最新用户消息<br/>在尾部?"}
       E -- 是 --> F["确定最终边界"]
       E -- 否 --> G["将 cut_idx<br/>回退到用户消息处"]
       G --> F
       F --> H{"compress_start<br/>>= compress_end?"}
       H -- 是 --> I["无法压缩<br/>返回原始消息"]
       H -- 否 --> J["进入 Phase 3"]

Phase 3: LLM 摘要生成
------------------------

首次摘要 vs. 迭代更新
~~~~~~~~~~~~~~~~~~~~~~~

摘要生成有两种模式，取决于是否存在上一次压缩产生的摘要：

**首次压缩（self._previous_summary is None）：**
从零开始生成结构化摘要，覆盖所有被压缩的中间消息。

**迭代更新（self._previous_summary exists）：**
将之前的摘要与新产生的对话轮次合并，更新摘要内容。

迭代更新是 Hermes 压缩系统的一个关键设计。随着对话的进行，
压缩可能被触发多次。每次压缩都会产生一个摘要，下一次压缩时，
这个摘要会被保留并更新，而不是从零重新生成。这确保了信息的累积性——
第 5 次压缩的摘要包含了从第 1 次压缩到第 5 次压缩之间所有关键信息。

摘要结构模板
~~~~~~~~~~~~~~

两种模式共享同一个结构化模板，包含以下字段：

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 字段名
     - 用途
   * - ``## Active Task``
     - **最重要的字段** 。用户最新的未完成请求的原文
   * - ``## Goal``
     - 用户的总体目标
   * - ``## Constraints & Preferences``
     - 用户的编码风格偏好和约束
   * - ``## Completed Actions``
     - 编号列表，每项包含工具名、目标和结果
   * - ``## Active State``
     - 当前工作目录、分支、已修改文件、测试状态
   * - ``## In Progress``
     - 压缩发生时正在进行的工作
   * - ``## Blocked``
     - 未解决的阻塞和错误
   * - ``## Key Decisions``
     - 重要技术决策及其原因
   * - ``## Resolved Questions``
     - 已回答的问题及答案
   * - ``## Pending User Asks``
     - 未回答的用户请求
   * - ``## Relevant Files``
     - 涉及的文件及说明
   * - ``## Remaining Work``
     - 剩余工作（作为上下文，不是指令）
   * - ``## Critical Context``
     - 不显式保留就会丢失的具体值

``## Active Task`` 被标记为"最重要的字段"是有原因的。
它直接决定了下一个模型实例从哪里继续工作。如果这个字段不准确，
Agent 可能会重复已完成的工作，或者跳过未完成的任务。

摘要模型的提示词设计
~~~~~~~~~~~~~~~~~~~~~~

摘要提示词包含几个精心的设计：

**身份分离（Handoff Framing）：**
提示词明确告诉摘要模型"你是一个摘要 Agent，正在为另一个不同的助手创建上下文检查点"。
这来自 Codex 的"another language model"设计理念。
通过创建身份分离，摘要模型不会试图继续用户的对话，而是专注于生成结构化的信息摘要。

**"不要回答问题"指令：**
来自 OpenCode 的设计理念。摘要模型可能看到用户在对话中提出的问题，
如果它试图回答这些问题，摘要就会偏离其目的。

**"Remaining Work"而非"Next Steps"：**
"Next Steps"可能被下一个模型误解为需要执行的指令，
而"Remaining Work"更准确地表达为"上下文信息"。

摘要的 Token 预算
~~~~~~~~~~~~~~~~~~~

摘要预算不是固定的，而是根据被压缩内容的大小动态计算：

.. code-block:: python

    def _compute_summary_budget(self, turns_to_summarize):
        content_tokens = estimate_messages_tokens_rough(turns_to_summarize)
        budget = int(content_tokens * _SUMMARY_RATIO)  # 0.20
        return max(_MIN_SUMMARY_TOKENS, min(budget, self.max_summary_tokens))

参数说明：

- ``_SUMMARY_RATIO = 0.20`` ：摘要目标是被压缩内容的 20%
- ``_MIN_SUMMARY_TOKENS = 2000`` ：最小预算，确保短对话也有足够的摘要空间
- ``_SUMMARY_TOKENS_CEILING = 12_000`` ：绝对上限，防止大上下文模型产生过长的摘要

``max_summary_tokens`` 额外受模型上下文长度的 5% 约束：

.. code-block:: python

    self.max_summary_tokens = min(
        int(self.context_length * 0.05),
        _SUMMARY_TOKENS_CEILING,
    )

序列化与截断
~~~~~~~~~~~~~~

发送给摘要模型的内容经过精心序列化。
每条消息的格式取决于角色：

- **工具结果：** ``[TOOL RESULT tool_call_id]: content``
- **助手消息：** ``[ASSISTANT]: content\n[Tool calls:\n  name(args)\n]``
- **用户消息：** ``[USER]: content``

每条消息的内容有截断限制：
- 总长度上限 6000 字符
- 保留头部 4000 字符 + 尾部 1500 字符
- 工具调用参数上限 1500 字符（保留头部 1200 字符）

这种"头+尾"截断策略确保了摘要模型能看到内容的开头和结尾——
开头通常包含查询参数，结尾通常包含最终结果。

焦点话题（Focus Topic）
~~~~~~~~~~~~~~~~~~~~~~~~~

用户可以通过 ``/compress <topic>`` 命令提供焦点话题。
当提供了焦点话题时，摘要提示词末尾会追加额外的指导：

- 与焦点话题相关的内容：包含完整细节（具体值、文件路径、命令输出）
- 不相关的内容：更激进地压缩（简短的一行描述或完全省略）
- 焦点话题相关部分获得约 60-70% 的摘要 token 预算

摘要生成的时序图：

.. mermaid::

   sequenceDiagram
       participant C as ContextCompressor
       participant S as 序列化器
       participant LLM as 摘要 LLM
   
       C->>C: _compute_summary_budget()
       C->>S: _serialize_for_summary(turns)
       S->>S: 逐条截断 (6000 chars/msg)
       S-->>C: 序列化文本
   
       alt 首次压缩
           C->>LLM: 首次摘要提示词<br/>+ 序列化文本
       else 迭代更新
           C->>LLM: 更新提示词<br/>+ 之前的摘要<br/>+ 新的序列化文本
       end
   
       alt LLM 成功
           LLM-->>C: 结构化摘要文本
           C->>C: _with_summary_prefix()
           C->>C: 存储 _previous_summary
       else 无提供者 (RuntimeError)
           LLM-->>C: 异常
           C->>C: 冷却 600 秒
           C-->>C: 返回 None
       else 模型未找到 (404/503)
           LLM-->>C: 异常
           C->>C: 回退到主模型
           C->>LLM: 用主模型重试
       else 瞬时错误 (超时/限速)
           LLM-->>C: 异常
           C->>C: 冷却 60 秒
           C-->>C: 返回 None
       end

Phase 4: 消息组装
-------------------

组装流程
~~~~~~~~~~

摘要生成后，需要将头部、摘要和尾部组装成新的消息列表：

.. code-block:: python

    compressed = []

    # 1. 复制头部消息
    for i in range(compress_start):
        msg = messages[i].copy()
        if i == 0 and msg.get("role") == "system":
            # 在系统提示中追加压缩通知
            msg["content"] += "\n\n" + _compression_note
        compressed.append(msg)

    # 2. 插入摘要消息
    compressed.append({"role": summary_role, "content": summary})

    # 3. 复制尾部消息
    for i in range(compress_end, n_messages):
        compressed.append(messages[i].copy())

系统提示注入
~~~~~~~~~~~~~~

压缩后，系统提示会被注入一条额外的通知：

.. code-block:: text

    [Note: Some earlier conversation turns have been compacted into a
    handoff summary to preserve context space. The current session state
    may still reflect earlier work, so build on that summary and state
    rather than re-doing work.]

这条通知告诉模型"上下文被压缩过，当前文件系统状态可能已经反映了之前的工作，
不要重复做"。

摘要前缀（SUMMARY_PREFIX）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

每条摘要都附带一个标准前缀，这是摘要"协议"的核心：

.. code-block:: text

    [CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted
    into the summary below. This is a handoff from a previous context
    window — treat it as background reference, NOT as active instructions.
    Do NOT answer questions or fulfill requests mentioned in this summary;
    they were already addressed. Your current task is identified in the
    '## Active Task' section of the summary — resume exactly from there.
    Respond ONLY to the latest user message that appears AFTER this summary.

这个前缀解决了几个关键问题：

1. **防止模型"回答"摘要中的问题**——那些问题已经被回答过了
2. **明确任务延续点**——通过"## Active Task"字段
3. **创建上下文边界**——模型知道摘要之前和之后是不同的上下文

角色选择与冲突避免
~~~~~~~~~~~~~~~~~~~~

OpenAI API 要求消息列表中相邻消息不能有相同的角色
（例如不能连续两条 ``user`` 消息）。
摘要消息的角色需要精心选择以避免冲突。

选择逻辑考虑头部最后一条消息的角色和尾部第一条消息的角色：

1. 如果头部最后是 ``assistant`` 或 ``tool`` ，摘要用 ``user``
2. 否则摘要用 ``assistant``
3. 如果摘要角色与尾部第一条消息冲突，尝试翻转
4. 如果翻转后与头部冲突，**将摘要合并到尾部第一条消息**

合并策略在尾部第一条消息的内容前插入摘要文本，并用分隔符标记：

.. code-block:: text

    [SUMMARY]
    --- END OF CONTEXT SUMMARY — respond to the message below, ---
     --- not the summary above ---
    [ACTUAL TAIL MESSAGE]

Phase 5: Tool 对清理
----------------------

工具调用的配对约束
~~~~~~~~~~~~~~~~~~~~

OpenAI API 有一条严格规则：**每个工具调用必须有对应的工具结果，反之亦然。**
压缩过程可能破坏这种配对关系：

- 场景 1：工具结果在摘要区域，但对应的助手消息中的工具调用在尾部
  → 孤儿结果（orphaned result）
- 场景 2：助手消息中的工具调用在摘要区域，但对应的工具结果在尾部
  → 孤儿调用（orphaned call）

``_sanitize_tool_pairs()`` 处理这两种情况：

.. code-block:: python

    def _sanitize_tool_pairs(self, messages):
        # 1. 收集所有幸存的工具调用 ID
        surviving_call_ids = set()
        for msg in messages:
            if msg.get("role") == "assistant":
                for tc in msg.get("tool_calls") or []:
                    cid = self._get_tool_call_id(tc)
                    if cid:
                        surviving_call_ids.add(cid)

        # 2. 收集所有工具结果引用的 ID
        result_call_ids = set()
        for msg in messages:
            if msg.get("role") == "tool":
                cid = msg.get("tool_call_id")
                if cid:
                    result_call_ids.add(cid)

        # 3. 删除孤儿结果
        orphaned_results = result_call_ids - surviving_call_ids
        if orphaned_results:
            messages = [m for m in messages
                if not (m.get("role") == "tool"
                        and m.get("tool_call_id") in orphaned_results)]

        # 4. 为孤儿调用插入桩结果
        missing_results = surviving_call_ids - result_call_ids
        if missing_results:
            for msg in messages:
                patched.append(msg)
                if msg.get("role") == "assistant":
                    for tc in msg.get("tool_calls") or []:
                        cid = self._get_tool_call_id(tc)
                        if cid in missing_results:
                            patched.append({
                                "role": "tool",
                                "content": "[Result from earlier conversation "
                                           "— see context summary above]",
                                "tool_call_id": cid,
                            })

这个清理步骤确保了压缩后的消息列表始终是 API 兼容的。

失败降级和迭代压缩
--------------------

摘要生成失败的降级策略
~~~~~~~~~~~~~~~~~~~~~~~~

摘要生成可能因多种原因失败：无 LLM 提供者、网络超时、模型不存在等。
``_generate_summary()`` 对不同的失败类型有不同的处理策略：

**无提供者（RuntimeError）：**
进入长冷却（600 秒），因为不太可能自行恢复。
中间消息仍然会被移除，但不会生成摘要。

**模型不存在（404/503）：**
如果使用了专门的摘要模型（``summary_model_override``）且该模型不可用，
自动回退到主模型并立即重试。这是一个**一次性的** 回退——设置了
``_summary_model_fallen_back`` 标志后，后续压缩始终使用主模型。

**瞬时错误（超时、限速、网络）：**
短冷却（60 秒），因为这些错误通常是暂时的。

静态回退上下文标记
~~~~~~~~~~~~~~~~~~~~

当摘要生成完全失败时，不会静默丢弃所有中间消息。
而是插入一个静态的回退标记：

.. code-block:: text

    [CONTEXT COMPACTION — REFERENCE ONLY]
    Summary generation was unavailable. 42 conversation turns were
    removed to free context space but could not be summarized.
    The removed turns contained earlier work in this session.
    Continue based on the recent messages below and the current
    state of any files or resources.

虽然这比结构化摘要差得多，但至少告诉模型"有些上下文丢失了"，
而不是让它困惑于为什么对话看起来不连贯。

迭代压缩的效果追踪
~~~~~~~~~~~~~~~~~~~~

每次压缩后，系统会计算并记录节省比例：

.. code-block:: python

    new_estimate = estimate_messages_tokens_rough(compressed)
    saved_estimate = display_tokens - new_estimate
    savings_pct = (saved_estimate / display_tokens * 100)

这个比例被用于两个目的：

1. **反抖动判断** ：如果连续两次节省比例低于 10%，停止压缩
2. **日志记录** ：帮助开发者理解压缩效果

典型的压缩效果：

- 首次压缩：节省 40-60%（摘要 + 修剪工具结果）
- 第二次压缩：节省 20-35%（主要靠修剪新产生的工具结果）
- 后续压缩：节省逐渐降低，最终触发反抖动

配置参数速查表
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 参数名
     - 默认值
     - 说明
   * - ``threshold_percent``
     - 0.50
     - 触发压缩的阈值比例
   * - ``protect_first_n``
     - 3
     - 头部保护的消息数
   * - ``protect_last_n``
     - 20
     - 尾部保护的最小消息数
   * - ``summary_target_ratio``
     - 0.20
     - 摘要目标大小占阈值的比例
   * - ``_MIN_SUMMARY_TOKENS``
     - 2000
     - 摘要最小 token 数
   * - ``_SUMMARY_RATIO``
     - 0.20
     - 摘要占被压缩内容的比例
   * - ``_SUMMARY_TOKENS_CEILING``
     - 12000
     - 摘要最大 token 数
   * - ``_CONTENT_MAX``
     - 6000
     - 摘要输入中每条消息的最大字符数
   * - ``_CONTENT_HEAD``
     - 4000
     - 摘要输入保留的消息头部字符数
   * - ``_CONTENT_TAIL``
     - 1500
     - 摘要输入保留的消息尾部字符数
   * - ``_SUMMARY_FAILURE_COOLDOWN_SECONDS``
     - 600
     - 摘要失败后的冷却时间

总结
------

Hermes 的上下文压缩系统是一个精心设计的多层机制：

1. **Phase 1（工具修剪）** 是廉价的预处理，用启发式规则而非 LLM
2. **Phase 2（边界确定）** 平衡了信息保留和 API 约束
3. **Phase 3（LLM 摘要）** 是核心，用结构化模板确保信息完整性
4. **Phase 4（消息组装）** 处理了角色冲突等边缘情况
5. **Phase 5（Tool 对清理）** 保证了 API 兼容性
6. **反抖动机制** 防止了无效压缩的无限循环
7. **失败降级** 确保了即使摘要失败，对话也能继续

这个系统使得 Hermes 能够在几乎无限长的会话中持续工作，
同时保持合理的成本和延迟。
