.. _chapter-security:

############################
安全设计：Agent 的攻防考量
############################

AI Agent 拥有执行代码、读写文件、发起网络请求的能力。与传统软件不同，Agent 的行为由 **自然语言指令** 驱动，而自然语言可以被 ** 恶意构造**。这使得 AI Agent 的安全模型必须同时应对来自用户、模型和外部工具的威胁。

Hermes Agent 的安全设计围绕七条防线展开：提示注入防御、MCP 安全、审批系统、凭证管理、沙箱执行、工具冲突保护和安全扫描。

****************************
1. Agent 安全的独特挑战
****************************

LLM 作为攻击面
================

传统软件的攻击面是代码接口（API 参数、网络端口、文件描述符）。Agent 的攻击面还包括 **自然语言输入**——模型无法可靠区分"用户的真实意图"和"被注入的恶意指令"。

攻击向量包括：

- **直接注入** ：用户输入中包含恶意指令（相对容易检测）
- **间接注入** ：从网页、文件、MCP 工具描述等外部来源注入的恶意指令（难以检测）
- **上下文文件注入** ：通过项目中的 ``.cursorrules`` 、``AGENTS.md`` 、``SOUL.md`` 等文件注入

工具访问的放大效应
====================

Agent 可以调用工具来执行命令、读写文件、访问网络。一次成功的提示注入可能导致：

- 执行任意 shell 命令（通过 ``terminal`` 工具）
- 读取敏感文件（如 ``.env`` 、``.ssh/`` 目录）
- 将敏感数据发送到外部服务器（通过 ``curl`` 、``wget``）
- 修改或删除重要文件

持久上下文的累积风险
======================

Agent 会话可能持续数小时，累积大量上下文。注入的恶意指令可能在上下文中 **休眠** ，等待特定条件触发（如用户请求删除文件时，注入的指令可能将 ``rm`` 的目标从临时文件替换为 ``/etc/passwd``）。

****************************
2. 提示注入防御
****************************

Hermes 的提示注入防御集中在 **上下文文件扫描**——在用户的项目配置文件（``AGENTS.md`` 、``.cursorrules`` 、``SOUL.md`` 等）被注入到系统提示之前，进行模式匹配检测。

``_scan_context_content()`` 函数
==================================

``agent/prompt_builder.py`` 中的 ``_scan_context_content()`` 是上下文文件安全扫描的入口::

    def _scan_context_content(content: str, filename: str) -> str:
        """Scan context file content for injection. Returns sanitized content."""
        findings = []

        # Check invisible unicode
        for char in _CONTEXT_INVISIBLE_CHARS:
            if char in content:
                findings.append(f"invisible unicode U+{ord(char):04X}")

        # Check threat patterns
        for pattern, pid in _CONTEXT_THREAT_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                findings.append(pid)

        if findings:
            logger.warning("Context file %s blocked: %s", filename, ", ".join(findings))
            return f"[BLOCKED: {filename} contained potential prompt injection ({', '.join(findings)}). Content not loaded.]"

        return content

13 种威胁模式
===============

``_CONTEXT_THREAT_PATTERNS`` 定义了 13 种正则表达式模式，覆盖主要的提示注入攻击类型：

