.. _build-your-own:

构建你自己的 Agent：从零开始的实践指南
===========================================

这是全书的压轴章节。在前面的章节中，我们深入分析了 Hermes Agent
的架构设计，提炼出了通用的工程模式和教训。现在，让我们把这些知识
转化为实践——从头构建一个生产级 Agent。

本章不是 Hermes 的使用教程。我们将基于从 Hermes 学到的经验，
设计一个更干净的架构，并提供可直接使用的代码模板。

最小可行 Agent：200 行 Python
-------------------------------

在深入复杂架构之前，让我们先实现一个最小可行 Agent（MVA）。
它包含了 Agent 的核心循环，但没有 Hermes 的复杂性。
理解这个 MVA 是理解任何 Agent 系统的基础。

.. mermaid::

   graph LR
       A["系统提示词"] --> B["API 调用"]
       C["用户消息"] --> B
       B --> D{"有工具调用?"}
       D -->|是| E["执行工具"]
       E --> B
       D -->|否| F["返回响应"]

完整代码如下：

.. code-block:: python

    """minimal_agent.py — A 200-line AI Agent with tool calling.

    Demonstrates the core observe-think-act loop that every Agent needs:
    1. Build system prompt with available tools
    2. Call LLM API
    3. Parse response for tool calls
    4. Execute tools and feed results back
    5. Repeat until model returns a final text response
    """

    import json
    import os
    import subprocess
    from typing import Any

    from openai import OpenAI


    # ── Tool registry (simplified self-registration pattern) ──────────

    _TOOLS: dict[str, dict[str, Any]] = {}

    def register_tool(name: str, description: str, parameters: dict, handler):
        """Register a tool with its schema and handler function."""
        _TOOLS[name] = {
            "schema": {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                },
            },
            "handler": handler,
        }

    def get_tool_schemas() -> list[dict]:
        """Return all registered tool schemas for the API call."""
        return [t["schema"] for t in _TOOLS.values()]

    def dispatch_tool(name: str, arguments: dict) -> str:
        """Execute a tool by name, return result as JSON string."""
        tool = _TOOLS.get(name)
        if not tool:
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            result = tool["handler"](arguments)
            return json.dumps(result) if not isinstance(result, str) else result
        except Exception as e:
            return json.dumps({"error": f"Tool failed: {e}"})


    # ── Built-in tools ────────────────────────────────────────────────

    def _handle_read_file(args: dict) -> str:
        path = args.get("path", "")
        try:
            return open(path).read()[:50_000]  # Truncate large files
        except FileNotFoundError:
            return json.dumps({"error": f"File not found: {path}"})

    def _handle_write_file(args: dict) -> str:
        path, content = args.get("path", ""), args.get("content", "")
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return json.dumps({"ok": True, "bytes_written": len(content)})

    def _handle_terminal(args: dict) -> str:
        cmd = args.get("command", "")
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30,
        )
        output = result.stdout + result.stderr
        return output[:20_000] if output else "(no output)"

    # Self-register tools (mirrors Hermes pattern)
    register_tool(
        "read_file", "Read a file from disk.",
        {"type": "object", "properties": {"path": {"type": "string"}},
         "required": ["path"]},
        _handle_read_file,
    )
    register_tool(
        "write_file", "Write content to a file.",
        {"type": "object",
         "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
         "required": ["path", "content"]},
        _handle_write_file,
    )
    register_tool(
        "terminal", "Run a shell command.",
        {"type": "object", "properties": {"command": {"type": "string"}},
         "required": ["command"]},
        _handle_terminal,
    )


    # ── Error classification (simplified from Hermes's 11-way) ────────

    def classify_error(error: Exception) -> str:
        """Return recovery strategy: 'retry', 'compress', or 'abort'."""
        status = getattr(error, "status_code", None)
        msg = str(error).lower()

        if status == 429 or "rate limit" in msg:
            return "retry"
        if status in (500, 502, 503):
            return "retry"
        if "context" in msg and ("length" in msg or "token" in msg):
            return "compress"
        if status in (401, 403):
            return "abort"
        return "retry"


    # ── Core Agent Loop ───────────────────────────────────────────────

    class MinimalAgent:
        """A minimal but functional AI Agent with tool calling."""

        def __init__(self, model: str = "gpt-4o", max_iterations: int = 30):
            self.client = OpenAI()
            self.model = model
            self.max_iterations = max_iterations

        def run(self, user_message: str, system_prompt: str = None) -> str:
            """Run the observe-think-act loop until completion."""
            messages = []

            # Build system prompt
            if system_prompt is None:
                system_prompt = (
                    "You are a helpful AI assistant with access to tools. "
                    "Use tools when needed to complete tasks. "
                    "Always provide a final text response when done."
                )
            messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_message})

            # Main loop
            for iteration in range(self.max_iterations):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        tools=get_tool_schemas(),
                    )
                except Exception as e:
                    strategy = classify_error(e)
                    if strategy == "retry":
                        continue  # Simplified: no backoff in MVA
                    if strategy == "abort":
                        return f"Fatal error: {e}"
                    # compress — not implemented in MVA
                    return f"Context too large: {e}"

                choice = response.choices[0]
                assistant_msg = choice.message

                # Append assistant response to history
                messages.append(assistant_msg.model_dump())

                # Check: final text response (no tool calls)
                if not assistant_msg.tool_calls:
                    return assistant_msg.content or "(empty response)"

                # Execute tool calls
                for tool_call in assistant_msg.tool_calls:
                    fn_name = tool_call.function.name
                    try:
                        fn_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        fn_args = {}

                    result = dispatch_tool(fn_name, fn_args)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })

            return "Maximum iterations reached without completion."


    # ── Entry point ───────────────────────────────────────────────────

    if __name__ == "__main__":
        agent = MinimalAgent()
        print("Minimal Agent ready. Type your message (Ctrl+C to quit):")
        while True:
            try:
                user_input = input("\n> ")
                if user_input.strip():
                    response = agent.run(user_input)
                    print(f"\n{response}")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

