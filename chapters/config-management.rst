.. _chapter-config-management:

########################
配置管理：分层配置系统
########################

Hermes Agent 的配置系统设计遵循 **渐进覆盖** 原则——用户只需要覆盖想要改变的设置，其余自动使用合理的默认值。``hermes_cli/config.py`` 实现了一个四层配置架构，支持环境变量、YAML 配置文件、.env 密钥管理和 Profile 隔离。

****************************
1. 配置层级（4 层）
****************************

Hermes 的配置解析遵循严格的优先级链，高优先级的值始终覆盖低优先级的值：

.. list-table::
   :header-rows: 1
   :widths: 10 30 60

   * - 优先级
     - 来源
     - 说明
   * - 1（最高）
     - 环境变量
     - ``os.environ`` 中的值，运行时直接覆盖
   * - 2
     - ``.env`` 文件
     - ``~/.hermes/.env`` ，存储 API Key 等敏感信息
   * - 3
     - ``config.yaml``
     - ``~/.hermes/config.yaml`` ，用户的主配置文件
   * - 4（最低）
     - ``DEFAULT_CONFIG``
     - 代码中的默认值字典，约 800 行

环境变量是最高优先级，这意味着用户可以通过 ``HERMES_FOO=bar hermes chat`` 临时覆盖任何设置，无需修改配置文件。这一设计在 CI/CD、Docker 和 NixOS 部署场景中尤为重要。

.. mermaid:: ../diagrams/config-resolution-priority.mmd

****************************
2. DEFAULT_CONFIG 结构
****************************

``DEFAULT_CONFIG`` 是一个约 800 行的 Python 字典，定义了 Hermes 的所有可配置选项及其默认值。以下是主要配置区块的概览：

模型与 Provider
=================

