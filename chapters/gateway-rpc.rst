.. _chapter-gateway-rpc:

**************************************
TUI Gateway：跨进程 JSON-RPC 通信
**************************************

.. contents::
   :local:
   :depth: 2

为什么需要 Gateway
====================

Hermes Agent 有两种主要的前端界面：

1. **CLI 模式** （``hermes chat``）：Python REPL，直接在终端中运行，Agent 和 UI 在同一个进程中
2. **TUI 模式** （TypeScript/React 前端）：一个独立的富 GUI 应用，用 Electron 或 Web 技术构建

问题在于：Agent 核心是 Python 写的（``AIAgent`` 类），而 TUI 前端是 TypeScript 写的。
它们运行在 **不同的进程中** ，甚至可能在不同的机器上（远程部署场景）。

Gateway 就是连接这两者的桥梁：

.. mermaid::
   :name: gateway-architecture
   :caption: Gateway 架构总览

   flowchart TD
       subgraph TUI["TUI 前端 (TypeScript/React)"]
           UI1["消息输入框"]
           UI2["工具状态面板"]
           UI3["对话历史"]
           UI4["设置面板"]
       end

       subgraph GW["TUI Gateway (Python 进程)"]
           GW1["JSON-RPC 调度器"]
           GW2["会话管理器"]
           GW3["Agent 工厂"]
           GW4["SlashWorker 子进程"]
       end

       subgraph AGENT["Agent 核心"]
           A1["AIAgent"]
           A2["工具执行"]
           A3["流式输出"]
           A4["上下文压缩"]
       end

       TUI -- "stdin/stdout JSON Lines" --> GW
       GW -- "线程池 + 回调" --> AGENT
       GW -- "stdin/stdout JSON Lines" --> GW4
       AGENT -- "事件流" --> GW
       GW -- "事件推送" --> TUI

Gateway 作为一个独立的 Python 进程运行，通过 **stdin/stdout 管道** 与 TUI 前端通信。
TUI 前端启动 Gateway 进程，将 JSON-RPC 请求写入 Gateway 的 stdin，从 Gateway 的 stdout 读取响应和事件。

这种架构的优势：

- **语言无关性** ：前端可以用任何语言实现，只需遵循 JSON-RPC 协议
- **进程隔离** ：Agent 崩溃不会拖垮前端，反之亦然
- **安全性** ：前端无法直接访问 Python 运行时，所有操作通过 RPC 方法暴露
- **可扩展性** ：Gateway 可以同时管理多个会话，每个会话有独立的 Agent 实例

通信协议
==========

Gateway 使用 **JSON-RPC 2.0 over stdin/stdout (JSON Lines)** 协议。

请求格式
----------

每个请求是一个单行 JSON 对象：

.. code-block:: json

   {"jsonrpc": "2.0", "id": 1, "method": "prompt.submit", "params": {"session_id": "abc123", "text": "Hello"}}

响应格式
----------

成功响应：

.. code-block:: json

   {"jsonrpc": "2.0", "id": 1, "result": {"status": "streaming"}}

错误响应：

.. code-block:: json

   {"jsonrpc": "2.0", "id": 1, "error": {"code": 4009, "message": "session busy"}}

事件推送（无 id，单向通知）：

.. code-block:: json

   {"jsonrpc": "2.0", "method": "event", "params": {"type": "message.delta", "session_id": "abc123", "payload": {"text": "Hello"}}}

Stdout 保护
-------------

Gateway 将 Python 的 ``sys.stdout`` 重定向到 ``sys.stderr`` ，
确保所有 Python 的 ``print()`` 调用不会污染 JSON 协议通道：

.. code-block:: python

   _real_stdout = sys.stdout
   sys.stdout = sys.stderr

所有 JSON 输出通过 ``write_json()`` 函数，使用 ``_stdout_lock`` 保证线程安全：

.. code-block:: python

   def write_json(obj: dict) -> bool:
       line = json.dumps(obj, ensure_ascii=False) + "\n"
       try:
           with _stdout_lock:
               _real_stdout.write(line)
               _real_stdout.flush()
           return True
       except BrokenPipeError:
           return False

当 ``write_json()`` 返回 ``False`` 时（管道断裂），Gateway 进程优雅退出。
这在 TUI 前端关闭时自动触发。

错误码体系
------------

Gateway 定义了一组语义化的错误码：

.. list-table:: Gateway 错误码
   :header-rows: 1
   :widths: 15 40 45

   * - 错误码
     - 含义
     - 典型场景
   * - -32700
     - JSON 解析错误
     - 格式错误的请求行
   * - -32601
     - 未知方法
     - 调用不存在的 RPC 方法
   * - -32000
     - 处理器内部错误
     - 未预期的异常
   * - 4001
     - 会话未找到
     - 使用无效的 session_id
   * - 4002
     - 参数无效
     - 缺少必需参数
   * - 4009
     - 会话繁忙
     - 在 Agent 运行时发送新请求
   * - 5032
     - Agent 初始化超时
     - 模型提供者不可用

双调度架构
============

Gateway 的 RPC 调度器采用 **双轨设计** ，根据方法名将请求路由到不同的执行通道：

.. mermaid::
   :name: gateway-dual-dispatch
   :caption: 双调度架构

   flowchart LR
       INPUT["stdin JSON-RPC"] --> PARSER["JSON 解析"]
       PARSER --> ROUTER{"dispatch() 路由"}

       ROUTER -->|"快速方法<br/>(prompt.submit,<br/>clarify.respond 等)"| INLINE["主线程<br/>handle_request()"]
       ROUTER -->|"长时方法<br/>(slash.exec,<br/>session.resume 等)"| POOL["ThreadPoolExecutor<br/>线程池"]

       INLINE --> RESP1["直接返回响应"]
       POOL --> RESP2["write_json()<br/>异步写入响应"]

       subgraph "长时处理器列表"
           L1["cli.exec"]
           L2["session.branch"]
           L3["session.resume"]
           L4["shell.exec"]
           L5["slash.exec"]
       end

