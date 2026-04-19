.. _chapter-session-state:

第十二章：状态与会话管理：Agent 的记忆系统
================================================

.. contents::
   :depth: 3
   :local:

为什么 Agent 需要持久化
-------------------------

无状态 Agent 的局限
~~~~~~~~~~~~~~~~~~~~~

最简单的 Agent 实现是无状态的——每次对话都从零开始，所有历史都存在于内存中。
一旦进程退出，一切消失。对于单次问答这没什么问题，但对于一个编程助手来说，
无状态意味着：

- 用户关闭终端后，Agent 忘记了之前做了什么
- 系统崩溃或网络中断后，对话无法恢复
- 无法搜索"上周那个关于数据库迁移的对话"
- 多个平台（CLI、Telegram、Discord）无法共享状态
- 无法追踪 token 消耗和费用

Hermes 选择了 **SQLite 持久化** 作为解决方案，
提供了完整的会话生命周期管理、全文搜索和跨平台状态共享。

持久化的需求层次
~~~~~~~~~~~~~~~~~~

Hermes 的持久化需求可以分为四个层次：

**1. 消息存储：** 完整保存每条消息（用户、助手、工具调用、工具结果），
包括时间戳、token 计数和推理链。

**2. 会话管理：** 创建、恢复、结束、删除会话，
支持会话标题、来源标记（CLI/gateway/Telegram）和父子关系。

**3. 全文搜索：** 在所有会话的所有消息中快速搜索关键词，
支持中英日韩等 CJK 字符。

**4. 并发安全：** 多个进程（gateway + CLI + 工作树 Agent）
同时访问同一个数据库，不丢失数据也不死锁。

SessionDB 架构概览
---------------------

技术选型：为什么是 SQLite？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hermes 选择了 SQLite 而非 PostgreSQL、Redis 或文件系统，原因如下：

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 特性
     - SQLite
     - 其他方案
   * - 部署
     - 零配置，单个文件
     - PostgreSQL 需要服务器
   * - 并发读
     - WAL 模式下无限并发读
     - 文件系统需要锁
   * - 事务
     - 完整 ACID
     - JSONL 无事务保证
   * - 全文搜索
     - 内置 FTS5
     - 需要外部搜索引擎
   * - 跨平台
     - Python 标准库自带
     - 依赖外部服务

核心设计决策记录在 ``hermes_state.py`` 的模块文档中：

- WAL 模式用于并发读 + 单写（gateway 多平台场景）
- FTS5 虚拟表用于快速文本搜索
- ``parent_session_id`` 链支持压缩触发的会话分割
- 批量运行器和 RL 轨迹不在这里存储（独立系统）
- 会话来源标记（``'cli'``, ``'telegram'``, ``'discord'`` 等）用于过滤

WAL 模式详解
~~~~~~~~~~~~~~

SQLite 的 **WAL（Write-Ahead Logging）** 模式是整个并发架构的基础。

在默认的 rollback journal 模式下，写操作会锁定整个数据库文件，
阻止所有读操作。而在 WAL 模式下：

- **写操作** 追加到 WAL 文件末尾，不修改主数据库文件
- **读操作** 直接读取主数据库文件（如果 WAL 中有未合并的修改，
  读操作会透明地合并 WAL 中的修改）
- **检查点（checkpoint）** 将 WAL 中的修改合并回主数据库

这意味着读写可以并发进行——写操作不阻塞读操作，读操作也不阻塞写操作。
唯一的限制是同一时刻只能有一个写操作。

SessionDB 在初始化时启用 WAL 模式：

.. code-block:: python

    self._conn = sqlite3.connect(
        str(self.db_path),
        check_same_thread=False,
        timeout=1.0,
        isolation_level=None,  # 手动管理事务
    )
    self._conn.execute("PRAGMA journal_mode=WAL")
    self._conn.execute("PRAGMA foreign_keys=ON")

注意 ``isolation_level=None``——Python 的默认隔离级别会在 DML 语句时
自动开启事务，这与我们手动的 ``BEGIN IMMEDIATE`` 冲突。
设置为 ``None`` 表示我们自己管理事务边界。

数据库 Schema 详解
--------------------

Schema 版本管理
~~~~~~~~~~~~~~~~~

当前 schema 版本为 **v6** ，通过 ``schema_version`` 表跟踪：

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER NOT NULL
    );

``_init_schema()`` 在每次连接数据库时检查版本号，
如果低于当前版本则依次运行迁移脚本。

sessions 表
~~~~~~~~~~~~~

