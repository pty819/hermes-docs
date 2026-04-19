工具系统：从注册到执行的完整管道
========================================

在本章中，我们将深入探讨 hermes-agent 的工具系统 —— 这是一个精心设计的管道，负责从工具的自注册、发现、解析、类型转换、调度到最终执行的完整生命周期。

这个系统代表了现代 AI Agent 架构中工具管理的最佳实践，它通过注册表模式、AST 预扫描、工具集组合、参数强制转换、并行执行引擎等多个创新机制，实现了高效、安全、可扩展的工具管理。

1. 工具系统设计哲学
---------------------

在深入技术细节之前，让我们首先理解为什么需要这样一个复杂的工具系统，以及它的设计哲学是什么。

为什么 Agent 需要工具？
~~~~~~~~~~~~~~~~~~~~~~~~~

传统的语言模型虽然拥有强大的知识和推理能力，但它们存在几个关键限制：

1. **知识截止日期** ：模型无法获得训练截止日期之后的实时信息
2. **环境交互缺失** ：模型无法直接与外部世界（文件系统、网络、API）交互
3. **执行能力有限** ：模型无法实际执行代码、运行命令或进行物理操作
4. **状态持久化困难** ：模型在多轮对话中难以可靠地保持状态

工具系统正是为了解决这些问题而设计的。通过工具，Agent 可以：

- 使用 ``web_search`` 获取实时信息
- 通过 ``read_file`` 和 ``write_file`` 操作文件系统
- 使用 ``terminal`` 执行任意命令
- 通过 ``execute_code`` 运行 Python 脚本
- 使用 ``memory`` 跨会话持久化信息
- 通过 ``delegate_task`` 拆分复杂任务

自注册模式：去中心化的工具管理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

hermes-agent 采用了**自注册模式** ，这是一个关键的设计决策。在这个模式中：

- 每个工具模块在模块级别调用 ``registry.register()`` 来声明自己
- 没有中心化的工具列表需要手动维护
- 工具可以独立添加、移除或修改，不会影响其他工具
- 模块导入即触发注册，无需额外的初始化步骤

这种设计与传统的中心化配置形成鲜明对比。在传统系统中，你可能需要在一个大的配置文件中列出所有工具，每次添加新工具都要修改这个文件。而在 hermes-agent 中，工具模块自己负责注册自己。

让我们看一个简化的例子，说明这种模式是如何工作的：

.. code-block:: python

    # tools/web_search.py
    from tools.registry import registry

    def web_search_handler(args):
        # 实现搜索逻辑
        pass

    registry.register(
        name="web_search",
        toolset="web",
        schema={
            "name": "web_search",
            "description": "Search the web",
            "parameters": {"type": "object", "properties": {}}
        },
        handler=web_search_handler
    )

当 ``model_tools.py`` 导入这个模块时，注册就自动发生了。这种设计使得工具系统具有极高的可扩展性。

2. 注册表单例 (ToolRegistry)
------------------------------

ToolRegistry 是整个工具系统的核心。它是一个线程安全的单例，负责管理所有工具的元数据、提供查询接口、处理调度逻辑。

单例模式与线程安全
~~~~~~~~~~~~~~~~~~~~

首先，让我们看看 ToolRegistry 是如何实现单例模式的：

.. code-block:: python

    # tools/registry.py
    class ToolRegistry:
        """Singleton registry that collects tool schemas + handlers from tool files."""

        def __init__(self):
            self._tools: Dict[str, ToolEntry] = {}
            self._toolset_checks: Dict[str, Callable] = {}
            self._toolset_aliases: Dict[str, str] = {}
            # MCP dynamic refresh can mutate the registry while other threads are
            # reading tool metadata, so keep mutations serialized and readers on
            # stable snapshots.
            self._lock = threading.RLock()

    # Module-level singleton
    registry = ToolRegistry()

这里有几个关键点值得注意：

1. **模块级单例** ：不是通过复杂的单例模式实现，而是简单地在模块级别创建一个实例。这是 Python 中最简洁、最可靠的单例实现方式。

2. **可重入锁 (RLock)** ：使用 ``threading.RLock()`` 而不是普通的 ``Lock`` 。这使得同一个线程可以多次获取锁，避免死锁。

3. **快照模式** ：注释提到"readers on stable snapshots"，这是一个重要的并发控制策略。我们马上会看到它的实现。

ToolEntry：使用 __slots__ 优化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ToolEntry 是存储单个工具元数据的类。让我们看看它的定义：

.. code-block:: python

    class ToolEntry:
        """Metadata for a single registered tool."""

        __slots__ = (
            "name", "toolset", "schema", "handler", "check_fn",
            "requires_env", "is_async", "description", "emoji",
            "max_result_size_chars",
        )

        def __init__(self, name, toolset, schema, handler, check_fn,
                     requires_env, is_async, description, emoji,
                     max_result_size_chars=None):
            self.name = name
            self.toolset = toolset
            self.schema = schema
            self.handler = handler
            self.check_fn = check_fn
            self.requires_env = requires_env
            self.is_async = is_async
            self.description = description
            self.emoji = emoji
            self.max_result_size_chars = max_result_size_chars

这里使用了 ``__slots__`` ，这是一个重要的 Python 优化技巧。通常，Python 对象使用字典来存储实例属性，这会带来一定的内存开销。通过定义 ``__slots__`` ，我们告诉 Python 使用固定大小的数据结构来存储这些属性，这样：

1. **内存使用减少** ：没有字典的开销
2. **属性访问更快** ：直接通过偏移量访问，而不是哈希表查找
3. **防止动态添加属性** ：使类更加安全，避免拼写错误

对于可能存储数百个工具的注册表来说，这种优化是有意义的。

快照机制：线程安全的读取
~~~~~~~~~~~~~~~~~~~~~~~~~~

ToolRegistry 实现了一个优雅的快照机制，让我们看看：

