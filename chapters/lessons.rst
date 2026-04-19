.. _lessons:

工程教训：从 12,000 行代码中提炼的模式
=============================================

Hermes Agent 的核心循环 ``run_agent.py`` 有 12,084 行。
加上工具系统、适配器、网关、CLI 等模块，总计超过 50,000 行 Python 代码。
这些代码不是凭空产生的——每一行都是对某个具体工程问题的回应。

本章的目标是从这些代码中提炼出可复用的模式、策略和教训。
我们将按照"架构模式"、"性能优化"、"错误处理"、"可扩展性"
和"技术债务"五个维度来组织分析。

.. mermaid::

   mindmap
     root((Hermes<br/>模式目录))
       架构模式
         Strategy Pattern
           API 路由
         Self-Registration
           AST 预检查
         Observer Pattern
           回调链
         Adapter Pattern
           SimpleNamespace
         Circuit Breaker
           MCP 断路器
         OCC
           history_version
         WAL
           SQLite WAL
       性能优化
         持久化事件循环
         三层结果预算
         Prompt 缓存
         并行工具执行
         双层技能缓存
       错误处理
         11 类错误分类
         抖动退避
         优雅降级
       可扩展性
         插件钩子系统
         MCP 动态发现
         工具集组合
         皮肤引擎
       技术债务
         上帝类
         提供商 Hack
         预算共享
         缓存失效

架构模式总结
--------------

Strategy Pattern：API 路由
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：Hermes 需要同时支持 OpenAI、Anthropic、Bedrock、Google 等多个
LLM 提供商，每个提供商的 API 格式、认证方式、流式协议都不同。

**Hermes 的做法** ：在 ``AIAgent.__init__`` 中，根据提供商类型设置
``api_mode`` 字段（如 ``"openai_chat"`` 、``"anthropic_messages"`` 、
``"codex_responses"``）。主循环根据 ``api_mode`` 选择不同的调用路径。

.. mermaid::

   graph TD
       A["run_conversation()"] --> B{"api_mode?"}
       B -->|"openai_chat"| C["OpenAI SDK<br/>chat.completions.create()"]
       B -->|"anthropic_messages"| D["Anthropic SDK<br/>messages.create()"]
       B -->|"codex_responses"| E["OpenAI SDK<br/>responses API"]
       B -->|"bedrock_converse"| F["Boto3 SDK<br/>converse()"]
       C --> G["统一响应格式<br/>SimpleNamespace"]
       D --> G
       E --> G
       F --> G
       G --> H["工具调度 / 文本输出"]

**为什么不用继承？** 用继承的话，每新增一个提供商就需要一个新的子类。
Hermes 选择了在单个类内部用 ``api_mode`` 分支来实现策略切换。
这看起来违反了"用组合代替继承"的原则，但实际上有合理的工程考量：

- 大部分逻辑（预算控制、工具调度、消息管理）在所有提供商之间是共享的，
  真正不同的只有 API 调用和响应解析两部分。
- 继承体系会导致共享逻辑在父类和子类之间来回搬移，
  而策略模式将这些差异点集中在几个方法内部。

**何时使用** ：当核心流程相同、只有特定步骤不同时。
**何时不用** ：当不同策略的差异大到足以构成独立的模块时。

Self-Registration Pattern：工具注册表
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：Hermes 有 40 多个工具，每个工具有自己的 schema、handler、
toolset 归属和可用性检查。如何让这些工具"自动发现"而非手动维护注册列表？

**Hermes 的做法** ：

1. 每个工具文件（如 ``tools/file_tools.py``）在模块级别调用
   ``registry.register()`` 。

2. ``tools/registry.py`` 的 ``discover_builtin_tools()`` 函数扫描
   ``tools/`` 目录，用 **AST 预检查** 判断哪些文件包含注册调用，
   只导入包含注册调用的文件。

3. 模块级代码在 import 时自动执行 ``register()`` ，将工具的 schema、
   handler、检查函数注册到全局单例 ``registry`` 。