``sessions`` 表是会话的元数据中心：

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,              -- UUID
        source TEXT NOT NULL,             -- 'cli', 'telegram', 'discord', etc.
        user_id TEXT,                     -- 平台用户 ID
        model TEXT,                       -- 使用的模型名称
        model_config TEXT,                -- JSON: 模型配置快照
        system_prompt TEXT,               -- 完整的系统提示快照
        parent_session_id TEXT,           -- 父会话 ID（分支机制）
        started_at REAL NOT NULL,         -- Unix 时间戳
        ended_at REAL,                    -- 结束时间
        end_reason TEXT,                  -- 结束原因
        message_count INTEGER DEFAULT 0,  -- 消息计数
        tool_call_count INTEGER DEFAULT 0,-- 工具调用计数
        -- Token 统计（v5 新增）
        input_tokens INTEGER DEFAULT 0,
        output_tokens INTEGER DEFAULT 0,
        cache_read_tokens INTEGER DEFAULT 0,
        cache_write_tokens INTEGER DEFAULT 0,
        reasoning_tokens INTEGER DEFAULT 0,
        -- 计费信息（v5 新增）
        billing_provider TEXT,
        billing_base_url TEXT,
        billing_mode TEXT,
        estimated_cost_usd REAL,
        actual_cost_usd REAL,
        cost_status TEXT,
        cost_source TEXT,
        pricing_version TEXT,
        -- 标题（v3 新增）
        title TEXT,
        FOREIGN KEY (parent_session_id) REFERENCES sessions(id)
    );

关键字段说明：

**id（TEXT PRIMARY KEY）：** UUID 格式的会话标识符。
作为主键，它同时也是外部引用（消息表、子会话）的锚点。

**source（TEXT NOT NULL）：** 会话来源平台。
在 gateway 多平台模式下，这个字段用于按平台过滤会话。

**parent_session_id（TEXT）：** 实现会话分支机制的核心字段。
当上下文压缩触发会话分割时，新的会话通过这个字段关联到原始会话。

**model_config（TEXT）：** JSON 格式的模型配置快照，
记录了会话开始时的模型参数（温度、top_p 等）。

**system_prompt（TEXT）：** 完整的组装后的系统提示快照。
这使得会话可以被完整恢复。

索引设计
~~~~~~~~~~

.. code-block:: sql

    CREATE INDEX idx_sessions_source ON sessions(source);
    CREATE INDEX idx_sessions_parent ON sessions(parent_session_id);
    CREATE INDEX idx_sessions_started ON sessions(started_at DESC);
    CREATE UNIQUE INDEX idx_sessions_title_unique
        ON sessions(title) WHERE title IS NOT NULL;

每个索引都有明确的目的：

- ``idx_sessions_source`` ：按平台过滤会话列表
- ``idx_sessions_parent`` ：快速查找会话的所有子会话（分支遍历）
- ``idx_sessions_started`` ：按时间排序的会话列表（降序，最新的在前）
- ``idx_sessions_title_unique`` ：确保标题唯一性（部分索引，NULL 不参与唯一性检查）

messages 表
~~~~~~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL REFERENCES sessions(id),
        role TEXT NOT NULL,                -- 'system', 'user', 'assistant', 'tool'
        content TEXT,                      -- 消息正文
        tool_call_id TEXT,                 -- 工具结果引用的调用 ID
        tool_calls TEXT,                   -- JSON: 工具调用数组
        tool_name TEXT,                    -- 工具名称
        timestamp REAL NOT NULL,           -- Unix 时间戳
        token_count INTEGER,               -- 消息的 token 数
        finish_reason TEXT,                -- 'stop', 'tool_calls', etc. (v2)
        reasoning TEXT,                    -- 推理文本 (v6)
        reasoning_details TEXT,            -- JSON: 推理细节 (v6)
        codex_reasoning_items TEXT         -- JSON: Codex 推理项 (v6)
    );

    CREATE INDEX idx_messages_session
        ON messages(session_id, timestamp);

``messages`` 表的设计关注点：

**AUTOINCREMENT 主键：** 使用自增整数而非 UUID，因为消息的插入频率很高，
整数主键的插入性能更好。``lastrowid`` 被用于返回新插入消息的 ID。

**tool_calls 和 tool_name 分离：** ``tool_calls`` 是完整的 JSON 数组
（包含 id、function.name、function.arguments），而 ``tool_name``
是从中提取的工具名称，用于快速过滤而不需要解析 JSON。

**reasoning 字段（v6 新增）：** 保存助手的推理链文本和结构化推理细节。
没有这些字段，推理链在会话重新加载时会丢失，
导致多轮推理的连续性被破坏。

FTS5 全文搜索
---------------

FTS5 虚拟表结构
~~~~~~~~~~~~~~~~~

.. code-block:: sql

    CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
        content,
        content=messages,
        content_rowid=id
    );

这里使用了 FTS5 的 **内容表模式（content table mode）** 。
``content=messages`` 指定 FTS 索引的内容来自 ``messages`` 表，
``content_rowid=id`` 将 FTS 的 rowid 映射到消息表的自增主键。
这种模式下，FTS 虚拟表本身不存储内容副本，只存储倒排索引，
节省了磁盘空间。

同步触发器
~~~~~~~~~~~~

FTS5 索引通过三个触发器与 ``messages`` 表保持同步：

.. code-block:: sql

    -- 插入时同步
    CREATE TRIGGER messages_fts_insert AFTER INSERT ON messages BEGIN
        INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
    END;

    -- 删除时同步
    CREATE TRIGGER messages_fts_delete AFTER DELETE ON messages BEGIN
        INSERT INTO messages_fts(messages_fts, rowid, content)
            VALUES('delete', old.id, old.content);
    END;

    -- 更新时同步（先删旧索引，再插新索引）
    CREATE TRIGGER messages_fts_update AFTER UPDATE ON messages BEGIN
        INSERT INTO messages_fts(messages_fts, rowid, content)
            VALUES('delete', old.id, old.content);
        INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
    END;

