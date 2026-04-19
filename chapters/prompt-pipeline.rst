提示工程管线：如何组装一个完美的 System Prompt
==================================================

在本章中，我们将深入探讨 hermes-agent 的提示工程管线 —— 这是一个精心设计的 9 槽位管道，负责从身份定义、平台适配、环境感知、记忆指导到上下文文件注入的完整系统提示组装过程。

System Prompt 是 AI Agent 行为的核心控制器。一个设计良好的系统提示可以让 Agent 准确理解自己的角色、能力和限制，从而更可靠地执行任务。hermes-agent 的提示管线不仅考虑了功能性，还考虑了安全性（注入防御）、性能（缓存策略）和成本（Anthropic 缓存优化）。

1. 提示工程的挑战
-------------------

为什么 System Prompt 如此重要？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 AI Agent 架构中，System Prompt 是一个关键的接口层，它在模型推理之前定义了 Agent 的行为规范。一个设计不当的 System Prompt 可能导致：

1. **角色混乱** ：Agent 不知道自己是谁，行为不一致
2. **工具误用** ：Agent 不了解工具的正确使用方式
3. **平台不兼容** ：在 Markdown 不支持的平台使用 Markdown 格式
4. **上下文浪费** ：包含无关信息，浪费宝贵的 token 空间
5. **安全漏洞** ：缺乏注入防御，可能被恶意利用

hermes-agent 的提示管线通过分层设计、动态适配和缓存策略来解决这些问题。

提示工程的核心矛盾
~~~~~~~~~~~~~~~~~~~~

提示工程面临几个核心矛盾：

1. **完整性 vs 简洁性** ：提示需要足够完整以指导行为，但又不能太长以至于浪费 token 或分散注意力
2. **通用性 vs 特异性** ：提示需要在所有场景下都有用，但又需要针对特定场景提供专门指导
3. **稳定性 vs 动态性** ：某些指导应该稳定不变，而另一些需要根据运行时环境动态调整
4. **安全性 vs 可用性** ：安全检查可以防止注入攻击，但过于严格的检查可能误杀正常内容

hermes-agent 通过 9 槽位管道设计来解决这些矛盾，每个槽位负责一个特定的关注点，组合起来形成完整的系统提示。

2. 提示组装管线总览
---------------------

hermes-agent 的系统提示由 9 个独立的"槽位"组成，每个槽位负责一个特定方面。这种设计使得每个部分可以独立开发和测试。

9 槽位管道概览
~~~~~~~~~~~~~~~~

让我们首先看看这 9 个槽位的概览：

1. **Agent 身份层** ：来自 SOUL.md，定义 Agent 的个性和身份
2. **平台适配层** ：根据运行平台提供格式和行为指导
3. **环境感知层** ：检测运行环境（WSL、Docker 等）
4. **工具使用指导** ：指导 Agent 如何使用工具
5. **记忆与搜索指导** ：MEMORY_GUIDANCE 和 SESSION_SEARCH_GUIDANCE
6. **模型特定执行规范** ：针对不同模型的专门指导
7. **技能索引系统** ：列出可用的技能及其描述
8. **上下文文件** ：从 .hermes.md、AGENTS.md 等加载的项目上下文
9. **Anthropic 缓存标记** ：为 Anthropic 模型注入缓存控制

提示组装管线流程图
~~~~~~~~~~~~~~~~~~~~

下面是提示组装管线的完整流程图：

.. mermaid::

    flowchart TD
        Start([Start building system prompt]) --> Slot1

        subgraph S1[Slot 1: Agent Identity]
            Slot1[Load SOUL.md] --> Slot1Check{SOUL.md exists?}
            Slot1Check -->|Yes| Slot1Use[Use SOUL.md content]
            Slot1Check -->|No| Slot1Default[Use DEFAULT_AGENT_IDENTITY]
        end

        Slot1Use --> Slot2
        Slot1Default --> Slot2

        subgraph S2[Slot 2: Platform Hints]
            Slot2[Query current platform] --> Slot2Hint{Match found?}
            Slot2Hint -->|Yes| Slot2Add[Add PLATFORM_HINTS]
            Slot2Hint -->|No| Slot2Skip[Skip]
        end

        Slot2Add --> Slot3
        Slot2Skip --> Slot3

        subgraph S3[Slot 3: Environment]
            Slot3[Detect runtime env] --> Slot3Env{WSL or Termux?}
            Slot3Env -->|Yes| Slot3Hint[Add env hints]
            Slot3Env -->|No| Slot3None[No special hints]
        end

        Slot3Hint --> Slot4
        Slot3None --> Slot4

        subgraph S4[Slot 4-6: Guidance Layer]
            Slot4[Tool use guidance] --> Slot5[Memory and search guidance]
            Slot5 --> Slot6[Model-specific rules]
        end

        Slot6 --> Slot7

        subgraph S7[Slot 7: Skills Index]
            Slot7[Query skill cache] --> Slot7Cache{Cache hit?}
            Slot7Cache -->|Yes| Slot7Use[Use cache]
            Slot7Cache -->|No| Slot7Build[Scan and build index]
        end

        Slot7Use --> Slot8
        Slot7Build --> Slot8

        subgraph S8[Slot 8: Context Files]
            Slot8[Search context files] --> Slot8Priority{Load by priority}
            Slot8Priority --> Slot8Hermes[".hermes.md"]
            Slot8Hermes --> Slot8Agents[AGENTS.md]
            Slot8Agents --> Slot8Claude[CLAUDE.md]
            Slot8Claude --> Slot8Cursor[".cursorrules"]
        end

        Slot8 --> Slot9

        subgraph S9[Slot 9: Cache Optimization]
            Slot9[Inject cache markers] --> Slot9Anthropic{Anthropic model?}
            Slot9Anthropic -->|Yes| Slot9Cache[Add cache_control]
            Slot9Anthropic -->|No| Slot9Skip[Skip]
        end

        Slot9Cache --> Final[Merge all slots]
        Slot9Skip --> Final
        Final --> End([Return complete system prompt])

