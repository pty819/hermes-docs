.. _chapter-skill-system:

#####################################
技能系统：Agent 的可复用知识单元
#####################################

.. contents::
   :depth: 3
   :local:

****************
1. 什么是技能
****************

在 AI Agent 的运行过程中，同一类型的任务往往反复出现——部署服务、调试测试、编写文档、配置 CI/CD 管道等等。每次面对相似的任务时，Agent 都需要重新探索最佳实践、犯同样的错误、走同样的弯路。这不仅浪费了 token 和时间，也降低了用户体验的一致性。

Hermes Agent 的技能系统（Skill System）正是为解决这一问题而设计的。技能是**持久的、可复用的指令集** ，它们捕获了"如何完成特定类型的任务"这一程序性知识。与一般记忆（MEMORY.md、USER.md）不同，记忆是宽泛的声明性知识（"我喜欢用 TypeScript"），而技能是窄域的、可操作的流程（"部署 AWS Lambda 函数的完整步骤"）。

技能的核心价值在于：

- **知识积累** ：成功的任务执行经验被保存为技能，避免重复探索。

- **一致性** ：相同类型的任务遵循相同的流程，产出质量更稳定。

- **渐进式披露** ：技能系统采用三层架构——索引（名称+描述）、完整内容（SKILL.md）、链接文件（参考、模板），按需加载以节省 token。

- **可组合性** ：技能之间可以通过 ``related_skills`` 建立关联，支持复杂任务的分解。

.. mermaid::

   flowchart TD
       subgraph Sources["技能来源"]
           Bundled["内置技能"]
           Hub["Hub 安装"]
           User["用户创建"]
           Plugin["插件提供"]
       end

       Bundled -->|"sync_skills() 同步"| Synced["同步后的技能树"]
       Hub -->|"安装后复制"| Synced
       User -->|"skill_manage(create)"| Synced
       Plugin -->|"plugin:skill 限定名"| Qualified["限定名技能"]

       Synced -->|"build_skills_system_prompt()"| Indexed["技能索引"]
       Qualified -->|"skill_view() 按需读取"| OnDemand["按需加载"]

       Indexed -->|"条件匹配"| Activated["激活技能"]
       Indexed -->|"未命中"| Dormant["休眠技能"]
       Dormant -->|"条件变化"| Activated

       Activated -->|"Agent 调用"| Used["执行中"]
       Used -->|"patch / edit"| Modified["已修改"]
       Used -->|"执行完成"| Unchanged["未修改"]

       Modified -->|"清除缓存并重建"| Indexed
       Unchanged --> Indexed

       SyncedNote["~/.hermes/skills/name/SKILL.md"]
       QualifiedNote["不进入 flat tree"]
       IndexedNote["进入 available_skills 区段"]
       ActivatedNote["注入到当前会话上下文"]

       SyncedNote -.-> Synced
       QualifiedNote -.-> Qualified
       IndexedNote -.-> Indexed
       ActivatedNote -.-> Activated

*****************
2. 技能来源
*****************

Hermes Agent 的技能来自四个渠道，每个渠道有不同的生命周期和管理方式。

内置技能（Bundled Skills）
============================

内置技能随 Hermes Agent 代码库分发，存放在仓库的 ``skills/`` 目录下。这些技能覆盖了常见的开发、运维和数据处理场景。

在 Agent 首次启动或更新时，``sync_skills()`` 函数会将内置技能同步到 ``~/.hermes/skills/`` 目录。同步策略尊重用户的修改——如果用户自定义了某个内置技能，更新时不会覆盖。

Hub 安装技能（Hub-installed Skills）
======================================

通过 ``hermes skills install NAME`` 命令从技能 Hub（如 agentskills.io）安装的技能。安装时经过安全扫描（``skills_guard.scan_skill()``），确认无害后复制到 ``~/.hermes/skills/`` 。

用户创建技能（User-created Skills）
=====================================

Agent 在执行复杂任务后，可以通过 ``skill_manage`` 工具主动创建技能。创建时机包括：

- 复杂任务成功完成（5+ 次工具调用）。

- 克服了错误才找到正确方案。

- 用户纠正了 Agent 的方法后成功完成。

- 发现了非平凡的工作流程。

- 用户明确要求保存流程。

