# Hermes Docs - Sphinx Documentation

This repo contains the source (RST) for "Hermes Agent 架构深度解析", published to GitHub Pages via GitHub Actions.

## Syncing from Upstream

Run the sync script to fetch latest changes from the hermes-agent source:

```bash
./scripts/sync-upstream.sh
```

This generates `scripts/changes-summary.md` listing all commits since the last sync. Then ask Claude to update the docs based on the summary.

### Manual sync process

1. `./scripts/sync-upstream.sh` — fetches upstream and writes change summary
2. Read `scripts/changes-summary.md` to see what changed
3. For each relevant change, update the corresponding RST file(s)
4. Commit and push — GitHub Actions auto-builds and deploys

## Source repo mapping

| Topic | RST file | Source paths |
|---|---|---|
| Agent loop | `chapters/agent-loop.rst` | `src/tui/`, agent dispatch logic |
| CLI / UI | `chapters/cli-ui.rst` | `src/tui/`, terminal UI components |
| Config management | `chapters/config-management.rst` | Config loading, resolution, profiles |
| Context compression | `chapters/context-compression.rst` | Context window, compaction logic |
| File reference | `chapters/file-reference.rst` | `CLAUDE.md`, `AGENTS.md`, `.claude/` |
| Gateway / RPC | `chapters/gateway-rpc.rst` | Gateway server, RPC pool, handlers |
| MCP integration | `chapters/mcp-integration.rst` | MCP server connections, tool routing |
| Model routing | `chapters/model-routing.rst` | Provider selection, model tier logic |
| Plugin system | `chapters/plugin-system.rst` | Plugin loading, lifecycle |
| Prompt pipeline | `chapters/prompt-pipeline.rst` | Prompt construction, system prompts |
| Security | `chapters/security.rst` | Permission model, sandbox |
| Session state | `chapters/session-state.rst` | Session persistence, state management |
| Skill system | `chapters/skill-system.rst` | Skill registration, invocation |
| Tool system | `chapters/tool-system.rst` | Tool definitions, dispatch |

## Build locally

```bash
pip install sphinx==8.2.3 sphinx-rtd-theme==3.0.2 sphinxcontrib-mermaid==1.0.0
sphinx-build -b html . _build/html
```

## Push to publish

Push to `main` triggers the GitHub Actions workflow which builds and deploys to GitHub Pages automatically.
