.. _chapter-mcp-integration:

###############################################
MCP 集成：Model Context Protocol 的生产级实现
###############################################

.. contents::
   :depth: 3
   :local:

*****************
1. MCP 协议概述
*****************

Model Context Protocol（MCP）是由 Anthropic 提出的一种开放协议，旨在标准化大语言模型（LLM）与外部工具和数据源之间的交互方式。在传统的 Agent 架构中，每增加一个外部工具就需要硬编码集成逻辑，这不仅维护成本高昂，而且使得 Agent 的能力受到代码库的束缚。MCP 的核心思想是将"工具提供"与"工具消费"彻底解耦——任何实现了 MCP 协议的服务器都可以向支持 MCP 的客户端暴露工具、资源和提示，而客户端不需要了解服务器的内部实现。

在 Hermes Agent 中，MCP 集成是扩展 Agent 能力的首要机制。通过 ``config.yaml`` 中的 ``mcp_servers`` 配置段，用户可以声明式地接入任意数量的 MCP 服务器，Agent 会在启动时自动发现这些服务器暴露的工具，并将其注册到内部工具注册表中，使得 LLM 可以像调用内置工具一样调用 MCP 工具。

MCP 协议的核心能力包括：

- **工具调用（Tools）** ：服务器暴露可被 LLM 调用的函数，客户端通过 ``tools/call`` 发送参数并获取结果。

- **资源读取（Resources）** ：服务器暴露可被客户端读取的数据资源，通过 URI 寻址。

- **提示管理（Prompts）** ：服务器提供预定义的提示模板，支持参数化。

- **采样（Sampling）** ：服务器可以反向请求 LLM 完成文本生成，实现更复杂的交互模式。

Hermes Agent 的 MCP 集成实现了上述所有能力，并在连接管理、认证、安全防护和容错机制方面做了大量生产级强化。

.. mermaid::

   graph TB
       subgraph "MCP 生态系统"
           LLM["LLM (Claude / GPT / ...)"]
           AGENT["Hermes Agent<br/>(MCP Client)"]
           PROXY["MCP 工具注册表<br/>(Registry)"]

           subgraph "MCP Servers"
               FS["Filesystem<br/>Server"]
               GH["GitHub<br/>Server"]
               API["Remote API<br/>Server"]
               DB["Database<br/>Server"]
           end
       end

       LLM -->|"tool_call"| AGENT
       AGENT -->|"dispatch"| PROXY
       PROXY -->|"mcp_filesystem_read"| FS
       PROXY -->|"mcp_github_prs"| GH
       PROXY -->|"mcp_api_query"| API
       PROXY -->|"mcp_db_sql"| DB
       FS -->|"result"| PROXY
       GH -->|"result"| PROXY
       API -->|"result"| PROXY
       DB -->|"result"| PROXY
       PROXY -->|"tool_result"| AGENT
       AGENT -->|"response"| LLM

       style AGENT fill:#dbeafe,stroke:#60a5fa,color:#1e3a8a
       style PROXY fill:#e0f2fe,stroke:#38bdf8,color:#0f4c75
       style LLM fill:#ede9fe,stroke:#a78bfa,color:#5b21b6

***************
2. 传输层架构
***************

MCP 协议定义了两种传输方式，Hermes Agent 均予以支持。选择哪种传输方式取决于 MCP 服务器的部署形态。

Stdio 传输
============

Stdio 传输适用于与 Agent 运行在同一台机器上的 MCP 服务器。配置格式包含 ``command`` 、``args`` 和 ``env`` 三个字段：

.. code-block:: yaml

   mcp_servers:
     filesystem:
       command: "npx"
       args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
       env:
         PATH: "/usr/local/bin:/usr/bin"
       timeout: 120
       connect_timeout: 60