::

    DEFAULT_CONFIG = {
        "model": "",                    # 默认模型（空字符串 = 未配置）
        "providers": {},                # 自定义 Provider 配置
        "fallback_providers": [],       # 回退 Provider 列表
        "toolsets": ["hermes-cli"],     # 启用的工具集

Agent 行为
============

::

    "agent": {
        "max_turns": 90,                # 单次会话最大轮次
        "gateway_timeout": 1800,        # 网关不活跃超时（秒）
        "tool_use_enforcement": "auto", # 工具调用强制模式
        "gateway_timeout_warning": 900, # 超时前警告阈值
        "gateway_notify_interval": 600, # "仍在工作"通知间隔
    },

终端与沙箱
============

::

    "terminal": {
        "backend": "local",             # local | docker | singularity | modal | daytona | ssh
        "timeout": 180,                 # 命令执行超时
        "docker_image": "nikolaik/python-nodejs:python3.11-nodejs20",
        "container_cpu": 1,
        "container_memory": 5120,       # MB
        "container_persistent": True,
        "persistent_shell": True,       # 跨命令保持 shell 状态
    },

浏览器
========

::

    "browser": {
        "inactivity_timeout": 120,
        "command_timeout": 30,
        "record_sessions": False,
        "allow_private_urls": False,
        "cdp_url": "",                  # Chrome DevTools Protocol 端点
    },

上下文压缩
============

::

    "compression": {
        "enabled": True,
        "threshold": 0.50,              # 上下文使用率超过 50% 时触发
        "target_ratio": 0.20,           # 压缩到阈值的 20%
        "protect_last_n": 20,           # 保留最近 20 条消息不压缩
    },

辅助任务配置
==============

辅助任务（``auxiliary``）是配置系统中最细致的部分，每个辅助任务都有独立的 Provider、模型、Base URL、API Key 和超时设置::

    "auxiliary": {
        "vision": {
            "provider": "auto",
            "model": "",
            "base_url": "",
            "api_key": "",
            "timeout": 120,
        },
        "compression": { ... },
        "web_extract": { "timeout": 360 },
        "session_search": { ... },
        "skills_hub": { ... },
        "approval": { ... },
        "mcp": { ... },
        "flush_memories": { ... },
        "title_generation": { ... },
    },

审批系统
==========

::

    "approvals": {
        "mode": "manual",               # manual | smart | off
        "timeout": 60,                  # 审批等待超时
        "cron_mode": "deny",            # deny | approve（cron 中的危险命令）
    },

安全配置
==========

::

    "security": {
        "redact_secrets": True,         # 在工具输出中过滤密钥
        "tirith_enabled": True,         # 预执行安全扫描
        "tirith_timeout": 5,
        "tirith_fail_open": True,       # 扫描超时时允许执行
    },

显示与交互
============

::

    "display": {
        "compact": False,
        "personality": "kawaii",
        "streaming": False,
        "inline_diffs": True,
        "show_cost": False,
        "skin": "default",
    },

配置版本控制
==============

::

    "_config_version": 19,

配置版本号 ``_config_version`` 用于配置迁移——当 Hermes 升级引入新的配置项时，版本号递增触发迁移流程。

****************************
3. load_config() 深度合并
****************************

``load_config()`` 是配置加载的主入口函数。它执行以下步骤：

1.  **确保 HERMES_HOME 存在** ：``ensure_hermes_home()`` 创建 ``~/.hermes/`` 及其子目录
2.  **深拷贝默认配置** ：``copy.deepcopy(DEFAULT_CONFIG)``
3.  **加载用户配置** ：从 ``~/.hermes/config.yaml`` 读取 YAML
4.  **向后兼容处理** ：将旧的顶层 ``max_turns`` 迁移到 ``agent.max_turns``
5.  **深度合并** ：``_deep_merge(config, user_config)``
6.  **规范化** ：``_normalize_root_model_keys()`` 和 ``_normalize_max_turns_config()``
7.  **环境变量展开** ：``_expand_env_vars()``
8.  **缓存** ：将展开后的配置存入 ``_LAST_EXPANDED_CONFIG_BY_PATH``

深度合并逻辑
==============

``_deep_merge()`` 是一个递归合并函数，确保用户的局部覆盖不会丢失默认值::

    def _deep_merge(base: dict, override: dict) -> dict:
        result = base.copy()
        for key, value in override.items():
            if (key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)):
                result[key] = _deep_merge(result[key], value)
            else:
                result[key] = value
        return result

例如，如果用户在 ``config.yaml`` 中只设置了::

    display:
      compact: true

合并后的 ``display`` 字典将包含 ``compact: True`` （来自用户配置）以及 ``personality: "kawaii"`` 、``streaming: False`` 等所有默认值（来自 ``DEFAULT_CONFIG``）。

环境变量展开
==============

``_expand_env_vars()`` 在配置值中展开 ``${VAR}`` 格式的环境变量引用。这使得用户可以在 ``config.yaml`` 中使用动态值，而无需硬编码。

配置路径
==========

Hermes 的所有配置文件存储在 ``HERMES_HOME`` 目录（默认 ``~/.hermes/``）中：

- ``config.yaml`` — 主配置文件
- ``.env`` — API Key 和密钥
- ``auth.json`` — OAuth Token 和 Provider 状态
- ``context_length_cache.yaml`` — 上下文长度缓存
- ``models_dev_cache.json`` — models.dev 注册表缓存
- ``SOUL.md`` — Agent 人格文件
- ``sessions/`` — 会话历史
- ``logs/`` — 日志文件
- ``memories/`` — 持久化记忆
- ``cron/`` — 定时任务定义

****************************
4. 环境变量管理
****************************

Hermes 的环境变量管理分为两个层面：**加载** （从 .env 文件读取到 ``os.environ``）和 **保存** （将 API Key 等写入 .env 文件）。

load_env() 加载
=================

``load_env()`` 从 ``~/.hermes/.env`` 读取环境变量：