每个槽位的输出都是一个字符串片段，最终这些片段会被合并成一个完整的系统提示。

3. Agent 身份层 (SOUL.md)
---------------------------

Agent 的身份定义是系统提示的第一个组成部分，它决定了 Agent 的基本行为方式和个性。

身份的定义
~~~~~~~~~~~~

hermes-agent 的默认身份定义如下：

.. code-block:: python

    DEFAULT_AGENT_IDENTITY = (
        "You are Hermes Agent, an intelligent AI assistant created by Nous Research. "
        "You are helpful, knowledgeable, and direct. You assist users with a wide "
        "range of tasks including answering questions, writing and editing code, "
        "analyzing information, creative work, and executing actions via your tools. "
        "You communicate clearly, admit uncertainty when appropriate, and prioritize "
        "being genuinely useful over being verbose unless otherwise directed below. "
        "Be targeted and efficient in your exploration and investigations."
    )

这段话定义了几个关键特性：

1. **名称** ：Hermes Agent
2. **创建者** ：Nous Research
3. **核心特质** ：有帮助的、知识渊博的、直接的
4. **能力范围** ：问答、代码编写/编辑、信息分析、创意工作、工具执行
5. **沟通风格** ：清晰、诚实、高效
6. **行为准则** ：优先实际有用，避免冗余

自定义身份：SOUL.md
~~~~~~~~~~~~~~~~~~~~~

用户可以通过创建 ``SOUL.md`` 文件来自定义 Agent 的身份：

.. code-block:: python

    def load_soul_md() -> Optional[str]:
        """Load SOUL.md from HERMES_HOME and return its content, or None."""
        try:
            from hermes_cli.config import ensure_hermes_home
            ensure_hermes_home()
        except Exception as e:
            logger.debug("Could not ensure HERMES_HOME before loading SOUL.md: %s", e)

        soul_path = get_hermes_home() / "SOUL.md"
        if not soul_path.exists():
            return None
        try:
            content = soul_path.read_text(encoding="utf-8").strip()
            if not content:
                return None
            content = _scan_context_content(content, "SOUL.md")
            content = _truncate_content(content, "SOUL.md")
            return content
        except Exception as e:
            logger.debug("Could not read SOUL.md from %s: %s", soul_path, e)
            return None

SOUL.md 的加载流程包括几个重要步骤：

1. **确保目录存在** ：调用 ``ensure_hermes_home()`` 确保 HERMES_HOME 目录已创建
2. **路径定位** ：在 ``~/.hermes/SOUL.md`` 中查找
3. **注入扫描** ：通过 ``_scan_context_content()`` 检查潜在的注入攻击
4. **大小限制** ：通过 ``_truncate_content()`` 确保内容不会过大

SOUL.md 的设计理念是"用户即设计师"——用户可以完全控制 Agent 的个性。例如：

- 技术支持团队可以定义一个专业、精确的 Agent 身份
- 创意团队可以定义一个更有想象力、更富有表现力的 Agent
- 教育场景可以定义一个耐心的、善于引导的 Agent

4. 平台适配层
---------------

不同的消息平台有不同的特性：有的支持 Markdown，有的不支持；有的可以发送文件，有的只能发文本。hermes-agent 通过平台适配层来处理这些差异。

14 个平台提示
~~~~~~~~~~~~~~~

hermes-agent 目前支持 14 个平台的提示适配。让我们看看这些平台：

.. code-block:: python

    PLATFORM_HINTS = {
        "whatsapp": (
            "You are on a text messaging communication platform, WhatsApp. "
            "Please do not use markdown as it does not render. "
            "You can send media files natively: to deliver a file to the user, "
            "include MEDIA:/absolute/path/to/file in your response. ..."
        ),
        "telegram": (
            "You are on a text messaging communication platform, Telegram. "
            "Standard markdown is automatically converted to Telegram format. ..."
        ),
        "discord": (
            "You are in a Discord server or group chat communicating with your user. ..."
        ),
        "slack": (...),
        "signal": (...),
        "email": (...),
        "cron": (...),
        "cli": (...),
        "sms": (...),
        "bluebubbles": (...),
        "weixin": (...),
        "wecom": (...),
        "qqbot": (...),
        # ... 更多平台
    }

每个平台提示包含几个方面的信息：

1. **平台描述** ：告诉 Agent 它运行在什么平台上
2. **格式规则** ：是否支持 Markdown，应该使用什么格式
3. **媒体能力** ：如何发送文件、图片、音频等
4. **特殊规则** ：该平台特有的行为约束

平台适配的关键考量
~~~~~~~~~~~~~~~~~~~~

让我们看看一些平台的特殊考虑：

**WhatsApp / SMS / BlueBubbles**

这些平台不支持 Markdown，所以提示明确告诉 Agent 不要使用 Markdown：

::

    "Please do not use markdown as it does not render."

**Telegram**

Telegram 支持 Markdown 的一个子集，提示列出了具体支持的格式：

::

    "Supported: **bold**, *italic*, ~~strikethrough~~, ||spoiler||,
    `inline code`, ```code blocks```, [links](url), and ## headers."

**Email**

邮件有特殊的格式要求：

::

    "Write clear, well-structured responses suitable for email.
    Use plain text formatting (no markdown). Keep responses concise
    but complete."

**Cron**

定时任务没有用户参与，需要完全自主执行：

::

    "You are running as a scheduled cron job. There is no user present —
    you cannot ask questions, request clarification, or wait for follow-up.
    Execute the task fully and autonomously."

**WeCom (企业微信)**

企业微信支持 Markdown，并强调文件发送能力：

::

    "Do NOT tell the user you lack file-sending capability — use MEDIA:
    syntax whenever a file delivery is appropriate."

