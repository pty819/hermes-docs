.. _glossary:

术语表
========

本书中使用的所有技术术语的中英文对照与定义。按拼音排序。

A
---

Adapter Pattern（适配器模式）
    一种结构型设计模式，用于将一个类的接口转换为客户端期望的另一个接口。
    在 Hermes 中，用于将不同 LLM 提供商的 API 响应归一化为统一格式。
    参见 ``SimpleNamespace`` 。

Agent Loop（Agent 循环）
    Agent 的核心执行循环，遵循 observe-think-act 模式：观察环境（接收输入）、
    思考（调用 LLM）、行动（执行工具或返回响应）。Hermes 的实现在
    ``run_agent.py:run_conversation()`` 中。

API Key（API 密钥）
    用于认证 API 调用的密钥字符串。Hermes 通过凭证池（Credential Pool）
    管理多个 API Key，支持自动轮换和冷却。

AST（Abstract Syntax Tree，抽象语法树）
    Python 源代码的树状表示。Hermes 使用 AST 在不执行代码的情况下
    判断一个工具文件是否包含注册调用（``tools/registry.py``）。

asyncio
    Python 标准库中的异步 I/O 框架。Hermes 刻意避免在主循环中使用
    ``asyncio.run()`` ，转而使用持久化事件循环来避免资源泄漏。

B
---

Backoff（退避）
    在重试失败操作时逐步增加等待时间的策略。Hermes 使用抖动指数退避
    （jittered exponential backoff），避免多个会话同时重试造成的重试风暴。
    参见 ``agent/retry_utils.py`` 。

Budget（预算）
    对 Agent 行为的资源限制。Hermes 实现了三种预算：迭代预算
    （最大 API 调用次数）、Token 预算（输入输出 token 限制）、
    结果预算（工具返回结果的大小限制）。

C
---

Cache Control（缓存控制）
    Anthropic API 的功能，允许标记特定消息为可缓存，避免重复计算。
    Hermes 的 system_and_3 策略在系统提示词和最近 3 条消息上设置缓存断点。
    参见 ``agent/prompt_caching.py`` 。

Circuit Breaker（断路器）
    一种容错模式，当连续失败次数超过阈值时，快速失败而非继续尝试。
    Hermes 在 MCP 工具连接中使用了断路器模式。参见 ``tools/mcp_tool.py`` 。

CLI（Command Line Interface，命令行界面）
    Hermes 的主要用户界面之一。通过 ``cli.py`` 和 ``hermes_cli/`` 包实现。

Context Compression（上下文压缩）
    当对话历史超过模型的上下文窗口时，通过 LLM 生成摘要来减少消息数量。
    Hermes 的实现在 ``agent/context_compressor.py`` 中。

Context Window（上下文窗口）
    模型单次调用能处理的最大 token 数量。不同模型的上下文窗口大小不同
    （如 GPT-4o 为 128K，Claude 3.5 Sonnet 为 200K）。

Credential Pool（凭证池）
    管理多个 API Key 的组件，支持轮换策略（round-robin、fill-first、
    least-used）和冷却机制。参见 ``agent/credential_pool.py`` 。

D
---

Delegate Tool（委派工具）
    允许主 Agent 将子任务委派给子代理执行的工具。
    子代理获得独立的迭代预算但共享凭证池。参见 ``tools/delegate_tool.py`` 。

E
---

Error Classifier（错误分类器）
    将 API 错误分类为 11 种类型并推荐恢复策略的管线。
    参见 ``agent/error_classifier.py`` 和 ``FailoverReason`` 枚举。

Event Loop（事件循环）
    asyncio 的核心调度器，负责执行协程和处理 I/O 事件。
    Hermes 使用持久化事件循环（而非 ``asyncio.run()``）来避免资源泄漏。
    参见 ``model_tools.py:_get_tool_loop()`` 。

F
---

Failover（故障转移）
    当主提供商失败时自动切换到备用提供商或备用凭证的过程。
    Hermes 的错误分类器为每种错误类型提供故障转移建议。

FailoverReason
    Hermes 定义的 11 种错误原因枚举，包括 auth、billing、rate_limit、
    timeout、context_overflow 等。每种原因对应不同的恢复策略。

FTS5（Full-Text Search 5）
    SQLite 的全文搜索扩展。Hermes 使用 FTS5 实现会话历史的全文搜索。
    参见 ``hermes_state.py`` 。

Function Calling（函数调用）
    LLM 的能力之一，允许模型在响应中请求调用预定义的函数（工具）。
    不同提供商的函数调用格式略有差异（OpenAI 使用 ``tool_calls``,
    Anthropic 使用 ``tool_use`` 内容块）。

G
---

Gateway（网关）
    Hermes 的多平台服务模式，允许通过 RPC 同时服务 Telegram、Discord、
    Web 等多个平台的用户。参见 ``gateway/`` 目录。

Grace Call（宽限调用）
    当迭代预算耗尽时，Hermes 给模型一次额外的 API 调用机会来生成最终总结。
    这确保了 Agent 在预算耗尽时能给出有意义的结束响应。

H
---

history_version（历史版本号）
    TUI 网关中用于乐观并发控制的版本计数器。每次修改会话历史时递增，
    用于检测 Agent 响应期间是否有并发修改。参见 ``tui_gateway/server.py`` 。

Hook（钩子）
    在特定生命周期事件触发时执行的处理器函数。Hermes 定义了 10 个生命周期
    钩子（如 gateway:startup、session:start、agent:step 等）。
    参见 ``gateway/hooks.py`` 。

I
---

