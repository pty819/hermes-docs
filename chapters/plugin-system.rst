.. _chapter-plugin-system:

###################################
插件系统：可扩展的 Agent 架构
###################################

.. contents::
   :depth: 3
   :local:

************************
为什么需要插件系统
************************

任何复杂的软件系统都面临一个核心挑战：如何在保持核心稳定的同时允许外部扩展。在 AI Agent 的场景下，这一挑战尤为突出——不同的用户、团队和组织有着截然不同的需求：有人需要对接特定的内存服务（如 Honcho、Mem0），有人需要自定义的上下文压缩引擎，还有人希望在 Agent 运行时注入消息以实现远程控制。

如果所有这些功能都硬编码在核心代码中，代码库会迅速膨胀，维护成本指数级增长。更关键的是，不同的扩展可能相互冲突，导致系统不稳定。

Hermes Agent 的插件系统解决了这一问题。它的设计哲学是：

- **核心做减法** ：核心代码只提供必要的抽象和接口，不实现具体的扩展逻辑。

- **插件做加法** ：每个功能扩展作为独立插件，通过标准接口与核心交互。

- **隔离与安全** ：每个插件在自己的模块空间中运行，钩子回调被独立的 try/except 包裹，单个插件的异常不会影响核心或其他插件。

- **多源发现** ：支持用户级、项目级和 Pip 安装三种来源，满足个人和团队的不同需求。

.. mermaid::

   classDiagram
       class PluginManager {
           -_plugins: Dict~str, LoadedPlugin~
           -_hooks: Dict~str, List~Callable~~
           -_plugin_tool_names: Set~str~
           -_cli_commands: Dict
           -_plugin_commands: Dict
           -_context_engine: ContextEngine
           -_plugin_skills: Dict
           -_cli_ref: Any
           +discover_and_load()
           +invoke_hook(hook_name, **kwargs) List
           +list_plugins() List~Dict~
           +find_plugin_skill(qualified_name) Path
           +list_plugin_skills(plugin_name) List~str~
       }

       class PluginManifest {
           +name: str
           +version: str
           +description: str
           +author: str
           +requires_env: List
           +provides_tools: List~str~
           +provides_hooks: List~str~
           +source: str
           +path: Optional~str~
       }

       class LoadedPlugin {
           +manifest: PluginManifest
           +module: ModuleType
           +tools_registered: List~str~
           +hooks_registered: List~str~
           +commands_registered: List~str~
           +enabled: bool
           +error: Optional~str~
       }

       class PluginContext {
           <<interface>>
           +manifest: PluginManifest
           +_manager: PluginManager
           +register_tool(name, toolset, schema, handler)
           +register_hook(hook_name, callback)
           +register_command(name, handler, description)
           +register_cli_command(name, help, setup_fn)
           +register_context_engine(engine)
           +register_skill(name, path, description)
           +inject_message(content, role)
           +dispatch_tool(tool_name, args)
       }

       PluginManager "1" --> "*" LoadedPlugin : 管理
       LoadedPlugin "1" --> "1" PluginManifest : 包含
       PluginContext "1" --> "1" PluginManager : 引用
       PluginContext ..> PluginManifest : 通过 manager 创建

*****************
插件发现
*****************

Hermes Agent 从三个来源发现插件，按优先级顺序扫描：

用户插件
==========

路径：``~/.hermes/plugins/<name>/``

用户级插件存放在 Hermes Home 目录下的 ``plugins/`` 子目录中。每个插件是一个独立的子目录，包含 ``plugin.yaml`` 清单文件和 ``__init__.py`` 入口模块。这类插件对当前用户的所有项目生效。

项目插件
==========

路径：``./.hermes/plugins/<name>/``

项目级插件存放在当前工作目录的 ``.hermes/plugins/`` 子目录中。与用户插件不同，项目插件需要通过环境变量 ``HERMES_ENABLE_PROJECT_PLUGINS`` 显式启用。这一设计是出于安全考虑——项目目录通常受版本控制，自动加载其中的代码可能带来供应链攻击风险。

项目级插件通常用于团队协作场景：团队成员可以共享针对特定项目的自定义工具和钩子。

Pip 入口点插件
================

入口点组：``hermes_agent.plugins``