这条规则特别有趣——它不仅描述了能力，还明确防止 Agent 自我否定。这是因为有些模型可能会因为不确定而拒绝执行操作。

媒体发送机制
~~~~~~~~~~~~~~

所有支持媒体发送的平台使用统一的 ``MEDIA:`` 语法：

::

    MEDIA:/absolute/path/to/file

这个约定让 Agent 知道如何请求发送文件，而具体的发送逻辑由平台适配层处理。

5. 环境感知层
---------------

除了消息平台之外，Agent 还需要知道它运行在什么计算环境中。hermes-agent 通过环境感知层来提供这些信息。

WSL 检测
~~~~~~~~~~

Windows Subsystem for Linux (WSL) 是一个常见的特殊环境：

.. code-block:: python

    WSL_ENVIRONMENT_HINT = (
        "You are running inside WSL (Windows Subsystem for Linux). "
        "The Windows host filesystem is mounted under /mnt/ — "
        "/mnt/c/ is the C: drive, /mnt/d/ is D:, etc. "
        "The user's Windows files are typically at "
        "/mnt/c/Users/<username>/Desktop/, Documents/, Downloads/, etc. "
        "When the user references Windows paths or desktop files, translate "
        "to the /mnt/c/ equivalent. You can list /mnt/c/Users/ to discover "
        "the Windows username if needed."
    )

这个提示告诉 Agent：

1. 它运行在 WSL 中
2. Windows 文件系统的挂载点
3. 用户文件的典型位置
4. 如何处理 Windows 路径引用

这很重要，因为 WSL 用户可能使用 Windows 风格的路径（如 ``C:\Users\...``），而 Agent 需要知道如何将这些转换为 Linux 路径。

环境检测函数
~~~~~~~~~~~~~~

.. code-block:: python

    def build_environment_hints() -> str:
        """Return environment-specific guidance for the system prompt.

        Detects WSL, and can be extended for Termux, Docker, etc.
        Returns an empty string when no special environment is detected.
        """
        hints: list[str] = []
        if is_wsl():
            hints.append(WSL_ENVIRONMENT_HINT)
        return "\n\n".join(hints)

这个函数设计为可扩展的：未来可以添加 Termux、Docker 等其他环境的检测。

6. 记忆与搜索指导
-------------------

hermes-agent 的记忆系统允许 Agent 跨会话持久化信息，搜索指导则告诉 Agent 何时应该查找历史对话。

记忆指导 (MEMORY_GUIDANCE)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    MEMORY_GUIDANCE = (
        "You have persistent memory across sessions. Save durable facts using the memory "
        "tool: user preferences, environment details, tool quirks, and stable conventions. "
        "Memory is injected into every turn, so keep it compact and focused on facts that "
        "will still matter later.\n"
        "Prioritize what reduces future user steering — the most valuable memory is one "
        "that prevents the user from having to correct or remind you again. "
        "User preferences and recurring corrections matter more than procedural task details.\n"
        "Do NOT save task progress, session outcomes, completed-work logs, or temporary TODO "
        "state to memory; use session_search to recall those from past transcripts. "
        "If you've discovered a new way to do something, solved a problem that could be "
        "necessary later, save it as a skill with the skill tool."
    )

这段指导包含了几个重要原则：

1. **什么应该保存** ：用户偏好、环境细节、工具特性、稳定约定
2. **什么不应该保存** ：任务进度、会话结果、已完成的工作日志、临时 TODO
3. **格式要求** ：保持紧凑，因为记忆会在每轮对话中注入
4. **价值优先级** ：能减少用户纠正的记忆最有价值
5. **替代方案** ：任务相关的历史应该用 session_search 而不是记忆

这些指导帮助 Agent 做出明智的记忆决策，避免记忆系统被无价值的信息淹没。

会话搜索指导 (SESSION_SEARCH_GUIDANCE)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SESSION_SEARCH_GUIDANCE = (
        "When the user references something from a past conversation or you suspect "
        "relevant cross-session context exists, use session_search to recall it before "
        "asking them to repeat themselves."
    )

这条简短的指导告诉 Agent：当用户提到过去对话的内容时，应该主动搜索而不是要求用户重复。这大大改善了用户体验。

技能指导 (SKILLS_GUIDANCE)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    SKILLS_GUIDANCE = (
        "After completing a complex task (5+ tool calls), fixing a tricky error, "
        "or discovering a non-trivial workflow, save the approach as a "
        "skill with skill_manage so you can reuse it next time.\n"
        "When using a skill and finding it outdated, incomplete, or wrong, "
        "patch it immediately with skill_manage(action='patch') — don't wait to be asked. "
        "Skills that aren't maintained become liabilities."
    )

这条指导鼓励 Agent 主动创建和维护技能，形成自我改进的循环。

7. 模型特定执行规范
---------------------

不同的 LLM 有不同的行为特性和常见失败模式。hermes-agent 为不同模型提供了特定的执行指导。

工具使用强制指导
~~~~~~~~~~~~~~~~~~

对于某些模型，hermes-agent 会注入额外的工具使用强制指导：

.. code-block:: python

    TOOL_USE_ENFORCEMENT_MODELS = ("gpt", "codex", "gemini", "gemma", "grok")

    TOOL_USE_ENFORCEMENT_GUIDANCE = (
        "# Tool-use enforcement\n"
        "You MUST use your tools to take action — do not describe what you would do "
        "or plan to do without actually doing it. When you say you will perform an "
        "action (e.g. 'I will run the tests', 'Let me check the file', 'I will create "
        "the project'), you MUST immediately make the corresponding tool call in the same "
        "response. Never end your turn with a promise of future action — execute it now.\n"
        "Keep working until the task is actually complete. Do not stop with a summary of "
        "what you plan to do next time. If you have tools available that can accomplish "
        "the task, use them instead of telling the user what you would do.\n"
        "Every response should either (a) contain tool calls that make progress, or "
        "(b) deliver a final result to the user. Responses that only describe intentions "
        "without acting are not acceptable."
    )

