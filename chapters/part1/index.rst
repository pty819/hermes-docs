.. _part1:

第一部分：基础概念
====================

什么是 AI Agent？
-------------------

定义
~~~~~~

AI Agent 是一个能够**自主感知环境、制定决策、执行动作，并根据反馈调整行为**
的软件系统。它与传统软件的核心区别在于：传统软件的行为由程序员预先编码，
而 Agent 的行为由大语言模型（LLM）在运行时动态决定。

但这一定义过于抽象。让我们通过对比来精确理解。

与聊天机器人的区别
^^^^^^^^^^^^^^^^^^^^

聊天机器人（Chatbot）是一个**单轮或固定多轮** 的对话系统：

.. code-block:: text

   用户 → LLM → 回复

用户发送一条消息，LLM 返回一条回复，交互结束。即使像 ChatGPT 这样的
多轮对话系统，其核心模式也是"用户提问，模型回答"。模型不会主动采取行动。

Agent 则引入了**行动能力** ：

.. code-block:: text

   用户 → LLM → 思考 → 选择工具 → 执行 → 观察结果 → 继续思考 → ... → 回复

关键区别在于 Agent 拥有一个**循环** ：它可以反复调用工具、观察结果、
调整策略，直到任务完成或预算耗尽。这个循环赋予了 Agent 处理复杂、
多步骤任务的能力。

与 RAG 管线的区别
^^^^^^^^^^^^^^^^^^^

检索增强生成（RAG）管线是一个**增强输入** 的系统：

.. code-block:: text

   用户查询 → 检索相关文档 → [文档 + 查询] → LLM → 回复

RAG 增强了 LLM 的知识，但没有给它行动能力。RAG 系统不会"决定"要去检索——
检索是管线中固定的步骤。RAG 系统也不会在检索失败时尝试另一种检索策略。

Agent 则可以**自主决定** 何时检索、检索什么、以及检索结果不满意时如何调整。
这种决策能力是 Agent 区别于所有"管线式"LLM 应用的核心特征。

一个精确的工作定义
^^^^^^^^^^^^^^^^^^^^

综合以上对比，我们可以给出一个更精确的工作定义：

**AI Agent = LLM + 工具 + 循环 + 状态**

- **LLM** ：作为"大脑"，负责理解输入、制定计划、选择行动
- **工具** ：作为"手和脚"，让 Agent 能够影响外部世界
- **循环** ：observe → think → act → observe 的迭代能力
- **状态** ：跨迭代的记忆与上下文管理

Hermes Agent 完美地体现了这四个要素：

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 要素
     - 抽象概念
     - Hermes 实现
   * - LLM
     - 推理与决策
     - ``AIAgent._interruptible_streaming_api_call()`` ，支持 OpenAI/Anthropic/Bedrock
   * - 工具
     - 行动能力
     - ``model_tools.handle_function_call()`` → ``registry.dispatch()``
   * - 循环
     - 自主迭代
     - ``run_conversation()`` 中的 ``while`` 主循环
   * - 状态
     - 记忆与上下文
     - SQLite 会话数据库、Memory Store、消息历史

基础循环：Observe → Think → Act → Observe
----------------------------------------------

所有 Agent 架构，无论多么复杂，都可以归结为一个基本循环：

.. mermaid::

   sequenceDiagram
       participant U as 用户/环境
       participant A as Agent (LLM)
       participant T as 工具集
   
       U->>A: 输入 (Observe)
       loop 直到任务完成或预算耗尽
           A->>A: 思考与规划 (Think)
           alt 需要使用工具
               A->>T: 调用工具 (Act)
               T-->>A: 返回结果 (Observe)
           else 任务完成
               A-->>U: 最终回复
           end
       end

这个循环看似简单，但真实的生产实现中隐藏着大量复杂性：

**Observe（观察）的复杂性：**

- 流式接收 LLM 输出时如何处理部分 JSON（工具调用的参数是不完整的）
- 如何统一不同提供商（OpenAI choices vs Anthropic content blocks vs Bedrock）的响应格式
- 如何在流式输出中检测工具调用与纯文本的边界

**Think（思考）的复杂性：**

- 如何将系统提示词、用户输入、工具结果、记忆上下文组合成有效的 prompt
- 当思考过程被输出 token 上限截断时如何处理
- 如何在不破坏 prompt 缓存的前提下注入动态上下文

**Act（行动）的复杂性：**

- 如何决定工具的并行执行还是顺序执行
- 如何处理模型幻觉出的不存在的工具名
- 如何处理工具参数的 JSON 解析错误
- 如何在执行过程中响应中断请求