插件提供技能（Plugin-provided Skills）
========================================

插件通过 ``PluginContext.register_skill()`` 注册的技能。这类技能使用限定名格式 ``"plugin_name:skill_name"`` ，不会出现在 ``~/.hermes/skills/`` 的目录树中，也不会出现在系统提示的技能索引里——它们是显式按需加载的。

******************
3. SKILL.md 格式
******************

每个技能的核心是 ``SKILL.md`` 文件，它使用 YAML 前置元数据 + Markdown 正文的格式，兼容 agentskills.io 标准。

完整格式
==========

.. code-block:: markdown

   ---
   name: axolotl                    # 必需，最长 64 字符
   description: "Fine-tune LLMs using Axolotl framework"
                                    # 必需，最长 1024 字符
   version: 1.0.0                   # 可选
   license: MIT                     # 可选（agentskills.io 标准）
   platforms: [macos, linux]        # 可选，限制运行平台
                                    #   有效值：macos, linux, windows
                                    #   省略 = 所有平台（默认）
   prerequisites:                   # 可选，运行时依赖
     env_vars: [HUGGINGFACE_TOKEN]  #   遗留格式，自动规范化
     commands: [python3, pip]       #   命令检查（仅建议）
   required_environment_variables:  # 可选，新版依赖声明
     - name: HUGGINGFACE_TOKEN
       prompt: "Enter your HuggingFace API token"
       help: "https://huggingface.co/settings/tokens"
       required_for: "model download"
   setup:                           # 可选，安装引导
     help: "https://docs.axolotl.ai/"
     collect_secrets:
       - env_var: WANDB_API_KEY
         prompt: "Enter your Weights & Biases API key"
         provider_url: "https://wandb.ai/authorize"
   metadata:                        # 可选，任意元数据（agentskills.io）
     hermes:
       tags: [fine-tuning, llm, axolotl]
       related_skills: [peft, lora, quantization]
   compatibility: "Requires Python 3.10+"  # 可选
   triggers:                        # 可选，自动激活条件
     - "fine-tune"
     - "train model"
     - "axolotl"
   fallback_for:                    # 可选，作为工具集的回退技能
     - "training"
   requires_toolsets:               # 可选，仅在特定工具集可用时激活
     - "mcp-gpu-cluster"
   ---

   # Axolotl Fine-tuning

   ## Instructions

   1. Check GPU availability with `nvidia-smi`
   2. Prepare the dataset in JSONL format...
   3. Create the config YAML...

   ## Pitfalls

   - OOM errors: reduce batch_size or enable gradient checkpointing
   - Dataset format must match the model's expected chat template

前置元数据字段详解
====================

name 和 description
---------------------

- ``name`` ：必需。技能的唯一标识符，最长 64 字符。推荐使用小写字母、数字和连字符（如 ``axolotl``）。

- ``description`` ：必需。技能的简短描述，最长 1024 字符。出现在 ``skills_list()`` 的索引中。

platforms
-----------

可选。限制技能仅在指定平台上加载和显示。有效值为 ``macos`` 、``linux`` 、``windows`` ，对应 ``sys.platform`` 的 ``darwin`` 、``linux`` 、``win32`` 。省略此字段意味着技能在所有平台上可用。

.. code-block:: python

   _PLATFORM_MAP = {
       "macos": "darwin",
       "linux": "linux",
       "windows": "win32",
   }

prerequisites 和 required_environment_variables
-------------------------------------------------

这两个字段声明技能运行所需的外部依赖。``prerequisites`` 是遗留格式，``required_environment_variables`` 是新版格式。两者在加载时会被合并处理。

当必需的环境变量缺失时，技能的 ``readiness_status`` 会被标记为 ``setup_needed`` 。如果在 CLI 模式下且配置了 ``_secret_capture_callback`` ，Agent 会提示用户输入缺失的值；在网关模式下，会返回一个提示信息引导用户手动配置。

triggers、fallback_for 和 requires_toolsets
---------------------------------------------

这三个字段控制技能的条件激活：

- ``triggers`` ：关键词列表。当用户消息包含这些关键词时，技能被自动激活。

- ``fallback_for`` ：工具集列表。当指定的工具集不可用时，该技能作为替代方案被推荐。