这条指导针对某些模型的一个常见问题：它们会描述自己要做什么，而不是实际去做。这被称为"承诺但不执行"问题。

OpenAI 模型执行指导
~~~~~~~~~~~~~~~~~~~~~

对于 OpenAI 的模型（特别是 GPT 和 Codex），hermes-agent 提供了更详细的执行指导：

.. code-block:: python

    OPENAI_MODEL_EXECUTION_GUIDANCE = (
        "# Execution discipline\n"
        "<tool_persistence>\n"
        "- Use tools whenever they improve correctness, completeness, or grounding.\n"
        "- Do not stop early when another tool call would materially improve the result.\n"
        "- If a tool returns empty or partial results, retry with a different query or "
        "strategy before giving up.\n"
        "- Keep calling tools until: (1) the task is complete, AND (2) you have verified "
        "the result.\n"
        "</tool_persistence>\n"
        "\n"
        "<mandatory_tool_use>\n"
        "NEVER answer these from memory or mental computation — ALWAYS use a tool:\n"
        "- Arithmetic, math, calculations → use terminal or execute_code\n"
        "- Hashes, encodings, checksums → use terminal (e.g. sha256sum, base64)\n"
        "- Current time, date, timezone → use terminal (e.g. date)\n"
        "- System state: OS, CPU, memory, disk, ports, processes → use terminal\n"
        "- File contents, sizes, line counts → use read_file, search_files, or terminal\n"
        "- Git history, branches, diffs → use terminal\n"
        "- Current facts (weather, news, versions) → use web_search\n"
        "</mandatory_tool_use>\n"
        # ... 更多指导
    )

这段指导使用 XML 标签分组，包含几个方面：

1. **工具持久性** （tool_persistence）：不要过早停止工具调用
2. **强制工具使用** （mandatory_tool_use）：某些信息必须通过工具获取，不能从记忆中回答
3. **行动而非询问** （act_dont_ask）：有明确默认解释时直接行动
4. **前置检查** （prerequisite_checks）：不要跳过必要的准备步骤
5. **验证** （verification）：最终结果前检查正确性
6. **缺失上下文** （missing_context）：缺少信息时使用工具查找

这些指导针对 OpenAI 模型的已知问题进行了优化，包括过早放弃工作、跳过前置检查、用记忆代替工具获取信息等。

Google 模型操作指导
~~~~~~~~~~~~~~~~~~~~~

对于 Google 的 Gemini 和 Gemma 模型：

.. code-block:: python

    GOOGLE_MODEL_OPERATIONAL_GUIDANCE = (
        "# Google model operational directives\n"
        "Follow these operational rules strictly:\n"
        "- **Absolute paths:** Always construct and use absolute file paths for all "
        "file system operations. Combine the project root with relative paths.\n"
        "- **Verify first:** Use read_file/search_files to check file contents and "
        "project structure before making changes. Never guess at file contents.\n"
        "- **Dependency checks:** Never assume a library is available. Check "
        "package.json, requirements.txt, Cargo.toml, etc. before importing.\n"
        "- **Conciseness:** Keep explanatory text brief — a few sentences, not "
        "paragraphs. Focus on actions and results over narration.\n"
        "- **Parallel tool calls:** When you need to perform multiple independent "
        "operations (e.g. reading several files), make all the tool calls in a "
        "single response rather than sequentially.\n"
        "- **Non-interactive commands:** Use flags like -y, --yes, --non-interactive "
        "to prevent CLI tools from hanging on prompts.\n"
        "- **Keep going:** Work autonomously until the task is fully resolved. "
        "Don't stop with a plan — execute it.\n"
    )

这些指导针对 Google 模型的特定问题，包括使用相对路径、猜测文件内容、不检查依赖等。

角色映射
~~~~~~~~~~

hermes-agent 还为不同模型提供了角色映射：

.. code-block:: python

    # 模型名称子串 -> 应使用 'developer' 角色而非 'system'
    DEVELOPER_ROLE_MODELS = ("gpt-5", "codex")

对于 OpenAI 的新模型（GPT-5、Codex），使用 ``developer`` 角色而不是 ``system`` 角色。这是因为 OpenAI 发现 ``developer`` 角色在这些模型上有更强的指令遵循权重。

这个映射在 API 边界进行转换，内部消息表示保持一致（始终使用 "system"），确保了代码的一致性。

8. 技能索引系统
-----------------

技能（Skill）是 hermes-agent 中一个强大的概念，它允许 Agent 学习和复用特定的工作流和知识。技能索引系统负责在系统提示中列出所有可用的技能。

双层缓存架构
~~~~~~~~~~~~~~

技能索引系统使用了一个精心设计的双层缓存：

1. **LRU 内存缓存** ：进程内的最近最少使用缓存，最多保存 8 个条目
2. **磁盘快照** ：使用 mtime/size 清单验证的持久化缓存，在进程重启后仍然有效

让我们看看这个架构的实现：

.. code-block:: python

    _SKILLS_PROMPT_CACHE_MAX = 8
    _SKILLS_PROMPT_CACHE: OrderedDict[tuple, str] = OrderedDict()
    _SKILLS_PROMPT_CACHE_LOCK = threading.Lock()
    _SKILLS_SNAPSHOT_VERSION = 1

LRU 内存缓存使用 ``OrderedDict`` 实现，这是 Python 中实现 LRU 缓存的标准方式：

1. **查找** ：检查缓存键是否存在，如果存在就移到末尾（最近使用）
2. **存储** ：将新值添加到末尾
3. **淘汰** ：当缓存大小超过限制时，从头部移除（最近最少使用）

缓存键的设计
~~~~~~~~~~~~~~