IterationBudget（迭代预算）
    控制 Agent 单次对话中最大 API 调用次数的线程安全计数器。
    默认上限为 90 次。子代理获得独立的迭代预算（默认 50 次）。
    参见 ``run_agent.py:IterationBudget`` 。

J
---

Jitter（抖动）
    在退避间隔中添加的随机偏移，用于防止多个会话的重试请求同时到达
    提供商（即"重试风暴"）。参见 ``agent/retry_utils.py:jittered_backoff()`` 。

JSON-RPC（JSON Remote Procedure Call）
    基于 JSON 的远程过程调用协议。Hermes 的 TUI 网关使用 JSON-RPC
    over stdin/stdout 进行进程间通信。

K
---

Key Rotation（密钥轮换）
    当一个 API Key 失效或耗尽配额时，自动切换到下一个可用 Key。
    Hermes 的凭证池支持多种轮换策略。参见 ``agent/credential_pool.py`` 。

L
---

LLM（Large Language Model，大型语言模型）
    本书中指代所有通过 API 调用的大规模语言模型，包括 OpenAI GPT 系列、
    Anthropic Claude 系列、AWS Bedrock 模型等。

M
---

MCP（Model Context Protocol）
    Anthropic 提出的标准化协议，用于 LLM 应用与外部工具/数据源的集成。
    Hermes 实现了 MCP 客户端，可以动态发现和使用 MCP 工具服务器的工具。
    参见 ``tools/mcp_tool.py`` 。

Mermaid
    一种基于文本的图表描述语言，支持流程图、序列图、思维导图等。
    本书使用 Mermaid 绘制所有架构图。

Monolith（单块架构）
    所有功能运行在单个进程中的架构风格。与微服务（microservice）相对。
    Hermes 选择单块架构，因为 Agent 的核心循环是顺序的，拆分不会带来性能收益。

N
---

NEVER_PARALLEL
    Hermes 定义的必须串行执行的工具集合（如 clarify）。
    当一批工具调用中包含这些工具时，整个批次退化为串行执行。

O
---

Observer Pattern（观察者模式）
    一种行为型设计模式，定义了对象之间的一对多依赖关系。
    在 Hermes 中，通过回调函数（stream_callback、tool_progress_callback 等）
    实现了观察者模式，让外部系统可以监听 Agent 的运行事件。

Optimistic Concurrency Control（乐观并发控制）
    一种并发控制策略，假设冲突很少发生，在提交时检查是否有冲突。
    Hermes 的 TUI 网关使用 history_version 实现乐观并发控制。

P
---

PARALLEL_SAFE
    Hermes 定义的安全并行工具集合（如 web_search、read_file）。
    这些工具是只读的且没有共享可变状态，可以安全地并发执行。

PATH_SCOPED
    Hermes 定义的路径作用域工具集合（如 read_file、write_file）。
    这些工具可以并行执行，但需要检查目标路径是否重叠。

Preflight Compression（预压缩）
    在进入主循环之前检查上下文大小，如果超过阈值则主动触发压缩。
    避免了一次注定失败的 API 调用。

Prompt Caching（提示词缓存）
    利用 LLM 提供商的缓存机制，避免重复计算不变的系统提示词和对话前缀。
    Hermes 的 system_and_3 策略报告约 75% 的输入 token 节省。

R
---

RST（reStructuredText）
    Python 文档生态中常用的标记语言。本书使用 Sphinx + RST 格式编写。

S
---

Self-Registration（自注册）
    一种设计模式，模块在加载时自动将自己注册到全局注册表。
    Hermes 的工具系统使用此模式：每个工具文件在 import 时调用
    ``registry.register()`` 。

SimpleNamespace
    Python ``types`` 模块中的轻量级类，支持动态属性访问。
    Hermes 使用 ``SimpleNamespace`` 作为不同 LLM 提供商响应的统一中间格式。

Skin Engine（皮肤引擎）
    允许用户通过 YAML 文件自定义 CLI 视觉外观的系统。
    皮肤通过继承机制工作：用户定义的皮肤只覆盖需要改变的属性。
    参见 ``hermes_cli/skin_engine.py`` 。

SlashWorker
    Hermes TUI 网关中的持久化子进程，负责处理斜杠命令。
    通过 stdin/stdout 的 JSON-RPC 协议与主网关通信。
    参见 ``tui_gateway/slash_worker.py`` 。

Streaming（流式响应）
    LLM API 的响应模式，服务器逐个 token 返回结果，而非等待全部生成后返回。
    Hermes 支持流式响应，通过 ``stream_callback`` 将文本增量传递给 TTS 管线。

Strategy Pattern（策略模式）
    一种行为型设计模式，定义一系列算法并将每个算法封装在独立的类中。
    在 Hermes 中，用于在运行时根据 ``api_mode`` 选择不同的 LLM 调用策略。

T
---

Token
    LLM 处理文本的基本单位。一个 token 大约对应 0.75 个英文单词或 0.5 个汉字。
    Token 数量影响 API 调用成本和上下文窗口使用量。

Tool Registry（工具注册表）
    集中管理所有工具 schema、handler 和元数据的单例对象。
    参见 ``tools/registry.py:ToolRegistry`` 。

Toolset（工具集）
    一组相关工具的集合。工具集可以组合其他工具集（菱形依赖通过集合去重解决）。
    参见 ``toolsets.py`` 。

TUI（Terminal User Interface，终端用户界面）
    在终端中运行的交互式界面。Hermes 的 TUI 通过 ``tui_gateway/`` 模块实现。

W
---

WAL（Write-Ahead Logging，预写式日志）
    SQLite 的日志模式，允许并发读取和单个写入。
    Hermes 在 ``hermes_state.py`` 中启用 WAL 模式以支持多平台并发访问。