.. list-table::
   :header-rows: 1
   :widths: 10 50 40

   * - 编号
     - 模式示例
     - 检测类型
   * - 1
     - ``ignore\s+(previous|all|above|prior)\s+instructions``
     - 指令覆盖
   * - 2
     - ``do\s+not\s+tell\s+the\s+user``
     - 欺骗/隐藏
   * - 3
     - ``system\s+prompt\s+override``
     - 系统提示覆盖
   * - 4
     - ``disregard\s+(your|all|any)\s+(instructions|rules|guidelines)``
     - 规则忽略
   * - 5
     - ``act\s+as\s+(if|though)\s+you\s+(have\s+no|don't\s+have)\s+(restrictions|limits|rules)``
     - 限制绕过
   * - 6
     - ``<!--[^>]*(?:ignore|override|system|secret|hidden)[^>]*-->``
     - HTML 注释注入
   * - 7
     - ``<\s*div\s+style\s*=\s*["'][\s\S]*?display\s*:\s*none``
     - 隐藏 div 注入
   * - 8
     - ``translate\s+.*\s+into\s+.*\s+and\s+(execute|run|eval)``
     - 翻译执行陷阱
   * - 9
     - ``curl\s+[^\n]*\${?\w*(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL|API)``
     - 凭证窃取
   * - 10
     - ``cat\s+[^\n]*(\.env|credentials|\.netrc|\.pgpass)``
     - 敏感文件读取

不可见 Unicode 字符
=====================

``_CONTEXT_INVISIBLE_CHARS`` 检测 10 个不可见 Unicode 字符::

    _CONTEXT_INVISIBLE_CHARS = {
        '\u200b',  # Zero Width Space
        '\u200c',  # Zero Width Non-Joiner
        '\u200d',  # Zero Width Joiner
        '\u2060',  # Word Joiner
        '\ufeff',  # Byte Order Mark
        '\u202a',  # Left-to-Right Embedding
        '\u202b',  # Right-to-Left Embedding
        '\u202c',  # Pop Directional Formatting
        '\u202d',  # Left-to-Right Override
        '\u202e',  # Right-to-Left Override
    }

这些字符可以被攻击者用来：

- **隐藏指令** ：零宽字符可以在视觉上不可见的位置嵌入恶意文本
- **方向覆盖** ：RTL/LTR 覆盖可以改变文本的视觉呈现顺序
- **BOM 伪装** ：字节顺序标记可能干扰文本解析

当检测到任何威胁时，文件内容被替换为 ``[BLOCKED: ...]`` 消息，阻止注入但保留文件名信息以便用户诊断。

.. mermaid:: ../diagrams/prompt-injection-detection.mmd

****************************
3. MCP 安全
****************************

Model Context Protocol (MCP) 允许第三方服务器向 Agent 注册工具。这引入了一个新的信任边界——MCP 服务器可能是恶意的或被入侵的。Hermes 的 MCP 安全措施覆盖工具描述、环境变量、工具名称和外部安全扫描四个维度。

工具描述注入扫描
==================

``tools/mcp_tool.py`` 中的 ``_scan_mcp_description()`` 扫描 MCP 工具描述中的提示注入模式::

    _MCP_INJECTION_PATTERNS = [
        (re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
         "prompt override attempt"),
        (re.compile(r"you\s+are\s+now\s+a", re.I),
         "identity override attempt"),
        (re.compile(r"your\s+new\s+(task|role|instructions?)\s+(is|are)", re.I),
         "task override attempt"),
        (re.compile(r"system\s*:\s*", re.I),
         "system prompt injection attempt"),
        (re.compile(r"<\s*(system|human|assistant)\s*>", re.I),
         "role tag injection attempt"),
        (re.compile(r"do\s+not\s+(tell|inform|mention|reveal)", re.I),
         "concealment instruction"),
        (re.compile(r"(curl|wget|fetch)\s+https?://", re.I),
         "network command in description"),
        (re.compile(r"base64\.(b64decode|decodebytes)", re.I),
         "base64 decode reference"),
        (re.compile(r"exec\s*\(|eval\s*\(", re.I),
         "code execution reference"),
        (re.compile(r"import\s+(subprocess|os|shutil|socket)", re.I),
         "dangerous import reference"),
    ]

与上下文文件扫描不同，MCP 描述扫描是 **警告级别** 的——记录日志但不阻止工具注册。这是因为误报（false positive）会导致合法 MCP 服务器被错误禁用。

环境变量过滤
==============

MCP 服务器在子进程中运行，可能访问宿主机的环境变量。Hermes 对传递给 MCP 子进程的环境变量进行过滤：

- 移除所有 ``*_API_KEY`` 、``*_TOKEN`` 、``*_SECRET`` 变量
- 仅传递 MCP 服务器声明的 ``required_environment_variables``
- 使用 ``_prepend_path()`` 管理 PATH 变量

凭证错误消息净化
==================

``_sanitize_error()`` 函数从错误消息中移除凭证模式，防止 API Key、Token 等敏感信息通过工具错误响应泄漏给模型::

    def _sanitize_error(text: str) -> str:
        """Strip credential-like patterns from error text."""
        return _CREDENTIAL_PATTERN.sub("[REDACTED]", text)

这确保了即使 MCP 工具调用失败并返回包含 API Key 的错误消息，该密钥也不会被包含在 Agent 的上下文中——否则模型可能被诱导将密钥输出给用户或写入文件。

工具名称清洗
==============

MCP 工具的名称经过清洗，确保：

- 不包含路径分隔符（``/`` 、``\``）
- 不以 ``mcp__`` 以外的双下划线前缀开头
- 符合正则表达式 ``[a-zA-Z0-9_-]+`` 的命名规范

****************************
4. 审批系统
****************************

Hermes 的审批系统是 Agent 安全的最后一道防线——在模型决定执行潜在危险的操作之前，要求用户确认。

危险命令检测
==============

``tools/approval.py`` 中的 ``DANGEROUS_PATTERNS`` 定义了 30+ 个正则表达式模式，覆盖以下危险操作类别：

**文件系统破坏**

- 在根路径删除（``rm /...``）
- 递归删除（``rm -r``）
- 写入系统配置（``> /etc/``）
- 复制/移动到系统路径（``cp ... /etc/``）

**权限提升**

- 设置 world-writable 权限（``chmod 777``）
- 递归 chown 到 root（``chown -R root``）

**数据破坏**

- SQL DROP/DELETE without WHERE/TRUNCATE
- 磁盘格式化（``mkfs``）
- 块设备写入（``dd if=``）

**远程代码执行**

- 管道远程内容到 shell（``curl | sh``）
- 通过 -c/-e 标志执行脚本（``python -e``）
- 通过 heredoc 执行脚本（``python << 'EOF'``）

**自毁保护**

- 杀死 Hermes/Gateway 进程（``pkill hermes``）
- 停止/重启 Gateway（``hermes gateway stop``）
- 通过 ``pgrep`` 扩展杀死进程（``kill $(pgrep hermes)``）

**Git 破坏性操作**

- ``git reset --hard``
- ``git push --force``
- ``git clean -f``
- ``git branch -D``

命令规范化
============

在模式匹配之前，命令经过规范化处理以防止绕过：

1.  **ANSI 转义序列剥离** ：``strip_ansi()`` 移除所有 ECMA-48 转义序列
2.  **Null 字节移除** ：``command.replace('\x00', '')``
3.  **Unicode 规范化** ：``unicodedata.normalize('NFKC', command)`` — 将全角拉丁字符（如 ``ｒｍ``）转换为半角等价物（``rm``）

审批决策流程
==============

Hermes 支持三种审批模式（通过 ``config.yaml`` 的 ``approvals.mode`` 配置）：

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 模式
     - 行为
   * - ``manual``
     - 每个危险命令都提示用户审批（默认）
   * - ``smart``
     - 使用辅助 LLM 自动批准低风险命令，高风险命令仍需用户确认
   * - ``off``
     - 跳过所有审批（等价于 ``--yolo`` 标志）

用户对每个审批提示有四种响应：

- **yes/once** ：仅本次批准
- **session** ：本次批准，且在当前会话内记住（不再提示同类命令）
- **always** ：本次批准，且将模式写入 ``config.yaml`` 的 ``command_allowlist`` 永久记住
- **no/deny** ：拒绝执行

会话级审批状态使用 ``contextvars.ContextVar`` 存储，支持 Gateway 的并发执行模型——每个会话的审批状态相互隔离。

Cron 模式特殊处理
===================

定时任务（Cron）无人值守运行，审批行为通过 ``approvals.cron_mode`` 配置：

- **deny** （默认）：阻止危险命令，Agent 需要寻找替代方案
- **approve** ：自动批准所有危险命令（需要用户显式启用）

敏感写入目标
==============

审批系统特别关注以下敏感写入目标，即使通过 shell 变量引用也触发审批：

- ``~/.ssh/`` 目录（SSH 密钥）
- ``~/.hermes/.env`` 文件（API Key）
- ``/etc/`` 目录（系统配置）
- ``/dev/sd*`` 设备（块设备）

::

    _SSH_SENSITIVE_PATH = r'(?:~|\$home|\$\{home\})/\.ssh(?:/|$)'
    _HERMES_ENV_PATH = r'(?:~\/\.hermes/|...\.)env\b'

.. mermaid:: ../diagrams/approval-decision-flow.mmd

****************************
5. 凭证管理
****************************

.env 文件隔离
===============

Hermes 将所有敏感凭证（API Key、Token、密码）存储在 ``~/.hermes/.env`` 文件中，与主配置文件 ``config.yaml`` 分离。这种分离有以下好处：

- **权限控制** ：.env 文件设置为 ``0600`` （仅所有者读写），比 config.yaml 更严格
- **版本控制** ：.env 文件不应被提交到版本控制（已添加到 .gitignore）
- **备份友好** ：可以只备份 config.yaml 而不包含敏感信息

凭证来源抑制
==============

``hermes_cli/auth.py`` 中的 ``suppress_credential_source()`` 允许用户标记某个凭证来源为"抑制"状态。被抑制的来源不会被重新检测和自动配置::

    def suppress_credential_source(provider_id: str, source: str) -> None:
        """Mark a credential source as suppressed so it won't be re-seeded."""

这防止了以下场景：用户曾配置过某个 Provider 的凭证，后来删除了它，但凭证源（如 Claude Code 的 ``~/.claude/.credentials.json``）仍然存在，导致 Hermes 在下次启动时自动重新检测到该凭证。

凭证错误消息脱敏
==================

``_sanitize_error()`` 函数确保 MCP 工具的错误消息不包含敏感信息。``_CREDENTIAL_PATTERN`` 正则表达式匹配常见的凭证格式（``sk-`` 前缀、Bearer Token、API Key 等），替换为 ``[REDACTED]`` 。

显式配置门控
==============

``is_provider_explicitly_configured()`` 检查用户是否 **显式** 配置了某个 Provider，防止自动发现和使用外部凭证::

    def is_provider_explicitly_configured(provider_id: str) -> bool:
        # 1. auth.json active_provider 匹配
        # 2. config.yaml model.provider 匹配
        # 3. Provider 特定环境变量已设置
        #    (排除 CLAUDE_CODE_OAUTH_TOKEN — 它是 Claude Code 自身设置的)

特别地，``CLAUDE_CODE_OAUTH_TOKEN`` 被排除在显式配置检测之外——这个环境变量由 Claude Code 自身设置，不应被视为用户有意在 Hermes 中使用 Anthropic Provider 的信号。

凭证池
========

Hermes 支持凭证池（credential pool），允许为同一个 Provider 配置多个凭证。凭证池存储在 ``auth.json`` 的 ``credential_pool`` 字段中，支持轮换和耗尽检测。

Auth Store 锁机制
===================

``_auth_store_lock()`` 实现了跨进程的文件锁，防止多个 Hermes 实例同时读写 ``auth.json`` ：

- 使用 ``fcntl.flock()`` （Unix）或 ``msvcrt.locking()`` （Windows）
- 可重入——同一线程多次获取锁不会死锁
- 15 秒超时——防止因崩溃导致的永久锁

****************************
6. 沙箱执行
****************************

execute_code 沙箱
===================

Hermes 的代码执行工具（``execute_code``）支持多种沙箱模式：

- **local** ：在宿主机直接执行（最低隔离度）
- **docker** ：在 Docker 容器中执行
- **singularity** ：在 Singularity 容器中执行
- **modal** ：在 Modal 云函数中执行
- **ssh** ：通过 SSH 在远程机器上执行

环境变量清理
==============

无论使用哪种执行模式，Hermes 都会清理传递给子进程的环境变量：

- 移除所有匹配 ``*_API_KEY`` 、``*_TOKEN`` 、``*_SECRET`` 、``*_PASSWORD`` 、``*_CREDENTIAL`` 模式的变量
- 仅传递 ``terminal.env_passthrough`` 中列出的变量
- 技能声明的 ``required_environment_variables`` 自动传递

Docker 沙箱配置
=================

Docker 模式支持以下安全配置：

- **资源限制** ：CPU 核数、内存上限、磁盘上限
- **卷挂载控制** ：默认不挂载宿主机目录（``docker_mount_cwd_to_workspace: false``）
- **持久化文件系统** ：跨会话保留文件系统（``container_persistent: true``）
- **环境变量注入** ：通过 ``docker_env`` 指定精确的键值对

代码执行模式
==============

``code_execution.mode`` 控制脚本执行环境：

- **project** （默认）：在项目工作目录中使用活跃的 virtualenv/conda 环境执行——项目依赖可用
- **strict** ：在隔离的临时目录中使用 Hermes 自身的 Python 执行——最大隔离

两种模式都执行相同的凭证清理和工具白名单检查。

浏览器隔离
============

浏览器工具（``browser_navigate`` 、``browser_click`` 等）有以下安全限制：

- **私有 URL 阻止** ：默认不允许导航到私有 IP 地址（localhost、192.168.x.x 等）
- **不活跃超时** ：120 秒无操作后自动关闭浏览器会话
- **命令超时** ：单个浏览器命令 30 秒超时

****************************
7. 工具冲突保护
****************************

MCP 工具不能覆盖 Hermes 的内置工具。这是通过工具名称前缀和注册顺序保证的：

命名空间前缀
==============

MCP 工具使用 ``mcp__<server_name>__<tool_name>`` 的命名格式，与内置工具的 ``<tool_name>`` 格式不同。这确保了即使 MCP 服务器注册了一个名为 ``terminal`` 的工具，它也不会覆盖内置的 ``terminal`` 工具。

注册顺序保护
==============

内置工具在 Hermes 启动时首先注册，MCP 工具在连接到 MCP 服务器时注册。如果 MCP 工具的名称与已注册的内置工具冲突，注册会被拒绝。

最小权限原则
==============

每个工具只暴露其功能所需的最小接口。例如：

- ``read_file`` 工具不暴露文件系统元数据
- ``terminal`` 工具的输出经过大小限制（防止通过大量输出耗尽上下文）
- ``web_extract`` 工具不暴露 HTTP 头部或 Cookie

*****************************
8. 预执行安全扫描（Tirith）
*****************************

Hermes 集成了 `Tirith <https://github.com/chrishayuk/tirith>`_ 安全扫描器，在执行命令前进行预扫描：

::

    "security": {
        "tirith_enabled": True,
        "tirith_path": "tirith",
        "tirith_timeout": 5,
        "tirith_fail_open": True,
    }

Tirith 的设计理念是 **快速失败**——在命令执行之前检测潜在的安全问题。``tirith_fail_open`` 设置为 ``True`` （默认）确保扫描超时不会阻止合法操作的执行。

****************************
9. 安全设计的权衡
****************************

Hermes 的安全设计需要在 **安全性** 和 ** 可用性** 之间做出权衡：

误报容忍度
============

- 上下文文件扫描：**零容忍**——检测到威胁即阻止（因为用户可以手动修复文件）
- MCP 描述扫描：**高容忍**——仅警告不阻止（因为误报会导致合法 MCP 服务器不可用）
- 危险命令检测：**中等容忍**——通过审批系统让用户判断

性能影响
==========

所有安全检查都对延迟有影响：

- 上下文文件扫描：每次加载文件时执行，使用编译后的正则表达式
- 环境变量过滤：MCP 服务器启动时执行一次
- 审批提示：增加用户交互延迟

Hermes 通过以下方式最小化性能影响：

- 正则表达式编译为 ``re.Pattern`` 对象（而非每次重新编译）
- 环境变量过滤在服务器启动时执行一次
- 审批状态缓存在会话级别

深度防御
==========

Hermes 采用 **深度防御（Defense in Depth）** 策略——没有单一安全措施是完美的，但多层防御的组合显著提高了攻击者的成本：

1.  **第一层** ：上下文文件扫描阻止已知注入模式
2.  **第二层** ：MCP 描述扫描检测恶意工具注册
3.  **第三层** ：凭证过滤防止密钥泄漏
4.  **第四层** ：工具名称保护防止内置工具覆盖
5.  **第五层** ：审批系统阻止未授权的危险操作
6.  **第六层** ：沙箱隔离限制操作影响范围
7.  **第七层** ：预执行安全扫描检测代码注入

****************************
总结
****************************

Hermes Agent 的安全设计面临独特的挑战：LLM 作为攻击面、工具访问的放大效应和持久上下文的累积风险。系统通过七层防线构建了深度防御体系：

1.  **提示注入防御** ：13 种正则模式 + 不可见 Unicode 检测，阻止上下文文件注入
2.  **MCP 安全** ：工具描述扫描、环境变量过滤、凭证错误净化、工具名称清洗
3.  **审批系统** ：30+ 种危险命令模式检测，三级审批模式，会话级状态管理
4.  **凭证管理** ：.env 隔离、来源抑制、显式配置门控、跨进程文件锁
5.  **沙箱执行** ：Docker/SSH/Modal 容器隔离，环境变量清理，资源限制
6.  **工具冲突保护** ：命名空间前缀、注册顺序保护
7.  **预执行扫描** ：Tirith 安全扫描器集成

这些安全措施共同构成了一个多层次的防御体系，在不显著影响用户体验的前提下，有效降低了 Agent 系统的攻击风险。