AST 预检查是这里的关键技巧：

.. code-block:: python

    def _module_registers_tools(module_path: Path) -> bool:
        """Return True when the module contains a top-level registry.register() call."""
        try:
            source = module_path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(module_path))
        except (OSError, SyntaxError):
            return False
        return any(_is_registry_register_call(stmt) for stmt in tree.body)

这段代码只检查 **模块顶层语句** （``tree.body``），不检查函数内部。
这意味着辅助模块（内部的 ``register()`` 调用被封装在函数中）
不会被误导入。这是一个精巧的权衡：它避免了"导入所有文件"的代价，
同时不需要维护一个手工的注册列表。

**优点** ：

- 新增工具只需创建文件并调用 ``register()`` ，零配置。
- AST 检查比 import-then-check 快得多（不需要执行任何代码）。
- 工具文件的注册声明与实现放在同一文件中，降低了遗漏风险。

**缺点** ：

- 依赖隐式 import 副作用，新开发者可能不理解"为什么 import 了这个文件"。
- AST 检查无法识别动态构造的注册调用（如 ``getattr(registry, "register")()``）。

Observer Pattern：回调链
~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：Agent 在运行过程中需要通知外部系统各种事件——流式文本输出、
工具执行开始/结束、思考过程展示、状态变更等。
如何在不耦合具体消费者的前提下实现这些通知？

**Hermes 的做法** ：通过一系列回调函数实现观察者模式。

- ``stream_callback`` ：流式文本输出，用于 TTS 管线和 TUI 渲染。
- ``tool_start_callback`` ：工具开始执行时通知。
- ``tool_progress_callback`` ：工具执行进度更新。
- ``status_callback`` ：状态变更通知（如压缩警告、连接重置）。
- ``step_callback`` ：每个迭代步骤通知，用于网关钩子系统。

这些回调在 ``run_conversation()`` 中以防御性方式调用——每个回调都被
try/except 包裹，确保回调失败不会影响主流程：

.. code-block:: python

    if self.step_callback is not None:
        try:
            self.step_callback(api_call_count, prev_tools)
        except Exception as _step_err:
            logger.debug("step_callback error (iteration %s): %s", api_call_count, _step_err)

**教训** ：回调必须与核心逻辑解耦。如果回调的失败能导致主流程崩溃，
那不是观察者模式，那是紧耦合。

Adapter Pattern：API 响应归一化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：不同 LLM 提供商返回不同格式的响应。OpenAI 返回
``response.choices[0].message`` ，Anthropic 返回
``response.content[0].text`` ，Bedrock 返回完全不同的结构。

**Hermes 的做法** ：使用 Python 标准库的 ``SimpleNamespace`` 创建
轻量级的统一响应对象。

``SimpleNamespace`` 的妙处在于它既支持属性访问（``msg.content``），
又支持动态添加属性，且没有 ``dict`` 的键引号冗余。
在 Hermes 的 ``_normalize_codex_response()`` 、
``normalize_anthropic_response()`` 等函数中，
不同提供商的响应都被转换为具有 ``content`` 、``tool_calls``
等统一属性的 ``SimpleNamespace`` 对象。

这样主循环只需要处理一种格式，提供商差异被完全封装在适配器层。

Circuit Breaker：MCP 断路器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：MCP（Model Context Protocol）工具服务器是外部进程，
可能崩溃、超时或返回错误。如果每次调用都等待完整的超时时间，
整个 Agent 循环会被阻塞。

**Hermes 的做法** ：在 ``tools/mcp_tool.py`` 中实现了断路器模式：

- 每个 MCP 服务器维护连续失败计数器。
- 当失败次数超过阈值时，服务器被标记为"短路"（short-circuited），
  后续调用直接返回错误而不尝试连接。
- 定期重试以检测服务器是否恢复。

这避免了"一个坏掉的 MCP 服务器拖慢整个 Agent"的问题。
断路器的价值不在于它能修复问题，而在于它能快速失败，
让 Agent 继续执行其他工具。

