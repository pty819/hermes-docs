.. _agent-loop:

核心循环：Agent Loop 的完整生命周期
======================================

本章是全书最重要的章节。我们将深入 ``run_agent.py`` 中 ``AIAgent`` 类的
``run_conversation()`` 方法，逐行分析一个生产级 Agent 的核心循环是如何工作的。

如果你只能读本书的一个章节，请读这一个。

第一节：AIAgent 类的架构
--------------------------

类概览
~~~~~~~~

``AIAgent`` 是 Hermes Agent 的核心类。它位于 ``run_agent.py:588`` ，
是一个超过 11000 行的巨型类。在传统 OOP 意义上，这样一个大类可能被视为
"代码坏味道"——但在 Agent 系统中，主循环需要访问几乎所有子系统的状态，
将它们分散到多个类中反而会增加状态传递的复杂度。

让我们将 ``AIAgent`` 的属性按职责分组来理解。

属性分组
^^^^^^^^^^

**API / 客户端层** —— 负责与 LLM 提供商通信：

- ``client`` ：OpenAI SDK 客户端实例（chat_completions / codex_responses 模式）
- ``_anthropic_client`` ：Anthropic SDK 客户端实例（anthropic_messages 模式）
- ``api_key`` ：当前使用的 API 密钥
- ``base_url`` ：API 端点 URL
- ``provider`` ：提供商标识符（``"openrouter"`` 、``"anthropic"`` 、``"bedrock"`` 等）
- ``api_mode`` ：API 调用模式（``"chat_completions"`` 、``"codex_responses"`` 、
  ``"anthropic_messages"`` 、``"bedrock_converse"``）
- ``model`` ：当前使用的模型名称
- ``_client_kwargs`` ：客户端构造参数

**工具层** —— 管理可用的工具集：

- ``tools`` ：传递给 API 的工具 schema 列表
- ``valid_tool_names`` ：当前会话中所有可用工具的名称集合
- ``enabled_toolsets`` / ``disabled_toolsets`` ：工具集过滤配置

**记忆与上下文层** —— 管理对话状态和长期记忆：

- ``_memory_store`` ：长期记忆存储实例
- ``_memory_manager`` ：外部记忆管理器（Honcho 等）
- ``_todo_store`` ：Todo 列表存储
- ``_session_db`` ：SQLite 会话数据库
- ``_cached_system_prompt`` ：缓存的系统提示词（用于 Anthropic 前缀缓存）
- ``context_compressor`` ：上下文压缩器实例

**预算与迭代控制** —— 防止 Agent 失控：

- ``max_iterations`` ：最大迭代次数（默认 90）
- ``iteration_budget`` ：``IterationBudget`` 实例，线程安全的迭代计数器
- ``_budget_exhausted_injected`` ：是否已注入预算耗尽提示
- ``_budget_grace_call`` ：是否处于宽限调用状态

**中断与回调** —— 外部交互接口：

- ``_interrupt_requested`` ：是否收到中断请求
- ``_pending_steer`` ：待注入的引导消息（不中断，在工具结果中追加）
- ``tool_progress_callback`` ：工具执行进度回调
- ``stream_delta_callback`` ：流式 token 回调
- ``clarify_callback`` ：用户澄清回调
- ``step_callback`` ：每步执行回调（网关用）

**会话统计** —— 监控与计费：

- ``session_prompt_tokens`` / ``session_completion_tokens`` ：token 使用统计
- ``session_estimated_cost_usd`` ：预估费用
- ``session_api_calls`` ：API 调用次数

类图
^^^^^^

.. mermaid::

   classDiagram
       class AIAgent {
           +model: str
           +provider: str
           +api_mode: str
           +max_iterations: int
           +tools: list
           +iteration_budget: IterationBudget
           +run_conversation() dict
           -_invoke_tool() str
           -_interruptible_streaming_api_call()
           -_compress_context()
           -_persist_session()
           -_execute_tool_calls()
           -_spawn_background_review()
       }
   
       class IterationBudget {
           +max_total: int
           +consume() bool
           +refund()
           +remaining: int
       }
   
       class ContextCompressor {
           +threshold_tokens: int
           +context_length: int
           +should_compress() bool
           +update_from_response()
       }
   
       class ToolRegistry {
           +register()
           +dispatch() str
           +get_definitions() list
           +get_all_tool_names() list
       }
   
       class ErrorClassifier {
           +classify_api_error() ClassifiedError
       }
   
       class SessionDB {
           +update_token_counts()
           +update_system_prompt()
           +get_session() dict
       }
   
       AIAgent *-- IterationBudget
       AIAgent *-- ContextCompressor
       AIAgent --> ToolRegistry : uses
       AIAgent --> ErrorClassifier : uses
       AIAgent --> SessionDB : persists to

构造函数 ``__init__`` （第 605-887 行）做了以下关键工作：

1. **确定 API 模式。** 根据提供商名称和 base URL 自动推断 API 模式。
   例如，如果 provider 是 ``"anthropic"`` 或 URL 包含 ``api.anthropic.com`` ，
   则使用 ``anthropic_messages`` 模式。这个自动推断机制避免了用户需要手动指定 API 模式。