这个 200 行的 Agent 实现了以下核心功能：

- **工具自注册** ：简化版的 Hermes 自注册模式，工具通过
  ``register_tool()`` 声明 schema 和 handler。
- **核心循环** ：observe-think-act 循环，包含 API 调用、响应解析、
  工具执行。
- **错误分类** ：简化版的错误分类器，将错误映射到三种恢复策略。
- **迭代预算** ：通过 ``max_iterations`` 限制循环次数。

它缺少 Hermes 的以下功能——这些是后续章节要讨论的：

- 流式响应
- 多提供商支持
- 上下文压缩
- 并行工具执行
- 会话持久化
- 认证与安全

架构选型决策
--------------

当你准备超越最小可行 Agent，构建一个更完整的系统时，
你面临的第一个问题不是"写什么代码"，而是"做什么选择"。

单块 vs 微服务
~~~~~~~~~~~~~~~~

.. mermaid::

   graph TD
       Q{"单块还是微服务?"}
       Q -->|"单用户 / 小团队"| M["单块架构<br/>Hermes 的选择"]
       Q -->|"多租户 / 大规模"| S["微服务架构"]
       M --> M1["优点：部署简单<br/>调试方便<br/>延迟最低"]
       M --> M2["缺点：单点故障<br/>难以水平扩展"]
       S --> S1["优点：独立扩展<br/>故障隔离<br/>技术异构"]
       S --> S2["缺点：运维复杂<br/>网络延迟<br/>分布式事务"]

**Hermes 的选择** ：单块架构（monolith）。整个 Agent 运行在单个进程中。

这个选择是正确的，原因如下：

- Hermes 的典型部署场景是单用户 CLI 或网关（单进程多会话）。
  没有多租户需求。
- Agent 的核心循环（API 调用 → 工具执行 → 消息更新）是严格的顺序依赖，
  拆分为微服务不会带来性能收益。
- 单进程内的函数调用比跨服务的 RPC 快几个数量级。
  在 Agent 的紧密循环中，这个延迟差异是显著的。

**何时选择微服务** ：

- 需要 Agent 作为服务同时服务成百上千用户。
- 工具执行需要隔离（不同用户的代码不能在同一进程运行）。
- 不同组件有不同的扩展需求（如工具执行需要大量 CPU，
  而 API 调用需要大量网络 I/O）。

同步 vs 异步
~~~~~~~~~~~~~~

**Hermes 的选择** ：同步主循环 + 异步桥接。

Hermes 的主循环（``run_conversation()``）是完全同步的。
异步操作（如 httpx 异步客户端）通过 ``_run_async()`` 桥接到同步上下文。

这个看似"不优雅"的选择有其深刻的原因：

1. **调试友好** ：同步代码的调用栈是线性的，异常直接传播。
   异步代码的异常传播跨越多个协程，调试难度显著增加。

