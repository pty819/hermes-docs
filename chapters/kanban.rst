.. _chapter-kanban:

#################################################
Kanban：多 Profile 协作的任务看板
#################################################

.. contents::
   :local:
   :depth: 2

为什么 Agent 需要 Kanban
==========================

单 Agent 的局限
~~~~~~~~~~~~~~~~~

到目前为止，我们讨论的所有子系统——Agent 主循环、工具调用、上下文压缩、
会话管理——都是围绕 **单个 Agent 进程** 设计的。一个 ``AIAgent`` 实例，
一次对话，一套工具，一个模型。

这在很多场景下足够了：用户提问，Agent 回答；用户要求写代码，Agent 调用工具完成。
但当你面对的是一个 **复杂的多步骤工程任务** 时，单 Agent 模式很快就暴露出瓶颈：

- **上下文窗口限制**：一个 200K token 的窗口听起来很大，但当你在一个长对话中
  既要理解整个项目架构、又要修改多个文件、又要运行测试时，上下文很快就会溢出
- **任务分解困难**：一个"重构认证模块"的任务可以分解为"分析依赖 → 修改接口 →
  更新调用方 → 迁移测试 → 验证集成"，但让单个 Agent 在一次对话中完成所有这些
  步骤，质量会随着对话长度下降
- **并行性缺失**：三个独立的 bug fix 可以并行进行，但单 Agent 只能串行处理
- **持久性不足**：Agent 进程崩溃或用户关闭终端，进行中的工作就丢失了

Hermes Kanban 的设计目标
~~~~~~~~~~~~~~~~~~~~~~~~~~

Hermes Kanban 是一个 **持久化的、SQLite 驱动的多 Agent 协作任务看板**。
它的核心理念可以用一句话概括：

    每个任务是 SQLite 中的一行；每次交接是任何人都能读写的一行；
    每个 Worker 是一个拥有独立身份和持久记忆的完整 OS 进程。

这不是一个轻量级的子代理（subagent）框架——子代理在父进程内运行，
共享上下文窗口，父进程崩溃则全部丢失。Kanban 的每个 Worker 都是
通过 ``hermes -p <profile>`` 启动的 **独立 Hermes 进程**，拥有自己的
模型配置、技能栈、记忆系统和工作空间。

设计决策：SQLite 而非消息队列
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

为什么选择 SQLite 而不是 Redis、RabbitMQ 或 Celery？

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 特性
     - SQLite (Kanban)
     - 消息队列
   * - 部署
     - 零配置，单文件（``~/.hermes/kanban.db``）
     - 需要独立服务进程
   * - 持久性
     - WAL 模式下的完整 ACID 事务
     - 需要额外配置持久化
   * - 查询能力
     - SQL 全文检索、聚合、JOIN
     - 只能按队列消费
   * - 并发控制
     - CAS（Compare-And-Swap）原子更新
     - 需要 ACK/NACK 协议
   * - 可观测性
     - 直接 ``SELECT *`` 查看所有任务状态
     - 需要专门的监控工具
   * - 单机场景
     - 完美匹配（Hermes 是单主机工具）
     - 过度设计

Kanban 的 SQLite 选型与第 :ref:`chapter-session-state` 章中 SessionDB 的选型
一脉相承——都是"单主机、零依赖、SQL 查询能力"的工程权衡。

架构总览
==========

三大接入面，一条代码路径
~~~~~~~~~~~~~~~~~~~~~~~~~~

Kanban 系统有三个用户可见的接入面，但它们共享同一个 ``kanban_db`` 模块：

核心层
~~~~~~~~~~

Kanban 的核心代码由四个模块组成：

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - 模块
     - 行数
     - 职责
   * - ``kanban_db.py``
     - ~5100
     - SQLite 持久化层：schema、数据模型、CAS claim、生命周期转换、调度循环、Worker spawn
   * - ``kanban.py``
     - ~2300
     - CLI 入口、argparse 子命令、命令调度、输出格式化
   * - ``kanban_diagnostics.py``
     - ~800
     - 诊断规则引擎（6 条规则）
   * - ``kanban_specify.py``
     - ~270
     - Specify 功能：辅助 LLM 展开模糊任务

.. mermaid::
   :name: kanban-system-architecture
   :caption: Kanban 系统架构

   flowchart TD
       subgraph entry["接入层"]
           CLI["hermes kanban &lt;verb&gt;<br/>CLI 命令行"]
           TOOL["kanban_* 工具调用<br/>Agent Tool-Call"]
           DASH["Dashboard<br/>React SPA + REST API"]
       end

       subgraph core["核心层"]
           KDB["kanban_db.py<br/>SQLite 持久化 + 生命周期"]
           DIAG["kanban_diagnostics.py<br/>诊断规则引擎"]
           SPEC["kanban_specify.py<br/>Specify 任务展开"]
       end

       subgraph storage["存储层"]
           DB["~/.hermes/kanban.db<br/>WAL 模式"]
           FS["~/.hermes/kanban/<br/>boards/ workspaces/ logs/"]
       end

       subgraph runtime["运行时"]
           DISP["Dispatcher<br/>调度循环 (60s)"]
           WORKER["Worker 进程<br/>hermes -p &lt;name&gt;"]
       end

       CLI --> KDB
       TOOL --> KDB
       DASH --> KDB
       KDB --> DB
       KDB --> FS
       KDB --> DIAG
       KDB --> SPEC
       KDB --> DISP
       DISP --> WORKER
       WORKER -->|"env: HERMES_KANBAN_*"| KDB
       SPEC -->|"辅助 LLM"| KDB