2. **初始化 LLM 客户端。** 对于 Anthropic 模式，使用 ``anthropic`` SDK 的
   ``Anthropic`` 类；对于 Bedrock 模式，使用 ``AnthropicBedrock`` 类；
   对于其他模式，使用 ``openai`` SDK 的 ``OpenAI`` 类。

3. **加载工具。** 通过 ``get_tool_definitions()`` 获取经过工具集过滤的 schema 列表。

4. **初始化压缩器。** 创建 ``ContextCompressor`` 实例，配置压缩阈值。

5. **安装安全 stdio。** 通过 ``_install_safe_stdio()`` 包装 stdout/stderr，
   防止在 systemd/Docker/无头模式下因管道断裂导致的崩溃。

一个值得注意的设计决策是 **``_SafeWriter``** （第 113-160 行）。
它是一个 stdout/stderr 的透明包装器，捕获 ``OSError`` 和 ``ValueError`` ：
当 Hermes 运行为 systemd 服务或 Docker 容器时，stdout 管道可能在空闲时关闭，
任何 ``print()`` 调用都会抛出 ``OSError: [Errno 5] Input/output error`` 。
这个包装器确保即使管道断裂，Agent 也不会崩溃。这是一个典型的生产系统防护措施——
在 demo 中永远不会出现，但在 7x24 运行的服务中至关重要。

第二节：run_conversation() —— 主循环
----------------------------------------

方法签名
~~~~~~~~~~

``run_conversation()`` 定义在第 8668 行，是整个 Agent 的入口方法：

.. code-block:: python

   def run_conversation(
       self,
       user_message: str,
       system_message: str = None,
       conversation_history: List[Dict[str, Any]] = None,
       task_id: str = None,
       stream_callback: Optional[callable] = None,
       persist_user_message: Optional[str] = None,
   ) -> Dict[str, Any]:

参数说明：

- ``user_message`` ：用户输入的文本
- ``system_message`` ：可选的系统提示词覆盖
- ``conversation_history`` ：之前的对话历史
- ``task_id`` ：任务 ID，用于隔离终端/浏览器等有状态资源
- ``stream_callback`` ：流式 token 回调（用于 TTS 等）
- ``persist_user_message`` ：持久化时使用的干净用户消息（当 ``user_message`` 包含
  API 专用前缀时使用）

返回值是一个字典，包含 ``final_response`` （最终文本）、``messages`` （完整消息历史）、
``api_calls`` （API 调用次数）、``completed`` （是否正常完成）等字段。

完整的时序图
~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
       autonumber
       participant User as 用户
       participant RC as run_conversation()
       participant SP as 系统提示词构建
       participant CC as 上下文压缩
       participant API as LLM API
       participant TE as 工具执行引擎
   
       User->>RC: user_message + conversation_history
       RC->>RC: 输入清洗 (surrogate, memory-context)
       RC->>SP: 构建或加载缓存系统提示词
       SP-->>RC: system_prompt
       RC->>CC: 预压缩检查 (preflight)
       CC-->>RC: 压缩后的 messages (如果需要)
       RC->>RC: 注入插件上下文 (pre_llm_call)
   
       loop 主循环: api_call_count < max_iterations
           RC->>RC: 检查中断 + 消费迭代预算
           RC->>RC: 构建 api_messages (注入记忆/插件上下文)
           RC->>RC: 应用 Anthropic prompt caching
           RC->>RC: 消息清洗 (surrogate/ASCII)
   
           loop 内部重试: retry_count < 3
               RC->>API: 流式 API 调用
               alt 成功
                   API-->>RC: response
               else 错误
                   API-->>RC: Exception
                   RC->>RC: 分类错误 (ErrorClassifier)
                   alt 可恢复
                       RC->>RC: 抖动退避 + 恢复策略
                   else 不可恢复
                       RC-->>User: 返回错误
                   end
               end
           end
   
           RC->>RC: 解析 response (统一格式)
           alt finish_reason == "length"
               RC->>RC: 截断处理 (continuation/retry)
           end
   
           alt 有 tool_calls
               RC->>RC: 验证工具名 + 修复幻觉
               RC->>RC: 验证 JSON 参数
               RC->>TE: 执行工具 (并行或顺序)
               TE-->>RC: 工具结果
               RC->>RC: 追加 assistant + tool 消息
               RC->>RC: 检查是否需要压缩
           else 无 tool_calls (最终回复)
               RC-->>User: final_response
           end
       end
   
       RC->>RC: 会话持久化 + 资源清理
       RC-->>User: 返回结果字典

步骤详解
^^^^^^^^^^

**步骤 1-3：输入准备（第 8696-8766 行）**

.. code-block:: python

   _install_safe_stdio()
   set_session_context(self.session_id)
   self._restore_primary_runtime()

首先安装安全 stdio 包装器，设置日志的会话上下文（以便 ``hermes logs --session <id>``
可以过滤单次对话），然后恢复主运行时（如果上一轮激活了回退模型）。

接下来是输入清洗：

.. code-block:: python

   user_message = _sanitize_surrogates(user_message)  # 移除 U+D800-U+DFFF
   user_message = sanitize_context(user_message)       # 移除 <memory-context> 块