内联处理器（主线程）
----------------------

大多数 RPC 方法在主线程中执行。这些是 **快速操作**——读取配置、返回会话信息、
响应交互请求等。它们的响应直接从 ``dispatch()`` 返回。

长时处理器（线程池）
----------------------

部分 RPC 方法可能阻塞数秒到数分钟。如果在主线程中执行它们，会阻塞 stdin 读取循环，
导致其他 RPC 请求（特别是 ``approval.respond`` 和 ``session.interrupt``）无法被处理。

.. code-block:: python

   _LONG_HANDLERS = frozenset({
       "cli.exec", "session.branch", "session.resume", "shell.exec", "slash.exec"
   })

   _pool = concurrent.futures.ThreadPoolExecutor(
       max_workers=max(2, int(os.environ.get("HERMES_TUI_RPC_POOL_WORKERS", "4") or 4)),
       thread_name_prefix="tui-rpc",
   )

长时处理器被提交到线程池执行。响应通过 ``write_json()`` 异步写入——
这个函数已经被 ``_stdout_lock`` 保护，所以并发写入是安全的。

初始化握手
============

Gateway 启动时，会进行一次 **初始化握手** ：

.. code-block:: python

   # entry.py main()
   if not write_json({
       "jsonrpc": "2.0",
       "method": "event",
       "params": {"type": "gateway.ready", "payload": {"skin": resolve_skin()}},
   }):
       sys.exit(0)

这条消息告诉 TUI 前端：

1. Gateway 已成功启动
2. 当前活跃的皮肤配置（颜色、品牌、工具前缀等）

TUI 前端收到 ``gateway.ready`` 事件后，才能开始发送 RPC 请求。

如果 stdout 已关闭（TUI 前端已退出），``write_json()`` 返回 ``False`` ，
Gateway 立即退出。

信号处理
----------

Gateway 注册了两个信号处理器：

.. code-block:: python

   signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # 管道断裂时优雅退出
   signal.signal(signal.SIGINT, signal.SIG_IGN)   # 忽略 Ctrl+C

- **SIGPIPE** ：当 TUI 前端关闭 stdout 管道时触发，使用默认处理器让进程退出
- **SIGINT** ：忽略终端的 Ctrl+C，防止意外中断。Agent 的中断通过 RPC 方法 ``session.interrupt`` 触发

prompt.submit 完整流程
========================

``prompt.submit`` 是 Gateway 最核心的 RPC 方法，它处理用户发送的每一条消息。
以下是完整的执行流程：

.. mermaid::
   :name: gateway-prompt-submit
   :caption: prompt.submit 完整时序

   sequenceDiagram
       autonumber
       participant TUI as TUI 前端
       participant GW as Gateway
       participant Session as 会话管理器
       participant Agent as AIAgent
       participant Stream as 流式渲染器

       TUI->>GW: prompt.submit {session_id, text}
       GW->>Session: 查找会话
       Session-->>GW: session dict

       alt 会话繁忙
           GW-->>TUI: error 4009 "session busy"
       end

       Note over Session: 设置 running = True<br/>快照 history_version

       GW->>GW: 附加图片预处理
       GW->>GW: @上下文引用展开
       GW-->>TUI: {status: "streaming"}<br/>（立即返回）

       Note over GW: 后台线程开始执行

       GW->>Agent: run_conversation(text, history)

       loop 流式输出
           Agent-->>GW: delta text
           GW->>Stream: feed(delta) → 渲染
           GW-->>TUI: event message.delta {text, rendered}
       end

       alt 工具调用
           Agent-->>GW: tool_start_callback
           GW-->>TUI: event tool.start {name, context}
           Agent-->>GW: tool_complete_callback
           GW-->>TUI: event tool.complete {name, summary, inline_diff}
       end

       alt 思维过程
           Agent-->>GW: thinking_callback
           GW-->>TUI: event thinking.delta {text}
       end

       Agent-->>GW: 最终结果

       GW->>Session: 写入历史（版本检查）
       Note over Session: history_version 匹配?<br/>匹配 → 写入<br/>不匹配 → 丢弃

       GW->>Session: 设置 running = False
       GW-->>TUI: event message.complete {text, usage, status}

时序分析
----------

1. **请求验证** （< 1ms）：检查 session_id 是否存在，会话是否繁忙
2. **状态锁定** （< 1ms）：设置 ``running = True`` ，快照 ``history_version``
3. **预处理** （0-5s）：图片附件通过 vision 预分析，``@`` 上下文引用展开
4. **立即响应** （< 1ms）：返回 ``{status: "streaming"}`` ，不等待 Agent 完成
5. **Agent 执行** （1s - 数分钟）：后台线程运行 ``run_conversation()``
6. **流式输出** （实时）：每个 token delta 立即推送到 TUI
7. **工具反馈** （实时）：工具开始/完成事件
8. **结果写入** （< 1ms）：带版本检查的历史写入
9. **状态释放** （< 1ms）：设置 ``running = False``

关键设计决策：**prompt.submit 立即返回 ``{status: "streaming"}``** 。
这意味着 TUI 前端不需要等待 Agent 完成，可以继续处理用户的其他操作（如发送 ``/interrupt``）。

56 个 RPC 方法分类表
======================

``tui_gateway/server.py``（3086 行）通过 ``@method`` 装饰器定义了 56 个 RPC 方法，
按功能分为十二大类。