关键设计决策：

1. **三接入面统一**：CLI（``hermes kanban create``）、工具调用（``kanban_create``）、
   Dashboard REST API 最终都调用 ``kanban_db`` 中的同一组函数。
   读取看到一致的视图；写入不会出现分歧。

2. **调度器内嵌 Gateway**：默认配置 ``kanban.dispatch_in_gateway: true``，
   调度循环运行在 Gateway 进程内部，每 60 秒 tick 一次。

3. **WAL + CAS 并发**：SQLite WAL 模式 + ``BEGIN IMMEDIATE`` 写事务 +
   ``claim_lock`` 的 Compare-And-Swap 更新，确保同一时刻只有一个 claimer
   能赢得某个任务。失败者看到零受影响行，直接跳过——不需要重试循环，
   不需要分布式锁。

4. **多 Board 隔离**：每个 Board 有独立的 SQLite 数据库、工作空间目录和日志目录。
   Worker 通过 ``HERMES_KANBAN_BOARD`` 环境变量只看到自己 Board 的任务。

数据模型
----------

Kanban 的数据模型围绕 **任务（Task）** 构建，辅以 **执行记录（Run）**、
**依赖链接（Link）**、**评论（Comment）**、**事件（Event）** 五张核心表。

tasks 表
^^^^^^^^^

``tasks`` 表是 Kanban 的核心，每行代表一个任务：

.. code-block:: sql

    CREATE TABLE tasks (
        id TEXT PRIMARY KEY,                    -- 任务 ID，如 t_a1b2c3d4
        title TEXT NOT NULL,                    -- 简短标题
        body TEXT,                              -- 完整规格说明（Markdown）
        assignee TEXT,                          -- 执行 Profile 名称
        status TEXT DEFAULT 'ready',            -- 状态机
        priority INTEGER DEFAULT 0,             -- 调度优先级（越大越先）
        created_by TEXT,                        -- 创建者（用户/Worker/Profile）
        created_at INTEGER,                     -- Unix 时间戳
        started_at INTEGER,                     -- 首次被 claim 的时间
        completed_at INTEGER,                   -- 移入 done 的时间
        workspace_kind TEXT DEFAULT 'scratch',  -- scratch | worktree | dir
        workspace_path TEXT,                    -- 解析后的工作空间路径
        claim_lock TEXT,                        -- CAS claim 令牌
        claim_expires INTEGER,                  -- Claim TTL 到期时间
        tenant TEXT,                            -- 可选的多租户命名空间
        result TEXT,                            -- 简短结果文本
        idempotency_key TEXT,                   -- 幂等键（重试去重）
        consecutive_failures INTEGER DEFAULT 0, -- 统一失败计数器
        worker_pid INTEGER,                     -- Worker 进程 PID
        last_failure_error TEXT,                -- 最近一次失败的错误摘要
        max_runtime_seconds INTEGER,            -- 单次运行时间上限
        last_heartbeat_at INTEGER,              -- 最近心跳时间
        current_run_id INTEGER,                 -- 当前 task_runs 外键
        skills TEXT,                            -- JSON：强制加载的技能列表
        UNIQUE(idempotency_key) WHERE idempotency_key IS NOT NULL
    );

**状态机**

任务的生命周期由一个七状态状态机管理：

.. mermaid::
   :name: kanban-task-states
   :caption: 任务状态转换

   stateDiagram-v2
       [*] --> triage: --triage 标志
       [*] --> ready: 无 parent 或全部 parent done
       [*] --> todo: 有未完成的 parent

       triage --> todo: 指定了 assignee
       triage --> ready: 指定了 assignee 且无未完成 parent

       todo --> ready: 所有 parent 完成 (promoted)
       ready --> running: CAS claim 成功

       running --> done: kanban_complete()
       running --> blocked: kanban_block()
       running --> ready: claim 过期 / 崩溃 / 超时

       blocked --> ready: kanban_unblock()
       blocked --> done: kanban_complete()

       done --> archived: kanban archive

每个状态的含义：

- **triage**：模糊想法，等待分配。创建时指定 ``--triage`` 标志
- **todo**：有明确的 assignee，但存在未完成的 parent 依赖，暂不调度
- **ready**：可以被调度器 claim 的就绪状态
- **running**：已被 claim，Worker 进程正在执行
- **blocked**：Worker 主动报告无法继续，附带原因
- **done**：任务完成，附带结果和摘要
- **archived**：已归档，不出现在默认列表中

task_runs 表
^^^^^^^^^^^^^^

每次任务被执行（或重新执行），都会产生一条 ``task_runs`` 记录。
这使得任务的历史执行轨迹完全可追溯：

