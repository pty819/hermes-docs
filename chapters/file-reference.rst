.. _chapter-file-reference:

文件索引
==========

Hermes Agent 仓库中关键文件的快速参考，按架构层次组织。
仅列出当前主分支上实际存在的文件。

核心层
--------

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``run_agent.py``
     - AIAgent 主类、对话循环、流式调用、工具调度、预算控制
   * - ``model_tools.py``
     - 工具发现编排、异步桥接、调用链编排
   * - ``toolsets.py``
     - 工具集定义与组合解析、内置工具集常量
   * - ``toolset_distributions.py``
     - 数据生成场景下的工具集概率分布配置
   * - ``utils.py``
     - 通用工具函数（原子 JSON 写入、环境变量判断等）
   * - ``hermes_state.py``
     - SQLite 会话存储、FTS5 全文搜索、WAL 模式
   * - ``hermes_constants.py``
     - 全局常量（路径、URL、默认值）、``get_hermes_home()``
   * - ``hermes_logging.py``
     - 日志配置、session context 注入
   * - ``hermes_time.py``
     - 时间格式化工具
   * - ``cli.py``
     - CLI 交互式入口、REPL 循环、命令路由
   * - ``batch_runner.py``
     - 批量任务运行器、检查点恢复
   * - ``mcp_serve.py``
     - MCP 服务器模式入口
   * - ``mini_swe_runner.py``
     - SWE 基准运行器，使用 Hermes 执行环境输出标准轨迹格式
   * - ``rl_cli.py``
     - RL 训练专用 CLI，扩展超时和专用系统提示词
   * - ``trajectory_compressor.py``
     - 轨迹后处理压缩，在保留训练信号的前提下缩减 token 数

Agent 子系统（agent/）
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``agent/error_classifier.py``
     - API 错误分类管线、FailoverReason 枚举
   * - ``agent/retry_utils.py``
     - 抖动指数退避算法
   * - ``agent/context_compressor.py``
     - 上下文窗口压缩、LLM 摘要生成
   * - ``agent/prompt_builder.py``
     - 系统提示词构建、身份注入、安全扫描
   * - ``agent/prompt_caching.py``
     - Anthropic prompt 缓存控制（system_and_3 策略）
   * - ``agent/credential_pool.py``
     - 多凭证管理、轮换策略、冷却机制
   * - ``agent/context_engine.py``
     - 上下文引擎抽象层
   * - ``agent/skill_utils.py``
     - 技能元数据工具（YAML 解析、平台匹配）
   * - ``agent/skill_commands.py``
     - CLI 与网关共享的斜杠命令辅助（技能调用、/plan 等）
   * - ``agent/anthropic_adapter.py``
     - Anthropic API 适配器（请求构建、响应归一化）
   * - ``agent/bedrock_adapter.py``
     - AWS Bedrock API 适配器
   * - ``agent/gemini_cloudcode_adapter.py``
     - Google Gemini Cloud Code Assist 适配器，OpenAI 兼容门面
   * - ``agent/copilot_acp_client.py``
     - GitHub Copilot ACP 服务器转发适配器
   * - ``agent/auxiliary_client.py``
     - 辅助任务统一路由（压缩、搜索、视觉等共用后端选择链）
   * - ``agent/memory_manager.py``
     - 外部记忆提供者管理、单提供者限制
   * - ``agent/memory_provider.py``
     - 可插拔记忆提供者抽象基类（内置 + 插件式）
   * - ``agent/model_metadata.py``
     - 模型元数据查询、Token 估算
   * - ``agent/models_dev.py``
     - Models.dev 注册表集成，4000+ 模型/109+ 提供者元数据
   * - ``agent/smart_model_routing.py``
     - 便宜/强力模型智能路由（关键词复杂度分析）
   * - ``agent/rate_limit_tracker.py``
     - API 速率限制追踪（x-ratelimit-* 头解析与展示）
   * - ``agent/nous_rate_guard.py``
     - Nous Portal 跨会话速率限制守卫，防止 429 重试放大
   * - ``agent/google_code_assist.py``
     - Google Code Assist API 客户端（项目发现、引导、配额）
   * - ``agent/google_oauth.py``
     - Google OAuth PKCE 流程（Gemini CLI 认证）
   * - ``agent/display.py``
     - UI 显示辅助（spinner、工具预览）
   * - ``agent/trajectory.py``
     - 轨迹存储与格式转换
   * - ``agent/usage_pricing.py``
     - API 使用量统计与成本估算
   * - ``agent/title_generator.py``
     - 异步自动生成短会话标题
   * - ``agent/context_references.py``
     - 上下文引用解析（文件路径、URL 提取与内容加载）
   * - ``agent/manual_compression_feedback.py``
     - 手动压缩命令的用户反馈摘要
   * - ``agent/subdirectory_hints.py``
     - 渐进式子目录上下文发现（AGENTS.md、CLAUDE.md 等）
   * - ``agent/insights.py``
     - 会话洞察引擎（用量统计、成本估算、工具模式分析）
   * - ``agent/redact.py``
     - 正则式密钥脱敏（日志与工具输出中的 API key/token 遮蔽）