2. **避免事件循环复杂性** ：Python 的 ``asyncio`` 在多线程环境中
   容易产生微妙的问题（如事件循环所有权、线程安全）。
   Hermes 通过"只在需要时桥接到异步"的策略，将异步的复杂性
   限制在工具执行层。

3. **工具兼容性** ：许多 Python 库（如 subprocess、文件 I/O）
   是同步的。使用异步主循环意味着每个同步调用都需要
   ``loop.run_in_executor()`` ，增加样板代码。

**何时选择全异步** ：

- 网关服务需要同时处理数百个并发连接。
- 大部分操作是 I/O 密集型（网络请求、文件读写）。
- 团队对 asyncio 有深入理解。

数据库：SQLite vs PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Hermes 的选择** ：SQLite + WAL 模式。

SQLite 的优势在于零配置、零运维。对于 Hermes 的场景
（单机部署、中等写入频率、读多写少），SQLite 完全足够。
WAL 模式解决了基本的并发读写问题。

**何时选择 PostgreSQL** ：

- 多实例部署（多个网关进程共享数据库）。
- 需要复杂的查询（如全文搜索、聚合分析）。
  注意 Hermes 通过 SQLite FTS5 实现了全文搜索，
  但 FTS5 的功能比 PostgreSQL 的全文搜索有限。
- 写入频率极高（SQLite 的写入吞吐量受 WAL checkpoint 影响）。

通信协议：JSON-RPC vs gRPC vs REST
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Hermes 的选择** ：JSON-RPC over stdin/stdout（TUI 网关）。

TUI（Terminal User Interface）与 Agent 之间的通信使用 JSON-RPC，
通过进程的 stdin/stdout 传输。这个选择是因为：

- **简单性** ：JSON-RPC 比 gRPC 简单得多，不需要 .proto 文件和代码生成。
- **进程隔离** ：TUI 和 Agent 可以是不同的进程，
  stdin/stdout 是最简单的跨进程通信方式。
- **可调试性** ：JSON-RPC 消息是人类可读的，
  方便调试和日志分析。

**何时选择 gRPC** ：

- 高频调用、低延迟需求。
- 强类型接口定义重要。
- 需要双向流式通信。

**何时选择 REST** ：

- 面向外部 API（第三方集成）。
- 需要通过 HTTP 代理/防火墙。

工具系统设计
--------------

从 Hermes 的经验中，我们可以提炼出设计工具系统的四步法。

第一步：定义工具注册接口
~~~~~~~~~~~~~~~~~~~~~~~~~~

工具注册接口应该包含以下信息：

- **name** ：工具的唯一标识符。
- **description** ：对 LLM 的描述（这直接影响模型是否正确选择工具）。
- **parameters** ：JSON Schema 格式的参数定义。
- **handler** ：实际的执行函数。
- **availability_check** （可选）：运行时检查工具是否可用。
- **max_result_size** （可选）：工具返回结果的最大大小限制。

第二步：实现自注册模式
~~~~~~~~~~~~~~~~~~~~~~~~

每个工具文件在模块级别调用注册函数。使用 Hermes 的 AST 预检查技巧
来高效发现需要导入的文件：

.. code-block:: python

    import ast
    from pathlib import Path

    def discover_tools(tools_dir: Path):
        """Discover and import tool modules that register themselves."""
        for path in sorted(tools_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue
            if not _has_register_call(path):
                continue
            importlib.import_module(f"tools.{path.stem}")

    def _has_register_call(path: Path) -> bool:
        """Check if a module contains a top-level register() call."""
        tree = ast.parse(path.read_text())
        return any(
            isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Call)
            and isinstance(stmt.value.func, ast.Name)
            and stmt.value.func.id == "register"
            for stmt in tree.body
        )

第三步：参数验证与类型强制转换
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LLM 返回的工具参数是 JSON 字符串，需要解析和验证。
Hermes 的经验表明，以下类型转换是必要的：

- **字符串 "true"/"false"** → 布尔值（模型经常返回字符串而非布尔值）。
- **数字字符串** → int 或 float（JSON schema 说 "type": "number"，
  但模型可能返回 "42" 而非 42）。
- **逗号分隔字符串** → 列表（模型可能将列表参数序列化为单个字符串）。

第四步：并行执行策略
~~~~~~~~~~~~~~~~~~~~~~

基于 Hermes 的三级并行策略：