.. code-block:: sql

    CREATE TABLE task_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT NOT NULL REFERENCES tasks(id),
        profile TEXT,                    -- 执行的 Profile 名称
        status TEXT,                     -- running | done | blocked | crashed | timed_out
        claim_lock TEXT,                 -- 本次 run 的 claim 令牌
        claim_expires INTEGER,
        worker_pid INTEGER,              -- Worker 进程 PID
        max_runtime_seconds INTEGER,
        last_heartbeat_at INTEGER,
        started_at INTEGER,              -- run 开始时间
        ended_at INTEGER,                -- run 结束时间（活跃时为 NULL）
        outcome TEXT,                    -- completed | blocked | crashed | timed_out | spawn_failed | gave_up | reclaimed
        summary TEXT,                    -- 结构化的交接摘要（下游 Worker 可见）
        metadata TEXT,                   -- JSON：自由格式的事实（changed_files, tests_run 等）
        error TEXT                       -- 失败时的错误文本
    );

``summary`` 字段是 Worker 之间的关键交接机制。当一个任务完成时，
Worker 在 ``summary`` 中写下做了什么、改了哪些文件、有什么注意事项。
下游 Worker（如依赖此任务的后续任务）在启动时会读取所有 parent 的
``summary``，获得隐式的上下文传递。

task_links 表
^^^^^^^^^^^^^^

依赖关系通过 ``task_links`` 表建模为简单的父子边：

.. code-block:: sql

    CREATE TABLE task_links (
        parent_id TEXT NOT NULL REFERENCES tasks(id),
        child_id TEXT NOT NULL REFERENCES tasks(id),
        PRIMARY KEY (parent_id, child_id)
    );

依赖机制的核心规则：

- 创建任务时指定 ``--parent t_xxx``，如果 parent 尚未 ``done``，
  新任务以 ``todo`` 状态创建
- 当所有 parent 都变为 ``done`` 时，``todo`` 任务自动提升为 ``ready``
  （``recompute_ready()`` 函数）
- 添加依赖边时进行 **环检测**——不允许创建循环依赖
- **不允许跨 Board 链接**——保持 schema 简洁和 Board 隔离
- **已归档的 parent 视为终态**——当 parent 处于 ``archived`` 状态时，
  不阻塞子任务的依赖解析（等价于 ``done``），防止已归档的工作流
  意外阻塞后续任务
- 删除依赖边后自动触发 ``recompute_ready()``——确保因依赖被移除
  而变为可执行的任务立即获得提升

task_comments 和 task_events 表
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

    CREATE TABLE task_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT NOT NULL,
        author TEXT NOT NULL,
        body TEXT NOT NULL,
        created_at INTEGER
    );

    CREATE TABLE task_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT NOT NULL,
        run_id INTEGER,
        kind TEXT NOT NULL,              -- 事件类型
        payload TEXT,                    -- JSON 负载
        created_at INTEGER
    );

``task_events`` 是 Kanban 的审计日志。每次状态变更、claim、释放、完成、
失败、阻塞都会写入一条事件。Dashboard 的 WebSocket 实时更新就是通过
tail 这张表实现的。

Specify：辅助 LLM 展开模糊任务
=================================

``kanban_specify.py`` 是 Kanban 系统的一个独特组件，它解决了
"triage 到 ready 之间的鸿沟"问题。

问题场景：用户通过 ``--triage`` 标志创建了一个模糊的任务想法
（例如"优化首页加载速度"），但没有指定具体的执行步骤、assignee 或
验收标准。这个任务停留在 ``triage`` 状态，等待人工细化。

Specify 功能利用 **辅助 LLM** 自动将模糊的 triage 任务展开为
结构化的执行计划：

.. mermaid::
   :name: kanban-specify-flow
   :caption: Specify 任务展开流程

   flowchart LR
       TRIAGE["triage 任务<br/>模糊想法"] -->|"specify"| AUX["辅助 LLM<br/>任务分析"]
       AUX --> PLAN["结构化输出<br/>title + body + skills"]
       PLAN --> READY["ready 任务<br/>可调度"]

Specify 的处理流程：

1. **读取 triage 任务**：获取标题和已有的 body 内容
2. **构建 Specify 提示词**：将任务信息、可用 Profile 列表和
   技能目录注入到提示词中
3. **调用辅助 LLM**：使用 ``auxiliary_client.call_llm()`` 让模型
   分析任务并输出结构化建议
4. **更新任务**：将 LLM 生成的详细描述、建议的 assignee 和技能
   写回任务记录

Specify 的关键设计决策：

- **幂等安全**：多次 specify 同一任务不会产生重复内容
- **辅助模型选择**：使用 ``resolve_provider_client()`` 的自动检测链，
   无需为 Specify 配置专用模型
- **写入隔离**：Specify 只更新 ``body`` 和 ``skills`` 字段，
   不修改 ``status``（状态转换仍由人工或 Orchestrator 控制）

Specify 在 CLI 中通过 ``hermes kanban specify <task_id>`` 调用，
也可以在 Dashboard 中通过按钮触发。

调度器：核心循环
==================

调度器是 Kanban 的"大脑"——一个每 60 秒执行一次的 tick 循环，
负责将就绪任务分配给合适的 Worker。