工具系统（tools/）
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``tools/registry.py``
     - 工具注册中心、自发现机制、schema 查询
   * - ``tools/mcp_tool.py``
     - MCP 客户端、动态工具发现、断路器、server 生命周期管理
   * - ``tools/delegate_tool.py``
     - 子代理委派、预算共享
   * - ``tools/budget_config.py``
     - 工具结果预算配置
   * - ``tools/terminal_tool.py``
     - 终端命令执行、进程管理、多后端环境接口
   * - ``tools/file_tools.py``
     - 文件读写、搜索、补丁工具
   * - ``tools/file_operations.py``
     - 跨后端统一文件操作（本地/Docker/SSH/Modal/Daytona 等）
   * - ``tools/fuzzy_match.py``
     - 8 策略模糊匹配链（处理 LLM 生成代码的空白/缩进差异）
   * - ``tools/patch_parser.py``
     - V4A 补丁格式解析器（codex/cline 兼容）
   * - ``tools/web_tools.py``
     - Web 搜索与内容提取
   * - ``tools/browser_tool.py``
     - 浏览器自动化主工具
   * - ``tools/browser_camofox.py``
     - Camofox 本地反检测浏览器后端（REST API 对接）
   * - ``tools/browser_camofox_state.py``
     - Camofox 持久化浏览器 profile 状态管理
   * - ``tools/browser_cdp_tool.py``
     - Chrome DevTools Protocol 直通工具（原生对话框、iframe 等）
   * - ``tools/vision_tools.py``
     - 图像分析工具
   * - ``tools/code_execution_tool.py``
     - 程序化工具调用（PTC）：LLM 写 Python 脚本通过 RPC 调用工具
   * - ``tools/mixture_of_agents_tool.py``
     - Mixture-of-Agents 多模型协作推理
   * - ``tools/send_message_tool.py``
     - 跨平台消息发送（Telegram/Discord/Slack）
   * - ``tools/clarify_tool.py``
     - 结构化澄清问题（多选/开放题）交互工具
   * - ``tools/todo_tool.py``
     - 任务列表管理（分解复杂任务、跟踪进度）
   * - ``tools/checkpoint_manager.py``
     - 文件操作前的透明快照（影子 git 仓库），支持回滚
   * - ``tools/memory_tool.py``
     - 持久化记忆（MEMORY.md/USER.md），跨会话写入不刷新系统提示词
   * - ``tools/session_search_tool.py``
     - 长期对话回忆（SQLite FTS5 搜索 + 摘要模型）
   * - ``tools/image_generation_tool.py``
     - FAL.ai 图像生成（多模型选择、放大）
   * - ``tools/tts_tool.py``
     - 文本转语音（7 个提供者：Edge/ElevenLabs/OpenAI/MiniMax/Mistral/Gemini/NeuTTS）
   * - ``tools/neutts_synth.py``
     - NeuTTS 本地合成辅助进程（独立进程，避免内存常驻）
   * - ``tools/transcription_tools.py``
     - 语音转文字（local faster-whisper/Groq Whisper/OpenAI Whisper）
   * - ``tools/voice_mode.py``
     - 推送式语音交互模式（录音/播放/STT/TTS）
   * - ``tools/homeassistant_tool.py``
     - Home Assistant 智能家居控制（实体列表/状态查询/服务调用）
   * - ``tools/feishu_doc_tool.py``
     - 飞书文档内容读取工具
   * - ``tools/feishu_drive_tool.py``
     - 飞书文档评论操作（列表/回复/添加）
   * - ``tools/rl_training_tool.py``
     - RL 训练管理工具（Tinker-Atropos 集成、环境发现、WandB 监控）
   * - ``tools/managed_tool_gateway.py``
     - Nous 托管工具网关通用辅助（供应商透传）
   * - ``tools/skills_tool.py``
     - 技能列表与查看工具（渐进式披露架构）
   * - ``tools/skill_manager_tool.py``
     - 技能创建/编辑/删除（程序化记忆管理）
   * - ``tools/skills_guard.py``
     - 外部技能安全扫描器（静态分析 + 信任等级策略）
   * - ``tools/skills_hub.py``
     - 技能中心源适配器（GitHub/官方/社区源）
   * - ``tools/skills_sync.py``
     - 内置技能清单式同步（manifest 追踪、hash 比对）
   * - ``tools/interrupt.py``
     - 线程安全的工具中断信号
   * - ``tools/approval.py``
     - 危险命令检测、审批提示与会话级许可状态
   * - ``tools/tirith_security.py``
     - Tirith 预执行安全扫描（同形 URL、管道注入等）
   * - ``tools/url_safety.py``
     - SSRF 防护（阻止请求私有/内部网络地址）
   * - ``tools/website_policy.py``
     - 网站访问策略（用户管理的 URL 黑名单）
   * - ``tools/osv_check.py``
     - MCP 扩展包恶意软件检查（OSV API 查询）
   * - ``tools/path_security.py``
     - 路径遍历检查辅助（resolve + relative_to 模式）
   * - ``tools/ansi_strip.py``
     - ANSI 转义序列剥离（防止进入模型上下文）
   * - ``tools/binary_extensions.py``
     - 二进制文件扩展名常量（跳过文本操作）
   * - ``tools/process_registry.py``
     - 后台进程注册表（输出缓冲、状态轮询、崩溃恢复）
   * - ``tools/tool_result_storage.py``
     - 大输出持久化（写入临时文件、上下文中替换为预览）
   * - ``tools/tool_backend_helpers.py``
     - 工具后端选择共享辅助
   * - ``tools/debug_helpers.py``
     - 共享调试会话基础设施（统一多工具的 DEBUG_MODE 逻辑）
   * - ``tools/env_passthrough.py``
     - 环境变量透传注册表（沙箱中的技能所需变量放行）
   * - ``tools/credential_files.py``
     - 远程终端后端的凭证文件/技能目录挂载注册
   * - ``tools/cronjob_tools.py``
     - Cron 任务管理工具（压缩式动作接口）
   * - ``tools/openrouter_client.py``
     - 共享 OpenRouter API 异步客户端
   * - ``tools/mcp_oauth.py``
     - MCP OAuth 2.1 客户端（PKCE 流程、token 持久化）
   * - ``tools/mcp_oauth_manager.py``
     - MCP OAuth 状态中心管理器（跨进程 token 重载、401 去重）
   * - ``tools/xai_http.py``
     - xAI HTTP 集成共享辅助