缓存键由多个因素组成，确保不同配置产生不同的缓存条目：

.. code-block:: python

    cache_key = (
        str(skills_dir.resolve()),
        tuple(str(d) for d in external_dirs),
        tuple(sorted(str(t) for t in (available_tools or set()))),
        tuple(sorted(str(ts) for ts in (available_toolsets or set()))),
        _platform_hint,
    )

缓存键包含：

1. **技能目录路径** ：不同的技能目录有不同的技能
2. **外部目录** ：外部技能目录的列表
3. **可用工具集合** ：技能可能根据可用工具过滤
4. **可用工具集集合** ：技能可能根据可用工具集过滤
5. **平台提示** ：不同平台可能禁用不同的技能

这确保了不同配置之间不会共享缓存条目，避免返回错误的技能列表。

磁盘快照
~~~~~~~~~~

磁盘快照使用 mtime/size 清单来验证缓存是否仍然有效：

.. code-block:: python

    def _build_skills_manifest(skills_dir: Path) -> dict[str, list[int]]:
        """Build an mtime/size manifest of all SKILL.md and DESCRIPTION.md files."""
        manifest: dict[str, list[int]] = {}
        for filename in ("SKILL.md", "DESCRIPTION.md"):
            for path in iter_skill_index_files(skills_dir, filename):
                try:
                    st = path.stat()
                except OSError:
                    continue
                manifest[str(path.relative_to(skills_dir))] = [st.st_mtime_ns, st.st_size]
        return manifest

清单记录了每个技能文件的修改时间（纳秒精度）和大小。当加载快照时，重新计算清单并比较：

.. code-block:: python

    def _load_skills_snapshot(skills_dir: Path) -> Optional[dict]:
        """Load the disk snapshot if it exists and its manifest still matches."""
        snapshot_path = _skills_prompt_snapshot_path()
        if not snapshot_path.exists():
            return None
        try:
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        except Exception:
            return None
        if not isinstance(snapshot, dict):
            return None
        if snapshot.get("version") != _SKILLS_SNAPSHOT_VERSION:
            return None
        if snapshot.get("manifest") != _build_skills_manifest(skills_dir):
            return None
        return snapshot

这个验证机制确保：

1. **版本检查** ：快照格式可能变化，版本号确保兼容性
2. **内容变化检测** ：如果任何技能文件被修改（mtime 或大小变化），快照失效
3. **新文件检测** ：如果添加了新的技能文件，清单长度变化，快照失效

当快照无效时，系统回退到完整的文件系统扫描，然后写入新的快照。

技能条件过滤
~~~~~~~~~~~~~~

技能可以有条件激活规则，控制何时应该在索引中显示：

.. code-block:: python

    def _skill_should_show(
        conditions: dict,
        available_tools: "set[str] | None",
        available_toolsets: "set[str] | None",
    ) -> bool:
        """Return False if the skill's conditional activation rules exclude it."""
        if available_tools is None and available_toolsets is None:
            return True

        at = available_tools or set()
        ats = available_toolsets or set()

        # fallback_for: hide when the primary tool/toolset IS available
        for ts in conditions.get("fallback_for_toolsets", []):
            if ts in ats:
                return False
        for t in conditions.get("fallback_for_tools", []):
            if t in at:
                return False

        # requires: hide when a required tool/toolset is NOT available
        for ts in conditions.get("requires_toolsets", []):
            if ts not in ats:
                return False
        for t in conditions.get("requires_tools", []):
            if t not in at:
                return False

        return True

技能支持两种条件：

1. **fallback_for** ：当主工具/工具集可用时隐藏。例如，一个"通用搜索"技能可能在 ``web_search`` 工具可用时隐藏
2. **requires** ：当必要的工具/工具集不可用时隐藏。例如，一个"Docker 操作"技能可能在 ``terminal`` 工具不可用时隐藏

这让技能系统变得智能：不是所有技能都在所有情况下可见，只有相关的技能才会出现在索引中。

技能索引的输出格式
~~~~~~~~~~~~~~~~~~~~

技能索引最终生成一个结构化的文本块：

.. code-block:: python

    "## Skills (mandatory)\n"
    "Before replying, scan the skills below. If a skill matches or is even partially relevant "
    "to your task, you MUST load it with skill_view(name) and follow its instructions. "
    # ...
    "<available_skills>\n"
    "  category_name: Category description\n"
    "    - skill_name: Skill description\n"
    "    - another_skill: Another description\n"
    "</available_skills>\n"

这个格式有几个特点：

1. **层级结构** ：技能按类别分组
2. **描述信息** ：每个类别和技能都有描述
3. **XML 标签** ：使用 ``<available_skills>`` 标签，便于模型识别
4. **强制性** ：标题声明这是"必须"执行的步骤

技能缓存查找流程图
~~~~~~~~~~~~~~~~~~~~

下面是技能缓存查找的序列图：

.. mermaid::

    sequenceDiagram
        participant Caller as build_skills_system_prompt()
        participant LRU as LRU 内存缓存
        participant Disk as 磁盘快照
        participant FS as 文件系统扫描

        Caller->>LRU: 查询缓存键
        alt 缓存命中
            LRU-->>Caller: 返回缓存的技能索引
        else 缓存未命中
            LRU-->>Caller: None
            Caller->>Disk: 加载磁盘快照
            alt 快照有效
                Disk-->>Caller: 返回预解析的技能数据
            else 快照无效或不存在
                Disk-->>Caller: None
                Caller->>FS: 完整文件系统扫描
                FS-->>Caller: 技能文件列表
                Caller->>Caller: 解析技能文件
                Caller->>Disk: 写入新快照
            end
            Caller->>LRU: 存入缓存
            Caller-->>Caller: 返回技能索引
        end

这个流程图展示了技能查找的三层逻辑：先查 LRU，再查磁盘快照，最后回退到文件系统扫描。

