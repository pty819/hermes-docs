.. _chapter-cli-ui:

***************************************
CLI 与 UI 系统：构建交互式 Agent 界面
***************************************

.. contents::
   :local:
   :depth: 2

为什么 Agent 需要精心设计的 UI
================================

在传统的认知中，命令行工具只是一种朴素的人机接口——黑底白字，输入命令，得到输出。
然而，当我们将大语言模型（LLM）引入终端后，CLI 的角色发生了质变：
它不再只是"执行命令的工具"，而是一个 **人机协作的实时交互界面** 。

Hermes Agent 的 CLI 面临的设计挑战远超一般终端应用：

- **长时间运行的异步任务** ：Agent 的一次请求可能触发多次工具调用（终端命令、文件读写、网页搜索），
  总耗时从数秒到数分钟不等。用户需要一个实时反馈机制来了解 Agent 正在做什么。
- **多模态交互** ：用户可能需要输入密码（sudo）、选择方案（clarify）、审批危险命令（approval），
  这些交互模式需要安全的输入通道，且不能干扰正在运行的任务。
- **丰富的视觉反馈** ：工具执行状态、文件编辑 diff、token 使用量、模型推理过程——
  这些信息的展示方式直接影响用户的工作效率。
- **主题个性化** ：不同用户有不同的审美偏好，有人喜欢暗色主题，有人需要亮色适配，
  而有些用户希望 Agent 拥有独特的人格化视觉风格。

Hermes 的答案是：用 **prompt_toolkit** 构建一个全功能的 TUI（Terminal User Interface），
同时为非交互式场景（管道、Docker、systemd）提供优雅降级。
皮肤系统让用户可以一键切换视觉风格，Kawaii Spinner 为等待过程注入趣味，
内联 diff 让代码审查变得直观——这些细节共同构成了一套 **令人愉悦的 Agent 交互体验** 。

本章将从架构总览开始，深入剖析 Hermes CLI 的每一个 UI 组件。

CLI 架构总览
==============

Hermes CLI 的启动流程遵循一个清晰的分层架构。从用户在终端输入 ``hermes`` 开始，
到 REPL 循环就绪，经历了以下阶段：

.. mermaid::
   :name: cli-architecture-overview
   :caption: CLI 架构总览

   flowchart TD
       A["用户执行 hermes"] --> B["hermes_cli/main.py<br/>argparse 子命令解析"]
       B --> C{"子命令类型?"}
       C -->|chat / 默认| D["HermesCLI() 初始化"]
       C -->|gateway| E["tui_gateway/entry.py<br/>JSON-RPC 网关"]
       C -->|setup| F["交互式配置向导"]
       C -->|其他子命令| G["一次性执行并退出"]

       D --> H["load_cli_config()<br/>加载 config.yaml"]
       H --> I["init_skin_from_config()<br/>初始化皮肤引擎"]
       I --> J["HermesCLI.run()<br/>启动 REPL 循环"]

       J --> K["prompt_toolkit Application"]
       K --> L["Layout 构建<br/>输入区 + Spinner + 状态栏"]
       K --> M["KeyBindings 注册<br/>Enter / Ctrl+C / Tab"]
       K --> N["Completer 注册<br/>Slash 命令补全"]
       K --> O["AutoSuggest 注册<br/>历史建议"]

       L --> P["REPL 主循环<br/>等待输入 → 路由 → 执行"]
       P --> Q{"输入类型?"}
       Q -->|Slash 命令| R["命令处理器"]
       Q -->|普通文本| S["AIAgent.run_conversation()"]
       Q -->|文件拖放| T["附件处理"]

       S --> U["流式输出 / Spinner / Diff"]
       U --> P

入口点解析
------------

``hermes_cli/main.py`` 是整个系统的入口。它使用 Python Fire 库将 ``HermesCLI`` 类
暴露为 CLI 命令，但在此之前完成了一系列关键的初始化工作：

**Profile 覆盖机制** ：在所有模块导入之前，从 ``sys.argv`` 中解析 ``--profile`` / ``-p`` 参数，
设置 ``HERMES_HOME`` 环境变量。这是因为许多模块在导入时就会缓存 ``HERMES_HOME`` 的值（模块级常量），
如果不在最早时机设置，后续的配置路径就会错误。

**.env 加载** ：按照优先级顺序加载环境变量——先 ``~/.hermes/.env`` ，再项目根目录的 ``.env`` 。
用户管理的 .env 文件应该覆盖过时的 shell 导出值。

**配置桥接** ：``load_cli_config()`` 从 ``config.yaml`` 读取配置，将终端配置映射为环境变量（如
``terminal.env_type`` → ``TERMINAL_ENV``），这样底层的 ``terminal_tool`` 可以通过
``os.getenv()`` 获取配置值。