Tick 循环的五个阶段
~~~~~~~~~~~~~~~~~~~~~

.. mermaid::
   :name: kanban-dispatcher-tick
   :caption: 调度器 Tick 循环

   flowchart LR
       A["1. 回收过期 Claim"] --> B["2. 检测崩溃 Worker"]
       B --> C["3. 执行超时上限"]
       C --> D["4. 提升依赖任务"]
       D --> E["5. Claim 并 spawn"]

**阶段 1：回收过期 Claim**

Worker 的 claim 有 15 分钟的 TTL（``DEFAULT_CLAIM_TTL_SECONDS = 900``）。
如果 Worker 在 TTL 内没有调用 ``heartbeat`` 延长 claim，调度器将其
状态从 ``running`` 重置为 ``ready``，outcome 设为 ``reclaimed``。

.. code-block:: python

    # 伪代码：回收过期 claim
    UPDATE tasks SET status = 'ready', claim_lock = NULL
    WHERE status = 'running'
      AND claim_expires < :now
      AND current_run_id IN (
          SELECT id FROM task_runs WHERE status = 'running'
      );

**阶段 2：检测崩溃 Worker**

通过检查 ``worker_pid`` 对应的进程是否仍然存活（``os.kill(pid, 0)``），
发现已崩溃的 Worker 并回收其任务。

**阶段 3：执行超时上限**

每个任务可以设置 ``max_runtime_seconds``。如果当前 run 的运行时间
超过此限制，调度器会向 Worker 发送 ``SIGTERM``（5 秒后 ``SIGKILL``），
将任务标记为 ``timed_out`` 并重新放入 ``ready`` 队列。

**阶段 4：提升依赖任务**

扫描所有 ``todo`` 状态的任务，检查其 parent 是否全部 ``done``。
如果是，将任务提升为 ``ready`` 并写入 ``promoted`` 事件。

.. code-block:: python

    # 伪代码：提升依赖任务
    def recompute_ready():
        for task in get_tasks_by_status('todo'):
            parents = get_parent_tasks(task.id)
            if all(p.status == 'done' for p in parents):
                update_status(task.id, 'ready')
                emit_event(task.id, 'promoted')

**阶段 5：Claim 并 Spawn**

对于每个 ``ready`` 且有有效 assignee 的任务：

1. 验证 assignee 存在为真实 Profile（``hermes -p <name>``）
2. 原子 CAS claim（``ready → running``）
3. 解析工作空间（scratch / worktree / dir）
4. spawn Worker 子进程

**调度并发上限**

``max_spawn`` 配置参数的含义是 **活跃 Worker 的并发上限**，而非每个 tick 的
spawn 预算。调度器在 spawn 新 Worker 前会检查当前正在运行的 Worker 数量
（通过 ``worker_pid`` 的进程存活检测），只有运行中的 Worker 少于
``max_spawn`` 时才会 spawn 新的。这防止了在短暂 tick 间隔内过度启动。

当 ``max_spawn`` 为 ``null``（默认）时，不限制并发数。

Orchestrator 的 Step-0 Profile 发现
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kanban Orchestrator 的技能（``kanban-orchestrator``）经历了一次重要的重构：
**硬编码的专家名单被移除**，取而代之的是 **Step-0 Profile 发现**。

旧设计：Orchestrator 技能中硬编码了一组预定义的专家角色（如 "frontend-dev"、
"backend-dev"、"tester"），Orchestrator 在分解任务时只能从这组角色中选择。

新设计：Orchestrator 在开始工作前（Step-0），动态扫描系统中所有可用的 Profile
及其配置的工具集和技能。这意味着：

- 用户新增的 Profile 自动被 Orchestrator 发现
- Profile 的工具集变更实时反映到任务分解中
- 不需要修改 Orchestrator 技能就能支持新的专家角色

这一改变使 Kanban 系统从"预定义流水线"转变为"自适应编排"。

Worker Spawn 机制
~~~~~~~~~~~~~~~~~~~

调度器通过 ``_default_spawn`` 函数启动 Worker。Worker 子进程使用
``sys.executable -m hermes`` 的形式启动，确保在虚拟环境和非标准安装路径下
都能正确找到 Hermes 入口：

.. code-block:: python

    # Worker 启动命令
    sys.executable -m hermes -p <assignee> --skills kanban-worker [--skills <extra>] chat -q "work kanban task <id>"

Worker 子进程通过环境变量获得所有必要上下文：

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 环境变量
     - 含义
   * - ``HERMES_KANBAN_TASK``
     - 当前任务 ID
   * - ``HERMES_KANBAN_WORKSPACE``
     - 解析后的工作空间目录
   * - ``HERMES_KANBAN_RUN_ID``
     - 当前 task_runs ID
   * - ``HERMES_KANBAN_CLAIM_LOCK``
     - claim 令牌
   * - ``HERMES_KANBAN_DB``
     - 数据库文件路径
   * - ``HERMES_KANBAN_BOARD``
     - Board slug（隔离作用域）
   * - ``HERMES_TENANT``
     - 租户命名空间（可选）
   * - ``HERMES_PROFILE``
     - 作者归因

