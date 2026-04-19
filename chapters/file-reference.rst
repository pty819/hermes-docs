.. _file-reference:

文件索引
==========

Hermes Agent 仓库中关键文件的快速参考，按架构层次组织。
代码行数为近似值，基于当前主分支。

核心层
--------

.. list-table::
   :header-rows: 1
   :widths: 30 10 30 30

   * - 文件路径
     - 行数
     - 职责
     - 核心类/函数
   * - ``run_agent.py``
     - ~12,000
     - AIAgent 类、主循环、流式调用、工具调度、预算控制
     - ``AIAgent``, ``run_conversation()``, ``IterationBudget``, ``_should_parallelize_tool_batch()``
   * - ``model_tools.py``
     - ~560
     - 工具发现编排、异步桥接
     - ``_run_async()``, ``_get_tool_loop()``, ``discover_builtin_tools()``
   * - ``toolsets.py``
     - ~720
     - 工具集定义与组合解析
     - ``resolve_toolset()``, ``TOOLSETS``, ``_HERMES_CORE_TOOLS``
   * - ``utils.py``
     - ~200
     - 通用工具函数
     - ``atomic_json_write()``, ``env_var_enabled()``

Agent 子系统（agent/）
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 30 30

   * - 文件路径
     - 行数
     - 职责
     - 核心类/函数
   * - ``agent/error_classifier.py``
     - ~830
     - API 错误分类管线、FailoverReason 枚举
     - ``classify_api_error()``, ``FailoverReason``, ``ClassifiedError``
   * - ``agent/retry_utils.py``
     - ~60
     - 抖动指数退避算法
     - ``jittered_backoff()``
   * - ``agent/context_compressor.py``
     - ~1,200
     - 上下文窗口压缩、LLM 摘要生成
     - ``ContextCompressor``, ``SUMMARY_PREFIX``
   * - ``agent/prompt_builder.py``
     - ~1,050
     - 系统提示词构建、身份注入、安全扫描
     - ``build_skills_system_prompt()``, ``load_soul_md()``, ``_scan_context_content()``
   * - ``agent/prompt_caching.py``
     - ~70
     - Anthropic prompt 缓存（system_and_3 策略）
     - ``apply_anthropic_cache_control()``
   * - ``agent/credential_pool.py``
     - ~1,330
     - 多凭证管理、轮换策略、冷却机制
     - ``CredentialPool``, ``STRATEGY_ROUND_ROBIN``
   * - ``agent/context_engine.py``
     - ~180
     - 上下文引擎抽象层
     - ``ContextEngine``
   * - ``agent/skill_utils.py``
     - ~470
     - 技能元数据工具（YAML 解析、平台匹配）
     - ``parse_frontmatter()``, ``skill_matches_platform()``
   * - ``agent/anthropic_adapter.py``
     - ~1,520
     - Anthropic API 适配器
     - ``build_anthropic_kwargs()``, ``normalize_anthropic_response()``
   * - ``agent/bedrock_adapter.py``
     - ~1,100
     - AWS Bedrock API 适配器
     - ``build_bedrock_kwargs()``, ``normalize_bedrock_response()``
   * - ``agent/memory_manager.py``
     - 变动
     - 外部记忆提供者管理
     - ``MemoryManager``
   * - ``agent/model_metadata.py``
     - 变动
     - 模型元数据查询、Token 估算
     - ``estimate_tokens_rough()``, ``get_model_context_length()``
   * - ``agent/display.py``
     - 变动
     - UI 显示辅助（spinner、工具预览）
     - ``KawaiiSpinner``, ``build_tool_preview()``
   * - ``agent/trajectory.py``
     - 变动
     - 轨迹存储与转换
     - ``convert_scratchpad_to_think()``, ``save_trajectory()``
   * - ``agent/usage_pricing.py``
     - 变动
     - API 使用量统计与成本估算
     - ``estimate_usage_cost()``, ``normalize_usage()``

工具系统（tools/）
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 30 30

   * - 文件路径
     - 行数
     - 职责
     - 核心类/函数
   * - ``tools/registry.py``
     - ~480
     - 工具注册中心、自发现机制、schema 查询
     - ``ToolRegistry``, ``discover_builtin_tools()``, ``registry``
   * - ``tools/mcp_tool.py``
     - ~2,600
     - MCP 客户端、动态工具发现、断路器
     - ``discover_mcp_tools()``, MCP server 生命周期管理
   * - ``tools/delegate_tool.py``
     - ~1,200
     - 子代理委派、预算共享
     - 子代理创建与执行
   * - ``tools/budget_config.py``
     - ~50
     - 工具结果预算配置
     - ``BudgetConfig``, ``DEFAULT_BUDGET``
   * - ``tools/terminal_tool.py``
     - 变动
     - 终端命令执行、进程管理
     - 终端环境管理
   * - ``tools/file_tools.py``
     - 变动
     - 文件读写、搜索、补丁
     - 文件操作工具
   * - ``tools/web_tools.py``
     - 变动
     - Web 搜索与内容提取
     - Web 工具
   * - ``tools/browser_tool.py``
     - 变动
     - 浏览器自动化
     - 浏览器工具
   * - ``tools/vision_tools.py``
     - 变动
     - 图像分析
     - 视觉分析工具
   * - ``tools/interrupt.py``
     - 变动
     - 线程安全的工具中断信号
     - ``set_interrupt()``, ``is_interrupted()``