Optimistic Concurrency Control：网关历史版本
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：TUI 网关允许多个操作并发执行（用户可能一边等 Agent 响应，
一边触发撤销或压缩）。如何确保 Agent 的响应写入不会被并发操作覆盖？

**Hermes 的做法** ：在 ``tui_gateway/server.py`` 中使用乐观并发控制：

每个会话维护一个 ``history_version`` 整数计数器。
每次修改历史（压缩、撤销、重试）时递增版本号。
当 Agent 完成一个 turn 时，检查当前版本是否与启动时的版本一致：

.. code-block:: python

    # 开始 turn 时快照版本
    history_version = int(session.get("history_version", 0))

    # ... Agent 运行 ...

    # 完成时检查版本
    current_version = int(session.get("history_version", 0))
    if current_version == history_version:
        session["history"] = result["messages"]
        session["history_version"] = history_version + 1
    else:
        # 历史在 turn 期间被外部修改了——不覆盖
        print("[tui_gateway] history_version mismatch — output NOT written")

这比加锁更轻量：不需要在整个 turn 期间持有锁（那会阻塞所有并发操作），
只需在最终写入时检查版本。冲突时选择丢弃 Agent 的输出而非覆盖——
因为在 Agent 运行期间发生的历史变更（如用户撤销）通常优先级更高。

Write-Ahead Log：SQLite WAL 模式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：网关模式下，多个平台（Telegram、Discord、CLI）的会话
同时读写同一个 ``state.db`` 。如何在不牺牲并发性的前提下保证数据完整性？

**Hermes 的做法** ：在 ``hermes_state.py`` 中启用 SQLite 的 WAL
（Write-Ahead Logging）模式：

.. code-block:: python

    self._conn.execute("PRAGMA journal_mode=WAL")

WAL 模式的核心优势：

- **读不阻塞写** ：多个读者可以同时访问数据库，即使有写入正在进行。
  这对网关场景至关重要——一个平台的 Agent 在写入消息时，
  另一个平台的用户应该能正常读取历史。
- **写不阻塞读** ：写入操作追加到 WAL 文件，不影响当前读者。
  只有在 WAL checkpoint 时才需要短暂的排他访问。

Hermes 还实现了定期 PASSIVE WAL checkpoint，防止 WAL 文件无限增长：

.. code-block:: python

    def _maybe_checkpoint(self):
        """Best-effort PASSIVE WAL checkpoint. Never blocks, never raises."""
        if self._write_count % 50 != 0:
            return
        try:
            self._conn.execute("PRAGMA wal_checkpoint(PASSIVE)")
        except Exception:
            pass

性能优化策略
--------------

持久化事件循环：避免 asyncio.run() 的陷阱
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：Hermes 的工具系统混合了同步和异步处理器。一些工具（如
web_search）使用 httpx 的异步客户端，但主循环是同步的。
如何高效地在同步上下文中调用异步工具？

**反模式** ：在每个异步调用时使用 ``asyncio.run()`` 。

``asyncio.run()`` 的行为是：创建一个新事件循环，运行协程，
然后 **关闭** 事件循环。问题是，httpx 和 AsyncOpenAI 客户端
会将连接池绑定到创建它们的事件循环。当事件循环被关闭后，
这些客户端在垃圾回收时尝试清理连接，触发
``RuntimeError: Event loop is closed`` 错误。

**Hermes 的做法** （``model_tools.py``）：

1. 主线程维护一个持久化事件循环 ``_tool_loop`` ，整个进程生命周期不关闭。
2. 工作线程（并行工具执行）使用线程局部存储维护各自的持久化循环。
3. 只有在已经处于异步上下文时（如网关的 async 栈），才退回到
   ``concurrent.futures.ThreadPoolExecutor`` + ``asyncio.run`` 的方案。

.. code-block:: python

    def _run_async(coro):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # 异步上下文中——用临时线程运行
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result(timeout=300)

        # 工作线程——用线程局部持久循环
        if threading.current_thread() is not threading.main_thread():
            worker_loop = _get_worker_loop()
            return worker_loop.run_until_complete(coro)

        # 主线程——用全局持久循环
        tool_loop = _get_tool_loop()
        return tool_loop.run_until_complete(coro)