Session（会话管理）— 13 个方法
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - session.create
     - 创建新会话（异步构建 Agent，返回 session_id）
     - 快速
   * - session.close
     - 关闭会话，释放 Agent 和 SlashWorker
     - 快速
   * - session.list
     - 列出历史会话（TUI + CLI，合并排序）
     - 快速
   * - session.resume
     - 恢复之前的会话（按 session_id 或标题查找）
     - **长时**
   * - session.title
     - 获取/设置会话标题
     - 快速
   * - session.usage
     - 获取 token 使用量
     - 快速
   * - session.history
     - 获取对话历史（转换为 messages 数组）
     - 快速
   * - session.undo
     - 撤销最后一轮对话（运行中拒绝执行）
     - 快速
   * - session.compress
     - 手动压缩上下文（运行中拒绝执行）
     - 快速
   * - session.save
     - 保存对话到 JSON 文件
     - 快速
   * - session.branch
     - 从当前会话分支新会话（加载完整历史）
     - **长时**
   * - session.interrupt
     - 中断当前 Agent 执行（设置 interrupted 标志）
     - 快速
   * - session.steer
     - 注入消息到下一个工具结果（不中断，不违反 role 交替规则）
     - 快速

Prompt（提示处理）— 4 个方法
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - prompt.submit
     - 提交用户消息（流式响应，立即返回 streaming 状态）
     - 快速（返回后异步执行）
   * - prompt.background
     - 后台执行提示（独立 Agent 实例，返回 task_id）
     - 快速
   * - prompt.btw
     - 旁注式提问（不持久化，无工具，max_iterations=8）
     - 快速
   * - clipboard.paste
     - 从系统剪贴板粘贴图片到附件列表
     - 快速

Media（媒体附件）— 2 个方法
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - image.attach
     - 附加本地图片（验证格式，读取元数据，估算 token）
     - 快速
   * - input.detect_drop
     - 检测文件拖放（区分图片和普通文件）
     - 快速

Interaction（交互响应）— 4 个方法
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - clarify.respond
     - 响应 clarify 请求（唤醒阻塞的 Agent 线程）
     - 快速
   * - sudo.respond
     - 响应 sudo 密码请求（唤醒阻塞的 Agent 线程）
     - 快速
   * - secret.respond
     - 响应 secret 输入请求（唤醒阻塞的 Agent 线程）
     - 快速
   * - approval.respond
     - 响应命令审批请求（approve/deny，支持 resolve_all）
     - 快速

Config（配置管理）— 3 个方法
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - config.set
     - 设置配置项（model/reasoning/skin/personality/voice 等）
     - 快速
   * - config.get
     - 读取配置项（provider/full/prompt/skin/reasoning/compact 等）
     - 快速
   * - config.show
     - 返回结构化的配置概览（Model/Agent/Environment 分节）
     - 快速

Completion（补全）— 2 个方法
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - complete.path
     - 文件路径补全（支持 ``@file:`` / ``@folder:`` 上下文引用）
     - 快速
   * - complete.slash
     - Slash 命令补全（合并 COMMAND_REGISTRY + skill commands + TUI extras）
     - 快速

Command（命令）— 4 个方法
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - command.resolve
     - 解析命令名/别名（返回规范名称和元数据）
     - 快速
   * - command.dispatch
     - 调度 slash 命令（skill/plugin/quick command 前置处理）
     - 快速
   * - commands.catalog
     - 获取完整命令目录（COMMAND_REGISTRY + skills + quick_commands）
     - 快速
   * - cli.exec
     - 执行 hermes CLI 子命令（subprocess，最长 600s 超时）
     - **长时**

Voice（语音）— 3 个方法
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - voice.toggle
     - 开关语音模式（status/on/off，持久化到 config）
     - 快速
   * - voice.record
     - 控制语音录制（start/stop，stop 时自动转录返回文本）
     - 快速
   * - voice.tts
     - 文字转语音播放（后台线程执行 speak_text）
     - 快速

Model & Tools（模型与工具）— 6 个方法
---------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - model.options
     - 列出所有已认证 Provider 及其可用模型
     - 快速
   * - tools.list
     - 列出所有 toolset 及其工具（含启用状态）
     - 快速
   * - tools.show
     - 列出所有工具定义（按 toolset 分组，含描述）
     - 快速
   * - tools.configure
     - 启用/禁用 toolset 或 MCP server（重置 Agent 刷新工具）
     - 快速
   * - toolsets.list
     - 列出所有 toolset 概览（不含工具详情）
     - 快速
   * - reload.mcp
     - 重新加载所有 MCP server（shutdown → discover → refresh_tools）
     - 快速

System（系统管理）— 8 个方法
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - terminal.resize
     - 更新终端宽度（影响流式渲染器列宽）
     - 快速
   * - setup.status
     - 检查是否有 Provider 已配置
     - 快速
   * - process.stop
     - 终止所有后台进程（process_registry.kill_all）
     - 快速
   * - paste.collapse
     - 折叠粘贴的长文本（保存到 ~/.hermes/pastes/，返回占位符）
     - 快速
   * - shell.exec
     - 执行 shell 命令（subprocess，30s 超时，含危险命令检测）
     - 快速
   * - agents.list
     - 列出所有后台 Agent 进程
     - 快速
   * - plugins.list
     - 列出所有已加载插件
     - 快速
   * - insights.get
     - 获取使用洞察（按天数统计会话数和消息数）
     - 快速

Rollback（快照回滚）— 3 个方法
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - rollback.list
     - 列出所有 Git 快照 checkpoint
     - 快速
   * - rollback.restore
     - 恢复到指定 checkpoint（支持 file_path 单文件回滚）
     - 快速
   * - rollback.diff
     - 查看 checkpoint 的 diff（含渲染后的 inline diff）
     - 快速