.. code-block:: python

    def _snapshot_state(self) -> tuple[List[ToolEntry], Dict[str, Callable]]:
        """Return a coherent snapshot of registry entries and toolset checks."""
        with self._lock:
            return list(self._tools.values()), dict(self._toolset_checks)

    def _snapshot_entries(self) -> List[ToolEntry]:
        """Return a stable snapshot of registered tool entries."""
        return self._snapshot_state()[0]

这个模式的工作原理是：

1. **写操作加锁** ：所有修改 ``_tools`` 或 ``_toolset_checks`` 的操作都在锁的保护下进行
2. **读操作获取快照** ：读操作不持有锁，而是获取一个当前状态的快照
3. **快照是不可变的** ：一旦获取快照，它就是稳定的，不会被其他线程的修改影响

这种设计比简单的读写锁有优势：

- 读操作不会阻塞写操作
- 读操作之间不会相互阻塞
- 每个读操作看到的是一致的状态，不会出现部分更新

注册 API：工具的自声明
~~~~~~~~~~~~~~~~~~~~~~~~

现在让我们看看核心的 ``register()`` 方法：

.. code-block:: python

    def register(
        self,
        name: str,
        toolset: str,
        schema: dict,
        handler: Callable,
        check_fn: Callable = None,
        requires_env: list = None,
        is_async: bool = False,
        description: str = "",
        emoji: str = "",
        max_result_size_chars: int | float | None = None,
    ):
        """Register a tool.  Called at module-import time by each tool file."""
        with self._lock:
            existing = self._tools.get(name)
            if existing and existing.toolset != toolset:
                # Allow MCP-to-MCP overwrites (legitimate: server refresh,
                # or two MCP servers with overlapping tool names).
                both_mcp = (
                    existing.toolset.startswith("mcp-")
                    and toolset.startswith("mcp-")
                )
                if both_mcp:
                    logger.debug(
                        "Tool '%s': MCP toolset '%s' overwriting MCP toolset '%s'",
                        name, toolset, existing.toolset,
                    )
                else:
                    # Reject shadowing — prevent plugins/MCP from overwriting
                    # built-in tools or vice versa.
                    logger.error(
                        "Tool registration REJECTED: '%s' (toolset '%s') would "
                        "shadow existing tool from toolset '%s'. Deregister the "
                        "existing tool first if this is intentional.",
                        name, toolset, existing.toolset,
                    )
                    return
            self._tools[name] = ToolEntry(
                name=name,
                toolset=toolset,
                schema=schema,
                handler=handler,
                check_fn=check_fn,
                requires_env=requires_env or [],
                is_async=is_async,
                description=description or schema.get("description", ""),
                emoji=emoji,
                max_result_size_chars=max_result_size_chars,
            )
            if check_fn and toolset not in self._toolset_checks:
                self._toolset_checks[toolset] = check_fn

这个方法包含了几个精心设计的安全检查：

1. **工具覆盖保护** ：默认情况下，不允许一个工具集的工具覆盖另一个工具集的同名工具。这防止了意外的工具覆盖。

2. **MCP 特殊处理** ：MCP（Model Context Protocol）工具可以覆盖其他 MCP 工具。这是合理的，因为 MCP 服务器可能会刷新，或者多个 MCP 服务器可能提供同名工具。

3. **工具集检查函数缓存** ：如果工具提供了 ``check_fn`` ，并且该工具集还没有检查函数，就将这个函数缓存到 ``_toolset_checks`` 中。这是一个性能优化，避免为每个工具都运行相同的检查。

注销 API：动态工具管理
~~~~~~~~~~~~~~~~~~~~~~~~

对于动态工具系统（如 MCP），注销工具的能力也很重要：

.. code-block:: python

    def deregister(self, name: str) -> None:
        """Remove a tool from the registry."""
        with self._lock:
            entry = self._tools.pop(name, None)
            if entry is None:
                return
            # Drop the toolset check and aliases if this was the last tool in
            # that toolset.
            toolset_still_exists = any(
                e.toolset == entry.toolset for e in self._tools.values()
            )
            if not toolset_still_exists:
                self._toolset_checks.pop(entry.toolset, None)
                self._toolset_aliases = {
                    alias: target
                    for alias, target in self._toolset_aliases.items()
                    if target != entry.toolset
                }
        logger.debug("Deregistered tool: %s", name)

这个方法不仅移除工具，还会进行清理：

- 如果这是某个工具集中的最后一个工具，移除该工具集的检查函数
- 同时清理指向该工具集的别名

这确保了注册表状态的一致性。

工具注册流程图
~~~~~~~~~~~~~~~~

下面是工具注册流程的序列图：

.. mermaid::

    sequenceDiagram
        participant T as Tool Module
        participant R as ToolRegistry
        participant L as _lock
        participant TE as ToolEntry

        T->>R: register(name, toolset, schema, handler, ...)
        R->>L: acquire lock
        R->>R: check for existing tool
        alt tool exists and not MCP
            R->>R: log error, return
        else tool is new or MCP overwrite
            R->>TE: create ToolEntry(...)
            R->>R: store in _tools[name]
            alt has check_fn and toolset has no check
                R->>R: cache check_fn in _toolset_checks
            end
        end
        R->>L: release lock
        R-->>T: return

这个流程图展示了工具注册的完整过程，包括锁的获取、冲突检查、ToolEntry 创建和状态更新。

3. AST 预扫描发现机制
-----------------------

现在让我们探讨工具系统是如何发现工具的。这是一个巧妙的机制，使用 AST（抽象语法树）预扫描来避免不必要的导入。

问题：导入的成本
~~~~~~~~~~~~~~~~~~

在一个有很多工具模块的系统中，盲目导入所有模块可能会有问题：

1. **启动时间** ：每个模块导入都有成本，包括解析、执行模块级代码等
2. **依赖问题** ：某些工具模块可能有可选依赖，如果这些依赖未安装，导入会失败
3. **副作用** ：模块级代码可能有不必要的副作用