持久化层
----------

.. list-table::
   :header-rows: 1
   :widths: 30 10 30 30

   * - 文件路径
     - 行数
     - 职责
     - 核心类/函数
   * - ``hermes_state.py``
     - ~1,300
     - SQLite 会话存储、FTS5 全文搜索、WAL 模式
     - ``SessionDB``, schema 管理，消息持久化

网关层（gateway/）
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 30 30

   * - 文件路径
     - 行数
     - 职责
     - 核心类/函数
   * - ``gateway/run.py``
     - ~10,900
     - 网关主进程、多平台集成（Telegram/Discord/Slack 等）
     - 网关启动与平台路由
   * - ``gateway/session.py``
     - ~1,250
     - 会话管理、PII 脱敏、重置策略
     - 会话上下文跟踪
   * - ``gateway/hooks.py``
     - ~170
     - 事件钩子系统（10 个生命周期钩子）
     - ``HookRegistry``, ``emit()``, ``discover_and_load()``
   * - ``gateway/config.py``
     - 变动
     - 网关配置定义
     - ``GatewayConfig``, ``Platform``, ``SessionResetPolicy``

TUI 网关层（tui_gateway/）
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 30 30

   * - 文件路径
     - 行数
     - 职责
     - 核心类/函数
   * - ``tui_gateway/server.py``
     - ~3,100
     - TUI JSON-RPC 服务器、会话管理、乐观并发控制
     - ``history_version``, ``_SlashWorker``, RPC 方法分发
   * - ``tui_gateway/slash_worker.py``
     - ~80
     - 持久化斜杠命令工作进程
     - ``_run()``, stdin/stdout JSON-RPC 协议
   * - ``tui_gateway/entry.py``
     - 变动
     - TUI 网关入口、异步 RPC 分发循环
     - 入口点与分发器
   * - ``tui_gateway/render.py``
     - 变动
     - 流式响应渲染、消息格式化
     - ``make_stream_renderer()``, ``render_message()``

CLI 层（hermes_cli/）
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 30 30

   * - 文件路径
     - 行数
     - 职责
     - 核心类/函数
   * - ``hermes_cli/main.py``
     - ~8,460
     - CLI 主入口、HermesCLI 类
     - ``HermesCLI``
   * - ``hermes_cli/skin_engine.py``
     - ~820
     - 皮肤/主题引擎（YAML 驱动）
     - 皮肤加载、继承、应用
   * - ``hermes_cli/callbacks.py``
     - ~240
     - Agent 回调函数（流式、工具进度）
     - 回调注册与分发
   * - ``hermes_cli/plugins.py``
     - ~840
     - 插件发现与加载
     - ``discover_plugins()``, ``invoke_hook()``
   * - ``hermes_cli/config.py``
     - 变动
     - YAML 配置加载与合并
     - ``load_config()``
   * - ``hermes_cli/auth.py``
     - 变动
     - 认证管理、OAuth 流程
     - 认证存储与刷新

常量与配置
------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 30 30

   * - 文件路径
     - 行数
     - 职责
     - 核心类/函数
   * - ``hermes_constants.py``
     - 变动
     - 全局常量（路径、URL、默认值）
     - ``get_hermes_home()``, ``OPENROUTER_BASE_URL``
   * - ``hermes_logging.py``
     - 变动
     - 日志配置
     - ``set_session_context()``
   * - ``hermes_time.py``
     - 变动
     - 时间工具
     - 时间格式化

入口脚本
----------

.. list-table::
   :header-rows: 1
   :widths: 30 10 30 30

   * - 文件路径
     - 行数
     - 职责
     - 核心类/函数
   * - ``cli.py``
     - ~10,600
     - CLI 交互式入口、命令处理
     - 命令路由、REPL 循环
   * - ``batch_runner.py``
     - 变动
     - 批量任务运行器
     - 批量执行与检查点
   * - ``mcp_serve.py``
     - 变动
     - MCP 服务器模式
     - MCP 服务入口

文件依赖关系
--------------

以下 Mermaid 图展示了关键文件之间的导入依赖关系：

.. mermaid::

   graph TD
       CLI["cli.py"] --> RA["run_agent.py"]
       GW["gateway/run.py"] --> RA
       TUI["tui_gateway/server.py"] --> RA
       RA --> MT["model_tools.py"]
       RA --> EC["agent/error_classifier.py"]
       RA --> CC["agent/context_compressor.py"]
       RA --> PB["agent/prompt_builder.py"]
       RA --> PC["agent/prompt_caching.py"]
       RA --> RU["agent/retry_utils.py"]
       RA --> CP["agent/credential_pool.py"]
       MT --> TR["tools/registry.py"]
       MT --> TS["toolsets.py"]
       TR --> TOOLS["tools/*.py"]
       MT --> MCP["tools/mcp_tool.py"]
       PB --> SU["agent/skill_utils.py"]
       RA --> HS["hermes_state.py"]
       GW --> GH["gateway/hooks.py"]
       GW --> GS["gateway/session.py"]

这个依赖图展示了 Hermes 的分层架构：CLI/网关层依赖核心层（``run_agent.py``），
核心层依赖子系统层（agent/ 包和 tools/ 包），子系统层之间保持松耦合。