Worker 的 stdout/stderr 被重定向到 ``<board-root>/logs/<task_id>.log``，
支持单代轮转。

失败熔断器
~~~~~~~~~~~

连续失败不是无限容忍的。``consecutive_failures`` 计数器统一统计
spawn 失败、超时、崩溃三类非成功结果。当计数达到
``DEFAULT_SPAWN_FAILURE_LIMIT``（5）时，任务被自动阻塞（``blocked``），
附带最后一次失败的错误信息作为原因。

计数器只在 **成功完成** 时归零（不是成功 spawn）——这防止了
"spawn 成功但立刻崩溃"的无限循环。

**逐任务重试上限**

每个任务可以通过 ``max_retries`` 字段覆盖全局的 ``dispatch_failure_limit``。
当任务有明确的 ``max_retries`` 设置时，使用任务级别的值而非全局默认的 5 次。
这允许对关键任务（如部署脚本）和实验性任务设置不同的容错阈值。

Worker 安全防护
~~~~~~~~~~~~~~~

Kanban 在 Worker 生命周期中加入了多层安全防护，确保异常情况不会导致
任务永久卡住：

**退出即阻塞**：当 Worker 进程退出但未调用 ``kanban_complete()``
或 ``kanban_block()`` 时（即"静默退出"），调度器会自动调用
``kanban_block()`` 将任务标记为 ``blocked``，附带原因 "Worker exited
without completing"。这防止了任务在 Worker 崩溃后无限停留在 ``running`` 状态。

**迭代预算耗尽自动阻塞**：当 Worker 因 Agent 的迭代预算耗尽（``max_iterations``
达到上限）而被迫停止时，系统会调用 ``kanban_block()`` 而非简单地退出，
确保任务不会因预算耗尽而丢失进度信息。

**Claim TTL 延伸**：心跳工具（``kanban_heartbeat``）现在不仅更新
``last_heartbeat_at`` 时间戳，还会实际延伸 ``claim_expires`` 的 TTL。
这确保了长时间运行的任务（如编译大型项目）不会被调度器因 TTL 过期而回收。

**Stale Claim 优雅处理**：当调度器发现某个 claim 已过期，但对应的
Worker 进程仍然存活时，不再直接杀死 Worker 回收任务，而是 **延伸过期的 claim**。
这避免了因调度器 tick 延迟导致的误回收——Worker 可能在处理一个耗时的操作，
心跳稍有延迟但不应该被中断。

**通知去重**：当任务进入 ``blocked`` 或 ``gave_up`` 状态时，
通知系统现在会去重投递声明（delivery claims），防止同一个状态变更事件
产生重复通知。

Worker 生命周期
=================

从 Worker Agent 的视角看，一个任务的完整生命周期是这样的：

.. code-block:: text

    1. 被 spawn → Agent 启动 → 调用 kanban_show() 读取任务详情
       （标题、body、parent 交接摘要、历史尝试、评论）

    2. cd $HERMES_KANBAN_WORKSPACE → 开始工作

    3. 对于长时间操作，定期调用 kanban_heartbeat(note="...")
       延长 claim TTL

    4. 完成时调用 kanban_complete(summary="...", metadata={...})
       或者遇到阻塞时调用 kanban_block(reason="...")

    5. 如果是 Orchestrator，调用 kanban_create(...) 分发子任务，
       然后调用 kanban_complete(...) 完成自己的任务

Kanban 工具集
~~~~~~~~~~~~~~

Worker 通过七个 ``kanban_*`` 工具与看板交互。这些工具通过
``tools/registry.py`` 注册，但只在满足以下条件之一时才出现在
模型的工具 schema 中：

- ``HERMES_KANBAN_TASK`` 环境变量已设置（Dispatcher spawn 的 Worker）
- Profile 的 toolset 配置中包含 ``kanban``（Orchestrator Profile）

普通 ``hermes chat`` 会话看不到任何 kanban 工具——这是通过
``check_fn`` 可见性守卫实现的。

七个工具及其职责：

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - 工具名
     - 功能
   * - ``kanban_show``
     - 读取任务详情（标题、body、parent 交接、历史 run、评论）
   * - ``kanban_complete``
     - 标记任务完成，附带 summary 和 metadata
   * - ``kanban_block``
     - 报告阻塞，附带原因
   * - ``kanban_heartbeat``
     - 延长 claim TTL，附带进度说明
   * - ``kanban_create``
     - 创建子任务（用于 fan-out 模式）
   * - ``kanban_link``
     - 建立任务依赖关系
   * - ``kanban_list``
     - 列出 Board 上的任务（可按状态、assignee 过滤）

Worker 的交接上下文
~~~~~~~~~~~~~~~~~~~~~

Worker 启动时，``build_worker_context()`` 函数组装一份上下文注入：

- 任务的标题和 body
- 所有 parent 的完成摘要（``task_runs.summary``）
- 同一 assignee 最近 5 次已完成 run 的历史（隐式连续性）
- 任务的评论列表

这份上下文让 Worker 不需要"从零开始"——它能立即理解任务的背景和
前置工作的结果。