通过 Pip 安装的 Python 包可以通过 ``pyproject.toml`` 或 ``setup.py`` 中声明的 ``hermes_agent.plugins`` 入口点注册为 Hermes 插件。这类插件适合发布到 PyPI 供社区使用。

.. code-block:: python

   # setup.py / pyproject.toml 中的入口点声明
   [project.entry-points."hermes_agent.plugins"]
   my_plugin = "my_package.hermes_plugin:register"

发现流程
==========

``PluginManager.discover_and_load()`` 方法执行以下步骤：

#. 扫描用户插件目录（``~/.hermes/plugins/``）。

#. 如果启用了 ``HERMES_ENABLE_PROJECT_PLUGINS`` ，扫描项目插件目录。

#. 扫描 Pip 入口点。

#. 读取配置文件中的 ``plugins.disabled`` 列表，跳过被禁用的插件。

#. 对每个未禁用的插件调用 ``_load_plugin()`` 。

整个发现过程是幂等的——多次调用不会重复加载。

.. mermaid::

   sequenceDiagram
       autonumber
       participant Main as Agent 启动
       participant PM as PluginManager
       participant UserDir as ~/.hermes/plugins/
       participant ProjDir as ./.hermes/plugins/
       participant Pip as importlib.metadata
       participant Config as config.yaml
       participant Plugin as 插件模块

       Main->>PM: discover_and_load()

       PM->>UserDir: _scan_directory(source="user")
       UserDir-->>PM: [PluginManifest, ...]

       PM->>ProjDir: _scan_directory(source="project")
       Note over ProjDir: 仅当 HERMES_ENABLE_PROJECT_PLUGINS=true
       ProjDir-->>PM: [PluginManifest, ...]

       PM->>Pip: _scan_entry_points()
       Pip-->>PM: [PluginManifest, ...]

       PM->>Config: _get_disabled_plugins()
       Config-->>PM: {"plugin_a", "plugin_b"}

       loop 每个清单
           alt 在禁用列表中
               PM->>PM: 标记为 disabled
           else 正常加载
               PM->>Plugin: _load_plugin(manifest)
               Plugin-->>PM: register(ctx) 调用完成
           end
       end

       PM-->>Main: 发现完成

*********************
plugin.yaml 格式
*********************

每个目录型插件必须包含一个 ``plugin.yaml`` （或 ``plugin.yml``）清单文件。该文件声明了插件的基本信息、依赖和能力。

.. code-block:: yaml

   # ~/.hermes/plugins/my-memory/plugin.yaml
   name: my-memory
   version: "1.2.0"
   description: "Memory provider using Honcho for persistent conversation context"
   author: "Developer Name"

   # 运行所需的环境变量（可选）
   requires_env:
     - HONCHO_API_KEY
     - name: HONCHO_PROJECT_ID
       description: "Honcho project identifier"

   # 声明此插件提供的工具（仅文档用途）
   provides_tools:
     - honcho_recall
     - honcho_store

   # 声明此插件注册的钩子（仅文档用途）
   provides_hooks:
     - pre_llm_call
     - post_llm_call

字段说明
==========

- ``name`` ：插件名称。如果省略，使用目录名作为名称。

- ``version`` ：语义化版本号。

- ``description`` ：人类可读的描述。

- ``author`` ：作者信息。

- ``requires_env`` ：运行所需的环境变量列表。支持两种格式——纯字符串或包含 ``name`` 、``description`` 的字典。如果环境变量不满足，插件可以选择降级运行或报错。

- ``provides_tools`` ：插件注册的工具名称列表（仅文档用途，不影响实际注册）。

- ``provides_hooks`` ：插件注册的钩子名称列表（仅文档用途，不影响实际注册）。

清单解析
==========

``_scan_directory()`` 方法遍历指定路径下的子目录，查找 ``plugin.yaml`` 或 ``plugin.yml`` 文件。找到后使用 ``yaml.safe_load()`` 解析内容并构建 ``PluginManifest`` 数据类实例。解析失败会记录 WARNING 日志但不影响其他插件。

****************************
PluginContext API
****************************

``PluginContext`` 是插件系统的核心接口。每个插件在 ``register()`` 函数中接收一个 ``PluginContext`` 实例（通常命名为 ``ctx``），通过它注册工具、钩子、命令和其他扩展点。