为什么要移除 surrogate 字符？因为从 Google Docs 或 Word 复制粘贴的富文本
可能包含孤立的 surrogate 代码点（U+D800 到 U+DFFF），这些字符在 UTF-8 中无效，
会导致 OpenAI SDK 内部的 ``json.dumps()`` 崩溃。这是一个典型的"真实世界输入永远不干净"的案例。

为什么要移除 ``<memory-context>`` 块？因为外部记忆提供商（如 Honcho）在保存消息时
可能将注入的上下文块也保存了，导致下一轮用户消息中出现过期的记忆标签。

**步骤 4-5：系统提示词与预压缩（第 8835-8943 行）**

系统提示词采用**缓存策略** ：首次构建后缓存在 ``_cached_system_prompt`` 中，
后续调用直接复用。这对于 Anthropic 的 prompt caching 至关重要——
如果系统提示词在每轮对话中都变化，前缀缓存就会失效，导致输入成本大幅增加。

对于继续的会话（网关模式，每次消息创建新的 AIAgent 实例），系统提示词从 SQLite
会话数据库中加载，确保与上一轮完全一致：

.. code-block:: python

   if self._cached_system_prompt is None:
       stored_prompt = None
       if conversation_history and self._session_db:
           session_row = self._session_db.get_session(self.session_id)
           if session_row:
               stored_prompt = session_row.get("system_prompt")
       if stored_prompt:
           self._cached_system_prompt = stored_prompt
       else:
           self._cached_system_prompt = self._build_system_prompt(system_message)

预压缩检查在主循环之前运行：如果加载的对话历史已经超过模型的上下文阈值，
就在进入循环前压缩。这处理了用户切换到更小上下文窗口模型的情况：

.. code-block:: python

   if self.compression_enabled and len(messages) > threshold:
       _preflight_tokens = estimate_request_tokens_rough(messages, ...)
       if _preflight_tokens >= self.context_compressor.threshold_tokens:
           for _pass in range(3):  # 最多 3 轮压缩
               messages, active_system_prompt = self._compress_context(...)

**步骤 6：主循环结构（第 9030-11298 行）**

主循环的核心结构是一个 ``while`` 循环：

.. code-block:: python

   while (api_call_count < self.max_iterations
          and self.iteration_budget.remaining > 0) or self._budget_grace_call:

循环条件有两个维度：硬上限（``max_iterations``）和共享预算（``iteration_budget``）。
``_budget_grace_call`` 是一个特殊标志——当预算耗尽时，它允许模型进行一次额外的
"宽限调用"来完成总结。这是一个精妙的设计：与其在预算耗尽时立即终止（可能导致
半成品的回复），不如给模型一次机会来收尾。

每次循环迭代包含以下步骤：

1. **中断检查** （第 9035 行）：如果用户发送了新消息，``_interrupt_requested`` 为 True，
   循环立即中断。

2. **预算消费** （第 9049-9055 行）：通过 ``iteration_budget.consume()`` 消费一个迭代。
   如果预算耗尽，设置 ``_budget_grace_call = True`` 允许一次额外迭代。

3. **API 消息构建** （第 9096-9213 行）：从 ``messages`` 构建发送给 API 的消息副本，
   注入记忆上下文、插件上下文、应用 prompt caching、清洗 surrogate 字符等。
   注意这里使用的是副本（``api_msg = msg.copy()``），原始 ``messages`` 不被修改。

4. **API 调用** （第 9264-9920 行）：在内部重试循环中调用 LLM API。
   最多重试 3 次，每次重试间使用抖动指数退避。

5. **响应解析** （第 10839-10870 行）：将不同 API 模式的响应统一为
   ``assistant_message`` 和 ``finish_reason`` 。

6. **工具调用处理** （第 11007-11298 行）：如果有工具调用，验证工具名和参数，
   执行工具，将结果追加到消息列表，然后 ``continue`` 继续循环。

7. **最终回复** （第 11300+ 行）：如果没有工具调用，将内容作为最终回复返回。

第三节：流式架构
------------------

三种 API 模式
~~~~~~~~~~~~~~~

Hermes 支持四种 API 模式，但核心流式处理涉及三种主流 LLM 协议：

**OpenAI Chat Completions**

这是最广泛支持的 API 模式。响应格式为：

.. code-block:: python

   response.choices[0].message.content      # 文本内容
   response.choices[0].message.tool_calls   # 工具调用列表
   response.choices[0].finish_reason        # 结束原因

流式响应通过 SSE（Server-Sent Events）返回 ``delta`` 对象：
前几个 chunk 包含部分文本（``delta.content``），
后续 chunk 可能包含工具调用（``delta.tool_calls``）。

**Anthropic Messages API**

Anthropic 使用不同的响应格式：

.. code-block:: python

   response.content      # ContentBlock 列表 (TextBlock / ToolUseBlock)
   response.stop_reason  # "end_turn" / "tool_use" / "max_tokens"

流式响应返回 ``event`` 对象，类型包括 ``content_block_start`` 、
``content_block_delta`` 、``content_block_stop`` 等。

**AWS Bedrock Converse API**

Bedrock 使用 boto3 风格的响应：

.. code-block:: python

   response['output']['message']['content']   # ContentBlock 列表
   response['stopReason']                      # "end_turn" / "tool_use" / ...

流式响应用 ``ConverseStream`` 返回事件流。