hermes-agent 的解决方案是：在实际导入之前，先使用 AST 快速扫描模块，检查它是否真的包含工具注册。

AST 扫描的实现
~~~~~~~~~~~~~~~~

让我们看看这个机制的核心代码：

.. code-block:: python

    def _is_registry_register_call(node: ast.AST) -> bool:
        """Return True when *node* is a ``registry.register(...)`` call expression."""
        if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
            return False
        func = node.value.func
        return (
            isinstance(func, ast.Attribute)
            and func.attr == "register"
            and isinstance(func.value, ast.Name)
            and func.value.id == "registry"
        )

这个函数检查一个 AST 节点是否是 ``registry.register(...)`` 调用。它不是执行代码，而是静态分析语法树。

它检查：
1. 节点是一个表达式（``ast.Expr``）
2. 表达式的值是一个函数调用（``ast.Call``）
3. 函数是一个属性访问（``ast.Attribute``）
4. 属性名是 "register"
5. 属性的值是一个名字（``ast.Name``）
6. 名字是 "registry"

这精确匹配了工具模块中的典型模式：

.. code-block:: python

    registry.register(...)  # 这会被识别

接下来，让我们看看模块级别的检查：

.. code-block:: python

    def _module_registers_tools(module_path: Path) -> bool:
        """Return True when the module contains a top-level ``registry.register(...)`` call.

        Only inspects module-body statements so that helper modules which happen
        to call ``registry.register()`` inside a function are not picked up.
        """
        try:
            source = module_path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(module_path))
        except (OSError, SyntaxError):
            return False

        return any(_is_registry_register_call(stmt) for stmt in tree.body)

这个函数：
1. 读取模块的源代码
2. 解析成 AST
3. 只检查模块顶层的语句（不是函数内部的）
4. 如果任何顶层语句是 ``registry.register(...)`` 调用，返回 True

关键是"只检查模块顶层语句"。这意味着如果一个辅助模块在函数内部调用 ``registry.register()`` ，它不会被误识别为工具模块。

发现与导入流程
~~~~~~~~~~~~~~~~

最后，让我们看看完整的发现流程：

.. code-block:: python

    def discover_builtin_tools(tools_dir: Optional[Path] = None) -> List[str]:
        """Import built-in self-registering tool modules and return their module names."""
        tools_path = Path(tools_dir) if tools_dir is not None else Path(__file__).resolve().parent
        module_names = [
            f"tools.{path.stem}"
            for path in sorted(tools_path.glob("*.py"))
            if path.name not in {"__init__.py", "registry.py", "mcp_tool.py"}
            and _module_registers_tools(path)
        ]

        imported: List[str] = []
        for mod_name in module_names:
            try:
                importlib.import_module(mod_name)
                imported.append(mod_name)
            except Exception as e:
                logger.warning("Could not import tool module %s: %s", mod_name, e)
        return imported

这个流程是：

1. 列出 tools 目录下的所有 Python 文件
2. 排除特殊文件（``__init__.py`` 、``registry.py`` 、``mcp_tool.py``）
3. 对剩余文件进行 AST 预扫描
4. 只导入通过预扫描的模块
5. 捕获并记录导入错误，但不会因为一个模块失败而停止整个流程

这种设计的优势很明显：

- **快速失败** ：没有工具注册的模块很快被跳过，不需要完整导入
- **弹性** ：有问题的工具模块不会破坏整个系统
- **精确** ：只导入真正包含工具的模块

4. 工具集系统
---------------

工具集（Toolset）是 hermes-agent 中的一个核心概念。它允许将相关工具分组，并支持灵活的组合和依赖管理。

工具集的设计目标
~~~~~~~~~~~~~~~~~~

工具集系统解决了几个重要问题：

1. **模块化配置** ：用户可以选择启用相关的工具组，而不是单独配置每个工具
2. **依赖管理** ：工具集可以包含其他工具集，形成层次结构
3. **平台适配** ：不同的平台（CLI、Telegram、Discord 等）可以有不同的默认工具集
4. **场景定制** ：特定场景（如调试、安全模式）可以有专门的工具集

让我们首先看看工具集是如何定义的：

.. code-block:: python

    # Core toolset definitions
    TOOLSETS = {
        # Basic toolsets - individual tool categories
        "web": {
            "description": "Web research and content extraction tools",
            "tools": ["web_search", "web_extract"],
            "includes": []  # No other toolsets included
        },

        "debugging": {
            "description": "Debugging and troubleshooting toolkit",
            "tools": ["terminal", "process"],
            "includes": ["web", "file"]  # Includes other toolsets
        },

        "hermes-cli": {
            "description": "Full interactive CLI toolset",
            "tools": _HERMES_CORE_TOOLS,  # 引用共享列表
            "includes": []
        },
    }

每个工具集定义包含三个部分：

1. **description** ：工具集的描述
2. **tools** ：直接包含的工具列表
3. **includes** ：包含的其他工具集列表

这种设计支持组合：一个工具集可以直接包含工具，也可以通过包含其他工具集来间接包含它们的工具。

共享工具列表
~~~~~~~~~~~~~~

你可能注意到了 ``_HERMES_CORE_TOOLS`` ，这是一个共享的工具列表：

.. code-block:: python

    # Shared tool list for CLI and all messaging platform toolsets.
    # Edit this once to update all platforms simultaneously.
    _HERMES_CORE_TOOLS = [
        # Web
        "web_search", "web_extract",
        # Terminal + process management
        "terminal", "process",
        # File manipulation
        "read_file", "write_file", "patch", "search_files",
        # ... 更多工具
    ]

这是一个避免重复的聪明设计。所有平台相关的工具集（``hermes-cli`` 、``hermes-telegram`` 、``hermes-discord`` 等）都引用这个共享列表，这样当需要添加或移除核心工具时，只需要修改一个地方。

递归解析与循环检测
~~~~~~~~~~~~~~~~~~~~

