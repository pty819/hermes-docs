# Hermes Agent 架构深度解析

> 通过深度分析真实生产代码，学习 AI Agent 架构设计

**在线阅读：** https://pty819.github.io/hermes-docs/

---

## 这本书讲什么？

AI Agent 从学术概念迅速走入工程现实（AutoGPT、CrewAI、LangGraph…），但生产环境中的真实挑战与 demo 展示之间存在巨大鸿沟——API 限流、多轮对话管理、上下文窗口压缩、错误恢复、凭证轮换、提供商回退……这些问题在论文和框架文档里几乎找不到系统论述。

本书选择 [Hermes Agent](https://github.com/nousresearch/hermes-agent)（Nous Research 开源的自进化 AI Agent）作为学习对象，核心 `run_agent.py` 约 11000 行，工具系统约 3000 行——规模足够覆盖关键挑战，又可被个人完整理解。

### 你会学到什么

- Agent Loop 的完整实现细节（`run_conversation` 逐行分析）
- 工具注册、发现、调度、自注册架构
- 上下文压缩：头尾保护、工具输出裁剪、摘要生成
- 错误分类管道与多级 Failover 机制
- 会话持久化（SQLite）、Prompt 构建、模型路由
- MCP 集成、插件系统、技能系统
- 从零构建生产级 Agent 的实践指南

### 阅读路径

| 背景 | 推荐起点 |
|------|----------|
| 完全新手 | 第一部分基础概念 → Agent Loop |
| 有 Agent 开发经验 | 直接跳到 Agent Loop / 工具系统 / 上下文压缩 |
| 做代码审查/架构评审 | Agent Loop + 错误分类与恢复 + 会话持久化 |

---

## 章节结构

### 第一部分：基础
- 基础概念（ReAct、Reflexion 等架构演进）
- Agent Loop（核心章节）
- 工具系统

### 核心架构
| 章节 | 内容 |
|------|------|
| `agent-loop` | 最重要章节——`run_conversation` 逐行分析，7 大主题，5+ Mermaid 图表 |
| `tool-system` | 工具注册、发现、调度、自注册模式 |
| `prompt-pipeline` | 系统提示词构建、身份注入、平台适配 |
| `context-compression` | 自动压缩机制、摘要生成、头尾保护、工具输出裁剪 |
| `session-state` | SQLite 存储、消息冲刷、跨轮次状态恢复 |
| `model-routing` | 提供商选择、模型分级逻辑 |
| `config-management` | 配置加载、解析、Profile 机制 |

### 平台层
| 章节 | 内容 |
|------|------|
| `cli-ui` | 命令行界面与 TUI |
| `gateway-rpc` | 网关服务器、RPC 连接池 |
| `mcp-integration` | MCP 服务器连接、工具路由 |
| `plugin-system` | 插件加载与生命周期 |
| `skill-system` | 技能注册与调用 |
| `security` | 权限模型、沙箱机制 |

### 第二部分：经验与实战
- `lessons` — Agent 工程原则和反模式
- `build-your-own` — 从零构建生产级 Agent 实践指南

### 附录
- `glossary` — 术语表
- `file-reference` — 核心文件索引（`run_agent.py`、`model_tools.py`、`error_classifier.py` 等）

---

## 部署

**GitHub Pages：** https://pty819.github.io/hermes-docs/

每次 push 到 `main` 分支，GitHub Actions 自动构建并发布。

**本地构建：**
```bash
pip install sphinx==8.2.3 sphinx-rtd-theme==3.0.2 sphinxcontrib-mermaid==1.0.0
sphinx-build -b html . _build/html
```

---

## 源码对照

每个章节都标注了对应的 Hermes Agent 源码路径：

| 章节 | RST 文件 | 源码路径 |
|------|----------|----------|
| Agent Loop | `chapters/agent-loop.rst` | `src/tui/`, agent dispatch |
| CLI / UI | `chapters/cli-ui.rst` | `src/tui/` |
| 上下文压缩 | `chapters/context-compression.rst` | context window, compaction |
| 网关 / RPC | `chapters/gateway-rpc.rst` | Gateway server, RPC pool |
| MCP 集成 | `chapters/mcp-integration.rst` | MCP server connections |
| 会话状态 | `chapters/session-state.rst` | SessionDB, state management |
| 工具系统 | `chapters/tool-system.rst` | Tool definitions, dispatch |
| …… | …… | …… |

---

## 与上游同步

上游 Hermes Agent 更新后，运行同步脚本并根据变更摘要更新文档：
```bash
./scripts/sync-upstream.sh
# 阅读 scripts/changes-summary.md，逐一更新对应 RST 文件
git add . && git commit && git push
# GitHub Actions 自动构建发布
```