幻觉门控
~~~~~~~~~~

Kanban 有一个独特的安全机制：**幻觉门控（Hallucination Gate）**。

当 Worker 调用 ``kanban_complete`` 时，如果声称通过 ``created_cards``
创建了子任务，系统会逐一验证这些 ID 是否真实存在于数据库中
（且确实是该 Worker 的 Profile 创建的）。如果发现不存在的 ID
（幻觉），完成操作会被 **阻止**，并写入 ``completion_blocked_hallucination``
审计事件。

此外，系统还会对完成摘要的文本进行扫描，检查是否引用了不存在的
``t_<hex>`` 格式 ID。这类引用产生 ``suspected_hallucinated_references``
警告事件（非阻塞）。

这个机制解决了一个真实问题：LLM 有时会在完成报告中"捏造"子任务 ID，
让 Orchestrator 误以为 fan-out 已成功。幻觉门控确保了任务图的完整性。

评论安全
~~~~~~~~~~

Kanban 的评论系统有一个重要的安全约束：``kanban_comment`` 工具的
``author`` 字段 **不接受调用者控制的覆盖**。作者身份始终从
Worker 的 Profile 配置（``HERMES_PROFILE`` 环境变量）中获取，
防止恶意 Worker 冒充其他 Profile 发表评论。

Orchestrator Board 工具
~~~~~~~~~~~~~~~~~~~~~~~~~

Kanban 新增了一组 **Board 级别的 Orchestrator 工具**，这些工具只对
配置为 Orchestrator 的 Profile 可见（通过 ``check_fn`` 守卫）：

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - 工具名
     - 功能
   * - ``kanban_board_create``
     - 创建新 Board，可指定名称和描述
   * - ``kanban_board_switch``
     - 切换当前活跃的 Board
   * - ``kanban_board_list``
     - 列出所有 Board 及其状态摘要
   * - ``kanban_board_show``
     - 查看当前 Board 的详细信息

这些工具使 Orchestrator 能够在运行时动态管理 Board，实现跨 Board 的
任务编排——例如，在一个 Board 上创建规划任务，在另一个 Board 上创建
执行任务。

技能验证
~~~~~~~~~

当任务的 ``skills`` 字段包含无效的工具集名称（如拼写错误的 ``web-serach``）
时，系统会 **聚合所有拼写错误** 在一条错误消息中报告，而非遇到第一个错误
就中断。这让 Worker 和 Orchestrator 能一次性修正所有问题。

CLI 命令参考
==============

Kanban 通过 ``hermes kanban <verb>`` 暴露了 30+ 个 CLI 子命令，
也可以通过 Gateway 的 ``/kanban <verb>`` 斜杠命令使用。

Board 管理
~~~~~~~~~~~

.. code-block:: bash

    # 初始化 Kanban 数据库，发现已有的 Profile
    hermes kanban init

    # 创建新 Board
    hermes kanban boards create backend-fixes --name "后端修复" --switch

    # 列出所有 Board
    hermes kanban boards list [--all] [--json]

    # 切换当前 Board
    hermes kanban boards switch backend-fixes

    # 查看当前 Board
    hermes kanban boards show

任务生命周期
~~~~~~~~~~~~~

.. code-block:: bash

    # 创建任务（默认状态：ready）
    hermes kanban create "修复登录超时" \
        --body "用户报告登录页面在高并发下超时" \
        --assignee backend-dev \
        --priority 10

    # 创建 triage 状态的任务（模糊想法）
    hermes kanban create "调查性能问题" --triage

    # 创建带依赖的任务
    hermes kanban create "集成测试" --parent t_a1b2 --parent t_c3d4

    # 列出任务
    hermes kanban list [--mine] [--assignee <name>] [--status running]

    # 查看任务详情
    hermes kanban show t_a1b2c3d4

    # 完成任务（支持批量）
    hermes kanban complete t_a1b2 t_c3d4 --result "已修复" --summary "..."

    # 阻塞任务
    hermes kanban block t_a1b2 "需要 API 密钥"

    # 解除阻塞
    hermes kanban unblock t_a1b2 t_c3d4

    # 归档任务
    hermes kanban archive t_a1b2

Worker 操作
~~~~~~~~~~~~

.. code-block:: bash

    # 原子 claim（通常由调度器自动执行）
    hermes kanban claim t_a1b2 --ttl 900

    # 心跳延长 claim
    hermes kanban heartbeat t_a1b2 --note "正在运行测试..."

    # 释放 claim，重置为 ready
    hermes kanban reclaim t_a1b2 --reason "需要人工干预"

    # 重新分配
    hermes kanban reassign t_a1b2 frontend-dev --reclaim

可观测性
~~~~~~~~~

.. code-block:: bash

    # 跟踪单个任务的事件流
    hermes kanban tail t_a1b2 --interval 5

    # 实时监控所有事件
    hermes kanban watch [--assignee <name>] [--tenant <t>]

    # 查看统计
    hermes kanban stats

    # 查看执行历史
    hermes kanban runs t_a1b2

    # 查看 Worker 日志
    hermes kanban log t_a1b2 --tail

    # 查看 Worker 可见的上下文
    hermes kanban context t_a1b2

    # 运行诊断
    hermes kanban diagnostics [--severity error] [--task t_a1b2]