统一的 SimpleNamespace 响应模式
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hermes 的核心设计之一是将所有这些不同的响应格式统一为
``types.SimpleNamespace`` 对象。这意味着无论底层使用哪种 API 模式，
后续的响应处理代码都可以使用统一的属性访问方式：

.. code-block:: python

   # 对于 Anthropic，normalize_anthropic_response() 将 Anthropic 响应
   # 转换为 SimpleNamespace，使其具有与 OpenAI 相同的接口
   assistant_message, finish_reason = normalize_anthropic_response(response)

   # 之后所有代码统一使用 assistant_message.content
   # 和 assistant_message.tool_calls，无需关心底层 API 模式

**为什么用 SimpleNamespace 而不是自定义类？**

因为它足够轻量——不需要定义一个完整的响应类，只需要一个可以动态设置属性的对象。
``SimpleNamespace`` 是 Python 标准库中最简单的此类对象。这种设计避免了
创建和维护一个臃肿的 ``Response`` 类，同时保持了类型安全的好处。

流式数据的累积
^^^^^^^^^^^^^^^^

流式 API 调用通过 ``_interruptible_streaming_api_call()`` 实现。
这个方法的核心挑战是：**如何在流式接收过程中区分文本内容和工具调用？**

OpenAI 的流式响应中，工具调用的 ``delta`` 对象包含 ``function.name`` 和
``function.arguments`` 的片段。这些片段需要被累积起来，直到流结束才能组合成完整的
工具调用。Hermes 的实现维护了以下累积状态：

- 当前的文本内容（拼接所有 ``delta.content``）
- 工具调用的名称（拼接所有 ``delta.tool_calls[i].function.name``）
- 工具调用的参数（拼接所有 ``delta.tool_calls[i].function.arguments``）

流式数据流图
^^^^^^^^^^^^^^

.. mermaid::

   graph TD
       API["LLM API<br/>(SSE Stream)"]
   
       subgraph "流式累积器"
           TEXT_BUF["文本缓冲区<br/>delta.content"]
           TC_BUF["工具调用缓冲区<br/>delta.tool_calls"]
           THINK_BUF["思考缓冲区<br/>delta.reasoning_content"]
       end
   
       subgraph "回调分发"
           STREAM_CB["stream_delta_callback<br/>→ TTS / CLI 显示"]
           THINK_CB["thinking_callback<br/>→ 思考动画"]
           REASON_CB["reasoning_callback<br/>→ 推理展示"]
       end
   
       RESULT["统一 Response<br/>(SimpleNamespace)"]
   
       API -->|"delta.content"| TEXT_BUF
       API -->|"delta.tool_calls"| TC_BUF
       API -->|"delta.reasoning"| THINK_BUF
   
       TEXT_BUF --> STREAM_CB
       THINK_BUF --> THINK_CB
       THINK_BUF --> REASON_CB
   
       TEXT_BUF -->|"流结束"| RESULT
       TC_BUF -->|"流结束"| RESULT
       THINK_BUF -->|"流结束"| RESULT
   
       STREAM_CB -->|"None 信号"| DISPLAY["关闭响应框"]

一个关键的流式处理细节是 **stale stream 检测** ：Hermes 维护了一个 90 秒的
陈旧流检测器。如果在 90 秒内没有收到任何新的 chunk，就认为连接已经僵死，
主动中断并触发重试。这是处理提供商"保持连接活跃但不发送数据"情况的防护措施。

为什么 Hermes 不使用 async/await？
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hermes 的主循环是纯同步代码（使用 ``time.sleep()`` 而非 ``await asyncio.sleep()``），
但工具处理器可能是异步的。这种"同步主循环 + 异步工具"的混合架构通过
``model_tools._run_async()`` 桥接。

原因有三：

1. **OpenAI SDK 是同步的。** ``openai.OpenAI`` 的 ``chat.completions.create()``
   是同步调用。虽然 SDK 提供了 ``AsyncOpenAI`` ，但混合使用同步和异步 SDK
   会增加代码复杂度。

2. **工具执行在 ThreadPoolExecutor 中。** 并行工具调用使用线程池实现，
   这与 asyncio 的事件循环模型有冲突——在 async 函数中运行同步代码需要
   ``asyncio.to_thread()`` 或 ``loop.run_in_executor()`` ，而工具本身可能是
   异步的，导致嵌套事件循环的问题。

3. **简化错误处理。** 同步代码的错误处理更直观——try/except 可以捕获所有异常，
   而异步代码中的异常可能在不同的事件循环迭代中抛出。

代价是需要手动管理事件循环（``_tool_loop`` 、``_worker_loop``），
但这比处理嵌套事件循环的问题更简单。``model_tools.py`` 第 39-125 行
详细实现了这个桥接层。

第四节：错误分类与恢复
------------------------

11 种 FailoverReason
~~~~~~~~~~~~~~~~~~~~~~

Hermes 的错误分类系统（``agent/error_classifier.py``）定义了 16 种错误原因。
每种错误对应不同的恢复策略：