执行环境子目录（tools/environments/）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``tools/environments/base.py``
     - 执行环境基类（spawn-per-call 模型、会话快照）
   * - ``tools/environments/local.py``
     - 本地执行环境（进程隔离、环境变量净化）
   * - ``tools/environments/docker.py``
     - Docker 执行环境（cap-drop ALL、资源限制、可选持久化）
   * - ``tools/environments/singularity.py``
     - Singularity/Apptainer 容器环境（containall、可写 overlay）
   * - ``tools/environments/ssh.py``
     - SSH 远程执行环境（ControlMaster 持久连接）
   * - ``tools/environments/modal.py``
     - Modal 云执行环境（Sandbox.create + exec）
   * - ``tools/environments/managed_modal.py``
     - 托管 Modal 环境（通过 tool-gateway）
   * - ``tools/environments/modal_utils.py``
     - Modal 传输层共享执行流程
   * - ``tools/environments/daytona.py``
     - Daytona 云沙箱环境（持久化沙箱、启停管理）
   * - ``tools/environments/file_sync.py``
     - 远程后端文件同步管理器（mtime+size 变更检测、事务同步）

浏览器提供者子目录（tools/browser_providers/）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``tools/browser_providers/base.py``
     - 云浏览器提供者抽象基类
   * - ``tools/browser_providers/browserbase.py``
     - Browserbase 云浏览器提供者
   * - ``tools/browser_providers/firecrawl.py``
     - Firecrawl 云浏览器提供者
   * - ``tools/browser_providers/browser_use.py``
     - Browser Use 云浏览器提供者