1.  读取文件所有行
2.  ``_sanitize_env_lines()`` 清理损坏的行（如合并的 KEY=VALUE 对）
3.  解析 ``KEY=VALUE`` 格式（跳过注释和空行）
4.  返回 ``Dict[str, str]``

清理逻辑处理以下边界情况：

- **合并行** ：单行包含多个 ``KEY=VALUE`` 对（如文件损坏导致）
- **过期占位符** ：值为 ``***`` 或 ``changeme`` 等无效占位符
- **引号处理** ：正确剥离单引号和双引号

save_env_value() 保存
=======================

``save_env_value()`` 将单个环境变量写入 .env 文件：

1.  **验证键名** ：``_ENV_VAR_NAME_RE`` 正则检查合法的变量名
2.  **清理值** ：移除换行符，检查非 ASCII 字符（API Key 应为纯 ASCII）
3.  **读取现有文件** ：保留未修改的行
4.  **更新或追加** ：如果键已存在则替换，否则追加到末尾
5.  **原子写入** ：使用临时文件 + ``os.replace()`` 确保写入不会损坏文件

::

    def save_env_value(key: str, value: str):
        if not _ENV_VAR_NAME_RE.match(key):
            raise ValueError(f"Invalid environment variable name: {key!r}")
        value = value.replace("\n", "").replace("\r", "")
        value = _check_non_ascii_credential(key, value)
        # ... 读取、更新、原子写入 ...

get_env_value() 查询
======================

``get_env_value()`` 按优先级查找值：

1.  **``os.environ``** — 运行时环境变量
2.  **.env 文件** — 通过 ``load_env()`` 读取

::

    def get_env_value(key: str) -> Optional[str]:
        if key in os.environ:
            return os.environ[key]
        env_vars = load_env()
        return env_vars.get(key)

可选环境变量注册表
====================

``OPTIONAL_ENV_VARS`` 字典定义了 Hermes 支持的所有可选环境变量，包含元数据：

- ``description`` ：变量用途描述
- ``prompt`` ：设置向导中的提示文本
- ``url`` ：获取 API Key 的链接
- ``password`` ：是否为敏感值（显示时脱敏）
- ``tools`` ：哪些工具需要此变量
- ``category`` ：分类（provider / tool / messaging）
- ``advanced`` ：是否为高级选项

这个注册表用于：

- ``hermes setup`` 向导中展示可选配置
- 配置迁移时检测新增的环境变量
- ``hermes config`` 命令展示当前配置

****************************
5. Profile 系统
****************************

Hermes 支持通过 ``--profile`` 标志创建隔离的配置环境。每个 Profile 拥有独立的 ``HERMES_HOME`` 目录，包含自己的配置文件、认证状态和会话历史。

HERMES_HOME 覆盖
==================

Profile 的核心机制是 ``HERMES_HOME`` 目录的覆盖：

- 默认：``~/.hermes/``
- Profile：``~/.hermes/profiles/<profile_name>/``

当用户使用 ``--profile work`` 启动 Hermes 时，所有配置文件的读写都指向 ``~/.hermes/profiles/work/`` 目录，完全与默认配置隔离。

隔离的资源
============

每个 Profile 包含以下独立资源：

- ``config.yaml`` — 配置文件（不同的 Provider、模型、工具集）
- ``.env`` — API Key（不同的凭证）
- ``auth.json`` — OAuth Token（不同的认证状态）
- ``sessions/`` — 会话历史（独立的会话存储）
- ``memories/`` — 持久化记忆（不同的 Agent 记忆）
- ``logs/`` — 日志文件

Profile 的典型使用场景：

- **工作/个人分离** ：使用不同的 Provider 和模型配置
- **多租户部署** ：每个租户使用独立的 Profile
- **测试环境** ：不影响生产配置的实验环境
- **区域隔离** ：中国/国际使用不同的 Provider 配置

****************************
6. 配置迁移
****************************

Hermes 的配置系统随版本演进。``_config_version`` 字段跟踪配置版本，当用户从旧版本升级时触发迁移流程。