- ``requires_toolsets`` ：工具集列表。仅在指定的工具集可用时才激活该技能。

metadata.hermes
-----------------

Hermes 特定的元数据，支持 ``tags`` （标签）和 ``related_skills`` （关联技能）。标签用于分类和搜索，关联技能用于推荐相关的技能。

正文结构
==========

SKILL.md 的正文部分通常包含以下节：

- **Instructions** ：分步骤的任务执行指南。推荐使用编号列表，包含精确的命令和参数。

- **Pitfalls** ：常见陷阱和错误，帮助 Agent 避免已知的坑。

- **Verification** ：验证步骤，确认任务是否成功完成。

- **Examples** ：具体的示例，展示典型的输入和期望输出。

****************************
4. 技能管理工具
****************************

``skill_manage`` 是 Agent 管理技能的核心工具。它支持六种操作：

create：创建技能
==================

创建一个新的技能。需要提供完整的 SKILL.md 内容（前置元数据 + 正文）。

.. code-block:: json

   {
     "action": "create",
     "name": "my-deploy-workflow",
     "content": "---\nname: my-deploy-workflow\ndescription: ...\n---\n\n# Deploy Workflow\n...",
     "category": "devops"
   }

创建流程：

#. 验证名称格式（小写字母、数字、连字符、下划线、点，最长 64 字符）。

#. 验证前置元数据完整性（必须有 ``name`` 和 ``description`` ，正文不能为空）。

#. 检查名称是否与已有技能冲突。

#. 创建目录结构并原子写入 SKILL.md。

#. 运行安全扫描，如果检测到危险内容则回滚删除。

edit：编辑技能
================

替换技能的完整 SKILL.md 内容。适用于大幅度重构。

patch：补丁技能
=================

对 SKILL.md 或支持文件进行精确的查找替换。使用模糊匹配引擎（``fuzzy_match.fuzzy_find_and_replace``），处理空白规范化、缩进差异和块锚定匹配。这是推荐的增量修改方式。

.. code-block:: json

   {
     "action": "patch",
     "name": "my-deploy-workflow",
     "old_string": "kubectl apply -f deployment.yaml",
     "new_string": "kubectl apply -f deployment.yaml --namespace=production"
   }

delete：删除技能
==================

永久删除一个用户创建的技能。不支持删除外部目录中的技能。

write_file：写入支持文件
==========================

在技能目录的允许子目录（``references/`` 、``templates/`` 、``scripts/`` 、``assets/``）中创建或替换文件。文件大小限制为 1 MiB。

.. code-block:: json

   {
     "action": "write_file",
     "name": "my-deploy-workflow",
     "file_path": "references/k8s-troubleshooting.md",
     "file_content": "# Kubernetes Troubleshooting Guide\n..."
   }

remove_file：删除支持文件
===========================

从技能目录中删除一个支持文件。

所有修改操作完成后，会清除技能系统提示缓存（``clear_skills_system_prompt_cache``），确保下次构建系统提示时使用最新内容。

原子写入与回滚
================

所有文件写入操作使用原子写入模式（``_atomic_write_text``）：

#. 在同一目录创建临时文件（前缀 ``.<name>.tmp.``）。

#. 写入内容并刷新到磁盘（``os.fsync``）。

#. 使用 ``os.replace()`` 原子替换目标文件。

如果在写入后安全扫描检测到问题，会使用备份内容回滚：

- 对于 ``create`` 操作：删除整个技能目录。

- 对于 ``edit``/``patch``/``write_file`` 操作：恢复原始文件内容。

****************************
5. 技能索引构建
****************************

技能索引通过 ``build_skills_system_prompt()`` 函数构建，注入到系统提示的 ``<available_skills>`` 段落中。这个索引是 Agent "知道"哪些技能可用的重要入口。

索引内容
==========

索引为每个技能提供最精简的元数据——名称和描述。这遵循"渐进式披露"原则：在系统提示中只包含足够的信息让 LLM 知道技能的存在，具体内容通过 ``skill_view()`` 按需加载。

条件激活
==========

技能的激活受多种条件控制：

- **平台过滤** ：``platforms`` 字段不匹配当前平台时，技能不出现在索引中。