**教训** ：在混合同步/异步的系统中，``asyncio.run()`` 是一个危险的陷阱。
它看起来简洁，但会在高频调用场景下造成资源泄漏和运行时错误。
持久化事件循环虽然不那么"优雅"，但在生产环境中更可靠。

三层结果预算系统
~~~~~~~~~~~~~~~~~~

**问题** ：工具返回的结果可能非常大（如 ``read_file`` 读取一个 1MB 的日志文件）。
如果将所有工具结果都保留在消息历史中，上下文窗口会被迅速填满。

**Hermes 的做法** （``tools/budget_config.py``）：三层预算控制。

.. mermaid::

   graph TB
       A["工具返回结果"] --> B{"Layer 1: 单工具阈值<br/>default 100K chars"}
       B -->|"超过"| C["持久化到磁盘<br/>替换为 preview (1.5K chars)"]
       B -->|"未超过"| D["保留在消息中"]
       C --> E{"Layer 2: 单轮聚合预算<br/>default 200K chars"}
       D --> E
       E -->|"超过"| F["触发 Layer 2 持久化<br/>大结果写入磁盘"]
       E -->|"未超过"| G["继续"]
       F --> H{"Layer 3: 总迭代预算<br/>max_iterations"}
       G --> H
       H -->|"耗尽"| I["终止循环"]

- **Layer 1（per-tool）** ：每个工具有独立的结果大小阈值（默认 100K 字符）。
  超过阈值的结果被持久化到磁盘文件，消息中只保留 1.5K 字符的预览。
  特殊工具如 ``read_file`` 被设为无限阈值，避免无限循环。

- **Layer 2（per-turn）** ：单个 assistant turn 内所有工具结果的聚合预算
  （默认 200K 字符）。超过时触发批量持久化。

- **Layer 3（total iterations）** ：总迭代次数预算（默认 90 次），
  通过 ``IterationBudget`` 类进行线程安全管理。

这种分层设计让预算控制既有粒度（per-tool）又有全局视野（per-turn），
避免了单一阈值要么太宽松、要么太严格的困境。

Prompt 缓存：system_and_3 策略
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：多轮对话中，系统提示词和早期对话在每次 API 调用时都被重新发送，
造成大量重复的 token 计费。

**Hermes 的做法** （``agent/prompt_caching.py``）：利用 Anthropic 的
``cache_control`` 机制实现 "system_and_3" 缓存策略。

Anthropic 允许最多 4 个缓存断点。Hermes 将它们分配为：

1. 系统提示词（在所有 turn 之间稳定不变）
2-4. 最近 3 条非系统消息（滚动窗口）

这意味着在多轮对话中，系统提示词和最近几条消息只需计算一次，
后续 turn 的 API 调用可以直接命中缓存。Hermes 报告约 75% 的
输入 token 节省。

一个关键实现细节：Hermes 在连续会话中会从 SQLite 加载之前存储的
系统提示词，而不是重新构建。这确保了提示词的逐字节一致性，
从而保证缓存命中率。如果每次都重新构建提示词，即使内容相同，
细微的格式差异也可能导致缓存未命中。

并行工具执行策略
~~~~~~~~~~~~~~~~~~

**问题** ：当模型在一个响应中请求调用多个工具时，是否应该并行执行？

**Hermes 的做法** ：三级并行策略。

- **NEVER_PARALLEL** ：``clarify`` 等交互式工具，必须串行执行。
- **PARALLEL_SAFE** ：``web_search`` 、``read_file`` 、``search_files``
  等只读工具，可以安全并行。
- **PATH_SCOPED** ：``read_file`` 、``write_file`` 、``patch`` 等文件操作，
  可以并行但需要检查路径是否重叠。