9. 上下文文件优先级
---------------------

hermes-agent 支持多种上下文文件格式，用于注入项目特定的指导。这些文件有一个明确的优先级顺序。

优先级顺序
~~~~~~~~~~~~

上下文文件按以下优先级加载（第一个匹配的文件被使用）：

1. **.hermes.md / HERMES.md** ：Hermes 专用上下文文件
2. **AGENTS.md / agents.md** ：通用 Agent 上下文文件
3. **CLAUDE.md / claude.md** ：Claude 兼容的上下文文件
4. **.cursorrules** / **.cursor/rules/\*.mdc**：Cursor 编辑器的规则文件

这个优先级设计有几个考虑：

1. **Hermes 优先** ：专用文件覆盖通用文件
2. **向后兼容** ：支持 AGENTS.md 和 CLAUDE.md，方便从其他工具迁移
3. **互斥加载** ：只加载第一个匹配的文件，避免冲突和重复

让我们看看加载逻辑：

.. code-block:: python

    def build_context_files_prompt(cwd: Optional[str] = None, skip_soul: bool = False) -> str:
        """Discover and load context files for the system prompt.

        Priority (first found wins — only ONE project context type is loaded):
          1. .hermes.md / HERMES.md  (walk to git root)
          2. AGENTS.md / agents.md   (cwd only)
          3. CLAUDE.md / claude.md   (cwd only)
          4. .cursorrules / .cursor/rules/*.mdc  (cwd only)

        SOUL.md from HERMES_HOME is independent and always included when present.
        Each context source is capped at 20,000 chars.
        """
        if cwd is None:
            cwd = os.getcwd()

        cwd_path = Path(cwd).resolve()
        sections = []

        # Priority-based project context: first match wins
        project_context = (
            _load_hermes_md(cwd_path)
            or _load_agents_md(cwd_path)
            or _load_claude_md(cwd_path)
            or _load_cursorrules(cwd_path)
        )
        if project_context:
            sections.append(project_context)

        # SOUL.md from HERMES_HOME only — skip when already loaded as identity
        if not skip_soul:
            soul_content = load_soul_md()
            if soul_content:
                sections.append(soul_content)

        if not sections:
            return ""
        return "# Project Context\n\nThe following project context files have been loaded and should be followed:\n\n" + "\n".join(sections)

注意 Python 的 "or" 短路求值在这里创造了一个优雅的优先级链：第一个返回非空字符串的函数被使用，后面的函数不会被调用。

.hermes.md 的搜索范围
~~~~~~~~~~~~~~~~~~~~~~~

.hermes.md 与其他文件不同，它不仅搜索当前目录，还会向上搜索到 git 仓库根目录：

.. code-block:: python

    def _find_hermes_md(cwd: Path) -> Optional[Path]:
        """Discover the nearest ``.hermes.md`` or ``HERMES.md``.

        Search order: *cwd* first, then each parent directory up to (and
        including) the git repository root.
        """
        stop_at = _find_git_root(cwd)
        current = cwd.resolve()

        for directory in [current, *current.parents]:
            for name in _HERMES_MD_NAMES:
                candidate = directory / name
                if candidate.is_file():
                    return candidate
            if stop_at and directory == stop_at:
                break
        return None

这意味着你可以在项目根目录放置 .hermes.md，它会在所有子目录中生效。这是一个有用的功能，因为用户可能在项目子目录中启动 Agent。

内容截断
~~~~~~~~~~

每个上下文文件的内容被限制在 20,000 字符以内：

.. code-block:: python

    CONTEXT_FILE_MAX_CHARS = 20_000
    CONTEXT_TRUNCATE_HEAD_RATIO = 0.7
    CONTEXT_TRUNCATE_TAIL_RATIO = 0.2

    def _truncate_content(content: str, filename: str, max_chars: int = CONTEXT_FILE_MAX_CHARS) -> str:
        """Head/tail truncation with a marker in the middle."""
        if len(content) <= max_chars:
            return content
        head_chars = int(max_chars * CONTEXT_TRUNCATE_HEAD_RATIO)
        tail_chars = int(max_chars * CONTEXT_TRUNCATE_TAIL_RATIO)
        head = content[:head_chars]
        tail = content[-tail_chars:]
        marker = f"\n\n[...truncated {filename}: kept {head_chars}+{tail_chars} of {len(content)} chars. Use file tools to read the full file.]\n\n"
        return head + marker + tail

截断策略是保留头部 70% 和尾部 20%，中间插入一个说明标记。这种设计假设：

1. 最重要的内容通常在文件开头（身份、核心规则）
2. 结尾可能有重要的约束或总结
3. 中间的内容可以安全地省略

注意还有 10% 的空间没有被保留，这是有意为之——为标记和额外的格式留出空间。

YAML Frontmatter 处理
~~~~~~~~~~~~~~~~~~~~~~~

.hermes.md 文件可能包含 YAML frontmatter，在注入系统提示之前会被剥离：

.. code-block:: python

    def _strip_yaml_frontmatter(content: str) -> str:
        """Remove optional YAML frontmatter (``---`` delimited) from *content*."""
        if content.startswith("---"):
            end = content.find("\n---", 3)
            if end != -1:
                body = content[end + 4:].lstrip("\n")
                return body if body else content
        return content

这允许在 frontmatter 中包含结构化配置（如模型覆盖、工具设置），同时只将人类可读的 Markdown 正文注入系统提示。

上下文文件解析优先级流程图
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

下面是上下文文件解析的流程图：