当使用 Stdio 传输时，Hermes Agent 会通过 MCP SDK 的 ``stdio_client()`` 启动一个子进程，通过标准输入/输出与服务器通信。子进程的环境变量经过严格过滤——仅保留 ``PATH`` 、``HOME`` 、``USER`` 、``LANG`` 、``LC_ALL`` 、``TERM`` 、``SHELL`` 、``TMPDIR`` 等安全变量以及所有 ``XDG_*`` 变量，加上用户在 ``env`` 字段中显式指定的变量。这一机制防止了 API 密钥、Token 等敏感信息意外泄露给 MCP 子进程。

HTTP/StreamableHTTP 传输
==========================

HTTP 传输适用于远程部署的 MCP 服务器。配置格式包含 ``url`` 和 ``headers`` 字段：

.. code-block:: yaml

   mcp_servers:
     remote_api:
       url: "https://my-mcp-server.example.com/mcp"
       headers:
         Authorization: "Bearer sk-..."
       timeout: 180
       connect_timeout: 60

HTTP 传输使用 MCP SDK 的 ``streamable_http_client()`` （新版 API）或 ``streamablehttp_client()`` （旧版兼容）建立连接。Hermes Agent 会自动检测 SDK 版本并选择合适的 API。对于需要认证的服务器，支持静态 Bearer Token（通过 ``headers`` 字段）和 OAuth 2.1 PKCE 动态认证（通过 ``auth: oauth`` 字段）。

如果配置中同时包含 ``url`` 和 ``command`` ，HTTP 传输优先，Agent 会输出一条警告日志。

.. mermaid::

   graph LR
       subgraph "传输方式选择"
           CONFIG["config.yaml"]
           CONFIG -->|"有 command?"| STDIO["Stdio 传输"]
           CONFIG -->|"有 url?"| HTTP["HTTP 传输"]
       end

       subgraph "Stdio 传输流程"
           CMD["command + args"] --> ENV["env 过滤"]
           ENV --> SPAWN["spawn 子进程"]
           SPAWN --> PIPE["stdin/stdout 管道"]
       end

       subgraph "HTTP 传输流程"
           URL["url + headers"] --> AUTH{"需要认证?"}
           AUTH -->|"Bearer Token"| HTTPX["httpx.AsyncClient"]
           AUTH -->|"OAuth 2.1"| OAUTH["MCPOAuthManager"]
           AUTH -->|"无"| HTTPX
           OAUTH --> HTTPX
           HTTPX --> STREAM["StreamableHTTP"]
       end

       STDIO --> SESSION["ClientSession"]
       STREAM --> SESSION
       SESSION --> TOOLS["list_tools()"]

       style CONFIG fill:#fef3c7,stroke:#f59e0b,color:#92400e
       style SESSION fill:#dcfce7,stroke:#34d399,color:#166534

******************
3. 连接生命周期
******************

Hermes Agent 中的每个 MCP 服务器由一个 ``MCPServerTask`` 实例管理。该类封装了从连接、发现、服务到断开的完整生命周期，运行在专用的后台事件循环上。

MCPServerTask 的核心状态
==========================

每个 ``MCPServerTask`` 维护以下关键状态：

- ``session`` ：当前的 MCP ``ClientSession`` 实例，用于与服务器通信。

- ``_ready`` ：一个 ``asyncio.Event`` ，连接成功并完成工具发现后设置，工具处理函数通过检查此事件判断服务器是否就绪。

- ``_shutdown_event`` ：关闭信号，设置后运行循环退出。

- ``_reconnect_event`` ：重连信号，用于 OAuth 令牌刷新等场景。

- ``_tools`` ：从服务器发现的工具列表。

- ``_registered_tool_names`` ：已注册到 Hermes 工具注册表的工具名称列表。

- ``_sampling`` ：采样处理器实例（如果启用）。

连接流程
==========

连接过程由 ``run()`` 方法驱动，其核心逻辑如下：

#. **配置解析** ：读取传输类型、超时设置、认证类型和采样配置。

#. **传输建立** ：根据配置调用 ``_run_stdio()`` 或 ``_run_http()`` 。两种方法都会在 ``async with`` 上下文中建立 MCP 会话。