版本追踪
==========

``ENV_VARS_BY_VERSION`` 字典记录了每个版本引入的环境变量::

    ENV_VARS_BY_VERSION = {
        3: ["FIRECRAWL_API_KEY", "BROWSERBASE_API_KEY"],
        4: ["VOICE_TOOLS_OPENAI_KEY", "ELEVENLABS_API_KEY"],
        5: ["WHATSAPP_ENABLED", "SLACK_BOT_TOKEN", ...],
        10: ["TAVILY_API_KEY"],
        11: ["TERMINAL_MODAL_MODE"],
    }

迁移流程
==========

当 Hermes 检测到用户的 ``_config_version`` 低于当前版本时：

1.  **识别新增变量** ：计算当前版本与用户版本之间的差异
2.  **提示用户** ：在设置向导中展示新增的可选变量
3.  **更新版本号** ：将 ``_config_version`` 更新为当前版本

向后兼容处理
==============

配置系统包含多个向后兼容适配：

- **顶层 ``max_turns``** ：旧版本将 ``max_turns`` 放在配置顶层，新版本移到 ``agent.max_turns`` 。``load_config()`` 自动迁移。
- **根级 ``model``** ：支持 ``model: "gpt-4o"`` 的简写格式和 ``model: {default: "gpt-4o", provider: "openrouter"}`` 的完整格式。
- **环境变量合并** ：``.env`` 文件中的变量在启动时加载到 ``os.environ`` ，与运行时环境变量合并。

Managed 模式
==============

当 Hermes 运行在 NixOS 或 Homebrew 管理模式下（通过 ``HERMES_MANAGED`` 环境变量或 ``.managed`` 标记文件检测），配置管理有以下限制：

- 配置文件由包管理器拥有，不允许直接编辑
- 目录权限由激活脚本设置（setgid + group-writable, 2770）
- 使用 ``umask(0o007)`` 确保新文件是 group-writable (0660)
- 升级通过 ``nixos-rebuild switch`` 或 ``brew upgrade`` 执行

容器感知
==========

在 Docker/Podman 容器中运行时，配置系统有以下特殊处理：

- 跳过文件权限设置（``_is_container()`` 检测 ``/.dockerenv`` 或 ``/proc/1/cgroup``）
- 支持 ``HERMES_SKIP_CHMOD=1`` 强制跳过权限设置
- 容器执行模式通过 ``~/.hermes/.container-mode`` 配置文件管理

****************************
安全与权限
****************************

文件权限
==========

Hermes 对配置文件和目录实施严格的权限控制：

- ``~/.hermes/`` ：``0700`` （仅所有者可读写执行）
- ``config.yaml`` 、``.env`` 、``auth.json`` ：``0600`` （仅所有者可读写）
- 在容器和 managed 模式下跳过权限设置

密钥脱敏
==========

``redact_key()`` 函数用于显示时脱敏 API Key::

    def redact_key(key: str) -> str:
        if not key:
            return "(not set)"
        if len(key) < 12:
            return "***"
        return f"{key[:4]}...{key[-4:]}"

非 ASCII 凭证检查
===================

``_check_non_ascii_credential()`` 在保存 API Key 时检查非 ASCII 字符，因为 API Key 应该只包含 ASCII 字符。非 ASCII 字符可能导致认证失败，且通常表示复制粘贴错误。

****************************
总结
****************************

Hermes 的配置管理系统是一个精心设计的分层架构，其核心原则是：

1.  **渐进覆盖** ：四层优先级链确保用户只需覆盖想要改变的设置
2.  **深度合并** ：递归合并保留未覆盖的默认值
3.  **安全存储** ：API Key 存储在权限受限的 .env 文件中
4.  **Profile 隔离** ：通过目录隔离实现完全独立的配置环境
5.  **向后兼容** ：自动迁移旧版配置格式，平滑升级路径
6.  **容器友好** ：在 Docker/NixOS 环境中自动适配权限和行为