工具集解析的核心是 ``resolve_toolset()`` 函数，它递归地展开工具集定义：

.. code-block:: python

    def resolve_toolset(name: str, visited: Set[str] = None) -> List[str]:
        """Recursively resolve a toolset to get all tool names."""
        if visited is None:
            visited = set()

        # Special aliases that represent all tools across every toolset
        if name in {"all", "*"}:
            all_tools: Set[str] = set()
            for toolset_name in get_toolset_names():
                resolved = resolve_toolset(toolset_name, visited.copy())
                all_tools.update(resolved)
            return sorted(all_tools)

        # Check for cycles / already-resolved (diamond deps).
        if name in visited:
            return []

        visited.add(name)

        # Get toolset definition
        toolset = get_toolset(name)
        if not toolset:
            return []

        # Collect direct tools
        tools = set(toolset.get("tools", []))

        # Recursively resolve included toolsets
        for included_name in toolset.get("includes", []):
            included_tools = resolve_toolset(included_name, visited)
            tools.update(included_tools)

        return sorted(tools)

这个函数包含了几个关键设计：

1. **特殊别名** ：``"all"`` 或 ``"*"`` 表示所有工具集中的所有工具
2. **循环检测** ：使用 ``visited`` 集合跟踪已经处理过的工具集，防止无限递归
3. **菱形依赖处理** ：如果一个工具集已经在 ``visited`` 中，直接返回空列表。这既处理了循环，也避免了重复处理菱形依赖中的公共节点
4. **集合去重** ：使用 ``set`` 存储工具，自动处理重复

让我们详细看看循环/菱形依赖的处理。考虑这种情况：

::

    A includes B and C
    B includes D
    C includes D

这是一个菱形依赖。解析流程是：

1. resolve_toolset("A", visited={})
2.   加入 "A" → visited={"A"}
3.   收集 A 的直接工具
4.   resolve_toolset("B", visited={"A"})
5.     加入 "B" → visited={"A", "B"}
6.     收集 B 的直接工具
7.     resolve_toolset("D", visited={"A", "B"})
8.       加入 "D" → visited={"A", "B", "D"}
9.       收集 D 的直接工具
10.      返回 D 的工具
11.    更新 tools
12.    返回 B + D 的工具
13.  更新 tools
14.  resolve_toolset("C", visited={"A", "B", "D"})
15.    加入 "C" → visited={"A", "B", "D", "C"}
16.    收集 C 的直接工具
17.    resolve_toolset("D", visited={"A", "B", "D", "C"})
18.      "D" 已经在 visited 中 → 返回 []
19.    更新 tools（无变化）
20.    返回 C 的工具
21.  更新 tools
22.  返回 A + B + D + C 的工具

注意第 17-18 步：当再次解析 "D" 时，它已经在 visited 中，所以直接返回空列表。这样 D 的工具不会被重复添加，但也不会导致错误。

工具集解析流程图
~~~~~~~~~~~~~~~~~~

下面是工具集解析的流程图，特别展示了菱形依赖的处理：