所有命令都支持 ``--json`` 输出（机器可解析）和 ``--board <slug>``
（临时作用域到指定 Board）。

诊断引擎
==========

Kanban 内置了一个 **无状态、只读的诊断规则引擎**
（``hermes_cli/kanban_diagnostics.py``），在 Board 加载、任务查询或
手动运行 ``hermes kanban diagnostics`` 时执行。

六条诊断规则
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - 规则名
     - 严重性
     - 描述
   * - ``hallucinated_cards``
     - error
     - Worker 的 ``kanban_complete(created_cards=[...])`` 包含不存在的任务 ID。
       完成被阻止。成功完成后自动清除。
   * - ``prose_phantom_refs``
     - warning
     - 完成摘要文本中引用了不存在的 ``t_<hex>`` ID。仅建议，不阻塞。
   * - ``repeated_failures``
     - error/critical
     - ``consecutive_failures`` 计数器上升（阈值：3）。按最近失败类型分类
       （spawn_failed / timed_out / crashed）并给出恢复建议。
   * - ``repeated_crashes``
     - error/critical
     - Worker 能 spawn 但持续崩溃（阈值：2）。建议检查日志。
   * - ``stuck_in_blocked``
     - warning
     - 任务被阻塞超过 24 小时，且没有评论或 unblock 操作。
   * - ``stranded_in_ready``
     - warning
     - 任务处于 ``ready`` 状态且已分配 assignee，但长时间未被 claim（#23578）。
       通常表示调度器未运行或 Profile 配置有误。

每条诊断携带 **结构化的恢复操作**（reclaim、reassign、CLI 提示、文档链接），
Dashboard 将其渲染为按钮，CLI 将其渲染为提示文本。

Dashboard UI
==============

Kanban Dashboard 是一个标准的 Hermes Dashboard 插件
（``plugins/kanban/dashboard/``），通过 ``hermes dashboard`` 打开。

看板视图
~~~~~~~~~

Dashboard 的核心是一个 **列式看板**，列对应任务状态：

``triage`` → ``todo`` → ``ready`` → ``running`` → ``blocked`` → ``done``

（``archived`` 通过工具栏开关切换显示）

每张卡片展示：任务 ID、标题、优先级徽标、租户标签、分配的 Profile、
评论/链接计数、子任务进度（N/M children done）、创建时间。

交互功能
~~~~~~~~~

- **拖拽**：在列之间拖拽卡片会触发状态转换（PATCH 请求）。
  支持多卡拖拽——选中多张卡片后一起拖到目标列，带有视觉反馈
- **内联创建**：任何列标题都可以快速创建任务。标题输入框支持多行文本
  （``textarea``），用 ``Shift+Enter`` 换行，``Enter`` 提交
- **多选与批量操作**：支持三种多选方式——单击选择、
  ``Shift+Click`` 范围选择、列标题的全选切换。批量操作包括状态变更、
  归档和重新分配（支持 ``reclaim_first`` 参数：优先回收已有的任务再分配新任务）
- **侧边抽屉**：点击卡片打开详情——可编辑标题/assignee/优先级、
  Markdown 渲染的 body、依赖编辑器、状态操作行、结果区、评论线程、
  事件日志、运行历史。运行历史的元数据面板使用原生 ``<details>``
  折叠元素，自动跳过空字段
- **Per-Profile 泳道**：Running 列内按 Profile 分组显示
- **工具栏过滤**：全文搜索、租户下拉、assignee 下拉、"显示已归档"开关、
  "nudge dispatcher" 按钮
- **工具提示与文档链接**：每个状态列标题提供上下文帮助提示和文档链接
- **主题兼容**：代码块和预格式化文本的样式在所有主题下保持一致

实时更新
~~~~~~~~~

Dashboard 通过 WebSocket 连接 tail ``task_events`` 表。
事件突发时触发单次 refetch；查看某个任务的抽屉在收到该任务的新事件时自动刷新。

REST API
~~~~~~~~~

所有路由挂载在 ``/api/plugins/kanban/``：

.. list-table::
   :header-rows: 1
   :widths: 10 40 50

   * - 方法
     - 路径
     - 功能
   * - GET
     - ``/board?tenant=&include_archived=``
     - 按状态分组的完整看板
   * - GET
     - ``/tasks/:id``
     - 任务 + 评论 + 事件 + 链接
   * - POST
     - ``/tasks``
     - 创建任务
   * - PATCH
     - ``/tasks/:id``
     - 更新字段
   * - POST
     - ``/tasks/bulk``
     - 批量操作
   * - POST
     - ``/tasks/:id/comments``
     - 添加评论
   * - POST
     - ``/links``
     - 添加依赖
   * - DELETE
     - ``/links``
     - 删除依赖
   * - POST
     - ``/dispatch``
     - 触发调度器
   * - WS
     - ``/events?since=``
     - 实时事件流

集成点
========

Kanban 不是一个孤立的系统——它与 Hermes 的多个子系统深度集成。

Gateway 集成
~~~~~~~~~~~~~~