注意 FTS5 的删除操作使用特殊的语法——向虚拟表插入一行，
但第一个列名为虚拟表自身名称（``messages_fts``），值为 ``'delete'`` 。
这是 FTS5 内容表模式的要求。

查询清理器（_sanitize_fts5_query）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FTS5 有自己的查询语法，其中 ``"`` 、``(`` 、``)`` 、``+`` 、``*`` 、
``{`` 、``}`` 和 ``AND`` 、``OR`` 、``NOT`` 都有特殊含义。
直接将用户输入传递给 ``MATCH`` 子句可能导致 ``OperationalError`` 。

``_sanitize_fts5_query()`` 方法通过六个步骤处理用户输入：

**步骤 1：提取并保护引号短语。** 使用占位符替换 ``"..."`` 格式的精确匹配短语，
防止后续步骤破坏它们。

**步骤 2：移除未匹配的 FTS5 特殊字符。** 去除 ``+{}()\"^`` 等字符。

**步骤 3：规范化通配符。** 将连续的 ``*`` 合并为一个，
移除前导的 ``*`` （FTS5 前缀搜索至少需要一个前导字符）。

**步骤 4：移除两端悬空的布尔运算符。** ``"hello AND"`` 或 ``"OR world"``
会导致语法错误。

**步骤 5：包装带连字符和点号的术语。** FTS5 默认分词器会在连字符和点号处分割，
导致 ``chat-send`` 变成 ``chat AND send`` ，``P2.2`` 变成 ``p2 AND 2`` 。
将它们用引号包装可以保持短语语义。

**步骤 6：恢复步骤 1 中保护的引号短语。**

CJK 回退机制
~~~~~~~~~~~~~~

FTS5 的默认分词器（tokenizer）是 ``unicode61`` ，
它按 Unicode 单词边界分词。对于 CJK 字符，
这个分词器会将每个字符视为一个独立的词元（token）。
这意味着搜索"数据库迁移"会被分解为"数"、"据"、"库"、"迁"、"移"五个独立的词元，
返回包含其中任何一个字符的所有结果。

``search_messages()`` 方法实现了 CJK 回退：

.. code-block:: python

    # 首先尝试 FTS5 搜索
    try:
        cursor = self._conn.execute(sql, params)
    except sqlite3.OperationalError:
        if not self._contains_cjk(query):
            return []  # 非 CJK 的语法错误直接返回空
        matches = []
    else:
        matches = [dict(row) for row in cursor.fetchall()]

    # 如果 FTS5 无结果且查询包含 CJK，回退到 LIKE
    if not matches and self._contains_cjk(query):
        raw_query = query.strip('"').strip()
        like_sql = """
            SELECT ... FROM messages m ...
            WHERE m.content LIKE ?
            ...
        """
        like_params = [f"%{raw_query}%"]

``_contains_cjk()`` 通过 Unicode 范围检查判断文本是否包含 CJK 字符：

.. code-block:: python

    @staticmethod
    def _contains_cjk(text):
        for ch in text:
            cp = ord(ch)
            if (0x4E00 <= cp <= 0x9FFF or   # CJK Unified Ideographs
                0x3400 <= cp <= 0x4DBF or   # CJK Extension A
                0x20000 <= cp <= 0x2A6DF or # CJK Extension B
                0x3000 <= cp <= 0x303F or   # CJK Symbols
                0x3040 <= cp <= 0x309F or   # Hiragana
                0x30A0 <= cp <= 0x30FF or   # Katakana
                0xAC00 <= cp <= 0xD7AF):    # Hangul Syllables
                return True
        return False

搜索结果包含上下文（每条匹配消息前后各一条），
使用 FTS5 的 ``snippet()`` 函数生成高亮摘要：

.. code-block:: sql

    snippet(messages_fts, 0, '>>>', '<<<', '...', 40) AS snippet

这会在匹配文本前后添加 ``>>>`` 和 ``<<<`` 标记，
上下文窗口为 40 个字符。

FTS5 搜索流程（含 CJK 回退）：

.. mermaid::

   flowchart TD
       A["用户输入搜索查询"] --> B["_sanitize_fts5_query()"]
       B --> C["构建 FTS5 MATCH 查询"]
       C --> D{"执行 FTS5 查询"}
       D -- 成功 --> E{"有结果?"}
       D -- OperationalError --> F{"查询含 CJK?"}
       F -- 否 --> G["返回空列表"]
       F -- 是 --> H["matches = []"]
       E -- 是 --> K["添加上下文消息"]
       E -- 否 --> I{"查询含 CJK?"}
       H --> I
       I -- 否 --> G
       I -- 是 --> J["LIKE 回退搜索<br/>%query%"]
       J --> K
       K --> L["返回结果<br/>(含 snippet + 上下文)"]

写入并发控制
--------------

问题：多进程写竞争
~~~~~~~~~~~~~~~~~~~~

在 gateway 模式下，多个 Hermes 进程同时运行：

- Gateway 主进程处理来自多个平台的请求
- CLI 会话独立连接数据库
- 工作树 Agent 在并行分支中工作