路径重叠检测（``_paths_overlap()``）是一个精巧的设计。
它比较两个路径的路径组件前缀，而非直接比较字符串：
``/tmp/a.txt`` 和 ``/tmp/b.txt`` 不重叠，可以并行；
但 ``/tmp/dir/`` 和 ``/tmp/dir/file.txt`` 重叠，需要串行。

**当不确定时，默认串行。** 这是并行工具执行的核心原则。
``_should_parallelize_tool_batch()`` 在任何解析失败或未知工具的情况下
都返回 ``False`` ，确保安全性优先于性能。

双层技能缓存
~~~~~~~~~~~~~~

**问题** ：技能索引（skills index）的构建需要扫描磁盘上的所有技能目录、
解析 YAML frontmatter、匹配平台条件。在每次 API 调用时重复这个过程代价太高。

**Hermes 的做法** ：双层缓存——LRU 内存缓存 + 磁盘快照。

- 内存层：使用 LRU 缓存存储最近使用的技能索引结果。
- 磁盘层：将索引序列化为 JSON 快照文件，下次启动时直接加载。

这种模式在"首次构建慢、后续读取快"的场景中非常有效。
技能列表不频繁变更（只有在用户安装/卸载技能时才变），
因此缓存的命中率极高。

错误处理哲学
--------------

11 类错误分类：精确优于泛型重试
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：API 调用可能因为各种原因失败。最简单的做法是捕获所有异常，
等待一段时间后重试。但这种"一刀切"的方式要么重试了不该重试的错误
（如认证失败），要么对可以恢复的错误（如限流）退避不足。

**Hermes 的做法** ：在 ``agent/error_classifier.py`` 中实现了
11 类精细错误分类：

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 错误类型
     - 恢复策略
     - 典型触发条件
   * - ``auth``
     - 凭证轮换
     - 401/403，API key 无效
   * - ``auth_permanent``
     - 终止，提示用户
     - 认证刷新后仍失败
   * - ``billing``
     - 切换凭证/提供商
     - 402，余额耗尽
   * - ``rate_limit``
     - 抖动退避 + 轮换
     - 429，请求频率过高
   * - ``overloaded``
     - 抖动退避
     - 503/529，提供商过载
   * - ``server_error``
     - 重试
     - 500/502，内部错误
   * - ``timeout``
     - 重建连接 + 重试
     - 连接/读取超时
   * - ``context_overflow``
     - 压缩上下文
     - 上下文窗口溢出
   * - ``payload_too_large``
     - 压缩 payload
     - 413，请求体过大
   * - ``model_not_found``
     - 切换模型/提供商
     - 404，模型不存在
   * - ``format_error``
     - 终止或剥离重试
     - 400，请求格式错误

分类管线的优先级顺序是一个重要的设计决策：

1. **提供商特定模式** （最高优先级）：Anthropic thinking block 签名错误、
   长上下文层级门控等。这些模式必须在通用处理之前检查，
   因为它们的恢复策略与通用模式不同。

2. **HTTP 状态码** ：基础分类层，根据 401/402/429/500 等状态码分类。

3. **错误码** ：响应体中的结构化错误码（如 ``resource_exhausted``）。

4. **消息模式匹配** ：当没有状态码时，通过错误消息中的关键词分类。
   这一层需要仔细区分歧义情况——例如 402 可能是余额耗尽或临时配额限制。

5. **传输错误启发式** ：连接中断、超时等网络层错误。

6. **上下文溢出启发式** ：当大会话遇到连接中断时，推测为上下文溢出。

7. **兜底：未知** ：可重试，但使用较长的退避间隔。

**402 歧义消解** 是分类管线中最精巧的部分。HTTP 402 通常意味着"需要付款"，
但有些提供商在临时配额耗尽时也返回 402。Hermes 通过检查错误消息中是否
包含临时信号（"try again"、"resets at"、"retry"）来区分：

- "Usage limit exceeded, try again in 5 minutes" → 临时配额 → 当作限流处理
- "Insufficient credits" → 余额耗尽 → 切换凭证

这种区分避免了将临时配额错误当作账户问题处理（导致不必要的凭证切换），
也避免了将真正的余额耗尽当作临时问题反复重试。