Agent 架构的演进
------------------

ReAct (2022)
~~~~~~~~~~~~~~

ReAct（Reasoning + Acting）是由 Yao 等人在 2022 年提出的 Agent 架构范式。
其核心思想是让 LLM 在每个步骤中先进行**推理** （Thought），然后选择**行动** （Action），
最后观察**结果** （Observation）。

.. code-block:: text

   Thought: 我需要查找北京今天的天气
   Action: weather_query(city="北京")
   Observation: 晴，25°C
   Thought: 我已经得到了答案
   Answer: 北京今天是晴天，25°C

ReAct 的贡献在于将推理和行动交织在一起，而不是先完成所有推理再执行所有行动。
这使得 Agent 能够根据中间结果动态调整策略。

Hermes 在 ``run_conversation()`` 的主循环中实现了 ReAct 模式：
每次 API 调用对应一个 "Thought"，工具调用对应 "Action"，工具结果对应 "Observation"。

Reflexion (2023)
~~~~~~~~~~~~~~~~~~

Reflexion 在 ReAct 的基础上增加了**自我反思** 能力。当 Agent 完成一个任务后，
它会回顾自己的执行轨迹，评估哪些步骤有效、哪些无效，并将这些反思保存下来
供未来的任务参考。

Hermes 的记忆系统（``memory_tool``）和技能系统（``skill_manage``）实现了
类似的反思机制。当对话结束时，Agent 会在后台线程中回顾对话内容，
自动将值得记住的信息保存到长期存储中（``run_agent.py:2458`` ，
``_spawn_background_review`` 方法）。

Toolformer (2023)
~~~~~~~~~~~~~~~~~~~

Toolformer 展示了 LLM 可以通过微调学会**自主决定何时调用工具** 。
在 Agent 架构中，这一思想的工程实现是 function calling API——
模型不是通过微调，而是通过 API 协议来获得工具调用能力。

Hermes 通过 OpenAI Chat Completions API 的 ``tools`` 参数、
Anthropic Messages API 的 ``tool_use`` content block、
以及 AWS Bedrock 的 ``toolConfig`` 来实现跨提供商的工具调用。

AutoGPT (2023)
~~~~~~~~~~~~~~~~

AutoGPT 是第一个引起广泛关注的自主 Agent 项目。它的核心创新是让 GPT-4
自主分解任务、设定子目标、并迭代执行。AutoGPT 暴露了一个关键问题：
**无限的自主迭代会导致失控。** Agent 可能陷入循环，不断调用工具却永远无法完成任务。

Hermes 通过 ``IterationBudget`` 类（``run_agent.py:170``）解决了这一问题：
每个 Agent 实例有固定的迭代预算，耗尽后触发一次"宽限调用"让模型完成总结，
然后强制退出循环。

为什么要工具、记忆和规划？
----------------------------

工具：Agent 的手脚
~~~~~~~~~~~~~~~~~~~~

没有工具的 LLM 只能生成文本。工具赋予了 Agent 影响外部世界的能力。

Hermes 提供了丰富的工具集：

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 工具类别
     - 具体工具
     - 能力
   * - 文件操作
     - read_file, write_file, patch, search_files
     - 读写和搜索本地文件
   * - 终端执行
     - terminal
     - 执行 shell 命令
   * - 网络访问
     - web_search, web_extract
     - 搜索和提取网页内容
   * - 浏览器
     - browser_navigate, browser_click, ...
     - 无头浏览器自动化
   * - 代码执行
     - execute_code
     - 沙箱中的代码执行
   * - 记忆
     - memory, todo, session_search
     - 长期和短期记忆管理
   * - 视觉
     - vision_analyze, image_generate
     - 图像理解与生成

**关键设计原则：** 工具通过自注册模式加入系统。每个工具文件（如 ``tools/terminal_tool.py``）
在模块加载时调用 ``registry.register()`` 将自己注册到全局工具注册中心。
这意味着添加新工具只需创建一个新文件并调用注册函数，无需修改核心调度代码。

记忆：Agent 的经验
~~~~~~~~~~~~~~~~~~~~

记忆系统让 Agent 能够跨越单次对话的限制，积累和利用长期知识。

Hermes 实现了两层记忆：

- **短期记忆（会话级）：** 通过 ``messages`` 列表中的对话历史实现。
  每次工具调用的结果都作为 tool 角色消息添加到历史中。
- **长期记忆（跨会话）：** 通过 ``memory_tool`` 实现。
  Agent 可以保存用户的偏好、项目信息、工作习惯等到持久化存储中，
  并在后续会话中通过系统提示词注入这些记忆。