#. **工具发现** ：调用 ``_discover_tools()`` ，内部执行 ``session.list_tools()`` 获取服务器暴露的工具列表。

#. **就绪信号** ：设置 ``_ready`` 事件，通知等待者连接已完成。

#. **等待阶段** ：调用 ``_wait_for_lifecycle_event()`` ，阻塞直到收到关闭或重连信号。

重连与指数退避
================

如果连接意外中断（非用户主动关闭），``run()`` 方法会自动重连，采用指数退避策略：

- 初始退避时间 1 秒，每次翻倍，最大 60 秒。

- 首次连接最多重试 3 次（``_MAX_INITIAL_CONNECT_RETRIES``）。

- 运行期间最多重试 5 次（``_MAX_RECONNECT_RETRIES``）。

- 在退避等待期间检查 ``_shutdown_event`` ，如果用户请求关闭则立即退出。

- OAuth 重连不计入重试计数——这是一种恢复行为而非失败。

.. mermaid::

   stateDiagram-v2
       [*] --> Initializing: start(config)

       Initializing --> Connecting: 解析传输类型
       Connecting --> StdioTransport: command 模式
       Connecting --> HTTPTransport: url 模式

       StdioTransport --> Discovering: spawn 子进程 + initialize()
       HTTPTransport --> Discovering: 建立 HTTP 连接 + initialize()

       Discovering --> Ready: list_tools() 成功
       Discovering --> Failed: 连接/发现失败

       Failed --> Connecting: 重试 (退避)
       Failed --> [*]: 超过最大重试次数

       Ready --> Serving: _wait_for_lifecycle_event()
       Serving --> Reconnecting: _reconnect_event (OAuth 刷新)
       Serving --> ShuttingDown: _shutdown_event
       Serving --> Connecting: 连接断开 (意外)

       Reconnecting --> Discovering: 重新建立连接
       ShuttingDown --> [*]: 清理资源

       note right of Ready: _ready.set()
       note right of Serving: 工具可调用
       note right of Reconnecting: 不计入重试计数

******************
4. 工具注册格式
******************

MCP 服务器暴露的工具在注册到 Hermes Agent 的工具注册表时，会经过严格的命名转换和格式规范化。

命名规范
==========

MCP 工具的注册名遵循 ``mcp_{server}_{tool}`` 的格式：

- ``server`` 部分来自配置中的服务器名称，经过 ``sanitize_mcp_name_component()`` 处理——将所有非 ``[A-Za-z0-9_]`` 字符替换为下划线。

- ``tool`` 部分来自 MCP 服务器 ``list_tools()`` 返回的工具原始名称，同样经过清洗。

例如，一个名为 ``github`` 的 MCP 服务器暴露的 ``list_prs`` 工具，注册名为 ``mcp_github_list_prs`` 。

工具集（Toolset）
===================

所有来自同一 MCP 服务器的工具归入名为 ``mcp-{server_name}`` 的工具集。工具集用于在 ``hermes tools`` TUI 中按组显示和切换工具。注册时还会创建一个别名映射 ``server_name -> mcp-{server_name}`` ，方便通过原始服务器名查找。

Schema 转换
=============

MCP 工具的 ``inputSchema`` 通过 ``_normalize_mcp_input_schema()`` 函数规范化。如果 Schema 的 ``type`` 为 ``object`` 但缺少 ``properties`` 字段，会自动添加空的 ``properties: {}`` 。这确保了与 OpenAI Function Calling 格式的兼容性。

.. code-block:: python

   # 原始 MCP Schema
   {"type": "object"}  # 缺少 properties

   # 规范化后
   {"type": "object", "properties": {}}

  # 完整的注册示例
   {
       "name": "mcp_github_list_prs",
       "description": "List pull requests from a repository",
       "parameters": {
           "type": "object",
           "properties": {
               "repo": {"type": "string", "description": "Repository name"},
               "state": {"type": "string", "enum": ["open", "closed", "all"]}
           },
           "required": ["repo"]
       }
   }

工具过滤
==========