.. mermaid::

   graph TD
       A["API 调用失败"] --> B{"提供商特定模式?"}
       B -->|是| C["thinking_signature / long_context_tier"]
       B -->|否| D{"有 HTTP 状态码?"}
       D -->|是| E{"状态码分类"}
       D -->|否| F{"有错误码?"}
       E --> G["401→auth, 402→歧义消解,<br/>429→rate_limit, 500→server_error"]
       F -->|是| H["resource_exhausted→rate_limit,<br/>insufficient_quota→billing"]
       F -->|否| I{"消息模式匹配"}
       I --> J["billing / rate_limit /<br/>context_overflow / auth"]
       I -->|无匹配| K{"传输错误?"}
       K -->|是| L["timeout / context_overflow"]
       K -->|否| M["unknown — 可重试"]
   
       G --> N["ClassifiedError<br/>+ 恢复策略提示"]
       C --> N
       H --> N
       J --> N
       L --> N
       M --> N

抖动退避：避免重试风暴
~~~~~~~~~~~~~~~~~~~~~~~~

**问题** ：当多个 Agent 会话同时遇到限流错误时，如果它们使用相同的
退避间隔，会在退避结束后同时重试，形成"重试风暴"（convoy effect）。

**Hermes 的做法** （``agent/retry_utils.py``）：抖动指数退避。

.. code-block:: python

    def jittered_backoff(attempt, *, base_delay=5.0, max_delay=120.0, jitter_ratio=0.5):
        exponent = max(0, attempt - 1)
        delay = min(base_delay * (2 ** exponent), max_delay)

        # 用时间戳 + 单调计数器做种子，确保不同线程的抖动不同
        seed = (time.time_ns() ^ (tick * 0x9E3779B9)) & 0xFFFFFFFF
        rng = random.Random(seed)
        jitter = rng.uniform(0, jitter_ratio * delay)

        return delay + jitter

关键设计点：

- **确定性伪随机** ：使用 ``random.Random(seed)`` 而非全局 ``random`` ，
  避免影响其他使用 random 的代码。
- **种子混合** ：将时间戳与单调计数器异或，即使系统时钟精度较低
  也能保证不同调用的种子不同。
- **线程安全** ：单调计数器通过 ``threading.Lock`` 保护。
- **上限保护** ：``max_delay=120.0`` 确保退避时间不会无限增长。

**为什么不用全随机？** 全随机退避的期望延迟可能过高。
抖动退避保留了指数增长的确定性骨架（``base * 2^n``），
只在骨架上叠加随机偏移，兼顾了"足够快恢复"和"不形成风暴"。

优雅降级
~~~~~~~~~~

**问题** ：上下文压缩依赖 LLM 生成摘要。如果摘要生成本身失败（例如
辅助模型不可用），系统不应该崩溃。

**Hermes 的做法** ：摘要生成失败时，回退到静态压缩策略——
直接删除中间的消息，保留头尾。虽然会丢失一些信息，
但系统仍然可以继续运行。

类似地，在迭代预算耗尽时，Hermes 会给模型一次"宽限调用"（grace call）
来生成最终总结。如果宽限调用也失败，使用静态的兜底消息：

.. code-block:: python

    except Exception as e:
        logging.warning(f"Failed to get summary response: {e}")
        final_response = (
            f"I reached the maximum iterations ({self.max_iterations}) "
            f"but couldn't summarize. Error: {str(e)}"
        )

**教训** ：在一个系统中，每一项"增强功能"（如 LLM 摘要）都应该有
一个"基础版本"的兜底方案。增强功能让系统更好用，兜底方案让系统不会坏。

可扩展性设计
--------------

插件钩子系统
~~~~~~~~~~~~~~

**问题** ：如何在不修改核心代码的前提下，让用户和第三方扩展 Agent 的行为？