.. code-block:: python

   # ~/.hermes/plugins/my-plugin/__init__.py
   def register(ctx):
       """插件入口函数，由 PluginManager 在加载时调用。"""
       ctx.register_tool(
           name="my_tool",
           toolset="my-plugin",
           schema={
               "name": "my_tool",
               "description": "A custom tool from my plugin",
               "parameters": {"type": "object", "properties": {}}
           },
           handler=lambda args, **kw: '{"result": "hello"}',
           description="My custom tool",
           emoji="🔧",
       )

       ctx.register_hook("pre_llm_call", my_pre_llm_hook)
       ctx.register_command("mycmd", my_command_handler, "My slash command")

register_tool
===============

在全局工具注册表中注册一个工具。注册后，该工具出现在 LLM 可见的工具列表中，可以通过标准的工具调用机制使用。

参数：

- ``name`` ：工具名称（字符串）。

- ``toolset`` ：所属工具集（用于 ``hermes tools`` TUI 分组）。

- ``schema`` ：OpenAI Function Calling 格式的 JSON Schema。

- ``handler`` ：工具处理函数，签名 ``handler(args: dict, **kwargs) -> str`` 。

- ``check_fn`` ：可选的连接检查函数，返回 ``bool`` 。

- ``requires_env`` ：可选的环境变量列表。

- ``is_async`` ：是否异步处理函数（默认 ``False`` ）。

- ``description`` ：工具描述。

- ``emoji`` ：在 TUI 中显示的图标。

工具覆盖标志
~~~~~~~~~~~~~

``register_tool`` 新增 ``override`` 布尔参数。当设为 ``True`` 时，插件注册的工具可以替换同名的内置工具。此前，只有 MCP 工具无法覆盖内置工具——这一限制同样适用于插件工具。现在，通过显式声明 ``override=True`` ，插件可以提供增强版的内置工具实现，例如为 ``bash`` 工具添加沙箱隔离、为 ``read_file`` 工具添加内容审计等。

需要注意的是，覆盖内置工具是一项高风险操作，仅在用户明确知情和配置的情况下才应启用。默认情况下 ``override=False`` ，保持向后兼容。

register_hook
===============

注册一个生命周期钩子回调。回调函数接收与钩子类型匹配的关键字参数。未知钩子名称会产生 WARNING 日志但仍被存储（前向兼容）。

register_command
==================

注册一个会话内斜杠命令（如 ``/mycmd``）。处理器签名 ``fn(raw_args: str) -> str | None`` ，支持异步。与内置命令冲突的名称会被拒绝。

register_cli_command
======================

注册一个 CLI 子命令（如 ``hermes myplugin ...``），用于终端级别的操作（如配置、初始化）。

register_context_engine
=========================

注册一个上下文引擎来替代内置的 ``ContextCompressor`` 。全局只允许一个上下文引擎插件，第二个注册尝试会被拒绝并输出 WARNING。

register_skill
================

注册一个只读技能（SKILL.md）。技能通过限定名 ``"<plugin_name>:<skill_name>"`` 访问。插件技能不会出现在系统提示的 ``<available_skills>`` 索引中——它们是显式按需加载的。

inject_message
================

向当前活跃的会话注入消息。如果 Agent 正在运行（处理工具调用），消息被放入中断队列；如果 Agent 空闲，消息被放入待处理输入队列。这一功能使插件能够实现远程控制、消息桥接等高级功能。

dispatch_tool
===============

通过全局工具注册表派发工具调用。插件斜杠命令可以使用此方法调用其他工具（如 ``delegate_task``），而无需直接访问 Agent 实例。在 CLI 模式下自动注入 ``parent_agent`` 上下文，在网关模式下优雅降级。

ctx.llm()
===========

``ctx.llm()`` 方法允许插件直接发起任意 LLM 调用，而无需自行构建 Provider 客户端或处理认证逻辑。方法签名::

    def llm(self, prompt: str, *, model: str = None, provider: str = None,
            system: str = None, max_tokens: int = 1024,
            temperature: float = None) -> str:

核心特性：

- **Provider 自动路由** ：如果不指定 ``provider`` ，自动使用当前会话的主 Provider 和主模型，确保插件行为与用户配置一致。
- **完整认证透传** ：复用 Hermes 的凭证池和客户端缓存，无需插件自行管理 API Key 或 OAuth 令牌。
- **适配器透明** ：自动根据 Provider 类型选择合适的适配器（OpenAI、Anthropic、Bedrock 等），插件无需关心 API 格式差异。