配置中支持 ``tools.include`` 和 ``tools.exclude`` 过滤器：

.. code-block:: yaml

   mcp_servers:
     github:
       command: "npx"
       args: ["-y", "@modelcontextprotocol/server-github"]
       tools:
         include: ["list_prs", "get_file"]    # 白名单：仅注册这些工具
         # exclude: ["delete_repo"]           # 黑名单：注册除这些之外的所有工具

当 ``include`` 和 ``exclude`` 同时存在时，``include`` 优先。

.. mermaid::

   sequenceDiagram
       participant SDK as MCP SDK
       participant Task as MCPServerTask
       participant Reg as 工具注册表

       Task->>SDK: list_tools()
       SDK-->>Task: [Tool(name="read"), Tool(name="write")]

       Note over Task: 过滤检查 (include/exclude)

       Task->>Task: _convert_mcp_schema("fs", Tool("read"))
       Note over Task: mcp_fs_read

       Task->>Task: _scan_mcp_description()
       Note over Task: 安全扫描工具描述

       Task->>Reg: registry.register(<br/>  name="mcp_fs_read",<br/>  toolset="mcp-fs",<br/>  handler=_make_tool_handler(),<br/>  check_fn=_make_check_fn())

       Task->>Task: _convert_mcp_schema("fs", Tool("write"))
       Task->>Reg: registry.register("mcp_fs_write", ...)

       Task->>Reg: registry.register_toolset_alias("fs", "mcp-fs")

       Note over Reg: 注册完成：2 个工具

*************************
5. OAuth 2.1 PKCE 认证
*************************

对于需要用户认证的远程 MCP 服务器，Hermes Agent 实现了完整的 OAuth 2.1 Authorization Code Flow with PKCE（Proof Key for Code Exchange）。这一实现覆盖了从浏览器授权到令牌持久化的全流程，并解决了跨进程令牌同步和 401 风暴等生产级问题。

配置方式
==========

.. code-block:: yaml

   mcp_servers:
     my_server:
       url: "https://mcp.example.com/mcp"
       auth: oauth
       oauth:                              # 所有字段均为可选
         client_id: "pre-registered-id"    # 跳过动态注册
         client_secret: "secret"           # 机密客户端
         scope: "read write"               # 默认：服务器提供
         redirect_port: 0                  # 0 = 自动选择空闲端口
         client_name: "My Custom Client"   # 默认："Hermes Agent"

HermesTokenStorage
====================

``HermesTokenStorage`` 类负责将 OAuth 令牌和客户端注册信息持久化到磁盘：

- 令牌文件：``~/.hermes/mcp-tokens/<server_name>.json``
- 客户端信息：``~/.hermes/mcp-tokens/<server_name>.client.json``

文件权限设置为 ``0o600`` （仅所有者可读写），并通过原子写入（先写临时文件再 ``rename``）防止损坏。

跨进程令牌重载
================

当多个 Hermes 实例（如 CLI 和定时任务）共享同一组 OAuth 令牌时，一个进程刷新令牌后，另一个进程需要感知到变化。``MCPOAuthManager.invalidate_if_disk_changed()`` 通过比较令牌文件的 ``st_mtime_ns`` 实现这一点：

#. 每次 OAuth 认证流开始前，检查令牌文件的 ``mtime`` 。

#. 如果与上次记录的 ``mtime`` 不同，将 MCP SDK 的 ``OAuthClientProvider._initialized`` 标志重置为 ``False`` 。

#. SDK 在下次认证流中会从存储重新加载令牌。

这一机制参考了 Claude Code 的 ``invalidateOAuthCacheIfDiskChanged`` 实现。

401 去重（Thundering Herd 保护）
==================================

当 N 个并发的工具调用同时遇到 401 错误时，如果每个都独立触发令牌刷新，会造成"惊群"问题。``MCPOAuthManager.handle_401()`` 通过 ``pending_401`` 字典实现去重：

- 以失败的 ``access_token`` 为键创建 ``asyncio.Future`` 。

- 第一个到达的调用启动恢复流程，后续调用等待同一个 Future。