.. list-table::
   :header-rows: 1
   :widths: 18 12 35 35

   * - 错误类型
     - 典型 HTTP 状态码
     - 含义
     - 恢复策略
   * - ``auth``
     - 401
     - 认证失败（可能 transient）
     - 轮换凭证 → 回退提供商
   * - ``auth_permanent``
     - 401（刷新后仍失败）
     - 永久性认证失败
     - 中止
   * - ``billing``
     - 402
     - 余额耗尽
     - 轮换凭证 → 回退提供商
   * - ``rate_limit``
     - 429
     - 请求频率过高
     - 抖动退避 → 轮换凭证 → 回退
   * - ``overloaded``
     - 503, 529
     - 提供商过载
     - 抖动退避
   * - ``server_error``
     - 500, 502
     - 服务器内部错误
     - 重试
   * - ``timeout``
     - 无（传输层）
     - 连接/读取超时
     - 重建客户端 → 重试
   * - ``context_overflow``
     - 400（某些提供商）
     - 上下文窗口溢出
     - 压缩上下文
   * - ``payload_too_large``
     - 413
     - 请求体过大
     - 压缩请求
   * - ``model_not_found``
     - 404
     - 模型不存在
     - 回退到其他模型
   * - ``format_error``
     - 400（非上下文溢出）
     - 请求格式错误
     - 清洗后重试 → 中止
   * - ``thinking_signature``
     - 400（特定模式）
     - Anthropic 思考块签名无效
     - 重试（自动修复）
   * - ``long_context_tier``
     - 429（特定模式）
     - Anthropic 长上下文层级限制
     - 压缩上下文
   * - ``unknown``
     - 任意
     - 无法分类
     - 抖动退避

错误分类管道
^^^^^^^^^^^^^^

``classify_api_error()`` 函数实现了一个**优先级管道** ：

.. mermaid::

   graph TD
       ERR["异常对象"] --> EX["提取 HTTP 状态码<br/>+ 错误体 + 消息"]
   
       EX --> P1["1. 特殊提供商模式<br/>thinking_signature / long_context_tier"]
       P1 -->|匹配| RESULT["返回 ClassifiedError"]
       P1 -->|不匹配| P2["2. HTTP 状态码分类<br/>401/402/404/429/500/..."]
   
       P2 -->|匹配| RESULT
       P2 -->|不匹配| P3["3. 结构化错误码<br/>resource_exhausted / insufficient_quota"]
   
       P3 -->|匹配| RESULT
       P3 -->|不匹配| P4["4. 消息模式匹配<br/>billing / rate_limit / context / auth"]
   
       P4 -->|匹配| RESULT
       P4 -->|不匹配| P5["5. 传输错误启发式<br/>timeout / connection"]
   
       P5 -->|匹配| RESULT
       P5 -->|不匹配| P6["6. 服务器断连 + 大会话<br/>→ context_overflow"]
       P6 -->|匹配| RESULT
       P6 -->|不匹配| P7["7. 兜底: unknown<br/>(retryable with backoff)"]
       P7 --> RESULT

这个管道的优先级顺序经过精心设计：

1. **提供商特定模式优先** ，因为 Anthropic 的 thinking_signature 错误可能被
   OpenRouter 包装后表现为 400，如果不先检查就会被误分类为 format_error。

2. **402 需要特殊消歧** （第 527-553 行）：有些 402 是临时的使用配额（
   "usage limit, try again in 5 minutes"），不应被当作计费耗尽处理。
   ``_classify_402()`` 通过检查 "try again"、"resets at" 等临时信号来区分。

3. **服务器断连 + 大会话可能是上下文溢出** （第 397-406 行）：
   当会话有大量消息时，提供商可能直接断开连接而不是返回有意义的错误。
   这个启发式检查必须在通用传输错误之前，否则会永远被归类为 timeout。

抖动指数退避
^^^^^^^^^^^^^^

``agent/retry_utils.py`` 实现了抖动指数退避算法：

.. code-block:: python

   delay = min(base_delay * 2^(attempt-1), max_delay) + jitter

其中 ``jitter`` 是 ``[0, 0.5 * delay]`` 范围内的均匀随机值。
默认参数：``base_delay=5.0`` ，``max_delay=120.0`` 。

**为什么要抖动？** 当多个 Hermes 会话同时遇到限流时，如果没有抖动，
它们会在完全相同的时刻重试，形成"惊群效应"（thundering herd），
再次触发限流。抖动使得重试时间分散，降低了集体重试的概率。

jitter 的种子使用 ``time.time_ns() ^ (counter * 0x9E3779B9)`` 来保证
即使在时钟精度较低的系统上也能产生不同的随机数。

错误恢复的状态机
^^^^^^^^^^^^^^^^^^

.. mermaid::

   stateDiagram-v2
       [*] --> Normal
   
       Normal --> Success : API returns valid response
       Normal --> ErrorClassify : Exception thrown
   
       ErrorClassify --> CredRotation : auth/billing/rate_limit
       ErrorClassify --> CtxCompress : context_overflow/payload_too_large
       ErrorClassify --> ProviderFallback : model_not_found/auth_permanent
       ErrorClassify --> JitterBackoff : overloaded/server_error/unknown
       ErrorClassify --> Abort : format_error after 3 retries
   
       CredRotation --> Normal : Credentials valid
       CredRotation --> ProviderFallback : No available credentials
   
       CtxCompress --> Normal : Compression succeeded
       CtxCompress --> Abort : Compression failed
   
       ProviderFallback --> Normal : Fallback provider available
       ProviderFallback --> Abort : No fallback available
   
       JitterBackoff --> Normal : retry_count less than max_retries
       JitterBackoff --> ProviderFallback : retry_count exceeded
   
       Success --> [*]
       Abort --> [*]