Advanced（高级功能）— 4 个方法
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - 方法名
     - 功能
     - 阻塞性
   * - browser.manage
     - 管理浏览器 CDP 连接（status/connect/disconnect）
     - 快速
   * - cron.manage
     - 管理定时任务（list/add/remove/pause/resume）
     - 快速
   * - skills.manage
     - 管理 Skill（list/search/install/browse/inspect）
     - 快速
   * - slash.exec
     - 在 SlashWorker 子进程中执行 slash 命令（含副作用镜像）
     - **长时**

阻塞式提示机制
================

Gateway 的阻塞式提示机制是其最精妙的设计之一。当 Agent 需要用户交互时（clarify、sudo、secret），
它会 **阻塞 Agent 线程** ，等待 TUI 前端的响应。

_block() 函数
---------------

.. code-block:: python

   def _block(event: str, sid: str, payload: dict, timeout: int = 300) -> str:
       rid = uuid.uuid4().hex[:8]      # 生成唯一请求 ID
       ev = threading.Event()           # 创建同步事件
       _pending[rid] = (sid, ev)       # 注册到全局等待表
       payload["request_id"] = rid
       _emit(event, sid, payload)       # 推送事件到 TUI
       ev.wait(timeout=timeout)         # 阻塞等待
       _pending.pop(rid, None)         # 清理
       return _answers.pop(rid, "")     # 返回答案

这个函数的工作原理：

1. 生成一个唯一的 ``request_id`` （8 字符十六进制）
2. 创建一个 ``threading.Event`` 作为同步原语
3. 将 ``(session_id, Event)`` 对注册到 ``_pending`` 字典
4. 通过 ``_emit()`` 向 TUI 前端推送交互请求
5. **阻塞当前线程** ，等待 Event 被设置
6. 从 ``_answers`` 字典获取 TUI 前端的响应

.. mermaid::
   :name: gateway-block-mechanism
   :caption: _block() 阻塞提示机制

   sequenceDiagram
       autonumber
       participant Agent as Agent 线程
       participant Block as _block()
       participant TUI as TUI 前端
       participant Pending as _pending 字典
       participant Answers as _answers 字典

       Agent->>Block: 需要用户输入<br/>(clarify/sudo/secret)
       Block->>Pending: 注册 (rid, sid, Event)
       Block->>TUI: 推送事件<br/>clarify.request {question, choices, request_id}

       Note over Block: ev.wait() 阻塞

       TUI->>TUI: 显示交互 UI
       TUI->>TUI: 用户做出选择
       TUI->>Answers: clarify.respond {request_id, answer}
       Note over Answers: _answers[rid] = answer
       Answers->>Pending: ev.set() 唤醒

       Note over Block: 阻塞解除
       Block->>Answers: _answers.pop(rid) → answer
       Block-->>Agent: 返回用户选择

超时处理
----------

如果用户在超时时间内没有响应，``ev.wait()`` 会自然返回，
``_answers.pop(rid, "")`` 返回空字符串。
Agent 的回调函数会根据空字符串做出合理的默认行为：

- **Clarify** ：返回超时消息，Agent 自行决定
- **Sudo** ：返回空密码，命令通常因权限不足而失败
- **Secret** ：返回空值，标记为 "skipped"

_pending 字典结构
-------------------

``_pending`` 字典存储所有等待中的交互请求：

.. code-block:: python

   _pending: dict[str, tuple[str, threading.Event]] = {}
   # request_id → (session_id, Event)

``_answers`` 字典存储已到达的响应：

.. code-block:: python

   _answers: dict[str, str] = {}
   # request_id → answer_text

这两个字典是线程安全的（GIL 保护下的原子操作）。

响应路由
----------

当 TUI 前端发送 ``clarify.respond`` 时：

.. code-block:: python

   def _respond(rid, params, key):
       r = params.get("request_id", "")
       entry = _pending.get(r)
       if not entry:
           return _err(rid, 4009, f"no pending {key} request")
       _, ev = entry
       _answers[r] = params.get(key, "")
       ev.set()          # 唤醒阻塞的 Agent 线程
       return _ok(rid, {"status": "ok"})

三种 respond 方法共享同一个 ``_respond()`` 辅助函数：

- ``clarify.respond`` → key = "answer"
- ``sudo.respond`` → key = "password"
- ``secret.respond`` → key = "value"

``approval.respond`` 是独立实现的——它不使用 ``_pending/_answers`` 机制，
而是调用 ``tools.approval.resolve_gateway_approval()`` 直接解析审批结果。

会话内存管理
==============

_sessions 字典结构
--------------------

Gateway 的所有会话状态存储在 ``_sessions`` 字典中：

.. code-block:: python

   _sessions: dict[str, dict] = {}
   # session_id → session dict

每个会话字典包含：

.. list-table:: 会话字典字段
   :header-rows: 1
   :widths: 25 25 50

   * - 字段
     - 类型
     - 说明
   * - agent
     - AIAgent | None
     - Agent 实例（延迟创建）
   * - agent_ready
     - threading.Event
     - Agent 初始化完成信号
   * - agent_error
     - str | None
     - Agent 初始化错误消息
   * - session_key
     - str
     - 数据库会话键（格式：YYYYMMDD_HHMMSS_XXXXXX）
   * - history
     - list[dict]
     - 对话历史（messages 数组）
   * - history_lock
     - threading.Lock
     - 历史读写互斥锁
   * - history_version
     - int
     - 乐观并发控制版本号
   * - running
     - bool
     - Agent 是否正在执行
   * - cols
     - int
     - 终端宽度（用于渲染）
   * - slash_worker
     - _SlashWorker | None
     - Slash 命令子进程
   * - attached_images
     - list[str]
     - 待附加的图片路径列表
   * - image_counter
     - int
     - 图片计数器
   * - edit_snapshots
     - dict
     - 工具调用 ID → LocalEditSnapshot
   * - tool_started_at
     - dict
     - 工具调用 ID → 开始时间戳
   * - show_reasoning
     - bool
     - 是否显示推理过程
   * - tool_progress_mode
     - str
     - 工具进度显示模式