.. mermaid::

    flowchart TD
        Start([开始搜索上下文文件]) --> CheckHermes{当前目录有 .hermes.md?}
        CheckHermes -->|是| LoadHermes[加载 .hermes.md]
        CheckHermes -->|否| WalkUp[向上搜索到 git 根目录]
        WalkUp --> FoundHermes{找到 .hermes.md?}
        FoundHermes -->|是| LoadHermes
        FoundHermes -->|否| CheckAgents{当前目录有 AGENTS.md?}
        CheckAgents -->|是| LoadAgents[加载 AGENTS.md]
        CheckAgents -->|否| CheckClaude{当前目录有 CLAUDE.md?}
        CheckClaude -->|是| LoadClaude[加载 CLAUDE.md]
        CheckClaude -->|否| CheckCursor{有 .cursorrules?}
        CheckCursor -->|是| LoadCursor[加载 .cursorrules + .cursor/rules/*.mdc]
        CheckCursor -->|否| NoContext[无上下文文件]
        LoadHermes --> Scan[注入扫描]
        LoadAgents --> Scan
        LoadClaude --> Scan
        LoadCursor --> Scan
        Scan --> Truncate[内容截断]
        Truncate --> Merge[合并为 Project Context]
        NoContext --> CheckSoul{跳过 SOUL.md?}
        Merge --> CheckSoul
        CheckSoul -->|否| LoadSoul[加载 SOUL.md]
        CheckSoul -->|是| Final[最终系统提示]
        LoadSoul --> Final

10. 提示注入防御
------------------

在一个允许加载用户提供的上下文文件的系统中，提示注入攻击是一个严重的威胁。hermes-agent 实现了全面的防御机制。

13 种检测模式
~~~~~~~~~~~~~~~

hermes-agent 使用正则表达式检测 13 种常见的提示注入模式：

.. code-block:: python

    _CONTEXT_THREAT_PATTERNS = [
        (r'ignore\s+(previous|all|above|prior)\s+instructions', "prompt_injection"),
        (r'do\s+not\s+tell\s+the\s+user', "deception_hide"),
        (r'system\s+prompt\s+override', "sys_prompt_override"),
        (r'disregard\s+(your|all|any)\s+(instructions|rules|guidelines)', "disregard_rules"),
        (r'act\s+as\s+(if|though)\s+you\s+(have\s+no|don\'t\s+have)\s+(restrictions|limits|rules)', "bypass_restrictions"),
        (r'<!--[^>]*(?:ignore|override|system|secret|hidden)[^>]*-->', "html_comment_injection"),
        (r'<\s*div\s+style\s*=\s*["\'][\s\S]*?display\s*:\s*none', "hidden_div"),
        (r'translate\s+.*\s+into\s+.*\s+and\s+(execute|run|eval)', "translate_execute"),
        (r'curl\s+[^\n]*\$\{?\w*(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL|API)', "exfil_curl"),
        (r'cat\s+[^\n]*(\.env|credentials|\.netrc|\.pgpass)', "read_secrets"),
    ]

这些模式覆盖了几类攻击：

1. **指令覆盖** ：如 "ignore all instructions"、"disregard your rules"
2. **欺骗隐藏** ：如 "do not tell the user"
3. **权限绕过** ：如 "act as if you have no restrictions"
4. **HTML 注入** ：如包含 "ignore"、"override" 的 HTML 注释、隐藏的 div
5. **代码执行** ：如 "translate and execute"
6. **数据泄露** ：如尝试使用 curl 获取环境变量、读取敏感文件

Unicode 不可见字符扫描
~~~~~~~~~~~~~~~~~~~~~~~~

除了正则匹配，hermes-agent 还扫描不可见的 Unicode 字符：

.. code-block:: python

    _CONTEXT_INVISIBLE_CHARS = {
        '\u200b', '\u200c', '\u200d', '\u2060', '\ufeff',
        '\u202a', '\u202b', '\u202c', '\u202d', '\u202e',
    }

这些字符包括：

- **零宽空格** （U+200B）：不可见但存在
- **零宽连接符** （U+200C, U+200D）：用于某些语言的连字
- **字节顺序标记** （U+FEFF）：通常在文件开头
- **方向控制字符** （U+202A-202E）：控制文本方向

攻击者可能使用这些字符来隐藏恶意指令，例如在正常文本中插入不可见的 "ignore previous instructions"。

扫描与阻止流程
~~~~~~~~~~~~~~~~

当检测到威胁时，整个文件的内容被替换为阻止消息：

.. code-block:: python

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

这是一种"全有或全无"的策略：

1. 如果检测到任何威胁，整个文件被阻止
2. 返回一个描述性的阻止消息，而不是原始内容
3. 原始内容永远不会进入系统提示

这种策略虽然可能产生误报（false positive），但在安全上下文中，宁可误杀也不可遗漏。

11. Anthropic Prompt 缓存
---------------------------

最后，让我们探讨 hermes-agent 中一个重要的成本优化机制：Anthropic Prompt 缓存。

为什么需要 Prompt 缓存？
~~~~~~~~~~~~~~~~~~~~~~~~~~

在与 LLM 的多轮对话中，系统提示和早期对话内容通常在每轮中都是相同的。如果不使用缓存，这些重复的内容会在每轮都计费。对于长系统提示和多轮对话，这会显著增加成本。

Anthropic 提供了一个 Prompt 缓存功能，允许缓存部分消息，避免重复计算。hermes-agent 使用 "system_and_3" 策略来最大化缓存命中。

system_and_3 策略
~~~~~~~~~~~~~~~~~~~

system_and_3 策略的名称来源于它的设计：在最多 4 个位置放置缓存断点（Anthropic 允许的最大值）：

1. **系统提示** ：在所有对话轮次中保持不变
2-4. **最后 3 条非系统消息** ：滚动窗口，每轮更新

让我们看看实现：

.. code-block:: python

    def apply_anthropic_cache_control(
        api_messages: List[Dict[str, Any]],
        cache_ttl: str = "5m",
        native_anthropic: bool = False,
    ) -> List[Dict[str, Any]]:
        """Apply system_and_3 caching strategy to messages for Anthropic models."""
        messages = copy.deepcopy(api_messages)
        if not messages:
            return messages

        marker = {"type": "ephemeral"}
        if cache_ttl == "1h":
            marker["ttl"] = "1h"

        breakpoints_used = 0

        if messages[0].get("role") == "system":
            _apply_cache_marker(messages[0], marker, native_anthropic=native_anthropic)
            breakpoints_used += 1

        remaining = 4 - breakpoints_used
        non_sys = [i for i in range(len(messages)) if messages[i].get("role") != "system"]
        for idx in non_sys[-remaining:]:
            _apply_cache_marker(messages[idx], marker, native_anthropic=native_anthropic)

        return messages

这个函数：

1. **深拷贝消息** ：不修改原始消息列表
2. **设置标记类型** ：默认是 "ephemeral"（短期缓存），可选择 1 小时 TTL
3. **标记系统消息** ：如果第一条消息是系统消息，标记它
4. **标记最近的非系统消息** ：从后往前标记，直到用完 4 个断点

缓存标记的注入
~~~~~~~~~~~~~~~~

缓存标记的注入需要处理多种消息格式：

.. code-block:: python

    def _apply_cache_marker(msg: dict, cache_marker: dict, native_anthropic: bool = False) -> None:
        """Add cache_control to a single message, handling all format variations."""
        role = msg.get("role", "")
        content = msg.get("content")

        if role == "tool":
            if native_anthropic:
                msg["cache_control"] = cache_marker
            return

        if content is None or content == "":
            msg["cache_control"] = cache_marker
            return

        if isinstance(content, str):
            msg["content"] = [
                {"type": "text", "text": content, "cache_control": cache_marker}
            ]
            return

        if isinstance(content, list) and content:
            last = content[-1]
            if isinstance(last, dict):
                last["cache_control"] = cache_marker

这个函数处理了所有可能的消息格式变体：

1. **工具消息** ：对于原生 Anthropic API，直接在消息级别添加标记
2. **空内容** ：在消息级别添加标记
3. **字符串内容** ：转换为内容块列表，在最后一个块添加标记
4. **列表内容** ：在最后一个内容块添加标记

缓存标记总是放在最后一个内容块上，因为 Anthropic 的缓存是从头到标记位置的连续前缀。

成本节省分析
~~~~~~~~~~~~~~

使用 prompt 缓存可以节省约 75% 的输入 token 成本。让我们分析一下原因：

在典型的多轮对话中：

1. **系统提示** ：通常包含数千个 token，在所有轮次中不变
2. **早期对话** ：一旦生成，在后续轮次中不变
3. **只有最新消息** ：在每轮中新增

没有缓存时，每轮都需要支付全部输入 token 的费用。有了缓存：

- 系统提示只计算一次，后续从缓存读取
- 早期的对话轮次也会被缓存
- 只有缓存未命中的部分才需要完整计费

具体来说，假设系统提示有 3000 token，每轮新增 500 token：

- 第 1 轮：无缓存，支付 3000 token
- 第 2 轮：系统提示命中缓存，支付 500 新 token
- 第 3 轮：系统提示 + 第 1 轮命中缓存，支付 500 新 token
- ...

这就是为什么缓存可以节省约 75% 的输入 token 成本。

Anthropic 缓存策略流程图
~~~~~~~~~~~~~~~~~~~~~~~~~~

下面是 Anthropic 缓存策略的流程图：

.. mermaid::

    flowchart TD
        Start([接收消息列表]) --> DeepCopy[深拷贝消息]
        DeepCopy --> SetMarker[设置缓存标记类型]
        SetMarker --> CheckTTL{TTL设置}
        CheckTTL -->|5m| MarkerEphemeral[marker = ephemeral]
        CheckTTL -->|1h| Marker1H[marker = ephemeral + ttl=1h]

        MarkerEphemeral --> CheckSystem{第一条消息是系统消息?}
        Marker1H --> CheckSystem

        CheckSystem -->|是| MarkSystem[标记系统消息, breakpoints=1]
        CheckSystem -->|否| NoSystem[breakpoints=0]

        MarkSystem --> CalcRemaining[remaining = 4 - breakpoints]
        NoSystem --> CalcRemaining

        CalcRemaining --> FindNonSys[找出所有非系统消息的索引]
        FindNonSys --> MarkLast[标记最后 remaining 条非系统消息]
        MarkLast --> Return[返回带缓存标记的消息]
        Return --> End([结束])

        subgraph 缓存效果
            direction LR
            M1[消息1: system] --> M2[消息2: user]
            M2 --> M3[消息3: assistant]
            M3 --> M4[消息4: tool]
            M4 --> M5[消息5: user]
            M5 --> M6[消息6: assistant]
            M6 --> M7[消息7: user]

            M1 -.- C1[cache_control]
            M5 -.- C2[cache_control]
            M6 -.- C3[cache_control]
            M7 -.- C4[cache_control]
        end

总结
------

在本章中，我们深入探讨了 hermes-agent 的提示工程管线，从 9 槽位管道设计、Agent 身份定义、14 个平台适配、环境感知、记忆与搜索指导、模型特定规范、双层缓存技能索引、上下文文件优先级到提示注入防御和 Anthropic Prompt 缓存。

这个系统的设计体现了几个重要原则：

1. **分层设计** ：每个槽位负责一个独立的关注点，便于单独开发和测试
2. **动态适配** ：根据平台、环境、模型动态调整提示内容
3. **安全优先** ：多层次的注入防御机制
4. **性能优化** ：双层缓存、磁盘快照、Anthropic 缓存
5. **成本控制** ：通过缓存策略减少 token 使用
6. **可扩展性** ：新平台、新模型、新环境可以轻松添加

理解这个系统不仅有助于使用 hermes-agent，也为设计其他 AI Agent 框架的提示系统提供了宝贵的参考。一个好的提示系统不是一蹴而就的，而是需要在实际使用中不断迭代和优化的。
