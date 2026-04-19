---
name: sync-docs
description: Sync Sphinx docs from upstream hermes-agent source code. Run this periodically to keep documentation up to date.
---

# Sync Docs Skill

Sync documentation from the upstream hermes-agent source repository, analyze changes, update RST files, and publish.

## Prerequisites

- Source repo at `/Users/liyifan/hermes-agent` (or set `HERMES_SOURCE_REPO`)
- This repo at `/Users/liyifan/hermes-docs`
- uv venv at `.venv/` (create with `uv venv .venv --python 3.13 && uv pip install --python .venv/bin/python sphinx sphinx-rtd-theme sphinxcontrib-mermaid`)

## Steps

### Step 1: Fetch upstream changes

```bash
./scripts/sync-upstream.sh
```

This updates `.last-sync` and writes `scripts/changes-summary.md` with all commits and diffs since last sync.

If no changes found, stop here.

### Step 2: Analyze changes

Read `scripts/changes-summary.md`. For each commit, determine which documentation topics are affected using the source mapping in `CLAUDE.md`.

### Step 3: Update RST files

For each affected topic, read the corresponding source files to understand the actual code changes, then update the matching RST file under `chapters/`.

Rules:
- Preserve existing RST structure and formatting style
- Use Chinese for prose (this is a Chinese documentation book)
- Keep Mermaid diagram references accurate
- Add new sections if significant new features are introduced
- Update existing descriptions if behavior changed

### Step 4: Verify build

Use the uv virtual environment (not system Python):

```bash
# If .venv doesn't exist yet:
# uv venv .venv --python 3.13
# uv pip install --python .venv/bin/python sphinx sphinx-rtd-theme sphinxcontrib-mermaid

.venv/bin/python -m sphinx -b html . _build/html
```

Check for warnings or errors. Fix any issues before committing.

### Step 5: Commit and push

```bash
git add chapters/ diagrams/ index.rst
git commit -m "docs: sync from hermes-agent ${LAST_SYNC:0:8}..${NEW_SYNC:0:8}"
git push origin main
```

GitHub Actions will auto-build and deploy to GitHub Pages.

## Source-to-Doc Mapping

| Source area | RST file |
|---|---|
| Agent dispatch, main loop | `chapters/agent-loop.rst` |
| Terminal UI, TUI components | `chapters/cli-ui.rst` |
| Config loading, profiles | `chapters/config-management.rst` |
| Context window, compaction | `chapters/context-compression.rst` |
| CLAUDE.md, AGENTS.md, .claude/ | `chapters/file-reference.rst` |
| Gateway server, RPC pool | `chapters/gateway-rpc.rst` |
| MCP server connections | `chapters/mcp-integration.rst` |
| Provider selection, model tier | `chapters/model-routing.rst` |
| Plugin loading | `chapters/plugin-system.rst` |
| Prompt construction | `chapters/prompt-pipeline.rst` |
| Permission model, sandbox | `chapters/security.rst` |
| Session persistence | `chapters/session-state.rst` |
| Skill registration | `chapters/skill-system.rst` |
| Tool definitions, dispatch | `chapters/tool-system.rst` |