网关层（gateway/）
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``gateway/run.py``
     - 网关主进程、多平台集成与消息路由
   * - ``gateway/session.py``
     - 会话管理、PII 脱敏、重置策略
   * - ``gateway/session_context.py``
     - 会话上下文 contextvars（替代 os.environ 防并发污染）
   * - ``gateway/hooks.py``
     - 事件钩子系统（生命周期钩子注册与触发）
   * - ``gateway/config.py``
     - 网关配置定义（GatewayConfig、Platform、SessionResetPolicy）
   * - ``gateway/channel_directory.py``
     - 平台频道/联系人缓存目录（send_message 名称解析）
   * - ``gateway/delivery.py``
     - 投递路由（cron 输出与代理响应的目标选择）
   * - ``gateway/display_config.py``
     - 按平台显示/详细度配置解析器
   * - ``gateway/mirror.py``
     - 跨平台消息投递镜像记录
   * - ``gateway/pairing.py``
     - DM 配对系统（一次性码审批流程、OWASP 安全特性）
   * - ``gateway/restart.py``
     - 网关重启常量与 drain 超时解析
   * - ``gateway/status.py``
     - 网关运行状态检测（PID 文件）
   * - ``gateway/sticker_cache.py``
     - Telegram 贴纸描述缓存（vision 工具结果复用）
   * - ``gateway/stream_consumer.py``
     - 网关流式消费器（同步回调 → 异步平台消息编辑）

内置钩子子目录（gateway/builtin_hooks/）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``gateway/builtin_hooks/boot_md.py``
     - 启动钩子：网关启动时执行 ~/.hermes/BOOT.md