典型使用场景包括：插件需要对工具结果进行二次总结、在钩子中生成元数据、或通过 LLM 增强自定义命令的响应质量。

**********************
生命周期钩子
**********************

Hermes Agent 定义了一组标准化的生命周期钩子（``VALID_HOOKS``），插件可以在 Agent 运行的关键节点注入自定义逻辑。

钩子列表
==========

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 钩子名称
     - 触发时机
   * - ``pre_tool_call``
     - 工具调用之前。参数：``tool_name``, ``args``, ``task_id``, ``session_id``, ``tool_call_id``
   * - ``post_tool_call``
     - 工具调用之后。参数：``tool_name``, ``args``, ``result``
   * - ``pre_llm_call``
     - LLM 调用之前。参数：``messages``, ``tools``
   * - ``post_llm_call``
     - LLM 调用之后。参数：``response``
   * - ``pre_api_request``
     - API 请求发送之前。参数：``request``
   * - ``post_api_request``
     - API 请求返回之后。参数：``response``
   * - ``on_session_start``
     - 会话开始时。参数：``session_id``
   * - ``on_session_end``
     - 会话结束时。参数：``session_id``
   * - ``on_session_finalize``
     - 会话最终确认时。参数：``session_id``
   * - ``on_session_reset``
     - 会话重置时。参数：``session_id``

pre_tool_call：策略执行
=========================

``pre_tool_call`` 钩子最强大的功能是**阻断工具调用** 。插件可以返回一个字典 ``{"action": "block", "message": "原因"}`` 来阻止工具执行。这支持以下场景：

- **速率限制** ：限制特定工具的调用频率。

- **安全策略** ：阻止对敏感资源的访问。

- **审批流程** ：某些操作需要用户确认后才能执行。

``get_pre_tool_call_block_message()`` 函数遍历所有 ``pre_tool_call`` 钩子的返回值，找到第一个有效的阻断指令并返回。无效或无关的返回值被静默忽略，不影响观察者模式的钩子。

.. code-block:: python

   # 插件中的策略钩子示例
   def my_policy_hook(tool_name, args, **kwargs):
       if tool_name == "bash" and "rm -rf" in str(args.get("command", "")):
           return {
               "action": "block",
               "message": "Dangerous rm -rf command blocked by security plugin"
           }
       return None  # 允许执行

   def register(ctx):
       ctx.register_hook("pre_tool_call", my_policy_hook)

pre_llm_call：上下文注入
==========================

``pre_llm_call`` 钩子允许插件在每次 LLM 调用前注入上下文信息。回调可以返回字符串或字典：

.. code-block:: python

   def memory_recall_hook(messages, tools, **kwargs):
       # 从内存服务中检索相关信息
       recalled = memory_service.recall(messages[-1].get("content", ""))
       if recalled:
           return {"context": recalled}
       return None

注入的上下文**始终注入到用户消息中，而非系统提示** 。这是一个重要的设计决策——保持系统提示不变，使得跨回合的 prompt cache 前缀保持一致，缓存的 token 可以被复用。所有注入的上下文是临时的，不会持久化到会话数据库。

on_session_start/end：会话生命周期
====================================

这两个钩子允许插件在会话开始和结束时执行初始化和清理操作。例如，内存提供者可以在会话开始时加载历史上下文，在会话结束时保存新的记忆。

**********************
Hook 执行机制
**********************

``PluginManager.invoke_hook()`` 是钩子分发的核心方法。它按注册顺序调用特定钩子的所有回调，收集非 ``None`` 的返回值。

异常隔离
==========

每个钩子回调被独立的 try/except 包裹。如果某个回调抛出异常，异常被捕获并记录 WARNING 日志，但不影响其他回调的执行。这一设计确保了单个有缺陷的插件不会破坏核心 Agent 循环。

.. code-block:: python

   def invoke_hook(self, hook_name: str, **kwargs: Any) -> List[Any]:
       callbacks = self._hooks.get(hook_name, [])
       results: List[Any] = []
       for cb in callbacks:
           try:
               ret = cb(**kwargs)
               if ret is not None:
                   results.append(ret)
           except Exception as exc:
               logger.warning(
                   "Hook '%s' callback %s raised: %s",
                   hook_name,
                   getattr(cb, "__name__", repr(cb)),
                   exc,
               )
       return results