**Hermes 的做法** ：定义了 10 个生命周期钩子（lifecycle hooks）：

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 钩子事件
     - 触发时机
   * - ``gateway:startup``
     - 网关进程启动时
   * - ``session:start``
     - 新会话创建时
   * - ``session:end``
     - 会话结束时
   * - ``session:reset``
     - 会话重置完成时
   * - ``agent:start``
     - Agent 开始处理消息时
   * - ``agent:step``
     - 工具循环的每个迭代步骤
   * - ``agent:end``
     - Agent 完成处理时
   * - ``command:*``
     - 任何斜杠命令执行时（通配符匹配）

钩子的设计遵循几个关键原则：

1. **错误隔离** ：钩子错误被捕获并记录，但绝不阻塞主流程。
   ``HookRegistry.emit()`` 中每个处理器都被独立的 try/except 包裹。

2. **通配符匹配** ：``command:*`` 匹配所有 ``command:xxx`` 事件，
   支持一次性监听整类事件。

3. **动态加载** ：钩子从 ``~/.hermes/hooks/`` 目录动态发现和加载，
   不需要修改配置文件。每个钩子目录包含 ``HOOK.yaml`` （元数据）
   和 ``handler.py`` （处理器代码）。

4. **同步/异步兼容** ：钩子处理器可以是同步函数或异步函数，
   框架自动检测并通过 ``asyncio.iscoroutine()`` 分发。

MCP 动态工具发现
~~~~~~~~~~~~~~~~~~

**问题** ：MCP 工具服务器在运行时可能启动、停止、或更新工具列表。
如何让 Agent 动态感知这些变化？

**Hermes 的做法** ：在 ``tools/mcp_tool.py`` 中实现了完整的
MCP 工具发现和动态注册：

- 启动时扫描 ``config.yaml`` 中的 ``mcp_servers`` 配置。
- 连接每个 MCP 服务器，获取其工具列表。
- 将工具注册到全局 ``ToolRegistry`` ，归属 ``mcp-<server_name>`` toolset。
- 当服务器发送 ``notifications/tools/list_changed`` 时，
  先 ``deregister`` 旧工具，再重新注册新工具。

注册表中有一个精巧的冲突解决机制：

.. code-block:: python

    both_mcp = (
        existing.toolset.startswith("mcp-")
        and toolset.startswith("mcp-")
    )
    if both_mcp:
        # MCP 工具允许同名覆盖（同一服务器的工具刷新）
        pass
    else:
        # 非 MCP 工具不允许覆盖内置工具
        logger.error("Tool registration REJECTED: '%s' would shadow existing tool")
        return

这防止了 MCP 工具意外覆盖内置工具，同时允许 MCP 工具之间的同名覆盖
（因为同一服务器刷新工具列表时，新旧版本可能暂时同名）。

工具集组合与菱形依赖
~~~~~~~~~~~~~~~~~~~~~~

**问题** ：工具集（toolsets）可以引用其他工具集，形成组合关系。
如果 A 包含 B 和 C，而 B 也包含 C，那么 C 的工具应该只出现一次。

**Hermes 的做法** （``toolsets.py``）：使用集合操作解析组合关系。

``resolve_toolset()`` 函数递归展开工具集引用，用 ``set()`` 去重，
确保每个工具只出现一次。这解决了工具集组合中的"菱形依赖"问题——
无论一个工具被多少个路径引用，最终只被包含一次。

皮肤主题引擎
~~~~~~~~~~~~~~

**问题** ：如何让用户自定义 CLI 的视觉外观，而不需要修改代码？

**Hermes 的做法** （``hermes_cli/skin_engine.py``）：数据驱动的皮肤系统。

皮肤定义为 YAML 文件，包含颜色、spinner 动画、品牌文案等配置。
缺失的值从 ``default`` 皮肤继承——这是一种主题继承模式。

皮肤的继承关系通过 YAML 的层级结构自然表达：
用户定义的新皮肤只需覆盖想要改变的属性，其余属性自动继承默认值。
这种"约定优于配置"的设计降低了定制门槛。

技术债务反思
--------------