网关平台适配器（gateway/platforms/）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``gateway/platforms/base.py``
     - 平台适配器基类（所有平台继承此类）
   * - ``gateway/platforms/helpers.py``
     - 平台共享辅助（去重、批量聚合、markdown 剥离、线程追踪）
   * - ``gateway/platforms/api_server.py``
     - OpenAI 兼容 API 服务器（Chat Completions/Responses API/SSE 流）
   * - ``gateway/platforms/telegram.py``
     - Telegram 适配器（python-telegram-bot）
   * - ``gateway/platforms/telegram_network.py``
     - Telegram 网络辅助（主机名保留回退传输）
   * - ``gateway/platforms/discord.py``
     - Discord 适配器（discord.py）
   * - ``gateway/platforms/slack.py``
     - Slack 适配器（slack-bolt + Socket Mode）
   * - ``gateway/platforms/signal.py``
     - Signal 适配器（signal-cli daemon HTTP + SSE）
   * - ``gateway/platforms/whatsapp.py``
     - WhatsApp 适配器（Business API / web 自动化多后端）
   * - ``gateway/platforms/email.py``
     - Email 适配器（IMAP 接收 + SMTP 发送）
   * - ``gateway/platforms/sms.py``
     - SMS 适配器（Twilio REST API + webhook）
   * - ``gateway/platforms/webhook.py``
     - 通用 Webhook 适配器（GitHub/GitLab/JIRA/Stripe 等）
   * - ``gateway/platforms/feishu.py``
     - 飞书/Lark 适配器（WebSocket + Webhook、媒体缓存、去重）
   * - ``gateway/platforms/feishu_comment.py``
     - 飞书文档评论事件处理
   * - ``gateway/platforms/feishu_comment_rules.py``
     - 飞书文档评论访问控制规则（3 级解析）
   * - ``gateway/platforms/weixin.py``
     - 微信个人号适配器（iLink Bot API 长轮询）
   * - ``gateway/platforms/wecom.py``
     - 企业微信适配器（AI Bot WebSocket 网关）
   * - ``gateway/platforms/wecom_callback.py``
     - 企业微信回调模式适配器（自建应用加密 XML 回调）
   * - ``gateway/platforms/wecom_crypto.py``
     - 企业微信 BizMsgCrypt AES-CBC 加解密
   * - ``gateway/platforms/dingtalk.py``
     - 钉钉适配器（Stream Mode + 会话 webhook）
   * - ``gateway/platforms/homeassistant.py``
     - Home Assistant 平台适配器（WebSocket 事件监听 + 通知）
   * - ``gateway/platforms/bluebubbles.py``
     - BlueBubbles iMessage 适配器（REST + webhook）
   * - ``gateway/platforms/matrix.py``
     - Matrix 适配器（mautrix SDK，可选 E2EE）
   * - ``gateway/platforms/mattermost.py``
     - Mattermost 适配器（REST API + WebSocket）
   * - ``gateway/platforms/qqbot/adapter.py``
     - QQ Bot 适配器（官方 v2 WebSocket + REST API）
   * - ``gateway/platforms/qqbot/constants.py``
     - QQ Bot 包级常量
   * - ``gateway/platforms/qqbot/crypto.py``
     - QQ Bot AES-256-GCM 凭证解密
   * - ``gateway/platforms/qqbot/onboard.py``
     - QQ Bot 扫码配置引导（QR 码生成与轮询）
   * - ``gateway/platforms/qqbot/utils.py``
     - QQ Bot 共享工具（User-Agent、HTTP 辅助、配置转换）

TUI 网关层（tui_gateway/）
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``tui_gateway/server.py``
     - TUI JSON-RPC 服务器、会话管理、乐观并发控制
   * - ``tui_gateway/slash_worker.py``
     - 持久化斜杠命令工作进程（stdin/stdout JSON-RPC）
   * - ``tui_gateway/entry.py``
     - TUI 网关入口、异步 RPC 分发循环
   * - ``tui_gateway/render.py``
     - 流式响应渲染、消息格式化