模块级便捷函数
================

为了简化核心代码中的调用，插件系统提供了一组模块级便捷函数：

- ``invoke_hook(hook_name, **kwargs)`` ：调用 ``get_plugin_manager().invoke_hook()`` 。

- ``get_pre_tool_call_block_message(tool_name, args, ...)`` ：检查 ``pre_tool_call`` 钩子的阻断指令。

- ``get_plugin_context_engine()`` ：返回插件注册的上下文引擎。

- ``get_plugin_command_handler(name)`` ：返回插件注册的斜杠命令处理器。

- ``get_plugin_commands()`` ：返回所有插件斜杠命令的字典。

- ``get_plugin_toolsets()`` ：返回插件工具集的元组列表，用于 TUI 显示。

.. mermaid::

   flowchart TD
       classDef start fill:#dbeafe,stroke:#3b82f6,color:#1e3a8a
       classDef success fill:#dcfce7,stroke:#16a34a,color:#166534
       classDef warn fill:#fef9c3,stroke:#ca8a04,color:#854d0e
       classDef fail fill:#fee2e2,stroke:#dc2626,color:#991b1b
       classDef info fill:#f1f5f9,stroke:#64748b,color:#334155

       EVENT["Agent 事件<br/>(工具调用/LLM调用/...)"] --> INVOKE["invoke_hook(hook_name, **kwargs)"]

       INVOKE --> CB1["回调 1<br/>(插件 A)"]
       INVOKE --> CB2["回调 2<br/>(插件 B)"]
       INVOKE --> CB3["回调 3<br/>(插件 C)"]

       CB1 --> R1["返回值 1"]
       CB2 -->|"异常!"| LOG["记录 WARNING 日志"]
       CB3 --> R3["返回值 3"]

       R1 --> COLLECT["收集非 None 返回值"]
       R3 --> COLLECT

       COLLECT --> RESULTS["返回 [value1, value3]"]

       LOG --> COLLECT

       class EVENT start
       class RESULTS success
       class LOG fail
       class INVOKE,CB1,CB2,CB3,R1,R3,COLLECT info

***********************
内存提供者插件
***********************

Hermes Agent 支持通过插件集成外部内存服务，为 Agent 提供跨会话的持久记忆能力。目前已支持的内存提供者包括：

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 提供者
     - 描述
   * - honcho
     - Honcho AI 的对话理解与记忆服务，提供深度的对话上下文追踪
   * - mem0
     - Mem0 的智能记忆层，自动提取和检索关键信息
   * - holographic
     - Holographic 内存服务，专注于结构化知识存储
   * - byterover
     - ByteRover 的记忆管理平台，支持多模态记忆
   * - supermemory
     - SuperMemory 的统一记忆接口，整合多种记忆源
   * - retaindb
     - RetainDB 的基于数据库的持久记忆，适合结构化数据
   * - openviking
     - OpenViking 的开源记忆方案，强调隐私和本地部署
   * - hindsight
     - Hindsight 的反思式记忆，支持从过往经验中学习

这些插件通常通过 ``pre_llm_call`` 钩子在每次 LLM 调用前注入相关记忆，通过 ``post_llm_call`` 或 ``on_session_end`` 钩子保存新的记忆。

内存提供者插件的设计遵循以下原则：

- **非侵入式** ：通过标准的钩子接口集成，不修改核心代码。

- **可替换** ：用户可以随时切换或禁用内存提供者。

- **安全** ：所有注入的内容进入用户消息（不修改系统提示），不会影响 prompt cache。

Hindsight 的后续改进
=======================

以内存提供者 hindsight 为例，该插件在后期经历了一系列重要的改进：

- **Probe API 的 ``update_mode='append'``** ：hindsight 引入了探测（probe）接口，
  允许以追加模式存储记忆条目。新的上下文信息可以增量添加到已有记忆中，
  而无需覆盖或重写整个记忆块。这大幅降低了在高频交互场景下的记忆丢失风险。

- **跨进程去重** ：在多 Agent 并发运行或会话频繁重启的场景中，
  相同的记忆片段可能被多个进程重复存储。hindsight 的去重机制确保同一条记忆
  在全局范围内只保留一份，提高了记忆检索的精确度并降低存储开销。

************************
上下文引擎插件
************************