.. code-block:: python

    NEVER_PARALLEL = {"clarify", "user_input"}
    PARALLEL_SAFE = {"web_search", "read_file", "list_files"}
    PATH_SCOPED = {"read_file", "write_file"}

    def should_parallelize(tool_calls):
        names = [tc.name for tc in tool_calls]
        if any(n in NEVER_PARALLEL for n in names):
            return False

        paths = []
        for tc in tool_calls:
            if tc.name not in PARALLEL_SAFE and tc.name not in PATH_SCOPED:
                return False
            if tc.name in PATH_SCOPED:
                path = Path(tc.args.get("path", ""))
                if any(paths_overlap(path, p) for p in paths):
                    return False
                paths.append(path)

        return len(tool_calls) > 1

上下文管理策略
----------------

上下文管理是 Agent 系统中最棘手的问题之一。以下是基于 Hermes 经验的指导原则。

何时压缩
~~~~~~~~~~

不要等到 API 返回上下文溢出错误再压缩。Hermes 的策略是**预压缩** ：

在每轮对话开始前，估算当前消息的 token 数。如果超过阈值
（通常是上下文窗口的 70-80%），主动触发压缩。

预压缩的好处是避免了一次注定失败的 API 调用（省时间、省钱），
以及避免了将上下文溢出错误与其他错误混淆的风险。

如何摘要
~~~~~~~~~~

Hermes 的摘要模板包含以下关键部分：

1. **免责声明** ：明确告知模型"这是历史摘要，不是当前指令"。
   这防止模型执行摘要中提到的已完成任务。

2. **已解决的问题** ：列出已经处理完毕的请求，避免重复执行。

3. **待解决的问题** ：列出尚未完成的任务，确保模型知道从哪里继续。

4. **当前状态** ：文件系统状态、配置变更等，帮助模型理解环境。

5. **活跃任务** ：明确标注当前应该继续的任务。

Token 预算
~~~~~~~~~~~~

为摘要分配足够的 token，但不浪费：

.. code-block:: python

    # Hermes 的公式：压缩内容的 20%，但有上限和下限
    summary_tokens = min(
        max(compressed_tokens * 0.20, 2000),
        12_000,
    )

缓存策略
~~~~~~~~~~

Prompt 缓存的关键原则：

1. **系统提示词必须稳定** ：在会话内不要修改系统提示词。
   如果必须修改（如加载新记忆），将变更放在用户消息中。

2. **缓存断点位置** ：系统提示词 + 最近几条消息。
   Anthropic 限制 4 个断点，合理分配。

3. **连续会话的一致性** ：当从数据库恢复会话时，
   使用存储的系统提示词而非重新构建，确保缓存命中。

多 Provider 支持
------------------

如果你需要支持多个 LLM 提供商，以下是基于 Hermes 经验的指导。

适配器模式实现
~~~~~~~~~~~~~~~~

为每个提供商实现一个适配器，将提供商特有的 API 转换为统一的内部格式：

.. code-block:: python

    from types import SimpleNamespace

    def normalize_openai_response(response) -> SimpleNamespace:
        """Convert OpenAI response to unified format."""
        choice = response.choices[0]
        msg = choice.message
        return SimpleNamespace(
            content=msg.content,
            tool_calls=msg.tool_calls,
            finish_reason=choice.finish_reason,
        )

    def normalize_anthropic_response(response) -> SimpleNamespace:
        """Convert Anthropic response to unified format."""
        content_blocks = response.content
        text = ""
        tool_calls = []
        for block in content_blocks:
            if block.type == "text":
                text += block.text
            elif block.type == "tool_use":
                tool_calls.append(block)
        return SimpleNamespace(
            content=text or None,
            tool_calls=tool_calls or None,
            finish_reason=response.stop_reason,
        )

``SimpleNamespace`` 的选择是有意为之的——它轻量、灵活、
不需要定义数据类，非常适合作为适配器层的中间格式。

客户端缓存考量
~~~~~~~~~~~~~~~~

不同提供商的 SDK 有不同的客户端生命周期管理。

- OpenAI SDK 的 ``OpenAI()`` 客户端维护连接池，可以复用。
- Anthropic SDK 类似，但有额外的认证刷新逻辑。
- Bedrock 使用 boto3 session，有自己的凭证链。

关键原则：**不要为每次 API 调用创建新的客户端实例** 。
客户端创建涉及连接建立和 TLS 握手，频繁创建会显著增加延迟。
Hermes 通过懒初始化和客户端缓存来避免这个问题。