所有这些进程共享同一个 ``state.db`` 文件。
SQLite 的 WAL 模式允许并发读，但写操作仍然需要排他锁。

SQLite 内置的忙等待处理器使用**确定性的** 退避策略——
固定的时间间隔重试。在高并发场景下，多个写入者会在相同的时间点重试，
形成**护航效应（convoy effect）** ，导致 TUI 冻结和响应延迟。

解决方案：BEGIN IMMEDIATE + 随机抖动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SessionDB 使用**应用层重试 + 随机抖动** 来打破护航效应：

.. code-block:: python

    _WRITE_MAX_RETRIES = 15
    _WRITE_RETRY_MIN_S = 0.020   # 20ms
    _WRITE_RETRY_MAX_S = 0.150   # 150ms
    _CHECKPOINT_EVERY_N_WRITES = 50

    def _execute_write(self, fn):
        last_err = None
        for attempt in range(self._WRITE_MAX_RETRIES):
            try:
                with self._lock:
                    self._conn.execute("BEGIN IMMEDIATE")
                    try:
                        result = fn(self._conn)
                        self._conn.commit()
                    except BaseException:
                        self._conn.rollback()
                        raise
                # 成功后周期性检查点
                self._write_count += 1
                if self._write_count % self._CHECKPOINT_EVERY_N_WRITES == 0:
                    self._try_wal_checkpoint()
                return result
            except sqlite3.OperationalError as exc:
                err_msg = str(exc).lower()
                if "locked" in err_msg or "busy" in err_msg:
                    last_err = exc
                    if attempt < self._WRITE_MAX_RETRIES - 1:
                        jitter = random.uniform(
                            self._WRITE_RETRY_MIN_S,
                            self._WRITE_RETRY_MAX_S,
                        )
                        time.sleep(jitter)
                        continue
                raise
        raise last_err or sqlite3.OperationalError("database is locked")

关键设计点：

**BEGIN IMMEDIATE：** 在事务开始时立即获取写锁，
而不是等到第一次写操作时。这使得锁竞争在事务开始时就显现，
而不是在事务中间——减少了死锁的风险。

**threading.Lock + SQLite 锁：** Python 的 ``threading.Lock``
确保同一个进程内的多个线程不会同时尝试写入。
SQLite 的 WAL 写锁处理不同进程之间的竞争。

**随机抖动：** ``random.uniform(20ms, 150ms)`` 的随机等待时间
使得竞争的写入者不会在同一时刻重试。

**15 次重试上限：** 最多重试 15 次，每次最长等待 150ms，
总等待时间上限为 15 * 150ms = 2.25 秒。
如果 15 次都失败，抛出异常。

**超时设置为 1 秒：** SQLite 连接的 ``timeout=1.0`` 是短超时——
如果 SQLite 内部的忙等待在 1 秒内无法获取锁，立即返回错误，
由应用层重试处理。

WAL 检查点
~~~~~~~~~~~~

每 50 次成功的写操作后，执行一次 **PASSIVE 检查点** ：

.. code-block:: python

    def _try_wal_checkpoint(self):
        try:
            with self._lock:
                result = self._conn.execute(
                    "PRAGMA wal_checkpoint(PASSIVE)"
                ).fetchone()
        except Exception:
            pass  # 尽力而为，永远不会致命

PASSIVE 模式不会阻塞——它只合并那些没有其他连接正在使用的 WAL 帧。
如果检查点无法合并某些帧（因为其他连接正在使用），它会静默跳过，
而不是等待。

这个机制防止了 WAL 文件在长时间运行中无限增长。
在 ``close()`` 方法中也执行了一次检查点，
确保退出的进程帮助保持 WAL 文件的合理大小。

写入并发时序图：

.. mermaid::

   sequenceDiagram
       participant T1 as 线程 1
       participant Lock as threading.Lock
       participant DB as SQLite (WAL)
       participant T2 as 线程 2
   
       T1->>Lock: acquire()
       T1->>DB: BEGIN IMMEDIATE
       T1->>DB: INSERT INTO messages ...
       T1->>DB: COMMIT
       T1->>Lock: release()
   
       Note over T2: T2 在 T1 持有锁期间尝试写入
   
       T2->>Lock: acquire() — 阻塞
       T1->>Lock: release()
       T2->>Lock: acquire() — 成功
       T2->>DB: BEGIN IMMEDIATE
       T2->>DB: INSERT INTO messages ...
       T2->>DB: COMMIT
       T2->>Lock: release()
   
       Note over T1,T2: 不同进程的竞争由 SQLite WAL 处理
   
       rect rgb(255, 230, 230)
           Note over DB: Process A: BEGIN IMMEDIATE holds WAL write lock
           Note over DB: Process B: BEGIN IMMEDIATE - database is locked
           Note over DB: Process B: sleep random 20-150ms
           Note over DB: Process B: retry BEGIN IMMEDIATE - success
       end

会话生命周期
--------------

SessionDB 管理的会话有完整的状态机，从创建到删除。