Agent 实例生命周期
--------------------

Agent 的创建是异步的——``session.create`` 立即返回，Agent 在后台线程中构建：

.. code-block:: python

   def _build() -> None:
       try:
           agent = _make_agent(sid, key)
           _get_db().create_session(key, source="tui", model=_resolve_model())
           session["agent"] = agent
           worker = _SlashWorker(key, getattr(agent, "model", _resolve_model()))
           session["slash_worker"] = worker
           _wire_callbacks(sid)
           _emit("session.info", sid, _session_info(agent))
       except Exception as e:
           session["agent_error"] = str(e)
           _emit("error", sid, {"message": f"agent init failed: {e}"})
       finally:
           ready.set()  # 通知主线程：初始化完成（无论成功还是失败）

后续的 RPC 方法（如 ``prompt.submit``）通过 ``_sess()`` 辅助函数等待 Agent 就绪：

.. code-block:: python

   def _sess(params, rid):
       s, err = _sess_nowait(params, rid)
       return (None, err) if err else (s, _wait_agent(s, rid))

   def _wait_agent(session, rid, timeout=30.0):
       ready = session.get("agent_ready")
       if ready is not None and not ready.wait(timeout=timeout):
           return _err(rid, 5032, "agent initialization timed out")
       err = session.get("agent_error")
       return _err(rid, 5032, err) if err else None

孤儿会话清理
--------------

存在一个竞态条件：``session.close`` 可能在 Agent 构建线程完成之前被调用。
``_build()`` 的 ``finally`` 块检测这种情况：

.. code-block:: python

   finally:
       if _sessions.get(sid) is not session:
           # session.close 已经移除了这个会话
           # 我们是新构建的 worker 和 notify 注册的孤儿
           if worker is not None:
               worker.close()
           if notify_registered:
               unregister_gateway_notify(key)
           ready.set()

乐观并发控制
==============

history_version 机制
----------------------

当用户在 Agent 运行时执行 ``/undo`` 、``/compress`` 或 ``/retry`` 时，
会话历史会被外部修改。为了防止 Agent 完成后的历史写入覆盖这些修改，
Gateway 使用 ``history_version`` 实现乐观并发控制：

.. code-block:: python

   # prompt.submit 开始时
   history_version = int(session.get("history_version", 0))

   # Agent 完成后
   with session["history_lock"]:
       current_version = int(session.get("history_version", 0))
       if current_version == history_version:
           session["history"] = result["messages"]
           session["history_version"] = history_version + 1
       else:
           # 历史在外部被修改了，丢弃 Agent 的输出
           print("history_version mismatch — agent output NOT written", file=sys.stderr)

这个机制确保：

1. 正常流程：版本匹配，Agent 输出正常写入
2. 并发修改：版本不匹配，Agent 输出被丢弃（但仍然在 TUI 中显示），并附带警告

busy-state 守卫
-----------------

``running`` 标志防止并发请求：

.. code-block:: python

   with session["history_lock"]:
       if session.get("running"):
           return _err(rid, 4009, "session busy")
       session["running"] = True

   # ... Agent 执行 ...

   finally:
       session["running"] = False  # 无论成功还是失败都释放

以下方法额外检查 ``running`` 状态：

- ``session.undo`` ：运行中拒绝执行（"session busy — /interrupt first"）
- ``session.compress`` ：同上
- ``config.set("model")`` ：运行中拒绝切换模型
- ``rollback.restore`` （完整历史回滚时）：运行中拒绝执行
- ``slash.exec`` 中的 ``/model`` / ``/personality`` / ``/prompt`` / ``/compress`` ：运行中拒绝执行

SlashWorker 子进程
====================

Gateway 中许多 slash 命令需要访问完整的 CLI 环境（配置、工具定义、会话状态），
但它们在 Gateway 进程中执行可能会与 Agent 的运行冲突。

解决方案是 ``_SlashWorker``——一个持久的 ``HermesCLI`` 子进程：

.. code-block:: python

   class _SlashWorker:
       def __init__(self, session_key: str, model: str):
           argv = [sys.executable, "-m", "tui_gateway.slash_worker",
                   "--session-key", session_key]
           if model:
               argv += ["--model", model]

           self.proc = subprocess.Popen(
               argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
               text=True, bufsize=1,
           )

``slash_worker.py`` 的入口逻辑非常简洁——它创建一个 ``HermesCLI`` 实例，
然后进入 stdin 循环逐行读取 JSON 请求，调用 ``cli.process_command()`` 处理，
将输出捕获为 JSON 响应写入 stdout：

.. code-block:: python

   # slash_worker.py 核心循环
   cli = HermesCLI(model=args.model or None, compact=True, resume=args.session_key, verbose=False)

   for raw in sys.stdin:
       req = json.loads(raw.strip())
       out = _run(cli, req.get("command", ""))
       sys.stdout.write(json.dumps({"id": rid, "ok": True, "output": out}) + "\n")

通信协议
----------

SlashWorker 使用简单的 JSON Lines 协议：

**请求** （Gateway → Worker）：

.. code-block:: json

   {"id": 1, "command": "/help"}

**响应** （Worker → Gateway）：

.. code-block:: json

   {"id": 1, "ok": true, "output": "Available Commands:\n..."}

错误响应：