- 恢复流程首先检查磁盘令牌是否已更新，然后检查 SDK 是否能就地刷新。

.. mermaid::

   sequenceDiagram
       participant User as 用户浏览器
       participant CLI as Hermes CLI
       participant Mgr as MCPOAuthManager
       participant Storage as HermesTokenStorage
       participant Server as MCP 服务器
       participant Auth as OAuth 授权服务器

       CLI->>Mgr: get_or_build_provider("my_server", ...)
       Mgr->>Storage: has_cached_tokens()
       Storage-->>Mgr: false (首次)

       Mgr->>Storage: 构建客户端元数据
       Note over Mgr: redirect_uri = http://127.0.0.1:{port}/callback

       CLI->>Server: 发起 MCP 连接
       Server-->>CLI: 401 Unauthorized

       CLI->>Auth: 发现授权端点 (/.well-known/oauth-authorization-server)
       Auth-->>CLI: authorization_endpoint, token_endpoint

       CLI->>Auth: 动态客户端注册 (optional)
       Auth-->>CLI: client_id, client_secret

       Note over CLI: 生成 PKCE code_verifier + code_challenge

       CLI->>User: 打开浏览器：<br/>authorization_endpoint?<br/>  response_type=code&<br/>  client_id=...&<br/>  redirect_uri=...&<br/>  code_challenge=...&<br/>  code_challenge_method=S256

       User->>Auth: 用户登录并授权
       Auth-->>User: 重定向到 callback URL

       User->>CLI: http://127.0.0.1:{port}/callback?code=xxx&state=yyy

       CLI->>Auth: POST token_endpoint<br/>  grant_type=authorization_code&<br/>  code=xxx&<br/>  code_verifier=...&<br/>  redirect_uri=...

       Auth-->>CLI: { access_token, refresh_token, expires_in }

       CLI->>Storage: set_tokens(OAuthToken)
       CLI->>Server: 重试 MCP 连接 (Bearer access_token)
       Server-->>CLI: 连接成功

       Note over Mgr: 后续：磁盘 mtime 检测<br/>跨进程令牌刷新

*******************
6. 动态工具发现
*******************

MCP 协议支持服务器在运行时通知客户端工具列表发生变化（``notifications/tools/list_changed``）。Hermes Agent 通过 ``MCPServerTask._make_message_handler()`` 和 ``_refresh_tools()`` 实现了动态工具发现。

消息处理器
============

在创建 ``ClientSession`` 时，如果 MCP SDK 支持 ``message_handler`` 参数（通过 ``inspect.signature`` 运行时检测），Hermes 会注册一个消息处理器。该处理器匹配以下通知类型：

- ``ToolListChangedNotification`` ：触发工具刷新。

- ``PromptListChangedNotification`` ：记录日志（未实现刷新）。

- ``ResourceListChangedNotification`` ：记录日志（未实现刷新）。

刷新机制
==========

``_refresh_tools()`` 方法使用 ``asyncio.Lock`` 防止并发的快速通知触发多次重叠刷新。刷新流程如下：

#. 获取锁（``async with self._refresh_lock``）。

#. 记录旧的工具名称集合。

#. 从服务器重新获取工具列表（``await session.list_tools()``）。

#. 注销旧工具（``registry.deregister()``）。

#. 用新的工具列表重新注册。

#. 比较新旧工具名称，记录增加和删除的工具。

刷新完成后会输出一条 WARNING 级别的日志，列出具体的变更内容，帮助用户确认变更是否预期。

.. code-block:: python

   # _refresh_tools() 核心逻辑
   async def _refresh_tools(self):
       async with self._refresh_lock:
           old_tool_names = set(self._registered_tool_names)
           tools_result = await self.session.list_tools()
           new_mcp_tools = tools_result.tools

           # 注销旧工具
           for prefixed_name in self._registered_tool_names:
               registry.deregister(prefixed_name)

           # 重新注册
           self._tools = new_mcp_tools
           self._registered_tool_names = _register_server_tools(
               self.name, self, self._config
           )

           # 计算差异
           new_tool_names = set(self._registered_tool_names)
           added = new_tool_names - old_tool_names
           removed = old_tool_names - new_tool_names