CLI 层（hermes_cli/）
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``hermes_cli/main.py``
     - CLI 主入口、HermesCLI 类、argparse 分发
   * - ``hermes_cli/commands.py``
     - 斜杠命令定义与自动补全（COMMAND_REGISTRY 中枢）
   * - ``hermes_cli/config.py``
     - YAML 配置加载与合并
   * - ``hermes_cli/auth.py``
     - 认证管理、OAuth 流程、凭证搜索顺序
   * - ``hermes_cli/auth_commands.py``
     - 凭证池 auth 子命令
   * - ``hermes_cli/copilot_auth.py``
     - GitHub Copilot OAuth 设备码流程与 token 管理
   * - ``hermes_cli/dingtalk_auth.py``
     - 钉钉设备流授权（QR 码扫描 + AppKey 获取）
   * - ``hermes_cli/plugins.py``
     - 插件发现与加载
   * - ``hermes_cli/plugins_cmd.py``
     - ``hermes plugins`` 子命令（安装/更新/移除/列表）
   * - ``hermes_cli/skin_engine.py``
     - 皮肤/主题引擎（YAML 驱动）
   * - ``hermes_cli/callbacks.py``
     - Agent 回调函数（流式、工具进度）
   * - ``hermes_cli/setup.py``
     - 交互式设置向导（模型/终端/Agent/平台/工具）
   * - ``hermes_cli/gateway.py``
     - ``hermes gateway`` 子命令（run/start/stop/restart/status/install）
   * - ``hermes_cli/cron.py``
     - ``hermes cron`` 子命令（list/create/edit/pause/remove）
   * - ``hermes_cli/webhook.py``
     - ``hermes webhook`` 子命令（订阅管理、热重载）
   * - ``hermes_cli/pairing.py``
     - ``hermes pairing`` 子命令（配对码审批/撤销/清理）
   * - ``hermes_cli/doctor.py``
     - ``hermes doctor`` 诊断命令
   * - ``hermes_cli/status.py``
     - ``hermes status`` 组件状态显示
   * - ``hermes_cli/dump.py``
     - ``hermes dump`` 纯文本调试信息导出
   * - ``hermes_cli/debug.py``
     - ``hermes debug`` 调试工具（分享调试报告）
   * - ``hermes_cli/logs.py``
     - ``hermes logs`` 日志查看与过滤（尾随/级别/会话/组件）
   * - ``hermes_cli/backup.py``
     - ``hermes backup/import`` 备份与恢复
   * - ``hermes_cli/uninstall.py``
     - Hermes 卸载器（完全卸载 / 保留数据）
   * - ``hermes_cli/profiles.py``
     - 多 profile 管理（隔离的 HERMES_HOME 实例）
   * - ``hermes_cli/models.py``
     - 模型目录与验证辅助
   * - ``hermes_cli/providers.py``
     - 提供者身份权威源（models.dev + Hermes overlays + 用户配置）
   * - ``hermes_cli/runtime_provider.py``
     - 运行时提供者解析（CLI/网关/cron 共享）
   * - ``hermes_cli/model_normalize.py``
     - 按提供者的模型名归一化（slash/dot/hyphen 格式差异）
   * - ``hermes_cli/model_switch.py``
     - 模型切换管线（CLI 与网关 /model 共享）
   * - ``hermes_cli/codex_models.py``
     - Codex 模型发现（API、本地缓存、配置）
   * - ``hermes_cli/nous_subscription.py``
     - Nous 订阅托管工具能力辅助
   * - ``hermes_cli/platforms.py``
     - 平台注册表（平台元数据唯一真相源）
   * - ``hermes_cli/skills_config.py``
     - 技能配置（按平台/全局启用/禁用）
   * - ``hermes_cli/skills_hub.py``
     - 技能中心 CLI 统一接口（hermes skills + /skills）
   * - ``hermes_cli/tools_config.py``
     - 工具配置（hermes tools 交互式启用/禁用）
   * - ``hermes_cli/mcp_config.py``
     - MCP 服务器管理 CLI（add/remove/list/test）
   * - ``hermes_cli/memory_setup.py``
     - 记忆提供者配置向导
   * - ``hermes_cli/env_loader.py``
     - .env 文件加载辅助（凭证 ASCII 清洗）
   * - ``hermes_cli/default_soul.py``
     - 默认 SOUL.md 模板
   * - ``hermes_cli/banner.py``
     - 欢迎横幅、ASCII art、技能摘要、更新检查
   * - ``hermes_cli/tips.py``
     - 会话启动随机提示
   * - ``hermes_cli/colors.py``
     - ANSI 颜色工具（NO_COLOR 支持）
   * - ``hermes_cli/cli_output.py``
     - 共享 CLI 输出辅助（print_info/success/warning/error）
   * - ``hermes_cli/completion.py``
     - Shell 补全脚本生成（bash/zsh/fish）
   * - ``hermes_cli/curses_ui.py``
     - curses 多选 UI 组件（工具/技能配置交互）
   * - ``hermes_cli/clipboard.py``
     - 剪贴板图片提取（macOS/Windows/Linux/WSL2）
   * - ``hermes_cli/claw.py``
     - OpenClaw 迁移命令（hermes claw migrate）
   * - ``hermes_cli/web_server.py``
     - Web UI 服务器（FastAPI + Vite/React 前端）