.. code-block:: json

   {"id": 1, "ok": false, "error": "command failed"}

序列号管理
------------

``_lock`` 保护的序列号确保请求-响应匹配：

.. code-block:: python

   with self._lock:
       self._seq += 1
       rid = self._seq
       self.proc.stdin.write(json.dumps({"id": rid, "command": command}) + "\n")
       self.proc.stdin.flush()

       while True:
           msg = self.stdout_queue.get(timeout=_SLASH_WORKER_TIMEOUT_S)
           if msg.get("id") != rid:
               continue  # 忽略旧请求的响应
           if not msg.get("ok"):
               raise RuntimeError(msg.get("error", "slash worker failed"))
           return str(msg.get("output", ""))

超时控制
----------

默认超时为 45 秒（可通过 ``HERMES_TUI_SLASH_TIMEOUT_S`` 环境变量调整）。
超时后抛出 ``RuntimeError("slash worker timed out")`` 。

Stderr 尾部追踪
-----------------

Worker 维护最近 80 行 stderr 输出：

.. code-block:: python

   def _drain_stderr(self):
       for line in (self.proc.stderr or []):
           if text := line.rstrip("\n"):
               self.stderr_tail = (self.stderr_tail + [text])[-80:]

当 Worker 异常退出时，这些尾部日志会包含在错误消息中，方便调试。

生命周期管理
--------------

- **创建** ：``session.create`` 时创建，或 ``_restart_slash_worker()`` 重建
- **重建** ：模型切换后需要重启 Worker（因为模型参数变了）
- **关闭** ：``session.close`` 时调用 ``worker.close()`` （terminate + wait）
- **atexit** ：进程退出时自动关闭所有 Worker

Agent 回调系统
================

当 Agent 执行工具调用、生成思维过程或需要用户交互时，
它通过一组 **回调函数** 通知 Gateway。

回调注册
----------

``_agent_cbs()`` 函数为每个会话创建一组回调闭包：

.. code-block:: python

   def _agent_cbs(sid: str) -> dict:
       return dict(
           tool_start_callback=lambda tc_id, name, args: _on_tool_start(sid, tc_id, name, args),
           tool_complete_callback=lambda tc_id, name, args, result: _on_tool_complete(sid, tc_id, name, args, result),
           tool_progress_callback=lambda event_type, name=None, preview=None, args=None, **kwargs: _on_tool_progress(
               sid, event_type, name, preview, args, **kwargs
           ),
           tool_gen_callback=lambda name: _emit("tool.generating", sid, {"name": name}),
           thinking_callback=lambda text: _emit("thinking.delta", sid, {"text": text}),
           reasoning_callback=lambda text: _emit("reasoning.delta", sid, {"text": text}),
           status_callback=lambda kind, text=None: _status_update(sid, str(kind), str(text) if text else None),
           clarify_callback=lambda q, c: _block("clarify.request", sid, {"question": q, "choices": c}),
       )

这些回调在 Agent 创建时注入：

.. code-block:: python

   AIAgent(
       model=_resolve_model(),
       quiet_mode=True,
       **_agent_cbs(sid),
   )

tool_start / tool_complete
----------------------------

**tool_start** ：

1. 捕获 ``LocalEditSnapshot`` （用于内联 diff）
2. 记录工具开始时间（用于持续时长计算）
3. 如果工具进度模式开启，推送 ``tool.start`` 事件

**tool_complete** ：

1. 计算 Duration（从 ``tool_started_at`` 到当前时间）
2. 生成工具摘要（如 "Did 3 searches in 2.1s"）
3. 渲染内联 diff（如果有 ``LocalEditSnapshot``）
4. 推送 ``tool.complete`` 事件，携带 duration、summary、inline_diff

tool_progress 回调
--------------------

``tool_progress_callback`` 处理多种进度事件：

- ``tool.started`` ：推送 ``tool.progress`` 事件（工具名称 + 预览）
- ``reasoning.available`` ：推送推理可用性通知
- ``subagent.*`` ：推送子 Agent 的状态更新（goal、task_count、task_index、summary、duration）

thinking / reasoning
----------------------

Agent 的思维过程通过两种回调推送：

- ``thinking_callback`` ：一般性思考文本
- ``reasoning_callback`` ：推理过程的增量文本

两者都推送为 ``thinking.delta`` / ``reasoning.delta`` 事件。
TUI 前端可以选择折叠或展开这些内容。

clarify 回调
--------------

``clarify_callback`` 通过 ``_block()`` 实现阻塞式交互：

.. code-block:: python

   clarify_callback=lambda q, c: _block("clarify.request", sid, {
       "question": q,
       "choices": c
   })

Agent 线程被阻塞，直到 TUI 前端发送 ``clarify.respond`` 。

额外的回调通过 ``_wire_callbacks()`` 注册：

- **sudo 密码** ：通过 ``_block("sudo.request", sid, {}, timeout=120)``
- **secret 捕获** ：通过 ``_block("secret.request", sid, pl)`` ，存储后返回确认

消息队列与 busy→false 转换
=============================

Agent 完成一次对话后，``running`` 标志从 ``True`` 变为 ``False`` 。
在这个转换时刻，Gateway 需要检查是否有排队的消息等待发送。

Drain 机制
------------

在 ``prompt.submit`` 的 ``finally`` 块中：

.. code-block:: python

   finally:
       with session["history_lock"]:
           session["running"] = False

当 ``running`` 变为 ``False`` 时，TUI 前端可以安全地发送下一个请求。
这个设计确保：

1. Agent 运行期间的请求被拒绝（``session busy``）
2. Agent 完成后立即可以接受新请求
3. 历史写入和 running 标志更新在同一个锁下完成，保证一致性

事件顺序保证
--------------