***************
7. 熔断器模式
***************

在分布式系统中，远程服务不可用是常态。如果 MCP 服务器持续失败而 Agent 不断重试，会造成"90 次迭代空转"问题（Issue #10447）。为此，Hermes Agent 为每个 MCP 服务器实现了熔断器模式。

工作原理
==========

每个服务器维护一个连续错误计数器（``_server_error_counts``）。每次工具调用失败时计数器加一，成功时重置为零。当连续错误次数达到阈值（默认 3 次），后续的调用会在处理器层面直接短路，返回一条清晰的错误消息，告知 LLM 不要重试该工具。

.. code-block:: python

   _CIRCUIT_BREAKER_THRESHOLD = 3

   def _handler(args: dict, **kwargs) -> str:
       # 熔断器检查
       if _server_error_counts.get(server_name, 0) >= _CIRCUIT_BREAKER_THRESHOLD:
           return json.dumps({
               "error": (
                   f"MCP server '{server_name}' is unreachable after "
                   f"{_CIRCUIT_BREAKER_THRESHOLD} consecutive failures. "
                   f"Do NOT retry this tool — use alternative approaches "
                   f"or ask the user to check the MCP server."
               )
           })

       # 正常调用流程...

当错误消息中明确包含"不要重试"的指令时，LLM 通常会停止调用该工具并转而使用替代方案或向用户求助。这一简单的策略有效避免了无意义的重试循环。

.. mermaid::

   flowchart TD
       CALL["工具调用请求"] --> CHECK{"连续错误 >= 3?"}

       CHECK -->|"是"| SHORT["熔断：返回<br/>'服务器不可达，请勿重试'"]
       CHECK -->|"否"| EXEC["执行 MCP 工具调用"]

       EXEC --> RESULT{"调用结果?"}

       RESULT -->|"成功"| RESET["重置计数器 = 0"]
       RESET --> RET["返回结果"]

       RESULT -->|"失败"| AUTH{"认证错误?"}

       AUTH -->|"是"| RECOVER["尝试 OAuth 恢复"]
       RECOVER --> RETRY{"恢复成功?"}
       RETRY -->|"是"| RET
       RETRY -->|"否"| INCR

       AUTH -->|"否"| INCR["计数器 += 1"]
       INCR --> ERR["返回错误消息"]

       RESULT -->|"错误"| AUTH

       style SHORT fill:#fee2e2,stroke:#f87171,color:#991b1b
       style RESET fill:#dcfce7,stroke:#34d399,color:#166534
       style INCR fill:#fef3c7,stroke:#f59e0b,color:#92400e

******************
8. Sampling 支持
******************

MCP 协议的 Sampling 特性允许服务器反向请求 LLM 生成文本，实现更复杂的交互模式（如 Agent-in-Agent）。Hermes Agent 通过 ``SamplingHandler`` 类实现了这一特性。

配置
======

.. code-block:: yaml

   mcp_servers:
     analysis:
       command: "npx"
       args: ["-y", "analysis-server"]
       sampling:
         enabled: true              # 默认 true
         model: "gemini-3-flash"    # 覆盖模型（可选）
         max_tokens_cap: 4096       # 每次请求最大 token 数
         timeout: 30                # LLM 调用超时（秒）
         max_rpm: 10                # 每分钟最大请求数
         allowed_models: []         # 模型白名单（空 = 全部允许）
         max_tool_rounds: 5         # 工具循环限制（0 = 禁用）
         log_level: "info"          # 审计日志级别

速率限制
==========

``SamplingHandler`` 使用滑动窗口算法实现速率限制。默认每分钟最多 10 次请求（``max_rpm``）。超出限制时返回 ``ErrorData`` 而非调用 LLM。