- 调度器默认内嵌在 Gateway 进程中（``kanban.dispatch_in_gateway: true``）
- ``/kanban <verb>`` 斜杠命令在所有 Gateway 平台（Telegram、Discord、Slack、
  WhatsApp、Signal 等）可用
- ``/kanban`` 被显式豁免于 Gateway 的 "running-agent guard"——即使有 Agent
  正在处理请求，你仍然可以操作看板
- 从 Gateway 创建的任务自动订阅源 chat 的终端事件通知

Profile 系统集成
~~~~~~~~~~~~~~~~~

- Worker 通过 ``hermes -p <assignee>`` 启动——每个 Worker 是一个命名 Profile，
  拥有自己的模型、记忆、技能和工具集配置
- Orchestrator Profile 通常配置受限工具集（kanban + gateway + memory），
  只负责路由不负责执行
- 调度器在 spawn 前验证 assignee 是否为真实存在的 Profile——跳过不存在的
  Profile 防止崩溃循环

Skills 系统集成
~~~~~~~~~~~~~~~~

- 每个被调度的 Worker 自动加载 ``kanban-worker`` 技能（通过 ``--skills kanban-worker``）
- 额外技能可以通过创建任务时的 ``--skill`` 参数或 ``kanban_create`` 工具的
  ``skills`` 字段指定
- ``kanban-orchestrator`` 技能教会 Orchestrator Profile 如何分解任务

通知系统集成
~~~~~~~~~~~~~~

``kanban_notify_subs`` 表存储每个任务的通知订阅（platform + chat + thread）。
终端事件（completed、blocked、gave_up、crashed、timed_out）被投递到
已订阅的 Gateway chat。任务达到 ``done`` 或 ``archived`` 时自动移除订阅。

配置参考
==========

``config.yaml`` 中的 Kanban 相关配置：

.. code-block:: yaml

    kanban:
      dispatch_in_gateway: true          # 默认：true；在 Gateway 内运行调度器
      dispatch_interval_seconds: 60      # 默认：60；tick 间隔
      max_spawn: null                    # 最大并发 Worker 数（null = 无限制）
      dispatch_failure_limit: 5          # 连续失败 N 次后自动阻塞

    dashboard:
      kanban:
        default_tenant: null             # 预选租户过滤
        lane_by_profile: false           # "按 Profile 分泳道"默认开关
        include_archived_by_default: false
        render_markdown: true            # false 则用 <pre> 渲染

协作模式
==========

Kanban 支持九种经典协作模式，无需新原语：

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - 模式
     - 描述
   * - **Fan-out**
     - Orchestrator 创建 N 个并行子任务（siblings），各自独立执行
   * - **Pipeline**
     - 角色链：A 完成 → B 启动 → C 启动，通过 parent-child 依赖实现
   * - **Voting / Quorum**
     - N 个 siblings + 一个 Aggregator，等所有 siblings 完成后聚合
   * - **Long-running Journal**
     - 共享目录 + cron 定期创建任务，Worker 在目录中追加日志
   * - **Human-in-the-loop**
     - Worker 遇到需要人工决策时 ``kanban_block()``，人工 ``unblock`` 后继续
   * - **@mention 路由**
     - 任务 body 中 @mention 某个 Profile，Orchestrator 将其设为 assignee
   * - **Thread-scoped Workspace**
     - 关联任务共享同一个 ``workspace_path``，实现线程级协作
   * - **Fleet Farming**
     - 一个 Profile 多个任务，适合"对 N 个文件执行相同操作"的场景
   * - **Triage Specifier**
     - 模糊想法 → triage → Specifier 展开为具体子任务 → todo → ready

这些模式的组合可以覆盖绝大多数多 Agent 协作场景，无需修改 Kanban 核心代码。

关键源文件
===========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文件
     - 职责
   * - ``hermes_cli/kanban.py`` (~2300 行)
     - CLI 入口、argparse 子命令、命令调度、输出格式化
   * - ``hermes_cli/kanban_db.py`` (~5100 行)
     - SQLite 持久化层：schema、数据模型、CAS claim、生命周期转换、调度循环、Worker spawn
   * - ``hermes_cli/kanban_diagnostics.py`` (~800 行)
     - 诊断规则引擎（6 条规则）
   * - ``hermes_cli/kanban_specify.py`` (~270 行)
     - Specify 功能：辅助 LLM 展开模糊任务
   * - ``tools/kanban_tools.py`` (~900 行)
     - Worker/Orchestrator 工具调用实现（含 Orchestrator Board 工具）
   * - ``plugins/kanban/dashboard/plugin_api.py`` (~1650 行)
     - FastAPI 路由：REST 端点 + WebSocket 事件流 + 批量操作
   * - ``plugins/kanban/dashboard/dist/``
     - React SPA 前端（多卡拖拽、Shift-Click 范围选择、<details> 折叠）
   * - ``skills/devops/kanban-worker/SKILL.md``
     - Worker 生命周期技能（每个 Worker 自动加载）
   * - ``skills/devops/kanban-orchestrator/SKILL.md``
     - Orchestrator 分解策略技能（Step-0 Profile 发现）