错误恢复跨提供商
~~~~~~~~~~~~~~~~~~

当主提供商失败时，Hermes 可以自动回退到备用提供商。
跨提供商的错误恢复需要考虑：

- 不同提供商的模型能力不同。回退时可能需要调整提示词
  （如移除 Anthropic 特有的 thinking 指令）。
- 上下文格式可能不兼容。OpenAI 的消息格式与 Anthropic 有细微差异。
- 工具 schema 格式需要转换（如 Anthropic 不支持某些 JSON Schema 特性）。

Hermes 通过 ``api_mode`` 分支来处理这些差异。
更优雅的做法是将差异完全封装在适配器层。

部署考量
----------

CLI vs Web vs API
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 部署模式
     - 优点
     - 缺点
   * - CLI
     - 开发者友好、零部署、本地访问
     - 单用户、无远程访问
   * - Web UI
     - 用户友好、远程访问
     - 需要 Web 服务器、认证、状态管理
   * - API 服务
     - 可编程集成、可水平扩展
     - 需要认证、限流、监控

Hermes 同时支持 CLI 模式（直接在终端运行）和网关模式
（通过 RPC 服务多平台用户）。两种模式共享同一个 ``AIAgent`` 核心，
差异只在"谁调用 ``run_conversation()``"和"回调如何传递"。

进程隔离：SlashWorker 模式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hermes 的 TUI 网关使用了一个精巧的进程隔离模式来处理斜杠命令：

.. mermaid::

   graph LR
       A["TUI 网关<br/>(主进程)"] -->|"JSON-RPC<br/>via stdin/stdout"| B["SlashWorker<br/>(子进程)"]
       B -->|"持久化<br/>HermesCLI"| C["会话状态"]
       A -->|"直接调用"| D["Agent 核心<br/>(AIAgent)"]

SlashWorker（``tui_gateway/slash_worker.py``）是一个持久化的子进程，
负责处理斜杠命令（如 ``/config`` 、``/model`` 、``/tools``）。
它在启动时创建一个 ``HermesCLI`` 实例，然后通过 stdin/stdout
的 JSON-RPC 协议接收命令、返回结果。

这个设计的好处是：

- **隔离** ：斜杠命令的崩溃不影响主网关进程。
- **持久化** ：``HermesCLI`` 实例在整个会话生命周期内保持，
  避免了每次命令都重新初始化的开销。
- **简单性** ：stdin/stdout 通信比 socket 或共享内存简单得多。

会话持久化
~~~~~~~~~~~~

Hermes 的会话持久化策略：

1. **SQLite + WAL 模式** ：多进程安全，零运维。
2. **批量写入** ：消息不是逐条写入，而是在 turn 结束时批量 flush。
3. **压缩触发会话分裂** ：上下文压缩会创建新的会话记录，
   通过 ``parent_session_id`` 链接。

一个完整的示例架构
--------------------

综合以上所有讨论，以下是一个推荐的生产级 Agent 架构：

.. mermaid::

   graph TB
       subgraph "用户界面层"
           CLI["CLI / TUI"]
           WEB["Web UI"]
           API["API Gateway"]
       end
       subgraph "Agent 核心"
           LOOP["Agent Loop<br/>observe-think-act"]
           BUDGET["Budget Manager<br/>迭代 / Token / 结果"]
           ERR["Error Classifier<br/>错误分类与恢复"]
       end
       subgraph "工具系统"
           REG["Tool Registry<br/>自注册 + AST 发现"]
           DISPATCH["Tool Dispatcher<br/>并行 / 串行策略"]
           MCP["MCP Client<br/>动态工具发现"]
       end
       subgraph "上下文管理"
           COMPRESS["Context Compressor<br/>预压缩 + LLM 摘要"]
           CACHE["Prompt Cache<br/>system_and_3"]
           MEMORY["Memory Manager<br/>长期记忆"]
       end
       subgraph "Provider 适配层"
           OA["OpenAI Adapter"]
           AN["Anthropic Adapter"]
           BR["Bedrock Adapter"]
           CRED["Credential Pool<br/>轮换 + 冷却"]
       end
       subgraph "持久化层"
           DB["SQLite / PostgreSQL<br/>WAL 模式"]
           FS["文件系统<br/>工具结果持久化"]
       end
       CLI --> LOOP
       WEB --> LOOP
       API --> LOOP
       LOOP --> BUDGET
       LOOP --> ERR
       LOOP --> REG
       REG --> DISPATCH
       REG --> MCP
       LOOP --> COMPRESS
       COMPRESS --> CACHE
       LOOP --> MEMORY
       LOOP --> OA
       LOOP --> AN
       LOOP --> BR
       OA --> CRED
       AN --> CRED
       BR --> CRED
       LOOP --> DB
       DISPATCH --> FS