一个值得深入讨论的恢复策略是 **提供商回退** 。Hermes 维护了一个回退链
（``_fallback_chain``），按优先级排列的备用提供商列表。当主提供商持续失败时，
``_try_activate_fallback()`` 会依次尝试回退链中的提供商。回退是临时的——
下一轮对话开始时，``_restore_primary_runtime()`` 会恢复主提供商。

第五节：工具执行引擎
----------------------

并行 vs 顺序决策
~~~~~~~~~~~~~~~~~~

当 LLM 在一次响应中返回多个工具调用时，Hermes 需要决定是并行执行还是顺序执行。

决策逻辑位于 ``_should_parallelize_tool_batch()`` 函数（第 267 行）：

.. mermaid::

   graph TD
       START["工具调用批次"] --> CHECK1{"只有 1 个调用?"}
       CHECK1 -->|是| SEQ["顺序执行"]
       CHECK1 -->|否| CHECK2{"包含交互式工具?<br/>(clarify)"}
       CHECK2 -->|是| SEQ
       CHECK2 -->|否| CHECK3{"所有工具都是<br/>只读/路径隔离的?"}
       CHECK3 -->|否| SEQ
       CHECK3 -->|是| CHECK4{"路径有重叠?"}
       CHECK4 -->|是| SEQ
       CHECK4 -->|否| PAR["并行执行<br/>(ThreadPoolExecutor)"]
   
       SEQ --> RESULT["追加结果到 messages"]
       PAR --> RESULT

具体的并行安全判定规则：

- ``_NEVER_PARALLEL_TOOLS`` ：永远不并行的工具。目前只有 ``clarify`` （需要用户交互）。
- ``_PARALLEL_SAFE_TOOLS`` ：只读、无共享可变状态的工具。包括 ``read_file`` 、
  ``search_files`` 、``web_search`` 、``web_extract`` 、``session_search`` 等。
- ``_PATH_SCOPED_TOOLS`` ：按文件路径隔离的工具。包括 ``read_file`` 、
  ``write_file`` 、``patch`` 。只要操作的目标路径不重叠，这些工具可以并行。

如果批次中所有工具调用都属于上述类别且路径不重叠，则使用
``ThreadPoolExecutor(max_workers=8)`` 并行执行。

Agent 循环拦截工具
^^^^^^^^^^^^^^^^^^^^

某些工具需要访问 Agent 级别的状态，不能通过通用的工具注册中心分发。
这些工具在 ``_invoke_tool()`` （第 7705 行）中被拦截：

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 工具名
     - 需要的 Agent 状态
     - 处理方式
   * - ``todo``
     - ``TodoStore`` 实例
     - 直接调用 ``todo_tool(store=self._todo_store)``
   * - ``memory``
     - ``MemoryStore`` 实例
     - 直接调用 ``memory_tool(store=self._memory_store)``
   * - ``session_search``
     - ``SessionDB`` 实例
     - 直接调用 ``session_search(db=self._session_db)``
   * - ``delegate_task``
     - 父 Agent 实例
     - 创建子 Agent 并运行
   * - ``clarify``
     - ``clarify_callback`` 回调
     - 直接调用 ``clarify_tool(callback=self.clarify_callback)``

**为什么要拦截而不是注册？** 因为这些工具需要的依赖（``TodoStore`` 、
``MemoryStore`` 、``SessionDB`` 、父 Agent 引用）是 Agent 实例特有的，
不能在模块加载时通过注册中心静态绑定。

在 ``model_tools.py`` 中，这些工具被列入 ``_AGENT_LOOP_TOOLS`` 集合。
如果由于某种原因调用通过了注册中心（不应该发生），会返回一个 stub 错误：

.. code-block:: python

   if function_name in _AGENT_LOOP_TOOLS:
       return json.dumps({"error": f"{function_name} must be handled by the agent loop"})

调用链：_invoke_tool → handle_function_call → registry.dispatch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

工具调用的完整路径：

.. mermaid::

   sequenceDiagram
       participant MainLoop as AgentLoop
       participant IT as invoke_tool
       participant Plugin as PluginHook
       participant Intercept as InterceptCheck
       participant HFC as handle_function_call
       participant Coerce as coerce_args
       participant Dispatch as registry.dispatch
       participant Handler as ToolHandler
   
       MainLoop->>IT: function_name + function_args
       IT->>Plugin: pre_tool_call hook
       Plugin-->>IT: block_message or None
       alt Blocked by plugin
           IT-->>MainLoop: blocked error message
       end
   
       IT->>Intercept: Check todo/memory/session_search
       alt Intercepted
           Intercept->>Handler: Direct call to tool
           Handler-->>IT: result JSON
       else Generic tool
           IT->>HFC: handle_function_call()
           HFC->>Coerce: coerce_tool_args()
           Coerce-->>HFC: converted args
           HFC->>Plugin: pre_tool_call hook observer
           HFC->>Dispatch: registry.dispatch()
           Dispatch->>Handler: Call registered handler
           Handler-->>Dispatch: raw result
           Dispatch-->>HFC: result JSON
           HFC->>Plugin: post_tool_call hook
           HFC-->>IT: result JSON
       end
   
       IT-->>MainLoop: tool result string