创建会话（create_session）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_session(self, session_id, source, model=None, model_config=None,
                       system_prompt=None, user_id=None, parent_session_id=None):
        def _do(conn):
            conn.execute(
                """INSERT OR IGNORE INTO sessions
                   (id, source, user_id, model, model_config,
                    system_prompt, parent_session_id, started_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (session_id, source, user_id, model,
                 json.dumps(model_config) if model_config else None,
                 system_prompt, parent_session_id, time.time()),
            )
        self._execute_write(_do)
        return session_id

使用 ``INSERT OR IGNORE`` 而非 ``INSERT`` — 如果会话 ID 已存在则静默忽略。
这使得 ``create_session`` 是幂等的，调用者不需要先检查会话是否存在。

追加消息（append_message）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def append_message(self, session_id, role, content=None,
                       tool_name=None, tool_calls=None, tool_call_id=None,
                       token_count=None, finish_reason=None,
                       reasoning=None, reasoning_details=None,
                       codex_reasoning_items=None):
        # 预序列化 JSON 字段
        tool_calls_json = json.dumps(tool_calls) if tool_calls else None
        reasoning_details_json = json.dumps(reasoning_details) if reasoning_details else None
        codex_items_json = json.dumps(codex_reasoning_items) if codex_reasoning_items else None

        def _do(conn):
            cursor = conn.execute(
                """INSERT INTO messages (...) VALUES (...)""",
                (session_id, role, content, ...),
            )
            msg_id = cursor.lastrowid
            # 更新计数器
            conn.execute(
                "UPDATE sessions SET message_count = message_count + 1, ...")
            return msg_id

        return self._execute_write(_do)

关键细节：JSON 序列化在进入写事务**之前** 完成。
这减少了在持有写锁时的工作量，缩短了锁持有时间，降低了竞争。

结束会话（end_session）
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def end_session(self, session_id, end_reason):
        def _do(conn):
            conn.execute(
                "UPDATE sessions SET ended_at = ?, end_reason = ? WHERE id = ?",
                (time.time(), end_reason, session_id),
            )
        self._execute_write(_do)

``end_reason`` 的典型值包括：``"user_exit"`` 、``"timeout"`` 、
``"reset"`` 、``"error"`` 等。

重新打开会话（reopen_session）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def reopen_session(self, session_id):
        def _do(conn):
            conn.execute(
                "UPDATE sessions SET ended_at = NULL, end_reason = NULL WHERE id = ?",
                (session_id,),
            )
        self._execute_write(_do)

清除结束时间和原因，使已结束的会话可以恢复。

确保会话存在（ensure_session）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def ensure_session(self, session_id, source="unknown", model=None):
        def _do(conn):
            conn.execute(
                """INSERT OR IGNORE INTO sessions
                   (id, source, model, started_at) VALUES (?, ?, ?, ?)""",
                (session_id, source, model, time.time()),
            )
        self._execute_write(_do)

这是一个**恢复机制** 。如果在 Agent 启动时 ``create_session()`` 因为
瞬时的 SQLite 锁而失败，后续的 ``append_message()`` 可以调用
``ensure_session()`` 来确保会话行存在。

删除会话（delete_session）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def delete_session(self, session_id):
        def _do(conn):
            # 先孤立子会话
            conn.execute(
                "UPDATE sessions SET parent_session_id = NULL "
                "WHERE parent_session_id = ?", (session_id,))
            # 删除消息
            conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            # 删除会话
            conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            return True
        return self._execute_write(_do)

**子会话不会被级联删除** ，而是被孤立（``parent_session_id = NULL``）。
这确保了压缩产生的分支会话不会因为原始会话被删除而消失。

修剪旧会话（prune_sessions）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def prune_sessions(self, older_than_days=90, source=None):
        cutoff = time.time() - (older_than_days * 86400)
        # 只删除已结束的会话
        # 先孤立子会话
        # 然后逐个删除

默认清理 90 天以前的已结束会话。**活跃会话不会被删除** ，
无论多老。

会话生命周期状态图：

.. mermaid::

   stateDiagram-v2
       [*] --> Created : create_session()
       Created --> Active : 第一条消息追加
       Active --> Active : append_message()
       Active --> Active : update_token_counts()
       Active --> Active : set_session_title()
       Active --> Ended : end_session()
       Ended --> Reopened : reopen_session()
       Reopened --> Active : append_message()
       Active --> Branched : 上下文压缩触发分割
       Branched --> Active : 新会话继续
       Ended --> Deleted : delete_session()
       Active --> Deleted : delete_session()
       Deleted --> [*]

会话分支机制
--------------

分支的设计动机
~~~~~~~~~~~~~~~~

当上下文压缩发生时，Hermes 有两种选择：

1. 在同一个会话中替换消息历史（当前方案）
2. 创建一个新会话，通过 ``parent_session_id`` 关联（可选方案）

当前实现主要使用方案 1（在同一个会话中压缩），
但 ``parent_session_id`` 基础设施已经就绪，支持以下场景：

- 子 Agent 任务（通过 ``delegate_task`` 工具创建）
- 压缩触发的会话分割
- 用户手动创建的分支

标题的血脉继承
~~~~~~~~~~~~~~~~

会话分支在标题层面有特殊的继承规则。

**``get_next_title_in_lineage()``** 生成血脉中的下一个标题：

.. code-block:: python

    def get_next_title_in_lineage(self, base_title):
        # 去除已有的 #N 后缀
        match = re.match(r'^(.*?) #(\d+)$', base_title)
        if match:
            base = match.group(1)
        else:
            base = base_title

        # 查找所有现有的编号变体
        existing = [查询 base 和 base #N 的所有标题]

        # 找到最大编号，+1
        max_num = 1  # 未编号的原始标题算 #1
        for t in existing:
            m = re.match(r'^.* #(\d+)$', t)
            if m:
                max_num = max(max_num, int(m.group(1)))
        return f"{base} #{max_num + 1}"

例如："数据库重构" → "数据库重构 #2" → "数据库重构 #3"。

**``resolve_session_by_title()``** 在查找标题时优先返回最新的编号变体：

.. code-block:: python

    def resolve_session_by_title(self, title):
        exact = self.get_session_by_title(title)
        numbered = [查询 "title #N" 的所有变体]

        if numbered:
            return numbered[0]["id"]  # 返回最新的编号变体
        elif exact:
            return exact["id"]
        return None

标题验证与清理
~~~~~~~~~~~~~~~~

``sanitize_title()`` 方法对标题进行严格清理：

- 去除 ASCII 控制字符（0x00-0x1F, 0x7F）
- 去除零宽字符（U+200B-U+200F, U+FEFF）
- 去除方向覆盖（U+202A-U+202E, U+2066-U+2069）
- 合并内部空白为单个空格
- 长度上限 100 字符
- 空白字符串规范化为 ``None``

标题唯一性由部分唯一索引保证：

.. code-block:: sql

    CREATE UNIQUE INDEX idx_sessions_title_unique
        ON sessions(title) WHERE title IS NOT NULL

Token 计数双模式
------------------

增量模式 vs. 绝对模式
~~~~~~~~~~~~~~~~~~~~~~~

``update_token_counts()`` 支持两种更新模式：

**增量模式（absolute=False，默认）：**
每次 API 调用后累加 delta 值。

.. code-block:: sql

    UPDATE sessions SET
        input_tokens = input_tokens + ?,
        output_tokens = output_tokens + ?,
        ...
    WHERE id = ?

**绝对模式（absolute=True）：**
直接设置累计值。

.. code-block:: sql

    UPDATE sessions SET
        input_tokens = ?,
        output_tokens = ?,
        ...
    WHERE id = ?

为什么需要两种模式？因为 Hermes 有两种运行模式：

**CLI 模式：** 每次只看到当前 API 调用的 delta，使用增量模式。

**Gateway 模式：** 缓存的 Agent 在内存中维护累计计数，
通过 ``update_token_counts(absolute=True)`` 一次性设置总值。

计费信息
~~~~~~~~~~

``update_token_counts()`` 还更新计费相关字段：

- ``billing_provider`` ：计费提供商（如 "openrouter"）
- ``billing_base_url`` ：API 基础 URL
- ``billing_mode`` ：计费模式
- ``estimated_cost_usd`` ：估算费用（美元）
- ``actual_cost_usd`` ：实际费用（来自 API 响应）
- ``cost_status`` ：费用状态（"estimated"、"final"）
- ``cost_source`` ：费用来源
- ``pricing_version`` ：定价版本

所有计费字段使用 ``COALESCE`` 模式——只有在提供新值时才更新：

.. code-block:: sql

    billing_provider = COALESCE(billing_provider, ?)

这意味着首次设置后，除非显式提供新值，否则不会被覆盖。

消息加载
----------

两种加载格式
~~~~~~~~~~~~~~

SessionDB 提供两种消息加载方法：

**``get_messages()`` ：** 返回数据库行格式的字典列表，
所有字段都保留（包括 id、session_id、timestamp 等）。
适合内部处理和数据导出。

**``get_messages_as_conversation()`` ：** 返回 OpenAI 对话格式的消息列表，
只包含 ``role`` 、``content`` 和工具相关字段。
适合网关恢复对话历史。

还原时的反序列化
~~~~~~~~~~~~~~~~~~

``tool_calls`` 字段在数据库中以 JSON 字符串存储。
加载时需要反序列化：

.. code-block:: python

    if msg.get("tool_calls"):
        try:
            msg["tool_calls"] = json.loads(msg["tool_calls"])
        except (json.JSONDecodeError, TypeError):
            logger.warning("Failed to deserialize tool_calls, falling back to []")
            msg["tool_calls"] = []

v6 新增的 reasoning 字段同样需要反序列化：

.. code-block:: python

    if row["role"] == "assistant":
        if row["reasoning"]:
            msg["reasoning"] = row["reasoning"]
        if row["reasoning_details"]:
            try:
                msg["reasoning_details"] = json.loads(row["reasoning_details"])
            except (json.JSONDecodeError, TypeError):
                msg["reasoning_details"] = None

反序列化失败时的策略是**降级而非崩溃**——返回空列表或 None，
让对话可以继续，而不是因为一条损坏的消息而中断整个会话。

会话列表与富预览
------------------

``list_sessions_rich()`` 提供了带预览的会话列表。

单查询优化
~~~~~~~~~~~~

早期版本使用 N+2 查询（1 次查询会话列表 + N 次查询预览 + N 次查询最后活跃时间），
性能很差。当前版本使用**单个查询 + 关联子查询** ：

.. code-block:: sql

    SELECT s.*,
        COALESCE(
            (SELECT SUBSTR(REPLACE(REPLACE(m.content, X'0A', ' '), X'0D', ' '), 1, 63)
             FROM messages m
             WHERE m.session_id = s.id AND m.role = 'user' AND m.content IS NOT NULL
             ORDER BY m.timestamp, m.id LIMIT 1),
            ''
        ) AS _preview_raw,
        COALESCE(
            (SELECT MAX(m2.timestamp) FROM messages m2 WHERE m2.session_id = s.id),
            s.started_at
        ) AS last_active
    FROM sessions s
    ...

预览取第一条用户消息的前 63 个字符（换行替换为空格），
``last_active`` 取最后一条消息的时间戳。

子会话过滤
~~~~~~~~~~~~

默认情况下，子会话（子 Agent 任务、压缩分支）被排除：

.. code-block:: python

    if not include_children:
        where_clauses.append("s.parent_session_id IS NULL")

这避免了会话列表被大量的子 Agent 任务淹没。

ID 解析
---------

SessionDB 支持多种 ID 解析方式：

**精确 ID：** 直接通过 ``get_session()`` 查找。

**前缀匹配：** ``resolve_session_id()`` 支持使用 UUID 的前缀来查找：

.. code-block:: python

    def resolve_session_id(self, session_id_or_prefix):
        exact = self.get_session(session_id_or_prefix)
        if exact:
            return exact["id"]
        # 模糊匹配
        cursor = self._conn.execute(
            "SELECT id FROM sessions WHERE id LIKE ? ESCAPE '\\' "
            "ORDER BY started_at DESC LIMIT 2",
            (f"{escaped}%",),
        )
        matches = [row["id"] for row in cursor.fetchall()]
        if len(matches) == 1:
            return matches[0]  # 唯一匹配
        return None  # 无匹配或歧义匹配

注意 ``LIKE`` 的通配符（``%`` 、``_``）在用户输入中被转义，
防止恶意的模式匹配。

**标题解析：** ``resolve_session_by_title()`` 通过标题或标题变体查找。

Schema 迁移链 v1→v6
----------------------

迁移策略
~~~~~~~~~~

SessionDB 使用**顺序迁移** 策略——从当前版本开始，
依次应用每个版本的迁移脚本：

.. code-block:: python

    def _init_schema(self):
        cursor.execute("SELECT version FROM schema_version LIMIT 1")
        row = cursor.fetchone()
        if row is None:
            cursor.execute("INSERT INTO schema_version (version) VALUES (?)",
                           (SCHEMA_VERSION,))
        else:
            current_version = row["version"]
            if current_version < 2:
                # v2 迁移
            if current_version < 3:
                # v3 迁移
            if current_version < 4:
                # v4 迁移
            ...

每个迁移都在 ``try/except`` 中执行——如果列或索引已存在，静默跳过。
这使得迁移是**幂等的** 。

迁移历史
~~~~~~~~~~

**v1 → v2：** 为 ``messages`` 表添加 ``finish_reason TEXT`` 列。
记录模型停止的原因（``"stop"`` 、``"tool_calls"`` 等）。

**v2 → v3：** 为 ``sessions`` 表添加 ``title TEXT`` 列。
支持用户为会话设置可读的标题。

**v3 → v4：** 创建 ``title`` 的唯一索引（部分索引，``WHERE title IS NOT NULL``）。
确保标题不重复。

**v4 → v5：** 批量添加计费和 token 相关列。

.. code-block:: python

    new_columns = [
        ("cache_read_tokens", "INTEGER DEFAULT 0"),
        ("cache_write_tokens", "INTEGER DEFAULT 0"),
        ("reasoning_tokens", "INTEGER DEFAULT 0"),
        ("billing_provider", "TEXT"),
        ("billing_base_url", "TEXT"),
        ("billing_mode", "TEXT"),
        ("estimated_cost_usd", "REAL"),
        ("actual_cost_usd", "REAL"),
        ("cost_status", "TEXT"),
        ("cost_source", "TEXT"),
        ("pricing_version", "TEXT"),
    ]

列名通过 ``replace('"', '""')`` 进行了双引号转义——
虽然列名来自硬编码的元组而非用户输入，但这是防御性编程的一环。

**v5 → v6：** 为 ``messages`` 表添加推理链相关列。

.. code-block:: python

    for col_name, col_type in [
        ("reasoning", "TEXT"),
        ("reasoning_details", "TEXT"),
        ("codex_reasoning_items", "TEXT"),
    ]:
        cursor.execute(f'ALTER TABLE messages ADD COLUMN "{safe}" {col_type}')

没有这些列，推理链在会话重新加载时会丢失，
导致 OpenRouter、OpenAI、Nous 等提供者的多轮推理连续性被破坏。

Schema 迁移流程图：

.. mermaid::

   flowchart TD
       A["_init_schema()"] --> B["创建基础表<br/>(sessions, messages, indexes)"]
       B --> C{"schema_version<br/>表有记录?"}
       C -- 否 --> D["插入当前版本号"]
       C -- 是 --> E["读取 current_version"]
       E --> F{"< v2?"}
       F -- 是 --> G["ALTER messages<br/>ADD finish_reason"]
       G --> H
       F -- 否 --> H{"< v3?"}
       H -- 是 --> I["ALTER sessions<br/>ADD title"]
       I --> J
       H -- 否 --> J{"< v4?"}
       J -- 是 --> K["CREATE UNIQUE INDEX<br/>idx_sessions_title_unique"]
       K --> L
       J -- 否 --> L{"< v5?"}
       L -- 是 --> M["批量添加<br/>billing/token 列<br/>(10 列)"]
       M --> N
       L -- 否 --> N{"< v6?"}
       N -- 是 --> O["添加 reasoning 列<br/>(3 列)"]
       O --> P
       N -- 否 --> P["确保 title 唯一索引"]
       P --> Q["初始化 FTS5<br/>(虚拟表 + 触发器)"]
       Q --> R["COMMIT"]
       D --> Q

轨迹记录
----------

轨迹格式
~~~~~~~~~~

``agent/trajectory.py`` 提供了独立的轨迹保存功能，
与 SessionDB 的会话存储互不干扰。

.. code-block:: python

    def save_trajectory(trajectory, model, completed, filename=None):
        if filename is None:
            filename = "trajectory_samples.jsonl" if completed \
                       else "failed_trajectories.jsonl"

        entry = {
            "conversations": trajectory,
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "completed": completed,
        }

        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

轨迹以 JSONL 格式追加到文件中，区分成功和失败的对话。
``ensure_ascii=False`` 保留了 CJK 字符和 emoji。

Scratchpad 转换
~~~~~~~~~~~~~~~~~

``trajectory.py`` 还包含两个辅助函数：

**``convert_scratchpad_to_think()`` ：** 将 ``<REASONING_SCRATCHPAD>`` 标签
转换为 ``<think`` 标签，用于 ShareGPT 格式的兼容性。

**``has_incomplete_scratchpad()`` ：** 检查内容中是否有未闭合的
``<REASONING_SCRATCHPAD>`` 标签——这在流式输出被截断时可能发生。

会话 ID 解析
--------------

SessionDB 支持灵活的会话 ID 解析策略：

**精确 UUID 匹配：** ``get_session(session_id)`` 直接按主键查找。

**UUID 前缀匹配：** ``resolve_session_id(prefix)`` 使用 ``LIKE 'prefix%'``
查找以给定前缀开头的唯一会话。如果前缀匹配多个会话，返回 ``None`` 。

**标题精确匹配：** ``get_session_by_title(title)`` 按标题精确查找。

**标题血脉解析：** ``resolve_session_by_title(title)`` 优先返回最新的
编号变体（例如 "项目 #3" 优先于 "项目"）。

**标题安全清理：** ``sanitize_title(title)`` 去除控制字符、零宽字符等。

导出与备份
------------

单会话导出
~~~~~~~~~~~~

.. code-block:: python

    def export_session(self, session_id):
        session = self.get_session(session_id)
        if not session:
            return None
        messages = self.get_messages(session_id)
        return {**session, "messages": messages}

全量导出
~~~~~~~~~~

.. code-block:: python

    def export_all(self, source=None):
        sessions = self.search_sessions(source=source, limit=100000)
        results = []
        for session in sessions:
            messages = self.get_messages(session["id"])
            results.append({**session, "messages": messages})
        return results

适合写入 JSONL 文件进行备份和分析。

消息清除
~~~~~~~~~~

.. code-block:: python

    def clear_messages(self, session_id):
        def _do(conn):
            conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            conn.execute(
                "UPDATE sessions SET message_count = 0, tool_call_count = 0 "
                "WHERE id = ?", (session_id,))
        self._execute_write(_do)

清除消息但保留会话记录本身——相当于"重置对话历史"。

配置参数速查表
----------------

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - 参数名
     - 默认值
     - 说明
   * - ``SCHEMA_VERSION``
     - 6
     - 当前数据库 schema 版本
   * - ``_WRITE_MAX_RETRIES``
     - 15
     - 写入重试最大次数
   * - ``_WRITE_RETRY_MIN_S``
     - 0.020
     - 重试最小等待时间（秒）
   * - ``_WRITE_RETRY_MAX_S``
     - 0.150
     - 重试最大等待时间（秒）
   * - ``_CHECKPOINT_EVERY_N_WRITES``
     - 50
     - 每 N 次写入执行 WAL 检查点
   * - ``MAX_TITLE_LENGTH``
     - 100
     - 标题最大长度（字符）
   * - SQLite timeout
     - 1.0
     - SQLite 内部忙等待超时（秒）

总结
------

Hermes 的会话状态系统是一个经过深思熟虑的持久化架构：

- **SQLite + WAL** 提供了零部署、高并发的存储基础
- **Schema 迁移链** 确保了数据库可以平滑升级
- **FTS5 + CJK 回退** 提供了跨语言的全文搜索能力
- **BEGIN IMMEDIATE + 随机抖动** 打破了多进程写竞争的护航效应
- **会话分支和标题血脉** 支持了复杂的会话管理场景
- **双模式 Token 计数** 适配了 CLI 和 Gateway 两种运行模式
- **防御性反序列化** 确保了即使数据损坏，会话也能继续

这个系统是 Hermes 能够在多平台、多进程环境下稳定运行的基石。