Gateway 的事件推送遵循以下顺序：

1. ``message.start`` — 对话开始
2. ``thinking.delta`` / ``reasoning.delta`` — 思维过程（多个）
3. ``tool.start`` → ``tool.complete`` — 工具调用（多轮）
4. ``tool.progress`` — 工具进度更新（可选）
5. ``message.delta`` — 响应文本（多个，流式）
6. ``message.complete`` — 对话完成（包含 usage、status、rendered）

TUI 前端可以依赖这个顺序来正确渲染对话界面。

内存与资源管理
================

配置缓存
----------

``_load_cfg()`` 使用文件修改时间（mtime）缓存配置：

.. code-block:: python

   def _load_cfg() -> dict:
       global _cfg_cache, _cfg_mtime
       p = _hermes_home / "config.yaml"
       mtime = p.stat().st_mtime if p.exists() else None
       with _cfg_lock:
           if _cfg_cache is not None and _cfg_mtime == mtime:
               return copy.deepcopy(_cfg_cache)
       # ... 读取文件 ...
       _cfg_cache = copy.deepcopy(data)
       _cfg_mtime = mtime
       return data

这避免了每次 RPC 调用都读取和解析 YAML 文件的性能开销。

会话关闭
----------

``session.close`` 清理所有资源：

1. 从 ``_sessions`` 字典中移除会话
2. 注销 approval 通知（``unregister_gateway_notify``）
3. 关闭 SlashWorker 子进程
4. Agent 的 ``atexit`` 钩子负责清理终端和浏览器会话

进程退出
----------

Gateway 注册了 atexit 处理器来清理所有 SlashWorker：

.. code-block:: python

   atexit.register(lambda: [
       s.get("slash_worker") and s["slash_worker"].close()
       for s in _sessions.values()
   ])

同时，线程池在进程退出时被关闭：

.. code-block:: python

   atexit.register(lambda: _pool.shutdown(wait=False, cancel_futures=True))

Platform 适配器基类
====================

Gateway 支持多种前端平台（Telegram、Discord、Slack、Signal、Matrix、微信、飞书、
钉钉、WhatsApp、Home Assistant 等 20+ 个），每个平台通过继承
``BasePlatformAdapter``（``gateway/platforms/base.py``）实现适配。

BasePlatformAdapter 接口
--------------------------

基类定义了所有平台必须实现的核心接口：

.. code-block:: python

   class BasePlatformAdapter(ABC):
       @abstractmethod
       async def connect(self) -> bool: ...
       @abstractmethod
       async def disconnect(self) -> None: ...
       @abstractmethod
       async def send(self, chat_id: str, content: str, ...) -> SendResult: ...
       @abstractmethod
       async def get_chat_info(self, chat_id: str) -> Dict[str, Any]: ...

并提供了丰富的默认实现：

- **媒体发送** ：``send_image()`` / ``send_voice()`` / ``send_video()`` / ``send_document()`` — 默认以文本降级，子类覆盖原生发送
- **消息编辑** ：``edit_message()`` — 用于流式更新，支持 ``finalize`` 标志
- **消息分块** ：``truncate_message()`` — 自动按平台长度限制分块，保持代码块完整性
- **媒体提取** ：``extract_images()`` / ``extract_media()`` / ``extract_local_files()`` — 从响应文本中提取多媒体附件
- **重试机制** ：``_send_with_retry()`` — 指数退避重试 + 纯文本降级
- **Typing 指示器** ：``_keep_typing()`` — 持续刷新 typing 状态，支持暂停（审批等待时）
- **图片缓存** ：``cache_image_from_url()`` / ``cache_image_from_bytes()`` — SSRF 安全的图片下载与本地缓存
- **音频缓存** ：``cache_audio_from_url()`` / ``cache_audio_from_bytes()`` — 语音消息的本地缓存
- **文档缓存** ：``cache_document_from_url()`` — 支持 PDF/DOCX/XLSX 等格式
- **代理支持** ：``resolve_proxy_url()`` — 自动检测 HTTPS_PROXY/HTTP_PROXY 及 macOS 系统代理

消息处理流水线
-----------------

``handle_message()`` 是平台适配器的核心方法，它实现了完整的异步消息处理生命周期：

.. mermaid::
   :name: platform-handle-message
   :caption: 平台适配器消息处理流水线

   sequenceDiagram
       autonumber
       participant P as 平台适配器
       participant HM as handle_message()
       participant PM as _process_message_background()
       participant Agent as AIAgent

       P->>HM: MessageEvent
       HM->>HM: 检查 _active_sessions

       alt 已有活跃会话
           alt 紧急命令 (/approve, /stop)
               HM->>PM: 直接调度
           else 图片突发
               HM->>HM: 合并到 _pending_messages
           else 普通消息
               HM->>HM: 触发 interrupt
               HM->>HM: 排入 _pending_messages
           end
       else 无活跃会话
           HM->>HM: 设置 _active_sessions guard
           HM->>PM: 创建后台 asyncio.Task
       end

       PM->>PM: 启动 _keep_typing
       PM->>Agent: _message_handler(event)
       Agent-->>PM: response text
       PM->>PM: extract_media / extract_images
       PM->>P: _send_with_retry (text + media)
       PM->>PM: 检查 _pending_messages
       PM->>PM: 清理 _active_sessions

平台注册与生命周期
--------------------

所有平台适配器位于 ``gateway/platforms/`` 目录中。当前支持的平台：