.. code-block:: python

   def _check_rate_limit(self) -> bool:
       now = time.time()
       window = now - 60  # 60 秒窗口
       self._rate_timestamps[:] = [t for t in self._rate_timestamps if t > window]
       if len(self._rate_timestamps) >= self.max_rpm:
           return False
       self._rate_timestamps.append(now)
       return True

工具循环治理
==============

当 LLM 响应包含 ``tool_calls`` 时，``SamplingHandler`` 会跟踪工具循环次数。每次返回 ``tool_use`` 类型的结果时计数器加一，返回文本结果时重置。当计数器超过 ``max_tool_rounds`` （默认 5）时，返回错误并终止循环。这防止了服务器通过反复请求工具调用导致无限循环。

消息转换
==========

``_convert_messages()`` 方法将 MCP 的 ``SamplingMessage`` 格式转换为 OpenAI 兼容的对话格式：

- 文本内容（``TextContent``）转为 ``{"role": "user/assistant", "content": "..."}`` 格式。

- 图像内容（``ImageContent``）转为 ``{"type": "image_url", "image_url": {"url": "data:..."}}`` 格式。

- 工具调用（``ToolUseContent``）转为 ``{"tool_calls": [...]}`` 格式。

- 工具结果（``ToolResultContent``）转为 ``{"role": "tool", "tool_call_id": "...", "content": "..."}`` 格式。

LLM 调用通过 ``agent.auxiliary_client.call_llm()`` 完成，并使用 ``asyncio.to_thread()`` 将同步调用卸载到线程池，避免阻塞 MCP 事件循环。

.. mermaid::

   sequenceDiagram
       participant MCP as MCP 服务器
       participant SDK as MCP SDK
       participant Handler as SamplingHandler
       participant LLM as LLM Provider

       MCP->>SDK: sampling/createMessage(params)
       SDK->>Handler: __call__(context, params)

       Handler->>Handler: _check_rate_limit()
       Handler->>Handler: _resolve_model(preferences)

       Handler->>Handler: _convert_messages(params)

       Handler->>Handler: 检查 allowed_models

       Handler->>LLM: call_llm(messages, tools, max_tokens)
       LLM-->>Handler: response

       alt 文本响应
           Handler->>Handler: _build_text_result()
           Handler-->>SDK: CreateMessageResult
       else 工具调用响应
           Handler->>Handler: _build_tool_use_result()
           Note over Handler: 检查 max_tool_rounds
           Handler-->>SDK: CreateMessageResultWithTools
       end

       SDK-->>MCP: 返回结果

*************
9. 安全机制
*************

MCP 集成涉及执行外部代码和加载外部数据，安全是首要关注点。Hermes Agent 实现了多层安全防御。

环境变量过滤
==============

Stdio 传输的子进程环境变量经过严格过滤。``_build_safe_env()`` 函数仅保留以下变量：

- 核心变量：``PATH`` 、``HOME`` 、``USER`` 、``LANG`` 、``LC_ALL`` 、``TERM`` 、``SHELL`` 、``TMPDIR``

- 所有 ``XDG_*`` 变量

- 用户在配置中显式指定的变量

这防止了诸如 ``OPENAI_API_KEY`` 、``AWS_SECRET_ACCESS_KEY`` 等敏感信息泄露给 MCP 子进程。

工具描述注入扫描
==================

MCP 服务器暴露的工具描述可能包含恶意指令，试图操纵 LLM 的行为。``_scan_mcp_description()`` 函数使用 10 个正则表达式模式检测以下威胁：

#. 提示覆盖尝试（"ignore previous instructions"）

#. 身份覆盖（"you are now a..."）

#. 任务覆盖（"your new task is..."）

#. 系统提示注入（"system:"）

#. 角色标签注入（``<system>`` 、``<human>`` 、``<assistant>``）

#. 隐匿指令（"do not tell/inform/mention"）

#. 网络命令（"curl/wget/fetch http://"）

#. Base64 解码引用（"base64.b64decode"）

#. 代码执行引用（"exec()"/"eval()"）