.. mermaid::

    flowchart TD
        Start([开始解析]) --> CheckName{检查工具集名称}
        CheckName -->|all/*| AllTools[解析所有工具集]
        CheckName -->|其他名称| CheckVisited{是否已访问?}
        CheckVisited -->|是| ReturnEmpty[返回空列表]
        CheckVisited -->|否| AddVisited[添加到已访问集合]
        AddVisited --> GetDef[获取工具集定义]
        GetDef --> CollectDirect[收集直接工具]
        CollectDirect --> ProcessIncludes[处理包含的工具集]
        ProcessIncludes --> Recurse[递归解析每个包含的工具集]
        Recurse --> Merge[合并工具]
        Merge --> ReturnResult[返回排序后的工具列表]
        AllTools --> ReturnResult

        subgraph 菱形依赖示例
            A[工具集 A]
            B[工具集 B]
            C[工具集 C]
            D[工具集 D]

            A --> B
            A --> C
            B --> D
            C --> D
        end

这个流程图展示了工具集解析的完整过程，包括特殊别名处理、循环检测、递归解析和结果合并。

5. 参数类型强制转换
---------------------

LLM（大语言模型）在调用工具时，经常会出现类型不匹配的问题。例如，它们可能会将数字作为字符串传递（``"42"`` 而不是 ``42``），或者将布尔值作为字符串传递（``"true"`` 而不是 ``true``）。

hermes-agent 通过参数类型强制转换系统优雅地解决了这个问题。

问题的根源
~~~~~~~~~~~~

为什么会出现这个问题？有几个原因：

1. **JSON 类型限制** ：某些 LLM API 使用 JSON 格式，虽然 JSON 支持数字和布尔值，但模型有时会选择用字符串表示
2. **模型偏好** ：模型在训练数据中可能看到更多用字符串表示的数字，因此倾向于生成这种格式
3. **类型歧义** ：对于某些参数，字符串和数字都可能是合理的，模型不确定应该用哪种

hermes-agent 的解决方案不是改变模型的行为，而是在工具调用之前自动修正这些类型问题。

类型强制转换的实现
~~~~~~~~~~~~~~~~~~~~

让我们看看核心的 ``coerce_tool_args()`` 函数：

.. code-block:: python

    def coerce_tool_args(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Coerce tool call arguments to match their JSON Schema types."""
        if not args or not isinstance(args, dict):
            return args

        schema = registry.get_schema(tool_name)
        if not schema:
            return args

        properties = (schema.get("parameters") or {}).get("properties")
        if not properties:
            return args

        for key, value in args.items():
            if not isinstance(value, str):
                continue
            prop_schema = properties.get(key)
            if not prop_schema:
                continue
            expected = prop_schema.get("type")
            if not expected:
                continue
            coerced = _coerce_value(value, expected)
            if coerced is not value:
                args[key] = coerced

        return args

这个函数的工作流程是：

1. 检查参数是否存在且是字典
2. 从注册表获取工具的 JSON Schema
3. 提取参数属性定义
4. 对每个字符串类型的参数值：
   - 获取该参数的期望类型
   - 尝试强制转换
   - 如果转换成功且结果不同，更新参数字典

注意它只尝试转换字符串类型的值。这是合理的：如果值已经是数字或布尔值，就不需要转换。

值转换逻辑
~~~~~~~~~~~~

实际的转换逻辑在 ``_coerce_value()`` 中：

.. code-block:: python

    def _coerce_value(value: str, expected_type):
        """Attempt to coerce a string *value* to *expected_type*."""
        if isinstance(expected_type, list):
            # Union type — try each in order, return first successful coercion
            for t in expected_type:
                result = _coerce_value(value, t)
                if result is not value:
                    return result
            return value

        if expected_type in ("integer", "number"):
            return _coerce_number(value, integer_only=(expected_type == "integer"))
        if expected_type == "boolean":
            return _coerce_boolean(value)
        return value

这个函数处理了几种情况：

1. **联合类型** ：如果 ``expected_type`` 是一个列表（如 ``["integer", "string"]``），它会依次尝试每种类型，返回第一个成功的转换
2. **数字类型** ：委托给 ``_coerce_number()``
3. **布尔类型** ：委托给 ``_coerce_boolean()``
4. **其他类型** ：返回原值，不进行转换

联合类型的处理特别聪明。JSON Schema 允许参数是多种类型之一（如既可以是字符串也可以是数字）。这个函数会按照类型列表的顺序尝试转换，返回第一个成功的结果。

数字转换
~~~~~~~~~~

让我们看看数字转换的实现：

.. code-block:: python

    def _coerce_number(value: str, integer_only: bool = False):
        """Try to parse *value* as a number.  Returns original string on failure."""
        try:
            f = float(value)
        except (ValueError, OverflowError):
            return value
        # Guard against inf/nan before int() conversion
        if f != f or f == float("inf") or f == float("-inf"):
            return f
        # If it looks like an integer (no fractional part), return int
        if f == int(f):
            return int(f)
        if integer_only:
            # Schema wants an integer but value has decimals — keep as string
            return value
        return f

这个函数有几个精心设计的细节：

1. **先尝试浮点数** ：所有整数也是有效的浮点数，所以先尝试解析为浮点数
2. **特殊值处理** ：检查 NaN（``f != f``）和无穷大，如果是这些特殊值，返回浮点数形式
3. **整数优化** ：如果浮点值实际上是整数（如 ``42.0``），返回整数形式
4. **整数模式** ：如果 ``integer_only=True`` 但值有小数部分，返回原字符串（不进行转换）

最后一点很重要。如果工具期望整数但模型传递了 ``"42.5"`` ，我们不会静默地截断为 42，而是保持原样，让工具处理这个类型不匹配的问题。

布尔转换
~~~~~~~~~~

布尔转换相对简单：

.. code-block:: python

    def _coerce_boolean(value: str):
        """Try to parse *value* as a boolean.  Returns original string on failure."""
        low = value.strip().lower()
        if low == "true":
            return True
        if low == "false":
            return False
        return value

它只识别 "true" 和 "false"（不区分大小写，忽略前后空白）。如果是其他值，返回原字符串。

为什么不识别更多的值（如 "yes"、"no"、"1"、"0"）？这是一个有意的设计决策，保持转换逻辑简单且可预测，避免误转换。

6. 执行调度
-------------

现在我们来到了工具系统的核心：执行调度。这是将工具调用从 API 请求转换为实际执行的关键环节。

调度流程总览
~~~~~~~~~~~~~~

让我们首先看看 ``handle_function_call()`` ，这是工具调度的主要入口点：

.. code-block:: python

    def handle_function_call(
        function_name: str,
        function_args: Dict[str, Any],
        task_id: Optional[str] = None,
        tool_call_id: Optional[str] = None,
        session_id: Optional[str] = None,
        user_task: Optional[str] = None,
        enabled_tools: Optional[List[str]] = None,
        skip_pre_tool_call_hook: bool = False,
    ) -> str:
        """Main function call dispatcher that routes calls to the tool registry."""
        # Coerce string arguments to their schema-declared types (e.g. "42"→42)
        function_args = coerce_tool_args(function_name, function_args)

        try:
            if function_name in _AGENT_LOOP_TOOLS:
                return json.dumps({"error": f"{function_name} must be handled by the agent loop"})

            # Check plugin hooks for a block directive
            if not skip_pre_tool_call_hook:
                block_message: Optional[str] = None
                try:
                    from hermes_cli.plugins import get_pre_tool_call_block_message
                    block_message = get_pre_tool_call_block_message(
                        function_name,
                        function_args,
                        task_id=task_id or "",
                        session_id=session_id or "",
                        tool_call_id=tool_call_id or "",
                    )
                except Exception:
                    pass

                if block_message is not None:
                    return json.dumps({"error": block_message}, ensure_ascii=False)
            else:
                # Still fire the hook for observers — just don't check for blocking
                try:
                    from hermes_cli.plugins import invoke_hook
                    invoke_hook(
                        "pre_tool_call",
                        tool_name=function_name,
                        args=function_args,
                        task_id=task_id or "",
                        session_id=session_id or "",
                        tool_call_id=tool_call_id or "",
                    )
                except Exception:
                    pass

            # Notify the read-loop tracker
            if function_name not in _READ_SEARCH_TOOLS:
                try:
                    from tools.file_tools import notify_other_tool_call
                    notify_other_tool_call(task_id or "default")
                except Exception:
                    pass

            # Dispatch to the registry
            if function_name == "execute_code":
                sandbox_enabled = enabled_tools if enabled_tools is not None else _last_resolved_tool_names
                result = registry.dispatch(
                    function_name, function_args,
                    task_id=task_id,
                    enabled_tools=sandbox_enabled,
                )
            else:
                result = registry.dispatch(
                    function_name, function_args,
                    task_id=task_id,
                    user_task=user_task,
                )

            # Post-tool call hook
            try:
                from hermes_cli.plugins import invoke_hook
                invoke_hook(
                    "post_tool_call",
                    tool_name=function_name,
                    args=function_args,
                    result=result,
                    task_id=task_id or "",
                    session_id=session_id or "",
                    tool_call_id=tool_call_id or "",
                )
            except Exception:
                pass

            return result

        except Exception as e:
            error_msg = f"Error executing {function_name}: {str(e)}"
            logger.error(error_msg)
            return json.dumps({"error": error_msg}, ensure_ascii=False)

这个函数包含了完整的调度流程：

1. **参数强制转换** ：首先调用 ``coerce_tool_args()`` 修正类型问题
2. **Agent Loop 工具检查** ：某些工具必须由 Agent Loop 处理，拒绝在这里调度
3. **前置钩子检查** ：检查插件是否要阻止这个工具调用
4. **读取循环通知** ：如果不是读取/搜索工具，通知读取循环追踪器
5. **实际调度** ：调用 ``registry.dispatch()`` 执行工具
6. **后置钩子** ：调用后置钩子
7. **异常处理** ：捕获所有异常，返回格式化的错误

让我们逐一分析这些步骤。

Agent Loop 拦截
~~~~~~~~~~~~~~~~~

你可能注意到了 ``_AGENT_LOOP_TOOLS`` ：

.. code-block:: python

    # Tools whose execution is intercepted by the agent loop (run_agent.py)
    # because they need agent-level state (TodoStore, MemoryStore, etc.).
    _AGENT_LOOP_TOOLS = {"todo", "memory", "session_search", "delegate_task"}
    _READ_SEARCH_TOOLS = {"read_file", "search_files"}

这些工具为什么需要特殊处理？因为它们需要访问 Agent 级别的状态：

- ``todo`` ：需要访问 TodoStore 来管理任务
- ``memory`` ：需要访问 MemoryStore 来读写持久化记忆
- ``session_search`` ：需要访问会话历史
- ``delegate_task`` ：需要创建子 Agent

这些状态在工具注册级别不可用，所以必须由 Agent Loop 直接处理。如果这些工具到达了 ``handle_function_call()`` ，说明有什么地方出错了，所以返回一个错误。

钩子系统
~~~~~~~~~~

hermes-agent 有一个灵活的钩子系统，允许插件观察和干预工具执行。

前置钩子有两种模式：

1. **阻塞模式** ：调用 ``get_pre_tool_call_block_message()`` ，如果返回消息，就用这个消息作为错误返回，阻止工具执行
2. **观察模式** ：调用 ``invoke_hook("pre_tool_call", ...)`` ，仅用于观察，不阻止执行

这种设计允许插件：

- **安全检查** ：在工具执行前检查是否允许
- **审计** ：记录所有工具调用
- **监控** ：跟踪工具使用统计

后置钩子只有观察模式，用于在工具执行后进行清理、记录或通知。

注册表调度
~~~~~~~~~~~~

实际的工具执行在 ``registry.dispatch()`` 中：

.. code-block:: python

    def dispatch(self, name: str, args: dict, **kwargs) -> str:
        """Execute a tool handler by name."""
        entry = self.get_entry(name)
        if not entry:
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            if entry.is_async:
                from model_tools import _run_async
                return _run_async(entry.handler(args, **kwargs))
            return entry.handler(args, **kwargs)
        except Exception as e:
            logger.exception("Tool %s dispatch error: %s", name, e)
            return json.dumps({"error": f"Tool execution failed: {type(e).__name__}: {e}"})

这个函数：

1. 获取工具的 ``ToolEntry``
2. 如果工具不存在，返回错误
3. 如果工具是异步的，使用 ``_run_async()`` 桥接
4. 否则直接调用处理器
5. 捕获所有异常，返回格式化的错误

注意所有异常都被捕获并转换为 JSON 格式的错误消息。这确保了工具执行永远不会导致整个系统崩溃，错误总是能被传递回 LLM。

工具调度流程图
~~~~~~~~~~~~~~~~

下面是工具调度流程的完整流程图：

.. mermaid::

   flowchart TD
       Start([Tool call request]) --> Coerce[coerce_tool_args type conversion]
       Coerce --> CheckAgent{Agent Loop tool?}
       CheckAgent -->|Yes| ReturnError[Return error: must be handled by agent loop]
       CheckAgent -->|No| CheckPreHook{Pre hook check}
       CheckPreHook -->|Blocked| ReturnBlocked[Return block message]
       CheckPreHook -->|Allowed| FirePreHook[Fire observer pre hook]
       FirePreHook --> CheckRead{Is read/search tool?}
       CheckRead -->|No| NotifyRead[Notify read cycle tracker]
       CheckRead -->|Yes| Dispatch[registry.dispatch]
       NotifyRead --> Dispatch
       Dispatch --> CheckAsync{Async tool?}
       CheckAsync -->|Yes| RunAsync[_run_async bridge]
       CheckAsync -->|No| CallSync[Direct sync handler call]
       RunAsync --> FirePostHook[Fire post hook]
       CallSync --> FirePostHook
       FirePostHook --> ReturnResult[Return result]
       ReturnError --> End([End])
       ReturnBlocked --> End
       ReturnResult --> End

这个流程图展示了从接收到工具调用请求到返回结果的完整处理流程，包括类型转换、钩子检查、调度决策和异常处理。

7. Agent Loop 拦截
--------------------

我们已经简要提到了 Agent Loop 拦截，但这个机制值得更深入的讨论。

为什么需要拦截？
~~~~~~~~~~~~~~~~~~

某些工具需要访问 Agent 级别的状态，这些状态在工具注册表中不可用。让我们看看这些工具的特殊需求：

1. **todo** ：需要访问 TodoStore，这是一个管理待办任务的状态存储
2. **memory** ：需要访问 MemoryStore，这是一个跨会话的持久化存储
3. **session_search** ：需要访问完整的会话历史记录
4. **delegate_task** ：需要创建新的子 Agent 实例

这些状态和功能都属于 Agent 本身，而不是工具系统。将它们的处理放在 Agent Loop 中是一个合理的架构决策。

拦截的工作原理
~~~~~~~~~~~~~~~~

在 Agent Loop（通常在 ``run_agent.py`` 中）中，工具调用会先经过一个检查：

.. code-block:: python

    # 伪代码，说明 Agent Loop 中的逻辑
    def process_tool_call(tool_name, tool_args):
        if tool_name in _AGENT_LOOP_TOOLS:
            # 直接在 Agent Loop 中处理
            if tool_name == "todo":
                return handle_todo(tool_args)
            elif tool_name == "memory":
                return handle_memory(tool_args)
            # ... 其他工具
        else:
            # 转发给 model_tools.handle_function_call()
            return handle_function_call(tool_name, tool_args, ...)

这样，需要 Agent 状态的工具直接在 Agent Loop 中处理，而其他工具则通过正常的调度管道。

注册表中的占位符
~~~~~~~~~~~~~~~~~~

虽然这些工具由 Agent Loop 处理，但它们的 schema 仍然在注册表中：

.. code-block:: python

    # 在某个工具模块中
    registry.register(
        name="todo",
        toolset="todo",
        schema=todo_schema,  # 完整的 JSON Schema
        handler=lambda args: json.dumps({"error": "todo must be handled by agent loop"}),
        # ...
    )

这很重要，因为：

1. **工具发现** ：这些工具需要出现在可用工具列表中，这样 LLM 才知道它们存在
2. **Schema 验证** ：LLM 需要知道这些工具的参数格式
3. **安全网** ：如果由于某种原因这些工具到达了调度器，会返回一个清晰的错误

8. 结果持久化与预算
---------------------

工具执行可能会产生大量输出，如果不加以控制，可能会耗尽上下文窗口或产生过高的成本。hermes-agent 实现了一个三层防御机制来管理工具输出。

三层防御策略
~~~~~~~~~~~~~~

hermes-agent 对工具结果采用三层防御策略：

1. **工具级截断** ：每个工具可以指定自己的最大结果大小
2. **单结果持久化** ：如果结果仍然太大，持久化到磁盘，只返回摘要
3. **轮次预算** ：限制每轮对话中工具结果的总大小

让我们看看这些机制是如何实现的。

工具级最大结果大小
~~~~~~~~~~~~~~~~~~~~

首先，每个工具可以在注册时指定最大结果大小：

.. code-block:: python

    registry.register(
        name="some_tool",
        # ...
        max_result_size_chars=10000,  # 10,000 字符限制
    )

如果没有指定，使用默认值：

.. code-block:: python

    def get_max_result_size(self, name: str, default: int | float | None = None) -> int | float:
        """Return per-tool max result size, or *default* (or global default)."""
        entry = self.get_entry(name)
        if entry and entry.max_result_size_chars is not None:
            return entry.max_result_size_chars
        if default is not None:
            return default
        from tools.budget_config import DEFAULT_RESULT_SIZE_CHARS
        return DEFAULT_RESULT_SIZE_CHARS

截断逻辑通常在工具处理器内部实现，或者在一个通用的包装器中。

结果持久化
~~~~~~~~~~~~

对于特别大的结果，hermes-agent 可以将结果持久化到磁盘，只返回一个摘要和访问路径。这通常在工具处理器中实现：

.. code-block:: python

    # 伪代码，说明结果持久化模式
    def tool_handler(args):
        result = compute_large_result()
        result_str = json.dumps(result)

        if len(result_str) > MAX_RESULT_SIZE:
            # 持久化到磁盘
            path = save_to_temporary_file(result_str)
            return tool_result({
                "summary": f"Result too large, saved to {path}",
                "path": path,
                "truncated": True
            })
        else:
            return tool_result(result)

这样，LLM 知道结果已经保存，可以使用文件工具读取它，而不会在上下文中消耗过多 token。

轮次预算
~~~~~~~~~~

最后，hermes-agent 还实现了轮次预算机制，限制每轮对话中工具结果的总大小。这通常在 Agent Loop 中实现，跟踪工具结果的累积大小，当接近限制时采取行动。

9. 并行执行引擎
-----------------

现代 LLM 支持在单个响应中调用多个工具，hermes-agent 的并行执行引擎可以智能地决定哪些工具可以并行执行，哪些必须顺序执行。

并行执行的好处
~~~~~~~~~~~~~~~~

并行工具有几个重要好处：

1. **降低延迟** ：多个工具可以同时执行，总延迟是最长的那个，而不是总和
2. **提高效率** ：充分利用系统资源
3. **改善用户体验** ：用户更快看到结果

但不是所有工具都可以安全地并行执行。hermes-agent 根据工具的特性将它们分类。

工具分类
~~~~~~~~~~

hermes-agent 将工具分为三类：

1. **NEVER_PARALLEL** ：永远不能并行执行的工具
2. **PARALLEL_SAFE** ：完全可以并行执行的工具
3. **PATH_SCOPED** ：可以并行，但需要考虑路径范围的工具

让我们看看这个决策逻辑（通常在并行执行管理器中）：

.. code-block:: python

    # 伪代码，说明并行分类
    NEVER_PARALLEL = {"terminal", "execute_code", "delegate_task", ...}
    PARALLEL_SAFE = {"web_search", "web_extract", "read_file", ...}
    PATH_SCOPED = {"write_file", "patch", ...}

    def _should_parallelize_tool_batch(tool_calls):
        """决定一批工具调用是否可以并行执行"""
        # 检查是否有 NEVER_PARALLEL 工具
        for call in tool_calls:
            if call.name in NEVER_PARALLEL:
                return False

        # 检查 PATH_SCOPED 工具是否有路径冲突
        path_tools = [call for call in tool_calls if call.name in PATH_SCOPED]
        if path_tools:
            # 检查是否有多个工具操作相同的路径
            paths = set()
            for call in path_tools:
                path = call.args.get("path")
                if path in paths:
                    return False  # 路径冲突，不能并行
                paths.add(path)

        return True

这个逻辑考虑了几个因素：

1. **危险工具** ：如 ``terminal`` 、``execute_code`` 等，它们的执行可能有副作用，或者相互影响
2. **路径冲突** ：对于写文件等工具，如果多个工具操作相同的路径，需要顺序执行以避免竞争条件

并行决策流程图
~~~~~~~~~~~~~~~~

下面是并行执行决策的流程图：

.. mermaid::

    flowchart TD
        Start([一批工具调用]) --> CheckNever{包含NEVER_PARALLEL工具?}
        CheckNever -->|是| NoParallel[顺序执行]
        CheckNever -->|否| CheckPathScoped{包含PATH_SCOPED工具?}
        CheckPathScoped -->|否| YesParallel[并行执行]
        CheckPathScoped -->|是| CollectPaths[收集所有操作路径]
        CollectPaths --> CheckConflict{路径冲突?}
        CheckConflict -->|是| NoParallel
        CheckConflict -->|否| YesParallel
        YesParallel --> End([执行])
        NoParallel --> End

这个流程图展示了决定一批工具调用是否可以并行执行的决策过程。

10. 异步桥接
--------------

最后，让我们探讨 hermes-agent 的异步桥接机制，这是一个将异步工具处理器集成到同步代码路径中的优雅解决方案。

为什么需要异步桥接？
~~~~~~~~~~~~~~~~~~~~~~

现代 Python 库越来越多地使用 async/await 模式，特别是对于 I/O 密集型操作（如 HTTP 请求、数据库查询等）。但是：

1. **Agent Loop 是同步的** ：主要的调度逻辑通常是同步的
2. **向后兼容** ：不是所有工具都需要或应该是异步的
3. **线程安全** ：异步代码和多线程需要小心协调

hermes-agent 的解决方案是提供一个同步桥接层，让异步工具可以在同步环境中无缝运行。

持久化事件循环
~~~~~~~~~~~~~~~~

异步桥接的一个关键组件是持久化事件循环。让我们看看：

.. code-block:: python

    _tool_loop = None          # persistent loop for the main (CLI) thread
    _tool_loop_lock = threading.Lock()
    _worker_thread_local = threading.local()  # per-worker-thread persistent loops

    def _get_tool_loop():
        """Return a long-lived event loop for running async tool handlers."""
        global _tool_loop
        with _tool_loop_lock:
            if _tool_loop is None or _tool_loop.is_closed():
                _tool_loop = asyncio.new_event_loop()
            return _tool_loop

    def _get_worker_loop():
        """Return a persistent event loop for the current worker thread."""
        loop = getattr(_worker_thread_local, 'loop', None)
        if loop is None or loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            _worker_thread_local.loop = loop
        return loop

这里有两个不同的循环获取器：

1. **_get_tool_loop()** ：为主线程提供一个单例的持久化循环
2. **_get_worker_loop()** ：为每个工作线程提供独立的持久化循环，使用线程本地存储

为什么不使用 ``asyncio.run()``？因为 ``asyncio.run()`` 每次都会创建一个新的事件循环，运行完协程后关闭它。这会导致问题：

- **资源泄漏** ：异步客户端（如 httpx、AsyncOpenAI）可能缓存连接，这些连接绑定到事件循环
- **关闭错误** ：当这些客户端尝试在已关闭的循环上清理资源时，会抛出 "Event loop is closed" 错误

通过使用持久化循环，这些客户端保持绑定到一个活跃的循环，避免了这些问题。

_run_async()：统一的桥接
~~~~~~~~~~~~~~~~~~~~~~~~~~

现在让我们看看核心的 ``_run_async()`` 函数：

.. code-block:: python

    def _run_async(coro):
        """Run an async coroutine from a sync context."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Inside an async context (gateway, RL env) — run in a fresh thread.
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result(timeout=300)

        # If we're on a worker thread, use a per-thread persistent loop.
        if threading.current_thread() is not threading.main_thread():
            worker_loop = _get_worker_loop()
            return worker_loop.run_until_complete(coro)

        tool_loop = _get_tool_loop()
        return tool_loop.run_until_complete(coro)

这个函数处理了三种场景：

1. **已有运行中的循环** ：如果当前已经有一个活跃的事件循环（如在网关或 RL 环境中），它在一个新线程中运行协程
2. **工作线程** ：如果在工作线程（如并行执行的线程）中，使用该线程的持久化循环
3. **主线程** ：否则，使用主线程的持久化循环

第一种场景特别值得注意。当已经有一个活跃的事件循环时，我们不能直接在那个循环中运行另一个 ``run_until_complete()`` ，这会导致嵌套事件循环错误。解决方案是在一个新线程中运行，这样新线程可以有自己的事件循环。

这个函数是 hermes-agent 中同步→异步桥接的单一真实来源，所有异步工具都通过它运行。这确保了一致性，避免了重复代码。

总结
------

在本章中，我们深入探讨了 hermes-agent 的工具系统，从自注册模式、线程安全注册表、AST 预扫描、工具集组合、参数类型强制转换、调度执行、Agent Loop 拦截、预算控制、并行执行到异步桥接。

这个系统的设计体现了几个重要原则：

1. **关注点分离** ：每个组件都有清晰的职责
2. **弹性** ：系统能够优雅地处理错误和边界情况
3. **性能** ：通过快照、缓存、持久化循环等优化
4. **可扩展性** ：新工具可以轻松添加，工具集可以灵活组合
5. **线程安全** ：多线程环境下的安全访问

理解这个系统不仅有助于使用 hermes-agent，也能为设计其他 AI Agent 框架提供参考。