**参数类型强制转换** （``model_tools.py:334``）是一个容易被忽略但至关重要的步骤。
LLM 经常返回错误类型的参数——例如用字符串 ``"42"`` 代替整数 ``42`` ，
用字符串 ``"true"`` 代替布尔值 ``true`` 。``coerce_tool_args()`` 根据工具的
JSON Schema 定义自动修正这些类型不匹配，避免下游处理器崩溃。

工具名幻觉修复
^^^^^^^^^^^^^^^^

LLM 有时会幻觉出不存在的工具名。Hermes 通过 ``_repair_tool_call()`` 方法
尝试自动修复常见的幻觉模式（如拼写错误、前后缀不匹配）。

如果修复失败，Hermes 会将可用工具列表作为错误消息返回给模型，
让模型在下一轮自行纠正。这种"软纠错"策略避免了因幻觉导致的硬终止：
模型通常能在看到可用工具列表后选择正确的工具。

重试限制为 3 次（``_invalid_tool_retries >= 3``）：
如果模型连续 3 次都无法生成有效的工具名，说明模型本身有问题，
此时应该终止并返回部分结果。

第六节：预算与迭代控制
------------------------

IterationBudget 的工作原理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``IterationBudget`` （第 170 行）是一个线程安全的迭代计数器：

.. code-block:: python

   class IterationBudget:
       def __init__(self, max_total: int):
           self.max_total = max_total
           self._used = 0
           self._lock = threading.Lock()

       def consume(self) -> bool:
           with self._lock:
               if self._used >= self.max_total:
                   return False
               self._used += 1
               return True

       def refund(self) -> None:
           with self._lock:
               if self._used > 0:
                   self._used -= 1

       @property
       def remaining(self) -> int:
           with self._lock:
               return max(0, self.max_total - self._used)

使用 ``threading.Lock`` 保护是因为父 Agent 和子 Agent 在不同线程中共享同一个预算。

**为什么需要 refund？** ``execute_code`` 工具允许模型在沙箱中进行程序化的工具调用。
这些调用是廉价的 RPC 风格操作，不应该消耗迭代预算。当一次迭代中唯一的工具调用
是 ``execute_code`` 时，预算被退回：

.. code-block:: python

   _tc_names = {tc.function.name for tc in assistant_message.tool_calls}
   if _tc_names == {"execute_code"}:
       self.iteration_budget.refund()

父 Agent 与子 Agent 的预算共享
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

当 Agent 通过 ``delegate_task`` 创建子 Agent 时，预算如何分配？

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 设计选择
     - 说明
   * - 方案 A：完全共享
     - 父子共享同一个 budget，子 Agent 的每次迭代都消耗父的预算
   * - 方案 B：完全独立
     - 子 Agent 有自己的 budget，不消耗父的预算
   * - 方案 C：独立但有上限
     - 子 Agent 有独立的 budget，上限由配置决定

Hermes 选择了**方案 A**——``delegate_task`` 将父 Agent 的 ``iteration_budget``
传递给子 Agent。这意味着整个 Agent 系统有一个全局的迭代上限。

但代码注释也提到："Each subagent gets an independent budget capped at
``delegation.max_iterations``"。这意味着虽然父子共享预算对象，
但子 Agent 的 ``max_iterations`` 参数是独立的。

预算耗尽的宽限机制
^^^^^^^^^^^^^^^^^^^^

当迭代预算耗尽时，Hermes 不会立即终止循环。它使用一个**两阶段退出** 机制：

1. **阶段一：注入预算耗尽提示** （设置 ``_budget_exhausted_injected = True``）。
   向消息列表追加一条系统消息，告知模型"这是最后一次迭代，请总结你的工作"。
   注意 Hermes 实际上不在预算耗尽时注入中间警告——注释说明"中间压力警告导致模型过早放弃"
   （#7915），所以只在真正耗尽时才通知一次。

2. **阶段二：宽限调用** （``_budget_grace_call = True``）。允许模型进行一次额外的
   API 调用来生成总结。如果这次调用仍然返回工具调用而非文本，循环强制退出。

这个设计的核心洞察是：**模型需要一次"收尾"的机会。** 如果在预算耗尽的瞬间直接终止，
用户可能看到半完成的回复、未保存的文件、或中断的操作。宽限调用让模型有机会
优雅地结束当前工作。

第七节：会话持久化与清理
--------------------------

循环退出时的处理
~~~~~~~~~~~~~~~~~~

无论 ``run_conversation()`` 以何种方式退出——正常完成、预算耗尽、中断、
错误——都会执行以下步骤：

.. code-block:: python

   self._cleanup_task_resources(effective_task_id)  # 清理 VM 和浏览器资源
   self._persist_session(messages, conversation_history)  # 持久化会话

``_persist_session()`` （第 2577 行）执行双重持久化：

1. **JSON 日志** ：通过 ``_save_session_log()`` 将消息列表写入 JSON 文件。
   这是增量写入的——每次工具迭代后都会调用，确保即使被强制终止也有进度记录。