#. 危险导入引用（"import subprocess/os/shutil/socket"）

检测结果仅记录 WARNING 日志，不阻止工具注册（避免误报导致合法服务器不可用）。

工具名称清洗
==============

``sanitize_mcp_name_component()`` 将所有非 ``[A-Za-z0-9_]`` 字符替换为下划线，防止注入恶意工具名称。

凭据脱敏
==========

``_sanitize_error()`` 函数在错误消息返回给 LLM 之前，使用正则表达式移除以下类型的凭据：

- GitHub PAT（``ghp_...``）

- OpenAI 风格密钥（``sk-...``）

- Bearer Token（``Bearer ...``）

- URL 中的 ``token=`` 、``key=`` 、``password=`` 、``secret=`` 参数

所有匹配项替换为 ``[REDACTED]`` 。

OSV 恶意软件检查
==================

在启动 Stdio MCP 服务器之前，Hermes 会调用 ``tools.osv_check.check_package_for_malware()`` 检查命令和参数是否匹配已知的恶意软件包。如果检测到威胁，连接会被阻止。

.. code-block:: python

   # _run_stdio() 中的 OSV 检查
   from tools.osv_check import check_package_for_malware
   malware_error = check_package_for_malware(command, args)
   if malware_error:
       raise ValueError(f"MCP server '{self.name}': {malware_error}")

*****************************
10. 与内置工具的冲突保护
*****************************

MCP 工具的注册名可能与 Hermes Agent 的内置工具发生冲突（例如，一个 MCP 服务器暴露了名为 ``read_file`` 的工具，而 Hermes 自身已有此工具）。为防止 MCP 工具意外覆盖内置功能，注册时会进行冲突检测。

.. code-block:: python

   # _register_server_tools() 中的冲突检测
   existing_toolset = registry.get_toolset_for_tool(tool_name_prefixed)
   if existing_toolset and not existing_toolset.startswith("mcp-"):
       logger.warning(
           "MCP server '%s': tool '%s' (-> '%s') collides with "
           "built-in tool in toolset '%s' — skipping to preserve built-in",
           name, mcp_tool.name, tool_name_prefixed, existing_toolset,
       )
       continue

此检查对普通工具和资源/提示工具都适用。只有 ``mcp-`` 前缀的工具集内的工具可以被覆盖（即同一 MCP 服务器的重连场景），任何试图覆盖非 MCP 工具集内工具的行为都会被拒绝。

线程安全架构
==============

整个 MCP 子系统运行在一个专用的后台事件循环（``_mcp_loop``）上，该循环在守护线程 ``mcp-event-loop`` 中运行。所有对 MCP 会话的异步操作都通过 ``run_coroutine_threadsafe()`` 调度到此循环。

``_lock`` （``threading.Lock``）保护所有跨线程共享状态：``_servers`` 、``_mcp_loop`` 、``_mcp_thread`` 和 ``_stdio_pids`` 。这确保了代码在 Python 3.13+ 的 free-threading 模式下也是安全的。

``_run_on_mcp_loop()`` 函数在等待异步结果时以 100ms 间隔轮询，允许检测用户中断（``is_interrupted()``），避免了长时间阻塞。

总结
======

Hermes Agent 的 MCP 集成是一个设计精良的生产级实现，覆盖了从传输层到安全防护的各个方面：

- 双传输支持（Stdio + HTTP）满足本地和远程部署需求。

- 自动重连与指数退避确保连接可靠性。

- OAuth 2.1 PKCE 实现了安全的远程认证，包括跨进程令牌同步和 401 去重。

- 熔断器模式防止无限重试循环。

- 动态工具发现允许服务器在运行时更新工具列表。

- 多层安全机制（环境过滤、描述扫描、凭据脱敏、OSV 检查）保护 Agent 不受恶意服务器侵害。

- 冲突保护确保内置工具不会被 MCP 工具意外覆盖。

这些机制共同构成了一个健壮的 MCP 客户端，能够在各种网络和服务条件下稳定运行，同时保持对安全威胁的警惕。