``run_agent.py`` 中 ``_memory_manager.on_turn_start()`` 在每轮对话开始时
预取长期记忆，并通过 ``build_memory_context_block()`` 注入到用户消息中。

规划：Agent 的大脑
~~~~~~~~~~~~~~~~~~~~

规划能力是 Agent 区别于简单工具调用的关键。一个没有规划能力的 Agent
只会对每条消息做即时反应；有规划能力的 Agent 能够分解复杂任务、
设定中间目标、并根据执行结果调整计划。

Hermes 的规划通过以下机制实现：

- **系统提示词引导：** 通过 ``TOOL_USE_ENFORCEMENT_GUIDANCE`` 等提示词片段
  引导模型进行结构化规划
- **Todo 工具：** 让 Agent 显式地创建和管理任务列表
- **子代理委派：** 通过 ``delegate_task`` 工具将子任务分配给专门的子 Agent
- **迭代预算：** ``IterationBudget`` 确保 Agent 有足够的迭代空间来完成复杂任务

通用 Agent 架构模式
---------------------

综合以上分析，我们可以绘制出通用 Agent 的架构模式：

.. mermaid::

   graph TB
       subgraph "用户接口层"
           CLI["CLI / TUI"]
           GW["网关 RPC"]
           BOT["Bot 集成"]
       end
   
       subgraph "Agent 核心"
           LOOP["主循环<br/>run_conversation()"]
           BUDGET["迭代预算<br/>IterationBudget"]
       end
   
       subgraph "LLM 适配层"
           OPENAI["OpenAI<br/>Chat Completions"]
           CODEX["Codex<br/>Responses API"]
           ANTHRO["Anthropic<br/>Messages API"]
           BEDROCK["AWS Bedrock<br/>Converse API"]
       end
   
       subgraph "工具层"
           REG["工具注册中心<br/>registry"]
           TOOLS["工具实现<br/>terminal / file / web / ..."]
           MCP["MCP 工具"]
           PLUGINS["插件工具"]
       end
   
       subgraph "状态层"
           SESSION["会话存储<br/>SQLite"]
           MEMORY["长期记忆<br/>MemoryStore"]
           COMPRESS["上下文压缩<br/>ContextCompressor"]
           TRAJ["轨迹保存<br/>trajectory"]
       end
   
       CLI --> LOOP
       GW --> LOOP
       BOT --> LOOP
   
       LOOP --> BUDGET
       LOOP --> OPENAI
       LOOP --> CODEX
       LOOP --> ANTHRO
       LOOP --> BEDROCK
   
       LOOP --> REG
       REG --> TOOLS
       REG --> MCP
       REG --> PLUGINS
   
       LOOP --> SESSION
       LOOP --> MEMORY
       LOOP --> COMPRESS
       LOOP --> TRAJ

Hermes 如何映射到这些概念
---------------------------

以下是 Hermes 核心模块与 Agent 概念的精确映射：

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Agent 概念
     - Hermes 模块
     - 关键实现细节
   * - 主循环
     - ``run_agent.py`` :: ``run_conversation()``
     - ``while`` 循环，每次迭代对应一次 LLM 调用，支持流式和非流式两种模式
   * - LLM 适配
     - ``run_agent.py`` :: ``api_mode``
     - 四种 API 模式：``chat_completions`` 、``codex_responses`` 、``anthropic_messages`` 、``bedrock_converse``
   * - 工具调度
     - ``model_tools.py`` :: ``handle_function_call()``
     - 先检查 Agent 级拦截工具（todo/memory/session_search），再分发到注册中心
   * - 错误恢复
     - ``agent/error_classifier.py`` :: ``classify_api_error()``
     - 16 种错误类型，自动选择凭证轮换/压缩/回退等恢复策略
   * - 上下文管理
     - ``agent/context_compressor.py``
     - 头尾保护 + 中间摘要，使用辅助模型生成摘要
   * - 会话持久化
     - ``run_agent.py`` :: ``_persist_session()``
     - JSON 日志 + SQLite 双重存储，确保任何退出路径都不丢失数据
   * - 子代理
     - ``tools/delegate_tool.py``
     - 父子共享 ``IterationBudget`` ，子代理有独立的迭代上限

在下一章中，我们将深入 ``run_agent.py`` 的 ``run_conversation()`` 方法，
逐行分析这个 2000+ 行的方法如何实现上述所有功能。
这是本书最核心、最详细的章节——请确保你已经准备好了。