2. **SQLite 数据库** ：通过 ``_flush_messages_to_session_db()`` 将消息写入
   会话数据库。这里有一个优化：只写入新增的消息（通过比较 ``conversation_history``
   的长度来确定哪些是新增的）。

**为什么需要双重持久化？** JSON 日志是 append-only 的，适合作为审计日志和调试工具。
SQLite 数据库支持结构化查询（如 ``session_search`` 工具需要搜索历史会话）。
两者互补，缺一不可。

轨迹保存
~~~~~~~~~~

当 ``save_trajectories=True`` 时，完整的对话轨迹（包括系统提示词、工具 schema、
模型响应中的思考过程）被保存为 JSONL 文件。轨迹文件用于训练数据收集、
质量评估和回归测试。

``agent/trajectory.py`` 中的 ``save_trajectory()`` 函数负责将消息列表转换为
标准化的轨迹格式。它会将模型内部的 ``<REASONING_SCRATCHPAD>`` 标签转换为
``<think`` 块，以适配不同的训练框架。

资源清理
~~~~~~~~~~

``_cleanup_task_resources()`` （第 2390 行）负责清理每次对话的资源：

- **终端 VM** ：如果终端环境不是持久化的（``persistent_filesystem=False``），
  调用 ``cleanup_vm()`` 销毁沙箱。持久化环境由空闲回收器在超时后清理。
- **浏览器实例** ：调用 ``cleanup_browser()`` 关闭无头浏览器。

注意资源清理在**每个退出路径** 都被调用——无论是正常完成、错误、还是中断。
这是通过在每个 ``return`` 语句前显式调用 ``_cleanup_task_resources()`` 实现的，
而不是通过 ``try/finally`` 块。这种"手动 finally"模式在代码中很常见，
因为不同退出路径需要不同的清理逻辑。

后台审查线程
^^^^^^^^^^^^^^

在主循环退出后，Hermes 可能会启动一个后台线程来审查对话内容：

.. code-block:: python

   if _should_review_memory or _should_review_skills:
       self._spawn_background_review(messages_snapshot, ...)

``_spawn_background_review()`` （第 2458 行）创建一个新的 AIAgent 实例，
在后台线程中运行，让模型回顾对话并自动保存值得记住的信息到长期记忆或技能库。

关键设计决策：

- 使用 ``messages_snapshot`` （消息列表的副本）而非引用，避免主线程修改影响审查。
- 审查 Agent 使用 ``quiet_mode=True`` ，所有输出被重定向到 ``/dev/null`` 。
- 审查 Agent 共享主 Agent 的 ``MemoryStore`` 和 ``SkillStore`` ，
  所以写入的记忆对后续会话立即可见。
- 审查 Agent 的迭代上限为 8（远低于主 Agent 的 90），防止审查本身消耗过多资源。

插件钩子
^^^^^^^^^^

在会话生命周期的关键节点，Hermes 触发插件钩子：

- ``on_session_start`` ：新会话创建时
- ``pre_llm_call`` ：每轮 LLM 调用前，插件可以注入上下文
- ``pre_api_request`` ：每次 API 请求前（更细粒度）
- ``post_api_request`` ：每次 API 响应后
- ``pre_tool_call`` ：工具执行前，插件可以阻止执行
- ``post_tool_call`` ：工具执行后

钩子机制通过 ``hermes_cli.plugins.invoke_hook()`` 实现，采用"尽力而为"模式——
如果钩子抛出异常，Hermes 捕获并记录，但不会中断主流程。这是一个重要的设计原则：
**插件永远不应该导致 Agent 崩溃。**

总结
------

通过分析 ``run_conversation()`` 的完整生命周期，我们可以提炼出以下 Agent 工程原则：

1. **输入永远不干净。** 从 surrogate 字符到过期记忆标签，真实世界的输入需要大量清洗。
   永远不要假设用户输入是"合理的"。

2. **错误恢复需要分类。** 不是所有错误都应该重试。认证失败需要换凭证，
   上下文溢出需要压缩，模型不存在需要回退。一个统一的 ``try/except Exception``
   是不够的——你需要一个错误分类管道。

3. **预算控制必须有宽限期。** 在预算耗尽时立即终止会导致糟糕的用户体验。
   给模型一次"收尾"的机会，让用户看到完整的回复。

4. **持久化在每个退出路径。** 不要只在正常完成时保存数据。错误、中断、
   超时——每个退出路径都需要调用持久化逻辑。

5. **流式处理需要统一抽象。** 不同提供商的流式协议差异巨大。
   在业务逻辑和传输协议之间建立一个统一的抽象层（如 SimpleNamespace），
   避免业务代码被提供商差异污染。

6. **同步主循环是合理的选择。** 在 Agent 系统中，async/await 不是必须的。
   同步代码更简单，更容易调试，而且通过线程池可以实现工具的并行执行。

7. **防御性编程是常态。** 从安全 stdio 包装器到 surrogate 清洗，
   从 JSON 参数修复到工具名幻觉修复，生产级 Agent 的代码中充满了防御性措施。
   这些措施在 demo 中不需要，但在 7x24 运行的服务中至关重要。

在下一章中，我们将深入 Hermes 的工具系统，理解工具如何通过自注册模式加入系统，
以及调度器如何处理参数转换、插件拦截和结果持久化。