数据流：从用户到 LLM 再回来
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
       participant U as 用户
       participant A as Agent Loop
       participant P as Provider Adapter
       participant L as LLM API
       participant T as Tool Registry
       participant D as 数据库
   
       U->>A: 用户消息
       A->>D: 加载会话历史
       A->>A: 构建系统提示词
       A->>A: 预压缩检查
       A->>P: API 调用 (带工具 schema)
       P->>L: HTTP 请求
       L-->>P: 流式响应
       P-->>A: 归一化响应
   
       alt 有工具调用
           A->>T: dispatch(tool_name, args)
           T-->>A: 工具结果
           A->>A: 追加消息到历史
           A->>P: API 调用 (带工具结果)
           P->>L: HTTP 请求
           L-->>P: 响应
           P-->>A: 归一化响应
       end
   
       A->>D: 持久化消息
       A-->>U: 最终响应

推荐技术栈
~~~~~~~~~~~~

基于 Hermes 的经验和教训，以下是我们推荐的技术栈：

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 组件
     - 推荐选择
     - 理由
   * - 语言
     - Python 3.11+
     - LLM SDK 生态最成熟
   * - LLM SDK
     - OpenAI SDK + provider adapters
     - 统一接口 + 差异封装
   * - 数据库
     - SQLite (单机) / PostgreSQL (分布式)
     - WAL 模式解决并发
   * - 异步框架
     - 同步主循环 + 按需桥接
     - 调试友好，避免 asyncio 陷阱
   * - 工具注册
     - 自注册 + AST 发现
     - 零配置扩展
   * - 错误处理
     - 分类器管线 + 抖动退避
     - 精确恢复策略
   * - 上下文管理
     - 预压缩 + LLM 摘要 + Prompt 缓存
     - 75%+ 输入 token 节省
   * - 部署
     - 单进程 (CLI) / JSON-RPC (网关)
     - 简单可靠

从原型到生产的路线图
----------------------

以下是将 MVA 发展为生产级 Agent 的建议路线图：

**阶段一：核心功能** （1-2 周）

- 实现基本的工具注册和调度。
- 添加错误分类和重试逻辑。
- 实现基本的会话持久化。

**阶段二：稳定性** （2-4 周）

- 添加上下文压缩。
- 实现预压缩检查。
- 添加多提供商支持（至少两个提供商）。
- 实现凭证池和轮换。

**阶段三：性能** （1-2 周）

- 实现并行工具执行。
- 添加 Prompt 缓存。
- 优化工具结果大小管理（三层预算）。

**阶段四：可扩展性** （2-4 周）

- 添加插件/钩子系统。
- 实现 MCP 工具集成。
- 添加皮肤/主题系统。

**阶段五：运营** （持续）

- 监控和告警。
- 日志分析和调试工具。
- 性能基准测试和回归检测。

每个阶段都建立在前一个阶段的基础上，且每个阶段结束时
都有一个可运行的、比之前更健壮的系统。这种增量式的方法
降低了"大爆炸失败"的风险，也让你在开发过程中持续获得反馈。

最后的话
----------

构建一个生产级 Agent 的核心挑战不是算法或架构，
而是工程——处理边界情况、做设计权衡、在混乱中保持可靠。

Hermes Agent 的 12,000 行代码是一个宝贵的工程学习素材。
它不是完美的——它有上帝类、分散的提供商 Hack、缓存失效的复杂性。
但正是这些不完美让它更有教育意义：它展示了真实系统如何在
时间压力、需求变更和资源约束下演进。

如果你从这本书中只带走一个教训，那就是：

**简单的、可靠的、可调试的方案，永远优于优雅的、复杂的、
难以理解的方案。** Hermes 的同步主循环、"简单粗暴"的错误消息匹配、
基于 AST 的工具发现——这些都不是最"优雅"的设计，
但它们在实际运行中证明了有效性。

在 Agent 的世界里，工程智慧就是知道什么时候选择简单。