没有完美的系统，Hermes 也不例外。在赞赏其设计亮点的同时，
我们也必须诚实地面对它的技术债务。

12,000 行的上帝类
~~~~~~~~~~~~~~~~~~~

``run_agent.py`` 是一个 12,084 行的单一文件，``AIAgent`` 类
承担了几乎所有核心职责。这是 Hermes 最大的技术债务。

**为什么会这样？** 在早期开发中，Agent 的核心逻辑相对紧凑。
随着功能增加（多提供商支持、流式调用、上下文压缩、错误恢复、
预算控制、插件集成、记忆管理……），逻辑自然地被添加到
``AIAgent`` 类中。每次新增功能似乎都不值得单独提取一个模块，
但累积起来就形成了庞大的上帝类。

**后果** ：

- 难以测试：单元测试需要模拟大量的依赖和状态。
- 难以理解：新开发者需要数天时间才能建立对 ``AIAgent`` 的整体认知。
- 合并冲突：多个开发者同时修改 ``run_agent.py`` 时频繁冲突。

**部分改善** ：Hermes 团队已经将一些功能提取到 ``agent/`` 包中
（如 ``error_classifier.py`` 、``retry_utils.py`` 、``prompt_builder.py`` 、
``context_compressor.py``），这是正确的方向。

分散的提供商特定 Hack
~~~~~~~~~~~~~~~~~~~~~~~

Hermes 对不同提供商的支持中有大量 "if Ollama..." 或
"if provider == 'openrouter'..." 的分支逻辑分散在各处。

这些 Hack 的存在是因为不同提供商的 API 行为差异很大——
例如 Ollama 的上下文长度需要通过 ``/api/show`` 端点查询，
而其他提供商通过模型元数据获取。

理想情况下，提供商差异应该被完全封装在适配器层。
但在实践中，某些差异（如错误消息格式、连接管理、特殊参数）
渗透到了核心逻辑中，因为它们影响的是全局流程而非单一调用点。

父子 Agent 间的预算共享
~~~~~~~~~~~~~~~~~~~~~~~~~

Hermes 的子代理（delegate_task）获得独立的迭代预算（默认 50 次），
但共享父代理的凭证池和 API 速率限制。这意味着一个子代理的大量调用
可能耗尽凭证池，影响父代理和其他并发的子代理。

这种设计在简单场景下工作良好（大部分子代理只执行少量调用），
但在复杂的委派场景（如 Mixture of Agents 工具同时启动多个子代理）
可能造成意外的限流。

缓存失效复杂性
~~~~~~~~~~~~~~~~

系统提示词的缓存依赖"每次构建完全一致"的假设。
但提示词的内容可能因为内存状态变更、技能列表更新、
上下文文件变化等原因而改变。Hermes 通过在内存变更后
标记 ``_cached_system_prompt = None`` 来强制重建，
但这种"手动失效"容易遗漏。

特别是当多个子系统（内存管理器、技能管理器、插件系统）
都能触发提示词变更时，确保每个触发点都正确失效缓存
需要持续 vigilance。

模式与反模式总结
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - 模式
     - 值得学习？
     - 关键要点
   * - 自注册 + AST 预检查
     - 是
     - 零配置扩展，快速发现
   * - 11 类错误分类
     - 是
     - 精确分类优于泛型重试
   * - 持久化事件循环
     - 是
     - 避免 asyncio.run() 陷阱
   * - 乐观并发控制
     - 是
     - 比全局锁更轻量
   * - 三层结果预算
     - 是
     - 分层控制避免单一阈值困境
   * - system_and_3 缓存
     - 是
     - 极高的缓存命中率
   * - 上帝类
     - 否
     - 尽早提取模块
   * - 提供商 Hack 散布
     - 否
     - 适配器层应完全封装差异
   * - 手动缓存失效
     - 警惕
     - 考虑版本号或内容哈希

本章提炼的模式和教训将在下一章——"构建你自己的 Agent"——中
转化为具体的实践指导。我们将基于这些教训，设计一个更干净的架构，
并提供可直接使用的代码模板。