- **禁用列表** ：用户在 ``config.yaml`` 的 ``skills.disabled`` 或 ``skills.platform_disabled`` 中列出的技能被过滤。

- **fallback_for** ：当指定的工具集不可用时，该技能作为替代被推荐。这允许技能在没有对应 MCP 服务器的情况下提供手动操作指南。

- **requires_toolsets** ：仅在指定的工具集可用时才激活。这防止了技能在缺少必要工具的情况下被推荐。

索引缓存
==========

技能索引使用内存缓存，避免每次构建系统提示时重新扫描文件系统。当技能被创建、修改或删除时，缓存被清除。

********************
6. 同步机制
********************

内置技能的同步由 ``tools/skills_sync.py`` 中的 ``sync_skills()`` 函数负责。它使用基于清单（manifest）的策略，确保用户的自定义修改不会被意外覆盖。

清单格式
==========

清单文件位于 ``~/.hermes/skills/.bundled_manifest`` ，采用 v2 格式——每行是 ``skill_name:origin_hash`` ，其中 ``origin_hash`` 是同步时内置技能目录内容的 MD5 哈希。

.. code-block:: text

   axolotl:a1b2c3d4e5f6...
   deploy-workflow:f6e5d4c3b2a1...
   mlops/training:b1c2d3e4f5a6...

v1 格式（纯技能名称，无哈希）在读取时被自动迁移。

同步策略
==========

对于每个内置技能，同步函数执行以下判断：

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - 状态
     - 条件
     - 操作
   * - 新技能
     - 不在清单中
     - 复制到用户目录，记录哈希
   * - 未修改
     - 用户副本 == origin_hash && 内置副本 == origin_hash
     - 跳过
   * - 有更新
     - 用户副本 == origin_hash && 内置副本 != origin_hash
     - 更新用户副本（先备份），记录新哈希
   * - 用户修改
     - 用户副本 != origin_hash
     - 跳过（保护用户修改）
   * - 用户删除
     - 在清单中但磁盘上不存在
     - 尊重删除，不重新添加
   * - 已移除
     - 在清单中但不在内置目录中
     - 从清单中移除

哈希计算
==========

``_dir_hash()`` 函数递归计算技能目录中所有文件内容的 MD5 哈希，包括相对路径作为哈希输入的一部分。这确保了文件重命名和内容变更都能被检测到。

.. code-block:: python

   def _dir_hash(directory: Path) -> str:
       hasher = hashlib.md5()
       for fpath in sorted(directory.rglob("*")):
           if fpath.is_file():
               rel = fpath.relative_to(directory)
               hasher.update(str(rel).encode("utf-8"))
               hasher.update(fpath.read_bytes())
       return hasher.hexdigest()

原子清单写入
==============

清单文件使用原子写入（临时文件 + ``os.replace``）并调用 ``os.fsync()`` 确保数据在磁盘上持久化，防止在崩溃后丢失同步状态。

重置功能
==========

``reset_bundled_skill()`` 函数允许用户重置某个内置技能的同步状态：

- **仅清除清单** （``restore=False``）：不清除用户的修改，但允许未来的更新被应用。

- **恢复原始版本** （``restore=True``）：删除用户的修改，重新从内置目录复制。

这在用户编辑了内置技能后又想恢复官方版本时特别有用。

类别描述
==========

同步过程还会复制 ``DESCRIPTION.md`` 文件——这些文件为技能类别目录提供人类可读的描述（如 ``~/.hermes/skills/mlops/DESCRIPTION.md``）。

********************
7. 技能缓存
********************

技能系统使用双层缓存策略，在保证数据新鲜度的同时最大化性能。

内存 LRU 缓存
===============

技能内容缓存使用 LRU（Least Recently Used）策略，容量为 8 个条目。当 ``skill_view()`` 被调用时，首先检查内存缓存：

- 命中：直接返回缓存的内容。

- 未命中：从磁盘读取 SKILL.md，存入缓存，返回内容。

磁盘快照缓存
==============

为了加速系统提示中技能索引的构建，技能系统维护一个磁盘快照。快照包含所有技能的元数据（名称、描述、类别），以 JSON 格式存储。

快照的有效性通过 ``mtime`` （修改时间）验证：

#. 检查 ``SKILLS_DIR`` 的 ``st_mtime_ns`` 。