Hermes Agent 的内置上下文管理使用 ``ContextCompressor`` 进行上下文压缩。然而，不同的使用场景可能需要不同的上下文管理策略——例如，某些场景需要基于向量的检索，某些需要基于图的关联，还有些需要完全自定义的压缩逻辑。

通过 ``PluginContext.register_context_engine()`` ，插件可以替换内置的 ``ContextCompressor`` ：

.. code-block:: python

   from agent.context_engine import ContextEngine

   class MyContextEngine(ContextEngine):
       name = "my-engine"

       def compress(self, messages, **kwargs):
           # 自定义压缩逻辑
           return compressed_messages

   def register(ctx):
       ctx.register_context_engine(MyContextEngine())

**全局唯一性约束** ：只允许一个上下文引擎插件。如果第二个插件尝试注册，会被拒绝并输出 WARNING 日志。这确保了上下文管理行为的一致性和可预测性。

插件还必须通过 ``isinstance(engine, ContextEngine)`` 检查，确保实现了必需的接口。

插件技能注册
==============

除了工具和钩子，插件还可以通过 ``register_skill()`` 注册技能。插件技能使用限定名格式 ``"<plugin_name>:<skill_name>"`` ，例如 ``"my-plugin:setup-guide"`` 。

插件技能的特点：

- **只读** ：不能通过 ``skill_manage`` 工具编辑。

- **显式加载** ：不出现在系统提示的 ``<available_skills>`` 索引中，需要用户显式请求。

- **名称隔离** ：技能名称不能包含冒号（``:``），因为冒号用于分隔插件名和技能名。

- **平台兼容** ：受 ``platforms`` 前置元数据约束。

- **安全扫描** ：加载时检查提示注入模式，发现可疑内容记录 WARNING 日志。

插件技能支持"捆绑上下文"：当加载一个插件技能时，如果同一插件注册了其他技能，返回的内容会包含一条捆绑提示，告知 Agent 还有哪些同级技能可用。

插件管理的全局单例模式
========================

``PluginManager`` 通过模块级单例模式管理（``get_plugin_manager()``），确保整个进程只有一个实例。这一设计保证了：

- 钩子注册的唯一性：不会因为多次实例化导致钩子被重复注册。

- 状态一致性：所有插件共享同一个管理器，工具集和命令注册不会冲突。

- 惰性初始化：管理器在第一次被请求时才创建，不会影响不使用插件功能的启动速度。

插件加载的错误处理
====================

每个插件的加载被独立的 try/except 包裹。如果某个插件的 ``register()`` 函数抛出异常，该插件会被标记为 ``enabled=False`` 并记录错误信息，但不影响其他插件的加载。``list_plugins()`` 方法返回所有插件的状态（包括失败原因），方便调试。

.. note::

   **模型提供者不是插件**

   Hermes 的 LLM Provider（如 Anthropic、Gemini、DeepSeek、Bedrock 等）并非通过插件系统管理。
   Provider 的身份、路由和认证逻辑统一由 ``hermes_cli/providers.py`` 中的核心叠加层（overlay）
   和 models.dev 目录数据合并实现。这种设计是刻意的——模型路由属于核心基础设施，
   不适合走插件的延迟加载和异常隔离路径。

   ``plugins/`` 目录下**不存在** ``model-providers`` 子目录，也不存在 ``ProviderProfile``
   抽象基类。新增 Provider 不需要创建插件目录，只需在 ``hermes_cli/providers.py`` 的
   ``HERMES_OVERLAYS`` 字典中添加条目即可。

   详细的 Provider 架构（数据源合并、传输类型、认证模式）请参见
   :ref:`chapter-model-routing`。

***************************
运营类插件
***************************