插件系统（plugins/）
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 60

   * - 文件路径
     - 职责
   * - ``plugins/context_engine/__init__.py``
     - 上下文引擎插件发现（扫描子目录实现 ContextEngine ABC）
   * - ``plugins/memory/__init__.py``
     - 记忆插件注册入口
   * - ``plugins/memory/honcho/``
     - Honcho 记忆提供者（client + session + CLI）
   * - ``plugins/memory/hindsight/``
     - Hindsight 记忆提供者
   * - ``plugins/memory/holographic/``
     - Holographic 记忆提供者（holographic + retrieval + store）
   * - ``plugins/memory/mem0/``
     - Mem0 记忆提供者
   * - ``plugins/memory/byterover/``
     - ByteRover 记忆提供者
   * - ``plugins/memory/openviking/``
     - OpenViking 记忆提供者
   * - ``plugins/memory/retaindb/``
     - RetainDB 记忆提供者
   * - ``plugins/memory/supermemory/``
     - SuperMemory 记忆提供者
   * - ``plugins/example-dashboard/``
     - 示例仪表盘插件（plugin_api）

文件依赖关系
--------------

以下 Mermaid 图展示了关键文件之间的导入依赖关系：

.. mermaid::
   :name: file-dependency-graph
   :caption: 关键文件导入依赖关系

   flowchart TD
       classDef start fill:#dbeafe,stroke:#3b82f6,color:#1e3a8a
       classDef success fill:#dcfce7,stroke:#16a34a,color:#166534
       classDef warn fill:#fef9c3,stroke:#ca8a04,color:#854d0e
       classDef fail fill:#fee2e2,stroke:#dc2626,color:#991b1b
       classDef info fill:#f1f5f9,stroke:#64748b,color:#334155

       subgraph ENTRY["入口层"]
           CLI["cli.py"]
           GW["gateway/run.py"]
           TUI["tui_gateway/server.py"]
       end

       subgraph CORE["核心层"]
           RA["run_agent.py"]
           HS["hermes_state.py"]
           TS["toolsets.py"]
       end

       subgraph AGENT["agent/ 子系统"]
           EC["agent/error_classifier.py"]
           CC["agent/context_compressor.py"]
           PB["agent/prompt_builder.py"]
           PC["agent/prompt_caching.py"]
           RU["agent/retry_utils.py"]
           CP["agent/credential_pool.py"]
           SMR["agent/smart_model_routing.py"]
           AUX["agent/auxiliary_client.py"]
           SU["agent/skill_utils.py"]
           SRD["agent/subdirectory_hints.py"]
       end

       subgraph TOOLSYS["tools/ 工具系统"]
           MT["model_tools.py"]
           TR["tools/registry.py"]
           TOOLS["tools/*.py"]
           MCP["tools/mcp_tool.py"]
           TTS["tools/transcription_tools.py"]
           VIS["tools/vision_tools.py"]
       end

       subgraph GATEWAY["gateway/ 网关"]
           GH["gateway/hooks.py"]
           GS["gateway/session.py"]
           GSC["gateway/session_context.py"]
       end

       CLI --> RA
       GW --> RA
       TUI --> RA
       RA --> MT
       RA --> EC
       RA --> CC
       RA --> PB
       RA --> PC
       RA --> RU
       RA --> CP
       RA --> SMR
       RA --> AUX
       MT --> TR
       MT --> TS
       TR --> TOOLS
       MT --> MCP
       PB --> SU
       PB --> SRD
       RA --> HS
       GW --> GH
       GW --> GS
       GW --> GSC
       AUX --> TTS
       AUX --> VIS

       class CLI,GW,TUI start
       class RA,HS,TS success
       class MT,TR,TOOLS,MCP,TTS,VIS warn
       class EC,CC,PB,PC,RU,CP,SMR,AUX,SU,SRD info
       class GH,GS,GSC fail

这个依赖图展示了 Hermes 的分层架构：CLI/网关层依赖核心层（``run_agent.py``），
核心层依赖子系统层（agent/ 包和 tools/ 包），子系统层之间保持松耦合。