#. 如果与快照记录的时间戳不同，快照失效，重新扫描文件系统。

#. 新扫描的结果更新快照和时间戳。

这一机制确保了在外部修改技能文件（如手动编辑或 ``hermes skills install``）后，索引会在下次构建时自动更新。

缓存清除
==========

以下操作会触发缓存清除：

- ``skill_manage()`` 的任何写操作（create/edit/patch/delete/write_file/remove_file）。

- ``clear_skills_system_prompt_cache(clear_snapshot=True)`` ：同时清除内存索引缓存和磁盘快照。

- 技能同步（``sync_skills()``）完成后，由于目录 mtime 变化，快照自然失效。

平台过滤在缓存层面也生效——即使技能在缓存中，如果 ``platforms`` 字段与当前平台不匹配，也不会出现在结果中。

.. mermaid::

   sequenceDiagram
       participant Agent as Agent
       participant Cache as 内存 LRU 缓存
       participant Disk as 磁盘快照
       participant FS as 文件系统

       Agent->>Cache: skill_view("axolotl")

       alt 缓存命中
           Cache-->>Agent: 返回缓存内容
       else 缓存未命中
           Cache->>FS: 读取 SKILL.md
           FS-->>Cache: 文件内容
           Cache->>Cache: 存入 LRU（淘汰最旧条目）
           Cache-->>Agent: 返回内容
       end

       Note over Agent,Disk: 技能索引构建

       Agent->>Disk: build_skills_system_prompt()
       Disk->>Disk: 检查 mtime

       alt mtime 未变
           Disk-->>Agent: 返回快照索引
       else mtime 已变
           Disk->>FS: 扫描所有 SKILL.md
           FS-->>Disk: 技能元数据
           Disk->>Disk: 更新快照 + mtime
           Disk-->>Agent: 返回新索引
       end

       Note over Agent,FS: skill_manage(create) 后

       Agent->>Cache: clear_skills_system_prompt_cache()
       Cache->>Cache: 清除内存缓存
       Cache->>Disk: 清除磁盘快照
       Cache-->>Agent: 缓存已清除

技能查找策略
==============

``skill_view()`` 使用多级查找策略定位技能文件：

#. **限定名路由** ：如果名称包含 ``:`` （如 ``plugin:skill``），路由到插件技能注册表。

#. **直接路径** ：尝试 ``SKILLS_DIR/NAME/SKILL.md`` 。

#. **递归搜索** ：在所有技能目录中搜索 ``NAME/SKILL.md`` 。

#. **遗留格式** ：搜索 ``NAME.md`` （向后兼容扁平文件格式）。

如果所有查找都失败，返回前 20 个可用技能名称作为建议。

安全检查
==========

技能加载时执行以下安全检查：

- **平台兼容性** ：``skill_matches_platform()`` 检查 ``platforms`` 字段。

- **禁用状态** ：``_is_skill_disabled()`` 检查用户配置。

- **目录安全** ：检查技能文件是否在受信任的目录内。

- **注入检测** ：扫描内容中的常见提示注入模式（``_INJECTION_PATTERNS``），包括 "ignore previous instructions"、"you are now"、"system prompt:" 等。

检测结果记录 WARNING 日志但不阻止加载（避免误报影响可用性）。

总结
======

Hermes Agent 的技能系统是一个精心设计的知识管理框架，其核心特点包括：

- **四种技能来源** （内置 / Hub / 用户 / 插件）满足不同场景的知识积累需求。

- **标准化的 SKILL.md 格式** 兼容 agentskills.io 生态，支持丰富的元数据。

- **渐进式披露架构** 通过三层加载策略优化 token 使用。

- **完善的技能管理** 通过 ``skill_manage`` 工具支持全生命周期操作，包含原子写入、安全扫描和自动回滚。

- **智能同步机制** 使用清单+哈希策略保护用户修改，同时允许官方更新。

- **双层缓存** （内存 LRU + 磁盘快照）在保证数据新鲜度的同时优化性能。

- **条件激活** 通过 triggers、fallback_for 和 requires_toolsets 实现技能的智能匹配。

技能系统将 Agent 从一个"每次从零开始"的工具转变为一个"积累经验、越用越强"的智能助手。