除了核心的内存和上下文引擎插件，Hermes 的插件生态已扩展到多个运营领域：

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 插件
     - 功能描述
   * - disk-cleanup
     - 磁盘空间管理。扫描临时文件、旧日志、过期缓存，提供清理建议和自动清理。
   * - image_gen (openai, xai, openai-codex)
     - 图片生成。支持 OpenAI DALL-E、xAI Grok Imagine、OpenAI Codex 三种后端，
       通过 ``agent/image_routing.py`` 智能路由到可用的后端。
   * - google_meet
     - Google Meet 集成。包含会议机器人（``meet_bot.py``）、音频桥接（``audio_bridge.py``）、
       实时转录（``realtime/``）和 Node.js 子进程管理。
   * - hermes-achievements
     - 成就系统。为 Agent 使用引入游戏化元素——追踪使用里程碑、技能掌握进度，
       提供可视化仪表板展示成就等级。
   * - kanban
     - 看板任务管理。包含 Web 仪表板（``dashboard/``）、任务调度器（dispatcher）、
       SQLite 数据库（``kanban_db``），支持多 Agent 并行任务分配和进度追踪。
   * - simplex-chat
     - SimpleX Chat 平台集成。SimpleX 是一个以隐私为核心的消息平台，不收集用户数据、
       不关联用户身份。该插件将 Hermes Agent 对接 SimpleX 协议，允许通过 SimpleX 的
       端到端加密通道与 Agent 交互，适合对隐私有极高要求的使用场景。
   * - BrowserProvider ABC
     - 浏览器操作抽象基类（Abstract Base Class）。``BrowserProvider`` 定义了统一的
       浏览器交互接口（页面导航、元素操作、截图等），``browserbase``、``browser-use``
       和 ``firecrawl`` 三个插件已迁移至该模式。通过 ABC 抽象，不同浏览器后端可互换
       使用，Agent 代码无需关心底层浏览器实现。
   * - WebSearchProvider ABC
     - 网页搜索抽象基类。``WebSearchProvider`` 定义了统一的搜索接口（查询、结果解析、
       速率限制），以下七个搜索插件已迁移至该模式：``brave_free``（Brave Search 免费
       API）、``ddgs``（DuckDuckGo Search）、``searxng``（SearXNG 自托管）、
       ``exa``（Exa AI 搜索）、``parallel``（并行多引擎搜索）、``tavily``（Tavily
       搜索 API）、``firecrawl``（Firecrawl 搜索）。通过 ABC 抽象，Agent 可在
       不同搜索后端之间无缝切换。

这些插件展示了 Hermes 插件架构的 **广度** ——从基础设施维护（磁盘清理）
到用户交互（成就系统、看板），所有扩展都遵循相同的 ``plugin.yaml`` + ``register()``
范式。

***************************
插件工具合并与命令发现
***************************

插件注册的工具现在会自动合并到内置工具集中。这意味着：

- **LLM 视角统一** ：LLM 看到的是一个统一的工具列表，无需区分工具来源
  是核心模块还是插件
- **工具集过滤生效** ：``hermes tools`` 命令中的工具集分组对插件工具同样有效
- **Schema 一致性** ：插件工具的 JSON Schema 与内置工具遵循相同的验证规则

此外，插件的 CLI 命令在 ``hermes`` 命令分发阶段被自动发现。
当用户执行 ``hermes <subcommand>`` 时，CLI 框架不仅查找内置子命令，
还会扫描所有已加载插件注册的 ``register_cli_command`` 条目。
这使得插件可以无缝扩展 CLI 命令空间，例如 ``hermes myplugin config`` 。

总结
======

Hermes Agent 的插件系统是一个设计良好的扩展框架，通过标准化的接口和清晰的隔离机制，实现了核心与扩展的解耦：

- **三源发现** （用户 / 项目 / Pip）满足不同规模的使用需求。

- **PluginContext API** 提供了丰富的扩展点（工具、钩子、命令、上下文引擎、技能）。

- **生命周期钩子** 覆盖了 Agent 运行的所有关键节点，支持策略执行和上下文注入。

- **异常隔离** 确保单个插件的故障不会影响系统稳定性。

- **内存提供者生态** 支持多种外部记忆服务，用户可按需选择。

- **上下文引擎替换** 允许完全自定义的上下文管理策略。

- **运营类插件** 涵盖磁盘清理、图片生成、会议集成、成就系统和看板管理等功能，展示插件生态的广度。

- **工具合并与命令发现** 使插件能力无缝融入核心体验，用户无需区分工具和命令的来源。

.. note::

   **模型提供者不属于插件系统** 。LLM Provider 的路由和认证由 ``hermes_cli/providers.py``
   中的核心叠加层管理，不属于插件系统的扩展点。详见 :ref:`chapter-model-routing`。

这一架构使得 Hermes Agent 能够在不修改核心代码的情况下，灵活地适应各种使用场景和集成需求。从核心的记忆管理到运营层面的会议机器人和项目看板，插件系统为 Agent 的能力扩展提供了统一而强大的基础设施。