- ``telegram.py`` — Telegram DM / Group / Topic
- ``discord.py`` — Discord（线程式对话）
- ``slack.py`` — Slack（Assistant API + thread replies）
- ``signal.py`` — Signal
- ``matrix.py`` — Matrix
- ``whatsapp.py`` — WhatsApp
- ``weixin.py`` — 微信/元宝
- ``wecom.py`` — 企业微信
- ``feishu.py`` — 飞书
- ``dingtalk.py`` — 钉钉
- ``homeassistant.py`` — Home Assistant
- ``email.py`` — Email
- ``sms.py`` — SMS
- ``webhook.py`` — 通用 Webhook
- ``bluebubbles.py`` — BlueBubbles (iMessage)
- ``mattermost.py`` — Mattermost
- ``qqbot/`` — QQ Bot
- ``api_server.py`` — HTTP/SSE API Server（Open WebUI 兼容）

Stream Consumer：Agent 输出流处理
===================================

``gateway/stream_consumer.py`` 负责处理 Agent 的输出流——将 Agent 产生的
原始 token 流转换为结构化的事件，推送给前端平台。

.. mermaid::
   :name: stream-consumer-pipeline
   :caption: Stream Consumer 处理流水线

   flowchart LR
       AGENT["AIAgent<br/>输出流"] --> SC["GatewayStreamConsumer"]
       SC --> PARSE["Token 解析"]
       PARSE --> BATCH["批次聚合"]
       BATCH --> DISPATCH["平台分发"]

       DISPATCH --> TUI["TUI 前端"]
       DISPATCH --> API["API Server<br/>(SSE)"]
       DISPATCH --> TG["Telegram"]
       DISPATCH --> DISC["Discord"]
       DISPATCH --> SLACK["Slack"]

核心设计
---------

``GatewayStreamConsumer`` 使用 **edit transport** 模式：
先发送一条初始消息，然后通过 ``editMessageText`` 持续更新内容。
这在 Telegram、Discord、Slack 等平台上是普遍支持的。

Stream Consumer 的核心配置：

.. code-block:: python

   @dataclass
   class StreamConsumerConfig:
       edit_interval: float = 1.0    # 编辑间隔（秒）
       buffer_threshold: int = 40    # 缓冲区触发阈值（字符数）
       cursor: str = " ▉"            # 流式光标字符
       buffer_only: bool = False     # 仅缓冲模式

核心职责
---------

Stream Consumer 承担以下核心职责：

1. **Token 流消费** ：从 Agent 的输出迭代器中逐个读取 token
2. **事件分类** ：区分文本 token、工具调用、思维过程、错误等不同类型
3. **批次聚合** ：将小 token 合并为适合网络传输的批次
4. **平台分发** ：将处理后的事件推送到目标平台适配器
5. **分段处理** ：工具调用边界触发新消息段（``_NEW_SEGMENT``），确保后续文本出现在工具进度消息下方

Stream Consumer 的设计将 Agent 的输出逻辑与平台的推送逻辑解耦——Agent 只需产生 token 流，
Stream Consumer 负责将其适配到不同平台的推送协议。

API Server：HTTP/SSE 接口
===========================

API Server（``gateway/platforms/api_server.py``）是 Gateway 的 HTTP/SSE 接口层，
为 Open WebUI 等第三方前端提供 Agent 访问能力。

X-Hermes-Session-Key：长期记忆作用域
--------------------------------------

``X-Hermes-Session-Key`` 是一个自定义 HTTP 请求头，允许外部客户端指定一个 **长期会话键**
来控制 Agent 的记忆范围：

.. code-block:: http

   POST /v1/chat/completions HTTP/1.1
   X-Hermes-Session-Key: user_20240101_primary
   Content-Type: application/json

其工作原理：

1. API Server 检查请求头中的 ``X-Hermes-Session-Key`` 值
2. 如果存在，使用该键查找或创建对应的持久化会话
3. Agent 加载该会话的历史记录，实现跨请求的长期记忆
4. 如果不存在，API Server 生成临时会话键（行为与之前一致）

这个特性使得 Open WebUI 等前端可以为每个用户维护独立的长期对话上下文，
而不仅仅是单次请求-响应的无状态交互。

SSE 流式输出
--------------

针对 Open WebUI 的 SSE（Server-Sent Events）流式输出进行了优化：

- **Token 批处理** ：将连续的小 token 合并为较大的批次再发送，减少 SSE 事件数量和网络开销
- **错误处理** ：在 SSE 流中增加结构化的错误事件，使前端能优雅地处理 Agent 异常

.. code-block::

   data: {"error": {"message": "Agent timeout", "type": "agent_error"}}

   data: [DONE]

源码文件索引
==============

本章涉及的主要源文件：

- ``tui_gateway/entry.py`` — Gateway 入口点，stdin 读取循环，信号处理，初始化握手
- ``tui_gateway/server.py`` — 56 个 RPC 方法定义（3086 行），会话管理，阻塞提示，SlashWorker，回调系统
- ``tui_gateway/render.py`` — 流式渲染器，消息渲染，diff 渲染
- ``tui_gateway/slash_worker.py`` — SlashWorker 子进程入口（77 行）
- ``gateway/platforms/base.py`` — 平台适配器基类（2343 行），消息处理流水线，媒体缓存，重试机制
- ``gateway/stream_consumer.py`` — Agent 输出流消费者，edit transport，token 批处理与平台分发
- ``gateway/platforms/api_server.py`` — HTTP/SSE API Server，X-Hermes-Session-Key 支持
- ``gateway/platforms/telegram.py`` — Telegram 平台适配器
- ``gateway/platforms/discord.py`` — Discord 平台适配器
- ``gateway/platforms/slack.py`` — Slack 平台适配器
- ``gateway/config.py`` — Gateway 配置管理，Platform/PlatformConfig 数据类
- ``gateway/session.py`` — 会话键构建，SessionSource 数据类
- ``gateway/status.py`` — 运行时状态写入，作用域锁管理