配置加载的优先级链条为：CLI 参数 > 环境变量 > config.yaml > 默认值。

HermesCLI 类的生命周期
------------------------

``HermesCLI`` 是整个交互式 REPL 的核心。它的初始化参数包括：

- ``model`` ：使用的模型名称（如 ``anthropic/claude-sonnet-4``）
- ``toolsets`` ：启用的工具集列表（如 ``["web", "terminal", "file"]``）
- ``provider`` ：推理服务提供者（如 ``auto`` 、``openrouter`` 、``openai``）
- ``compact`` ：紧凑显示模式
- ``resume`` ：恢复之前的会话 ID
- ``checkpoints`` ：启用文件系统检查点

初始化时会设置大量状态变量，包括对话历史、输入队列、中断队列、各种交互状态
（clarify、sudo、approval、secret、model picker）、语音模式状态等。
``AIAgent`` 实例本身被延迟创建——直到用户发送第一条消息时才真正初始化，避免启动时的长时间等待。

prompt_toolkit 集成
=====================

Hermes 使用 ``prompt_toolkit`` 库来构建一个功能完备的 TUI。
这是一个被 IPython、ptpython 等项目广泛使用的高质量终端 UI 框架。

Layout 布局结构
-----------------

TUI 的布局由 ``HSplit`` 垂直排列的多个区域组成：

.. code-block:: python

   # 简化的布局结构
   layout = HSplit([
       Window(FormattedTextControl(input_area), height=Dimension(min=1)),     # 输入区
       Window(FormattedTextControl(spinner_widget), height=spinner_height),    # Spinner
       ConditionalContainer(                                                   # 状态栏
           Window(FormattedTextControl(status_bar), height=1),
           filter=Condition(lambda: self._status_bar_visible),
       ),
   ])

**输入区（Input Area）** ：用户输入提示符和文本的地方。它显示 ``❯ `` 提示符号（可通过皮肤系统自定义），
并支持多行输入。当有图片附件时，会在输入区上方显示附件徽章（如 ``[📎 Image #1]``）。

**Spinner 区域** ：Agent 运行时显示的动态等待指示器。它会显示当前工具名称、执行时间、
以及随机出现的可爱表情。当 Agent 空闲时，此区域高度为 0，自动隐藏。

**状态栏（Status Bar）** ：显示当前模型名称、上下文使用百分比、会话时长等关键信息。
状态栏的可见性可以通过 ``/statusbar`` 命令切换。

此外，布局还包含一个 ``CompletionsMenu``——当用户按下 Tab 键时，会弹出一个浮动的补全菜单，
显示匹配的 slash 命令。

KeyBindings 键绑定
--------------------

Hermes 注册了丰富的键绑定来支持各种交互模式：

**Enter 键** ：根据当前状态有三种行为——

1. 正常模式：提交用户输入
2. Agent 运行中（interrupt 模式）：中断当前 Agent 执行
3. 交互模式（clarify/approval/sudo/secret）：确认当前选择

**Ctrl+C 键** ：五级优先级的中断处理（详见后文）。

**Tab 键** ：触发 slash 命令补全。

**方向键（上/下）** ：在 clarify 模式中导航选项，在正常模式中浏览历史。

**Ctrl+B** ：切换语音录制模式。

Completer 补全器
------------------

``SlashCommandCompleter`` 是一个 ``prompt_toolkit.Completer`` 子类，
它从 ``COMMAND_REGISTRY`` 中获取所有已注册的命令，并提供前缀匹配补全。

补全逻辑：

1. 当用户输入以 ``/`` 开头时，激活命令补全模式
2. 收集所有命令名称和别名，进行前缀匹配
3. 匹配结果按字母排序，显示命令描述作为 meta 信息
4. 对于有子命令的命令（如 ``/reasoning``），在空格后提供子命令补全
5. 集成 skill 命令——通过 ``skill_commands_provider`` 回调动态获取可用的 skill 列表

AutoSuggest 自动建议
----------------------

``SlashCommandAutoSuggest`` 基于 ``FileHistory`` 提供历史输入建议。
当用户开始输入时，它会查找最匹配的历史记录并显示为灰色提示文本。
用户只需按右箭头键即可接受建议。

输入路由优先级
================

Hermes CLI 的输入处理遵循一个 **九级优先级** 系统。当用户按下 Enter 键时，
输入会被依次检查，直到匹配到某个处理器：

.. mermaid::
   :name: cli-input-routing
   :caption: 输入路由优先级

   flowchart TD
       INPUT["用户按 Enter"] --> P1{"Level 1: sudo_state?"}
       P1 -->|是| SUDO["提交 sudo 密码"]
       P1 -->|否| P2{"Level 2: secret_state?"}
       P2 -->|是| SECRET["提交 secret 值"]
       P2 -->|否| P3{"Level 3: approval_state?"}
       P3 -->|是| APPROVAL["确认审批选择"]
       P3 -->|否| P4{"Level 4: model_picker?"}
       P4 -->|是| MODEL["确认模型选择"]
       P4 -->|否| P5{"Level 5: clarify_state?"}
       P5 -->|是| CLARIFY["确认 clarify 选择<br/>或提交自由文本"]
       P5 -->|否| P6{"Level 6: 空输入?"}
       P6 -->|是| IGNORE["忽略空输入"]
       P6 -->|否| P7{"Level 7: Agent 运行中?"}
       P7 -->|是 + interrupt 模式| INTERRUPT["中断 Agent"]
       P7 -->|是 + queue 模式| QUEUE["排队等待"]
       P7 -->|否| P8{"Level 8: _pending_input?"}
       P8 -->|有| PENDING["从队列取出输入"]
       P8 -->|无| P9{"Level 9: 正常输入"}
       P9 --> SLASH{"是 Slash 命令?"}
       SLASH -->|是| CMD["执行命令"]
       SLASH -->|否| AGENT["发送给 Agent"]

这个设计确保了无论 Agent 处于什么状态，用户的紧急交互（密码输入、命令审批）
总是能被正确路由，不会被遗漏或阻塞。

各级别详细说明
----------------

**Level 1 — Sudo** ：当 ``terminal_tool`` 需要提升权限时，CLI 进入 sudo 输入模式。
输入会被直接路由到 sudo 密码回调，不会经过任何其他处理。密码以隐藏形式显示。

**Level 2 — Secret** ：类似 sudo，用于安全地输入 API Key 等敏感信息。
通过 ``save_env_value_secure()`` 存储到 ``~/.hermes/.env`` ，从不暴露给模型。

**Level 3 — Approval** ：当 Agent 尝试执行危险命令时，CLI 显示审批 UI。
用户可以选择 ``once`` （本次允许）、``session`` （本次会话允许）、``always`` （永久允许）、``deny`` （拒绝）。

**Level 4 — Model Picker** ：``/model`` 命令触发的模型选择 UI。用户可以通过方向键导航可用模型列表。

**Level 5 — Clarify** ：当 Agent 需要用户澄清时，显示选择题界面。
支持方向键导航和 "Other" 选项（自由文本输入）。超时后 Agent 自行决定。

**Level 6 — 空输入** ：纯空白输入被直接忽略，不触发任何操作。

**Level 7 — Agent 运行中** ：取决于 ``busy_input_mode`` 配置——

- ``interrupt`` （默认）：Enter 键中断当前 Agent 执行
- ``queue`` ：输入被排队，等待 Agent 完成后自动发送

**Level 8 — 待处理输入队列** ：某些命令（如 ``/queue`` 、``/steer``）会将消息放入 ``_pending_input`` 队列。

**Level 9 — 正常输入** ：检查是否以 ``/`` 开头（slash 命令），否则作为普通消息发送给 Agent。

Slash 命令系统
================

Hermes 的 slash 命令系统采用 **声明式注册** 架构，通过一个中心化的注册表管理所有命令。

CommandDef 数据类
-------------------

每个命令由 ``CommandDef`` 数据类定义：

.. code-block:: python

   @dataclass(frozen=True)
   class CommandDef:
       name: str                          # 命令名（不含斜杠）
       description: str                   # 人类可读描述
       category: str                      # 分类：Session, Configuration 等
       aliases: tuple[str, ...] = ()      # 别名
       args_hint: str = ""                # 参数提示
       subcommands: tuple[str, ...] = ()  # Tab 补全子命令
       cli_only: bool = False             # 仅 CLI 可用
       gateway_only: bool = False         # 仅网关可用
       gateway_config_gate: str | None = None  # 配置门控

命令注册表（COMMAND_REGISTRY）包含约 50 个命令，按功能分为六大类：

.. list-table:: 命令分类概览
   :header-rows: 1
   :widths: 20 60 20

   * - 分类
     - 代表命令
     - 数量
   * - Session
     - /new, /clear, /history, /save, /retry, /undo, /title, /branch, /compress, /rollback, /stop
     - ~18
   * - Configuration
     - /model, /provider, /personality, /skin, /yolo, /reasoning, /fast, /voice
     - ~10
   * - Tools & Skills
     - /tools, /skills, /cron, /reload, /reload-mcp, /browser, /plugins
     - ~8
   * - Info
     - /help, /usage, /insights, /copy, /paste, /image, /debug
     - ~8
   * - Exit
     - /quit, /exit
     - 1

命令解析流程
--------------

.. mermaid::
   :name: cli-slash-resolution
   :caption: Slash 命令解析流程

   sequenceDiagram
       participant User as 用户
       participant PT as prompt_toolkit
       participant CR as COMMAND_REGISTRY
       participant Handler as 命令处理器
       participant Agent as AIAgent

       User->>PT: 输入 /bg some task
       PT->>PT: Tab 补全（如果按下）
       Note over PT: SlashCommandCompleter<br/>匹配 /background

       User->>PT: 按 Enter
       PT->>CR: resolve_command("bg")

       alt 命令名匹配
           CR-->>PT: CommandDef(name="background", aliases=("bg",))
       else 命令名不匹配
           CR-->>PT: None → 作为普通文本发送
       end

       PT->>Handler: 执行 background 命令
       Handler->>Agent: 创建后台任务
       Handler-->>PT: 返回结果

别名解析机制
--------------

``resolve_command()`` 函数处理命令名解析：

1. 去除输入中的前导斜杠（``/``）
2. 转换为小写
3. 在 ``_COMMAND_LOOKUP`` 字典中查找

这个查找表在模块导入时由 ``_build_command_lookup()`` 构建，
它为每个命令的主名和所有别名创建映射。例如：

.. code-block:: python

   _COMMAND_LOOKUP = {
       "background": CommandDef(name="background", ...),
       "bg": CommandDef(name="background", ...),          # alias
       "exit": CommandDef(name="quit", ...),               # alias
       "q": CommandDef(name="queue", ...),                 # alias
       "snap": CommandDef(name="snapshot", ...),           # alias
   }

这样，用户输入 ``/bg some task`` 和 ``/background some task`` 会被路由到同一个处理器。

Tab 补全实现
--------------

``SlashCommandCompleter`` 实现了 ``prompt_toolkit.Completer`` 接口：

1. 解析当前输入，提取出命令名部分和参数部分
2. 如果只有命令名（无空格），提供命令名补全
3. 如果已有空格，检查是否有 ``subcommands`` 定义，提供子命令补全
4. 额外集成 skill 命令——通过 ``skill_commands_provider`` 动态获取可用的 skill 列表

补全菜单的样式由皮肤系统控制——``completion_menu_bg`` 、``completion_menu_current_bg`` 等颜色键。

皮肤/主题引擎
===============

皮肤引擎是 Hermes CLI 最独特的视觉特性之一。它允许用户通过一个 YAML 文件
完全自定义 CLI 的外观，无需修改任何代码。

SkinConfig 数据结构
---------------------

``SkinConfig`` 是皮肤配置的核心数据类：

.. code-block:: python

   @dataclass
   class SkinConfig:
       name: str
       description: str = ""
       colors: Dict[str, str] = field(default_factory=dict)      # 20+ 颜色键
       spinner: Dict[str, Any] = field(default_factory=dict)     # Spinner 自定义
       branding: Dict[str, str] = field(default_factory=dict)    # 品牌文案
       tool_prefix: str = "┊"                                    # 工具输出前缀
       tool_emojis: Dict[str, str] = field(default_factory=dict) # 工具表情覆盖
       banner_logo: str = ""    # Rich 标记 ASCII 艺术
       banner_hero: str = ""    # Rich 标记英雄图案

内置主题
----------

Hermes 提供了 8+ 个内置主题，每个都有独特的视觉风格：

.. list-table:: 内置皮肤一览
   :header-rows: 1
   :widths: 15 30 25 30

   * - 名称
     - 描述
     - 色调
     - 特殊元素
   * - default
     - 经典 Hermes 金色/可爱
     - 金色 #FFD700 / 青铜色
     - Kawaii 表情、蛇杖图案
   * - ares
     - 战神主题 — 深红与青铜
     - 深红 #9F1C1C / 青铜 #C7A96B
     - ⚔ Spinner翅膀、战神ASCII
   * - mono
     - 单色灰度
     - 灰度 #555555 ~ #e6edf3
     - 简洁专业
   * - slate
     - 冷蓝开发者
     - 蓝色 #4169e1 / #7eb8f6
     - 技术风格
   * - daylight
     - 亮色主题（浅色终端）
     - 蓝色 #2563EB / 深色文字
     - 完整亮色UI
   * - warm-lightmode
     - 暖棕/金色（浅色终端）
     - 棕色 #5C3D11 / 金色
     - 温暖舒适
   * - poseidon
     - 海神主题 — 深蓝与海沫
     - 蓝色 #2A6FB9 / 海沫 #A9DFFF
     - Ψ 三叉戟图案
   * - sisyphus
     - 西西弗斯主题 — 严谨灰度
     - 灰度 #4A4A4A ~ #F5F5F5
     - 巨石 ASCII、坚持语录
   * - charizard
     - 喷火龙主题 — 火山橙
     - 橙色 #C75B1D / 琥珀 #FFD39A
     - ✦ 火焰图案

颜色键系统
------------

皮肤系统定义了 20+ 个颜色键，每个键控制 UI 中的一个特定元素：

.. list-table:: 主要颜色键
   :header-rows: 1
   :widths: 25 35 40

   * - 颜色键
     - 控制元素
     - 默认值
   * - banner_border
     - 横幅边框
     - #CD7F32（青铜色）
   * - banner_title
     - 横幅标题文字
     - #FFD700（金色）
   * - ui_accent
     - 通用 UI 强调色
     - #FFBF00（琥珀色）
   * - ui_ok / ui_error / ui_warn
     - 成功/错误/警告指示器
     - 绿/红/橙
   * - prompt
     - 输入提示文字颜色
     - #FFF8DC（乳白色）
   * - input_rule
     - 输入区分隔线
     - #CD7F32
   * - response_border
     - 响应框边框
     - #FFD700
   * - status_bar_bg
     - 状态栏背景色
     - #1a1a2e（深蓝黑）
   * - completion_menu_*
     - 补全菜单（4个键）
     - 深色背景

继承机制
----------

.. mermaid::
   :name: cli-skin-inheritance
   :caption: 皮肤引擎继承机制

   classDiagram
       class SkinConfig {
           +name: str
           +description: str
           +colors: Dict
           +spinner: Dict
           +branding: Dict
           +tool_prefix: str
           +tool_emojis: Dict
           +banner_logo: str
           +banner_hero: str
           +get_color(key, fallback) str
           +get_spinner_wings() List
           +get_branding(key, fallback) str
       }

       class DefaultSkin {
           金色/青铜色配色
           Kawaii spinner 表情
           Hermes 品牌
       }

       class UserSkin {
           仅覆盖部分颜色键
           其余从 default 继承
       }

       class AresSkin {
           深红/青铜配色
           自定义 spinner 翅膀
           战神品牌
       }

       DefaultSkin <|-- AresSkin : 完整定义
       DefaultSkin <|-- UserSkin : 部分覆盖

       note for UserSkin "_build_skin_config() 将<br/>default 的值作为基础，<br/>然后用用户的值覆盖"
       note for SkinConfig "所有字段都是可选的。<br/>缺失值自动继承 default 皮肤。"

``_build_skin_config()`` 函数实现了继承逻辑：

1. 以 ``default`` 皮肤的值为基础
2. 用用户提供的值覆盖对应字段
3. 返回一个完整的 ``SkinConfig`` 实例

这意味着用户只需要定义想要修改的颜色，其余自动继承。例如，
一个只修改了 ``banner_border`` 和 ``prompt_symbol`` 的用户皮肤：

.. code-block:: yaml

   name: mytheme
   description: 只改了边框和提示符
   colors:
     banner_border: "#FF00FF"
   branding:
     prompt_symbol: ">>> "

其余 20+ 个颜色键会自动使用 ``default`` 皮肤的值。

prompt_toolkit 样式桥接
-------------------------

``get_prompt_toolkit_style_overrides()`` 函数将皮肤颜色键映射为
prompt_toolkit 的样式类名。例如：

.. code-block:: python

   {
       "input-area": prompt,                    # 输入区文字颜色
       "status-bar": f"bg:{status_bg} {text}",  # 状态栏背景+前景
       "clarify-selected": f"{title} bold",      # Clarify 选中项
       "approval-title": f"{warn} bold",         # Approval 标题
       "sudo-prompt": f"{error} bold",           # Sudo 提示
       "completion-menu": f"bg:{menu_bg} {text}",# 补全菜单
   }

这套桥接机制确保 ``/skin`` 命令切换后，TUI 的所有元素（包括补全菜单、交互 UI）
都会立即反映新的配色方案。

KawaiiSpinner
===============

``KawaiiSpinner`` 是 Hermes CLI 的标志性 UI 组件——一个带有可爱表情的动画等待指示器。

9 种动画风格
--------------

Spinner 支持以下动画类型，每种都有独特的视觉节奏：

.. list-table:: Spinner 动画风格
   :header-rows: 1
   :widths: 15 40 30

   * - 名称
     - 帧序列
     - 视觉效果
   * - dots
     - ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏
     - 经典 braille 旋转
   * - bounce
     - ⠁⠂⠄⡀⢀⠠⠐⠈
     - 弹跳线条
   * - grow
     - ▁▂▃▄▅▆▇█▇▆▅▄▃▂
     - 生长柱状图
   * - arrows
     - ←↖↑↗→↘↓↙
     - 箭头旋转
   * - star
     - ✶✷✸✹✺✹✸✷
     - 星形闪烁
   * - moon
     - 🌑🌒🌓🌔🌕🌖🌗🌘
     - 月相变化
   * - pulse
     - ◜◠◝◞◡◟
     - 脉冲圆弧
   * - brain
     - 🧠💭💡✨💫🌟💡💭
     - 大脑思维
   * - sparkle
     - ⁺˚*✧✦✧*˚
     - 闪烁星光

Kawaii 表情
-------------

除了动画帧，Spinner 还定义了两套表情：

**等待表情（KAWAII_WAITING）** ：

.. code-block:: python

   "(｡◕‿◕｡)", "(◕‿◕✿)", "٩(◕‿◕｡)۶", "(✿◠‿◠)", "( ˘▽˘)っ",
   "♪(´ε` )", "(◕ᴗ◕✿)", "ヾ(＾∇＾)", "(≧◡≦)", "(★ω★)"

**思考表情（KAWAII_THINKING）** ：

.. code-block:: python

   "(｡•́︿•̀｡)", "(◔_◔)", "(¬‿¬)", "( •_•)>⌐■-■", "(⌐■_■)",
   "(´･_･`)", "◉_◉", "(°ロ°)", "( ˘⌣˘)♡", "ヽ(>∀<☆)☆"

**思考动词（THINKING_VERBS）** ：

.. code-block:: python

   "pondering", "contemplating", "musing", "cogitating", "ruminating",
   "deliberating", "mulling", "reflecting", "processing", "reasoning",
   "analyzing", "computing", "synthesizing", "formulating", "brainstorming"

这些表情和动词都支持通过皮肤系统自定义。例如，``ares`` 主题使用战神风格的动词：

.. code-block:: python

   "forging", "marching", "sizing the field", "holding the line",
   "hammering plans", "tempering steel", "plotting impact", "raising the shield"

线程安全渲染
--------------

``KawaiiSpinner`` 在一个独立的守护线程中运行动画循环：

.. code-block:: python

   def start(self):
       self.running = True
       self.start_time = time.time()
       self.thread = threading.Thread(target=self._animate, daemon=True)
       self.thread.start()

动画循环每 0.12 秒刷新一帧，使用 ``\r`` 回车符覆盖当前行（而不是打印新行），
这样 spinner 始终保持在同一行。通过 ``self.last_line_len`` 记录上一行的长度，
在写入新帧时用空格填充差值，确保旧内容被完全覆盖。

``print_above()`` 方法允许在 spinner 上方打印文本而不破坏动画：
先清除 spinner 行，打印文本，然后让下一帧重新绘制 spinner。

环境适配
----------

Spinner 会根据运行环境自动调整行为：

**TTY 检测** ：通过 ``self._out.isatty()`` 判断标准输出是否连接到真正的终端。
如果输出被重定向到文件或管道（Docker、systemd），跳过所有动画，
只打印一行静态的 ``[tool] message`` 和 ``[done] message`` 。

**prompt_toolkit StdoutProxy 检测** ：当运行在 ``patch_stdout()`` 上下文中时，
``sys.stdout`` 被 prompt_toolkit 的 ``StdoutProxy`` 包装，它会在每次刷新时注入换行符，
导致 ``\r`` 覆盖失败——每个 spinner 帧都出现在新行上。在这种情况下，spinner 退化为
一个空循环（``time.sleep(0.1)``），让 TUI 的 ``_spinner_text`` 小部件接管显示。

工具预览系统
==============

当 Agent 调用工具时，CLI 需要在紧凑的一行中展示工具调用的关键信息。
这就是 ``build_tool_preview()`` 和 ``get_cute_tool_message()`` 的工作。

build_tool_preview()
----------------------

这个函数接受工具名和参数字典，返回一个简短的预览字符串：

.. list-table:: 工具预览示例
   :header-rows: 1
   :widths: 20 40 30

   * - 工具名
     - 参数
     - 预览输出
   * - terminal
     - {"command": "npm test"}
     - npm test
   * - web_search
     - {"query": "python async"}
     - python async
   * - read_file
     - {"path": "/src/main.py"}
     - /src/main.py
   * - write_file
     - {"path": "/src/main.py"}
     - /src/main.py
   * - search_files
     - {"pattern": "TODO", "target": "content"}
     - TODO
   * - memory
     - {"action": "add", "target": "user", "content": "likes cats"}
     - +user: "likes cats"
   * - todo
     - {"todos": [...], "merge": false}
     - planning 3 task(s)

对于没有专门处理逻辑的工具，函数会尝试从一组候选参数键（``query``, ``text``,
``command``, ``path``, ``name``, ``prompt``, ``code``, ``goal``）中提取预览文本。

get_cute_tool_message()
-------------------------

这个函数生成工具完成后的格式化输出行：

.. code-block:: text

   ┊ 🔍 search    python async                  2.3s
   ┊ 💻 $         npm test                      1.5s
   ┊ 📖 read      /src/main.py                  0.1s
   ┊ ✍️  write     /src/main.py                  0.3s
   ┊ 🔧 patch     /src/main.py                  0.2s

格式为 ``| {emoji} {verb:9} {detail}  {duration}`` ，其中：

- **前缀字符** （``┊``）：由皮肤的 ``tool_prefix`` 控制
- **emoji** ：由皮肤的 ``tool_emojis`` 覆盖或工具注册表的默认值
- **动词** ：左对齐 9 字符（如 ``search``, ``$``, ``read``, ``write``）
- **详情** ：截断到 35-42 字符
- **持续时间** ：格式化为 ``X.Xs``

工具失败检测
--------------

``_detect_tool_failure()`` 检查工具结果是否表示失败：

- ``terminal`` ：检查 ``exit_code`` 是否非零，显示 ``[exit N]``
- ``memory`` ：检查是否超出限制，显示 ``[full]``
- 通用：检查 ``"error"`` / ``"failed"`` 关键词，显示 ``[error]``

失败的工具调用会以红色前缀显示。

内联 Diff 系统
================

当 Agent 编辑文件时，Hermes CLI 会在工具输出下方直接显示 **unified diff** 预览，
让用户即时看到文件变更。这是通过 ``LocalEditSnapshot`` 和 ``extract_edit_diff()``
实现的。

LocalEditSnapshot
-------------------

在工具执行 **之前** ，``capture_local_edit_snapshot()`` 会记录目标文件的当前内容：

.. code-block:: python

   @dataclass
   class LocalEditSnapshot:
       paths: list[Path] = field(default_factory=list)
       before: dict[str, str | None] = field(default_factory=dict)

支持的工具有：

- ``write_file`` ：快照目标路径
- ``patch`` ：快照目标路径
- ``skill_manage`` ：快照 skill 相关文件（create/edit/patch/write_file/remove_file/delete）

工具执行 **之后** ，``extract_edit_diff()`` 比较快照和当前文件内容，
生成 unified diff。

皮肤感知的 ANSI 渲染
----------------------

diff 的颜色由皮肤系统控制。``_diff_ansi()`` 函数从活跃皮肤中提取颜色：

.. list-table:: Diff 颜色映射
   :header-rows: 1
   :widths: 15 30 30

   * - 元素
     - 皮肤颜色键
     - 默认值
   * - 文件头
     - session_label
     - 紫色 #180;160;255
   * - Hunk 头
     - session_border
     - 灰色 #120;120;140
   * - 删除行（-）
     - ui_error（半透明背景）
     - 深红背景
   * - 新增行（+）
     - ui_ok（半透明背景）
     - 深绿背景
   * - 上下文行
     - banner_dim
     - 灰色 #150;150;150

diff 输出有截断保护：最多显示 6 个文件、80 行 diff。超出部分会显示省略摘要。

交互模式
==========

Hermes CLI 支持多种交互模式，每种都针对特定的用户交互需求。

Clarify（澄清）
-----------------

当 Agent 需要用户做出选择时，触发 clarify 回调：

.. code-block:: python

   def clarify_callback(cli, question, choices):
       timeout = CLI_CONFIG.get("clarify", {}).get("timeout", 120)
       response_queue = queue.Queue()
       is_open_ended = not choices

       cli._clarify_state = {
           "question": question,
           "choices": choices,
           "selected": 0,
           "response_queue": response_queue,
       }
       cli._clarify_deadline = time.monotonic() + timeout

       # 阻塞等待用户响应
       while True:
           try:
               result = response_queue.get(timeout=1)
               return result
           except queue.Empty:
               if time.monotonic() > cli._clarify_deadline:
                   break

       # 超时：让 Agent 自行决定
       return "The user did not provide a response. Use your best judgement."

关键特性：

- **方向键导航** ：上下键在选项之间移动，选中项高亮显示
- **"Other" 选项** ：用户可以切换到自由文本输入模式
- **超时机制** ：默认 120 秒，超时后 Agent 自行决定
- **实时倒计时** ：UI 显示剩余时间

Approval（审批）
------------------

当 Agent 尝试执行危险命令时，触发 approval 回调：

.. list-table:: Approval 选项
   :header-rows: 1
   :widths: 15 30 55

   * - 选项
     - 效果
     - 说明
   * - once
     - 本次允许
     - 仅当前命令
   * - session
     - 本次会话允许
     - 同一命令在当前会话中不再询问
   * - always
     - 永久允许
     - 写入永久白名单
   * - deny
     - 拒绝
     - 不执行命令
   * - view（可选）
     - 查看完整命令
     - 命令超过 70 字符时自动出现

approval 回调使用 ``_approval_lock`` 序列化并发请求（例如来自并行委派子任务的请求），
确保每个提示都有自己的处理轮次。

Secret（密码输入）
--------------------

Secret 输入有两种模式：

**TUI 模式** （有 ``_app``）：通过 prompt_toolkit 的 ``PasswordProcessor`` 隐藏输入，
``response_queue`` 阻塞等待。输入缓冲区在进入密码模式前被清空，
防止残留的草稿被误提交。

**Fallback 模式** （无 ``_app``）：使用标准库的 ``getpass.getpass()`` 。

Secret 值通过 ``save_env_value_secure()`` 存储到 ``~/.hermes/.env`` ，
**从不暴露给模型** 。

状态栏三层自适应
==================

状态栏是 CLI 底部的一行信息条，显示模型名称、上下文使用量和会话时长。
它有三层自适应布局：

.. list-table:: 状态栏布局
   :header-rows: 1
   :widths: 15 45 40

   * - 层级
     - 终端宽度
     - 显示内容
   * - Narrow
     - < 52 列
     - ``⚕ model · 3m``
   * - Medium
     - 52 - 75 列
     - ``⚕ model · 45% · 3m 12s``
   * - Wide
     - >= 76 列
     - ``⚕ model · ctx ████████░░ 45% · in:12k out:8k · $0.42 · 3m 12s``

Wide 布局额外显示：

- **上下文进度条** ：``████████░░`` 可视化上下文使用率
- **Token 统计** ：输入 token、输出 token
- **费用估算** ：基于当前模型的定价
- **压缩次数** ：上下文被压缩的次数

颜色编码
----------

上下文使用率的颜色编码：

.. list-table:: 上下文颜色
   :header-rows: 1
   :widths: 20 30 30

   * - 使用率
     - 样式类
     - 视觉含义
   * - < 50%
     - status-bar-good
     - 绿色：充裕
   * - 50% - 80%
     - status-bar-warn
     - 黄色：注意
   * - 80% - 95%
     - status-bar-bad
     - 橙色：紧张
   * - >= 95%
     - status-bar-critical
     - 红色：危急

Ctrl+C 分级处理
=================

Ctrl+C 在 Hermes CLI 中有五级优先级的处理逻辑：

.. list-table:: Ctrl+C 五级处理
   :header-rows: 1
   :widths: 10 30 30 30

   * - 级别
     - 条件
     - 行为
     - 目的
   * - 1
     - 在交互模式（clarify/approval/sudo/secret）中
     - 取消当前交互，返回默认值
     - 允许用户退出不想回答的提示
   * - 2
     - Agent 正在运行
     - 中断 Agent 执行（设置 ``_should_exit`` 标志）
     - 停止正在进行的工具调用
   * - 3
     - 空闲状态，距离上次 Ctrl+C < 1 秒
     - 退出 REPL（设置 ``_should_exit = True``）
     - 双击 Ctrl+C 快速退出
   * - 4
     - 空闲状态，距离上次 Ctrl+C < 3 秒
     - 显示确认退出提示
     - 防止误触
   * - 5
     - 其他情况
     - 记录时间戳，不做任何事
     - 重置超时计时

这个分级系统确保了：

- 在 **紧急情况下** （Agent 运行中），第一次 Ctrl+C 就能中断执行
- 在 **空闲状态下** ，需要双击才能退出，防止误触
- 在 **交互模式中** ，Ctrl+C 优雅地取消当前提示，而不是退出整个程序

源码文件索引
==============

本章涉及的主要源文件：

- ``cli.py`` — ``HermesCLI`` 类，REPL 主循环，输入路由，状态栏，Ctrl+C 处理
- ``hermes_cli/main.py`` — CLI 入口点，argparse 子命令解析，profile 覆盖
- ``hermes_cli/commands.py`` — ``CommandDef`` 数据类，``COMMAND_REGISTRY`` ，别名解析，Tab 补全
- ``hermes_cli/callbacks.py`` — Clarify、Secret、Approval 交互回调
- ``hermes_cli/skin_engine.py`` — ``SkinConfig`` ，8+ 内置主题，颜色继承，prompt_toolkit 样式桥接
- ``agent/display.py`` — ``KawaiiSpinner`` ，工具预览，内联 diff
