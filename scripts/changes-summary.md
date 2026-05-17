# Changes since last sync

From: 39f451f5ada6
To:   280c63ce9162
Date: 2026-05-17T18:43:16Z

## Commits

- **fix(mcp): prevent parallel-safe prefix collisions** (280c63ce9)
- **test(delegation): add regression test for runtime missing 'provider' key** (874dad5cc)
- **fix(delegation): preserve configured_provider name when runtime returns 'custom'** (84667cbc2)
- **Merge pull request #27489 from NousResearch/bb/tui-composer-cursor-drift-v2** (08a66b2ae)
- **chore(release): AUTHOR_MAP entries for batch salvage group 6 contributors** (3f01e9493)
- **fix(dashboard): respect HERMES_BASE_PATH in WebSocket URLs (#25547)** (74031e1e2)
- **fix(web_server): pass proxy_headers=False to uvicorn.run so the dashboard's loopback gate sees the real connection peer** (714b3b2bd)
- **fix(gateway): use service restart path in Docker/Podman containers** (4afd479f5)
- **fix(agent): honor provider timeout config in streaming API calls** (55d6a1636)
- **fix(send_message): preserve Slack and Matrix thread targets resolved from channel directory** (2f28b60a4)
- **fix(transports): use monotonic deadlines in codex app-server turn loop** (d5a0815c3)
- **chore(release): map QuenVix, Mind-Dragon, soynchux emails for Tier 4 salvage** (37286a5bc)
- **fix(doctor): show xAI OAuth login state in hermes doctor Auth Providers section** (d0f551b44)
- **feat(status): show xAI OAuth login state in hermes status** (016893f5e)
- **fix(doctor): isolate per-provider OAuth imports to prevent fallback regression** (e10bb9dff)
- **fix(doctor): suppress stale XAI_API_KEY issue when xAI OAuth is healthy** (e89d78ff0)
- **chore: revert unrelated package-lock + nix hash churn to keep PR diff minimal** (caac54796)
- **review(tui): update stale comment refs to renamed visualLines helper** (711f46e4b)
- **chore(nix): refresh ui-tui npmDeps hash after wrap-ansi direct-dep drop** (220736f41)
- **review(tui): route cursorLayout through @hermes/ink wrapAnsi shim (Bun runtime parity)** (8c78f533d)
- **chore(nix): refresh ui-tui npmDeps hash for wrap-ansi dep addition** (55f13be65)
- **review(tui): address Copilot feedback on cursorLayout wrap-ansi rewrite** (1c0e59e55)
- **fix(tui): align composer cursorLayout with wrap-ansi to kill multiline cursor drift** (3b4dd6832)
- **fix(plugins/browser): carry forward requests.RequestException wrapping** (f36c89cd5)
- **fix(browser): self-review pass — dead-import, log levels, future-proofing** (c74ff2c8e)
- **fix(browser): ensure plugin discovery before registry lookup; parity harness** (1bb6f0372)
- **test(plugins/browser): coverage for the 3-plugin migration** (fec0a0da9)
- **refactor(browser): delete tools/browser_providers/ directory; migrate tests** (250caebeb)
- **feat(tools): mirror image_gen plugin-injection in Browser Automation picker** (1b9c539c6)
- **refactor(browser): dispatch _get_cloud_provider through agent.browser_registry** (40fde853f)
- **feat(browser): browser-use + firecrawl plugins; drop single-eligible shortcut** (a15cdfb05)
- **feat(browser): browserbase plugin (spike — first migration)** (b8138ac40)
- **feat(browser): add BrowserProvider ABC mirroring web_search_provider template** (c6e6909e5)
- **chore(release): AUTHOR_MAP entries for batch salvage group 5 contributors** (150b577da)
- **chore(deps): lazy-install boto3/botocore for bedrock adapter** (c02606a38)
- **fix(telegram): re-trigger typing indicator after sending messages** (1856bd9cc)
- **fix(doctor): SSH check ignores TERMINAL_SSH_USER, TERMINAL_SSH_PORT, TERMINAL_SSH_KEY** (c9298bba0)
- **refactor(security): extract _block_message helper to unify block logic in _parse_response** (dbeaaa47f)
- **fix(security): restore type safety and extract constant in shell hook block handler** (63805965e)
- **fix(security): honor shell hook blocks even when message/reason is absent** (aeda14611)
- **fix(webui): allow native text selection in chat via xterm.js bypass (#25720)** (8e3cfdfb6)
- **fix ACP start events for polished tools** (6622277f1)
- **fix(cli): sync _skill_commands after /reload-skills so Tab completion picks up new skills** (3c51da1cb)
- **fix(metadata): qwen3.6-plus has a 1M context window (#27008)** (d9abbe7fa)
- **test(restart_drain): assert i18n catalog resolved (#22266)** (5a2a858b8)
- **fix(gateway): add codex runtime telegram alias** (d87b27cff)
- **chore: ruff auto-fix PLR6201 resweep — tuple → set in membership tests (#27355)** (5fba23664)
- **fix(mcp-oauth): print SSH tunnel hint in _redirect_handler** (ad00777f0)
- **chore(release): map EloquentBrush0x email for #26642 salvage** (cc59880ab)
- **fix(tools): run post_setup in _reconfigure_provider() for env-var providers** (a9ba636d5)
- **feat(x_search): auto-enable toolset when xAI OAuth or XAI_API_KEY is configured (#27376)** (ad1aa1a03)
- **fix(matrix): warn on clock-skew silent message drops (#12614) (#27330)** (519657aa9)
- **Merge pull request #27248 from NousResearch/hermes/hermes-27dc9cc2** (56ad30de1)
- **fix: strip image parts for non-vision models with provider profiles + getattr-safe _custom_providers** (563b4d9e5)
- **fix(run_agent): guard memory provider init against empty/whitespace string** (36ad8336f)
- **fix(run_agent): isolate background review fork from external memory plugins (#27190)** (4ece521bc)
- **fix(fallback): forward custom_providers to fallback model context-length detection** (b5bcffe16)
- **fix(agent): reset _fallback_index at turn start even when no fallback activated** (4ab9a06a5)
- **fix(xai): surface provider 'error' SSE frame in Codex fallback stream (#27184)** (aa05ffba5)
- **fix(codex): rotate pool on usage limit 429 — port to extracted modules** (80fa92a49)
- **fix(copilot): GitHub Models 413 hint — port to extracted conversation_loop** (df22d2952)
- **feat: add supports_parallel_tool_calls for MCP servers (#26825) — port to tool_dispatch_helpers** (3fbedd732)
- **fix(agent): retry malformed anthropic stream parser errors — port to extracted modules** (fe4c87eb2)
- **fix(auxiliary): resolve xai oauth compression from pool — port to conversation_compression** (f885be030)
- **fix(xai-oauth): entitlement-403 chain — final state (ce0e189d3 + 9818b9a1a + 6784c8079 + dffb602f3)** (6975a2d9a)
- **port(refactor): deepseek thinking-mode (068c24f8a + cd9470f41) — no net change** (408aa4fbc)
- **fix(xai-oauth): recover from prelude SSE errors, gate reasoning replay, surface entitlement 403s** (6362e7197)
- **feat(nvidia): add NIM billing origin header — port to extracted modules** (27df24956)
- **feat(xai-oauth): add xAI Grok OAuth (SuperGrok Subscription) provider — port to extracted modules** (b07524e53)
- **fix(langfuse): complete observability fix — port to extracted conversation_loop** (7d221aa1f)
- **perf(run_agent): accumulate length-continuation prefix via list+join** (a77ca9295)
- **fix(run_agent): detect kimi models via model name for reasoning pad** (94b3131be)
- **feat(agent): Added gemma 4 to reasoning allowlist** (8f3bc17db)
- **Merge origin/main into pr-27248 (resolving run_agent.py = ours)** (152d42d1a)
- **chore(release): AUTHOR_MAP entries for batch salvage group 4 contributors** (7322816ef)
- **fix(line): add trust_env=True to all _LineClient aiohttp sessions** (35b7befc6)
- **fix: respect user-configured vision model for OpenRouter** (52c89715a)
- **[agent] fix: harden api server response headers** (5631345b1)
- **fix(auxiliary): resolve api_key_env alias in named custom provider path of resolve_provider_client** (b389796ae)
- **feat(gateway): extract auto-TTS markdown strip into prepare_tts_text() hook** (0afab4a32)
- **fix(gateway): preserve underscores in plain-text identifiers** (a3017508b)
- **Local: doctor uses x-goog-api-key for Google generativelanguage endpoint** (364a1dd29)
- **fix(gateway): avoid zsh status variable in update wrapper** (fdd455bc5)
- **fix(gateway): add trust_env=True to aiohttp sessions in SMS, Slack, Teams, Google Chat adapters** (c1ae18ee8)
- **chore(release): AUTHOR_MAP entries for batch salvage group 3 contributors** (04bb30730)
- **fix(scripts): fix UnicodeEncodeError in footgun checker on Windows** (8973b00ff)
- **fix(tests): mock keychain in TestReadClaudeCodeCredentials to prevent credential leakage** (a52f014a8)
- **fix(cron): prevent parallel job result loss on exception** (7a7e78a36)
- **feat: inject current time into goal judge prompt** (6158964ff)
- **fix(model-switch): probe /models for custom providers without api_key** (6f50c26b2)
- **fix(windows): suppress console window flash on subprocess spawns** (8bf09455d)
- **fix(gateway): add direct_messages_topic_id for synthetic Telegram DM events** (5338250da)
- **fix: strip image parts for non-vision models with provider profiles** (75e5d0f6b)
- **fix: preserve discover_models in _normalize_custom_provider_entry** (bde3c7982)
- **fix(api_server): coerce stringified booleans in request payloads** (8d4766afc)
- **refactor(run_agent): review fixes — keyword-forward __init__, drop dead code, tighten guards** (47823790b)
- **fix(install.ps1): Stage-Node honest reporting + reject empty -Stage** (fb138d91c)
- **fix(install.ps1): trim completion banner + strip em-dash in test** (3925be279)
- **fix(install.ps1): address Copilot review on #27224** (c0b64f087)
- **feat(install.ps1): stage protocol + Windows clean-VM hardening pass** (e5f19af2a)
- **fix(teams): fall back to default port on invalid port config** (ea2ee51f0)
- **chore(release): AUTHOR_MAP entries for batch salvage group 2 contributors** (e90a52dea)
- **fix(deepseek): set default_aux_model on profile so aux warning stops firing** (773a0faca)
- **fix(run_agent): detect kimi models via model name for reasoning pad** (9a9f8a6d9)
- **fix(install): use resolved python variable in setup_open_webui.sh** (5f72dd817)
- **fix(credential_pool): parse ISO-string last_status_at during from_dict rehydration (#25516)** (1a4e64ba0)
- **feat(gateway): add .ts/.py/.sh to SUPPORTED_DOCUMENT_TYPES** (508b022ac)
- **fix(delegate): tool_trace false-positive error detection for short outputs** (7d09bb191)
- **fix(windows): make PowerShell installer parse in 5.1** (4279da4db)
- **fix: add paste collapse logging to aid debugging** (7282ef1b9)
- **fix(run_agent): guard memory provider init against empty/whitespace string** (8d756a421)
- **fix(kanban): --severity filter uses >= comparison per documented behavior (#26379)** (1eadb069c)
- **test(skills): add regression test for skill load failure returning None** (782d74373)
- **fix(skills): return None instead of truthy stub when skill load fails** (4b17c2411)
- **fix: remove unused import and hoist module-level constant** (60531889d)
- **chore(release): map 0xchainer and kronexoi emails for upcoming salvages** (a81cfd0a0)
- **test(gateway): add smoke test for logger init (regression guard for #27154)** (57feef320)
- **fix(gateway): add missing logger definition to prevent NameError in _all_platforms** (4e9cedcd4)
- **docs(readme): remove hermes-eval and Hermes MemPalace from Community links (#27271)** (32c3f06a5)
- **Merge pull request #27251 from NousResearch/bb/skin-render-magenta-bleed** (9f182bd7b)
- **fix(review): address Copilot follow-up on sanitizer and file decode errors** (a65f723e6)
- **fix(tui): harden ansi sanitizers for dangling CSI** (7e1788db5)
- **fix(cli): satisfy ruff encoding requirement in send_cmd** (9b2d58159)
- **fix(tui): harden Terminal.app render behavior** (290bf9310)
- **refactor(run_agent): extract 10 more helpers to agent/agent_runtime_helpers.py** (94c3e0ab8)
- **fix(run_agent): isolate background review fork from external memory plugins (#27190)** (973f27e95)
- **chore(release): AUTHOR_MAP entries for batch salvage contributors** (96b7f3da4)
- **feat(agent): Added gemma 4 to reasoning allowlist** (7244116b6)
- **fix(fallback): forward custom_providers to fallback model context-length detection** (21078ebce)
- **docs(dashboard): clarify chat tab tui flag** (903ac23bc)
- **docs(spotify): document Home Assistant speaker routing** (c741eacd0)
- **docs(security): document YOLO mode visual indicators added in #26238** (49bd95c43)
- **docs(cron): document name-based job lookup from #26231** (6f7292a55)
- **docs(delegation): document api_mode wire-protocol override from #26824** (86f3776a7)
- **docs(delegation): show api_mode override in custom-endpoint example** (31a805883)
- **docs: add computer-use-linux community MCP** (d5ce85c42)
- **docs: add Hermes MemPalace to Community plugins section** (df80bda77)
- **docs: add hermes-eval to Community section** (a1e3d7969)
- **feat(discord): allow_any_attachment config to accept arbitrary file types** (407a11b41)
- **refactor(run_agent): extract __init__ (1,381 LOC) to agent/agent_init.py** (9f408989c)
- **refactor(run_agent): extract run_conversation to agent/conversation_loop.py** (053025238)
- **refactor(run_agent): move review prompts to agent/background_review.py** (d35ee7bcd)
- **refactor(run_agent): extract Codex runtime + assorted helpers to dedicated modules** (c42fa94af)
- **refactor(run_agent): extract streaming API caller (893 LOC) to agent/chat_completion_helpers.py** (0430e71ec)
- **refactor(run_agent): extract chat-completion helpers to agent/chat_completion_helpers.py** (4b25619bc)
- **refactor(run_agent): extract stream diagnostics to agent/stream_diag.py** (57f6762ca)
- **refactor(run_agent): extract tool execution to agent/tool_executor.py** (79559214a)
- **refactor(run_agent): extract system-prompt builder to agent/system_prompt.py** (2d2cd5e90)
- **refactor(run_agent): extract context compression to agent/conversation_compression.py** (5311d9959)
- **refactor(run_agent): extract background memory/skill review to agent/background_review.py** (1f6eb1738)
- **refactor(run_agent): extract OpenAI proxy, safe stdio, IterationBudget** (5f309ae68)
- **refactor(run_agent): extract tool-dispatch helpers to agent/tool_dispatch_helpers.py** (59f1c0f0b)
- **refactor(run_agent): extract message sanitization to agent/message_sanitization.py** (885d1242a)
- **Port from Kilo-Org/kilocode#9434: strip historical media after compression (#27189)** (3b3909690)
- **test(plugins): cover _discover_all_plugins recursion + cross-link loader** (5cbe0b1c4)
- **refactor(plugins): drop dead bundled-source guard in _discover_all_plugins** (21be7025c)
- **fix(plugins): remove unreachable hermes tools → Langfuse path** (8ab8bc2f0)
- **fix(plugins): surface category-namespaced plugins in hermes plugins list** (9b82586c6)
- **feat(cli): add `hermes send` to pipe script output to any messaging platform (#27188)** (29b1bd0e2)
- **fix(agent): reset _fallback_index at turn start even when no fallback activated** (33528b428)
- **fix(xai): surface provider 'error' SSE frame in Codex fallback stream (#27184)** (2b193907d)
- **feat(status): append session recap to /status output (#27176)** (e21cb8d14)
- **feat(cli): show ▶ N indicator in status bar when /background tasks are running (#27175)** (226cee43d)
- **fix(telegram): restore DM topic typing indicator** (6f817e144)
- **fix(codex): rotate pool on usage limit 429** (e51d74ab9)
- **fix(xai): drop stale X Premium+ hint from entitlement 403 surfacing (#27110)** (dffb602f3)
- **fix(mcp): validate remote URLs up-front with a clear error (#27105)** (fb05f5d4b)
- **fix(moonshot): strip $ref siblings and collapse tuple items in tool schemas (#27104)** (93e109a1d)
- **Port from cline/cline#10343: periodic gateway memory logging (#27102)** (dc3d0fe14)
- **feat(cli): add /exit --delete flag to remove session on quit (#27101)** (fc03c95da)
- **fix(update): stream npm install output so postinstall progress is visible (#18840)** (c844d15c3)
- **fix(update): make Camofox lazy-installed instead of eager (#27055)** (05af78c53)
- **docs(release): expand v0.14.0 highlights with newcomer-friendly context (#27053)** (8a2b2b9f6)
- **fix(signal): read groupV2.id in envelope, fall back to legacy groupInfo (#27051)** (6c2406c5e)
- **docs(tools): add video_generate / video_gen toolset to user-facing tool docs (#27050)** (35f25523c)
- **docs(release): rewrite v0.14.0 highlights for excitement framing (#27035)** (683698742)
- **fix(acp): replay session history before responding to session/load (#12285 follow-up) (#26957)** (3034eee38)
- **fix(acp): replay assistant reasoning as agent_thought_chunk on session/load (#12285) (#26943)** (f3a4af9cf)
- **chore: release v0.14.0 (2026.5.16) (#26862)** (a91a57fa5)
- **test(security): regression guard for OAuth PKCE state/verifier separation** (72f94f4a7)
- **style: move secrets import alongside other function-level imports** (345821b4a)
- **fix(security): separate OAuth PKCE state from code_verifier** (fcd9011f8)
- **fix(gateway): merge rapid TEXT follow-ups during active sessions (#4469) (#26822)** (585d6b643)
- **fix(copilot-acp): tighten deprecation detection + sharpen GitHub Models 413 hint** (374dc81c2)
- **test: add tests for copilot ACP deprecation detection and Azure URL mapping** (b85b938b1)
- **fix: detect gh-copilot deprecation and improve GitHub Models 413 errors (#10648)** (4ded3ede3)
- **chore: add worlldz to AUTHOR_MAP for #26704 salvage** (7bb97b952)
- **fix(doctor): suppress stale direct-key issues when oauth is healthy** (d0a183cad)
- **feat(skills): add osint-investigation optional skill (closes #355) (#26729)** (5f91b1a48)
- **security(deps): bump aiohttp, anthropic, cryptography to CVE-fixed versions (#26830)** (d725407c5)
- **Inspired by Claude Code: tighten dangerous-command detection (#26829)** (6ba35ec33)
- **feat: add supports_parallel_tool_calls for MCP servers (#26825)** (395e9dd9e)
- **fix(delegation): honor api_mode + auto-detect anthropic_messages URLs (#26824)** (c445f48b7)
- **feat(x_search): gated X (Twitter) search tool with OAuth-or-API-key auth (#26763)** (74d0b392e)
- **security: sanitize tool error strings before injecting into model context (#26823)** (627f8a5f1)
- **fix(tui): keep Ink displayCursor in sync with fast-echo writes so cursor stops drifting (#26717)** (70b663504)
- **feat(skills): add optional pinggy-tunnel skill** (559c6ad94)
- **docs: add Programmatic Integration overview (closes #360)** (afb97dbc5)
- **feat(plugins): tool override flag for replacing built-in tools (closes #11049) (#26759)** (016c772e7)
- **fix(agent): retry malformed anthropic stream parser errors** (9c304a7f5)
- **chore(skills/darwinian-evolver): AUTHOR_MAP + docs regen** (53637fb17)
- **feat(skill): darwinian-evolver optional skill** (c9b32a654)
- **Merge pull request #26711 from NousResearch/austin/fix/dashboard-kanban** (e377833fa)
- **Revert "fix(cli): tolerate unreadable dirs when building systemd PATH"** (16ff9464a)
- **fix(cli): tolerate unreadable dirs when building systemd PATH** (965610f92)
- **fix(dashboard): align Ukrainian Kanban Ready column help** (ca413c616)
- **fix(windows): silence tirith-unavailable banner + skip install/spawn attempts on unsupported platforms (#26718)** (c5dc9700e)
- **fix(docs): unique sidebar keys for duplicate skill categories (#26726)** (a31191c3f)
- **fix(tui): allow transcript scroll + Esc during approval/clarify/confirm prompts (#26414)** (44b63fc6d)
- **fix(auxiliary): resolve xai oauth compression from pool** (97a32afdc)
- **fix(dashboard): clarify Kanban Ready vs assignment** (63503ebb1)
- **Merge pull request #26702 from NousResearch/remove-pip-docs** (c7db6a580)
- **remove pip installation method from docs** (86a368d83)
- **fix(tui): width-aware markdown table rendering with vertical fallback (#26195)** (55c9f3206)
- **fix(tui): handle timeout/error subagent statuses in /agents (#26687)** (006937f7d)
- **fix(tui): keep DECSTBM scroll region off bottom row (#26683)** (566d8f0d7)
- **fix(xai-oauth): lead entitlement-403 hint with X Premium+ gotcha (#26672)** (6784c8079)
- **fix(xai-oauth): rewrite entitlement-403 hint to not accuse subscribers (#26666)** (9818b9a1a)
- **fix(xai-oauth): break entitlement-403 credential-refresh loop, bump grok-4.3 context to 1M (#26664)** (ce0e189d3)
- **feat(docs): show per-skill pages in the left sidebar (#26646)** (dc4cde278)
- **fix(deepseek): wire thinking-mode via DeepSeekProfile, not legacy fallback** (cd9470f41)
- **feat(deepseek): add thinking.type + reasoning_effort mapping for DeepSeek API** (068c24f8a)
- **fix(xai-oauth): recover from prelude SSE errors, gate reasoning replay, surface entitlement 403s (#26644)** (31ba2b0cb)
- **fix(windows): stop spamming cwd-missing + tirith-spawn warnings on every terminal call** (4aec25bc4)
- **fix(memory): eliminate TOCTOU race in Windows file lock creation** (7fee1f61e)
- **fix(delegate): guard heartbeat join against unstarted thread** (606836331)
- **fix(delegate): move heartbeat thread start inside try block to prevent orphan** (2d7182f72)
- **feat(skills/notion): overhaul for Notion Developer Platform (May 2026) (#26612)** (42070ecef)
- **ci: reject PRs with no common ancestor on main (#26611)** (887ba1fb0)
- **docs(xai): link OAuth-over-SSH guide from xAI provider surfaces (#26610)** (233d4170c)
- **docs: add hermes postinstall to installation + quickstart, fix update --check description** (a480d345e)
- **refactor: DRY cleanup from code review** (47c0efe1c)
- **docs: add pip install path to installation, quickstart, updating, and CLI reference** (164a77dec)
- **feat: add `hermes postinstall` command for pip users** (99b81cd54)
- **chore: gitignore hermes_cli/scripts/ (bundled at wheel build time)** (b1edf3dfc)
- **feat: wire ensure_dependency into TUI and browser tool call sites** (c57709a3d)
- **chore(ci): pin actions/setup-node to SHA for supply-chain consistency** (e38a478c0)
- **fix(update): handle --check for pip installs (missed code path)** (55a7c45d3)
- **refactor: fix review findings — remove duplicate imports and deduplicate update command** (96917fb74)
- **feat: add ensure_dependency() wrapper + ship install.sh in wheel** (259ae846c)
- **chore(config): expand ensure_hermes_home to create full directory scaffold** (bea96e5ca)
- **feat(update): support pip install --upgrade for PyPI installs** (79afa5070)
- **feat(config): detect pip install method and recommend correct update command** (624ce11ee)
- **feat(tui): find bundled entry.js from wheel before falling back to npm build** (b2bf65844)
- **fix(gateway): build service PATH from existing dirs only, include ~/.hermes/node_modules** (d69eab1ef)
- **fix(doctor): generate config from defaults when template file is missing** (c4bda3f27)
- **feat(install): add --ensure and --postinstall modes for targeted dep bootstrap** (cc07e30f4)
- **feat(banner): check PyPI for updates when not a git install** (384ec9684)
- **ci(pypi): build web dashboard + TUI bundle before creating wheel** (3215ef160)
- **docs(hermes_tools_mcp_server): align scope docstring with EXPOSED_TOOLS (#26603)** (032fb8422)
- **fix(gateway): keep running when platforms fail; add per-platform circuit breaker + /platform (#26600)** (518f39557)
- **fix(auth): point SSH OAuth users at the tunnel they actually need (#26592)** (3b9368a0c)
- **Merge pull request #26048 from stephenschoettler/fix/discord-e2e-history-mock** (9e67c8e8b)
- **fix(install.ps1): restore EAP=Continue around uv python install, skip Store stub (#26586)** (622c27e55)
- **fix(acp): replay native todo plans** (bd3a5873e)
- **fix(acp): emit native plan updates for todo** (4444d5fe4)
- **chore(release): add AUTHOR_MAP entry for kchantharuan@nvidia.com** (6fc0fa6e5)
- **feat(nvidia): add NIM billing origin header** (13c3d4b4e)
- **fix(async): close unscheduled coroutines in all threadsafe bridges (#26584)** (4e89c5308)
- **fix(env-flags): widen truthy-only session env checks to sibling sites** (931caf2b2)
- **fix(cronjob): require explicit truthy session env values** (734aa0f36)
- **docs(xai-oauth): add xai-oauth to provider enumeration pages (#26542)** (4ad5fa702)
- **chore(xai-oauth): trim CORS allowlist to xAI auth origins** (aac6d97a1)
- **test(xai-oauth): use grok-4.3 instead of retiring grok-code-fast-1** (7d7cdd48e)
- **docs(xai-oauth): correct logout command (was hermes auth remove)** (1e4801b8d)
- **refactor(transports/codex): trim duplicated cache-key comments** (7fdc16dd4)
- **fix(xai-http): preserve ~/.hermes/.env fallback and XAI_STT_BASE_URL precedence** (e13c1b806)
- **chore(release): map Jaaneek@users.noreply.github.com to Jaaneek** (9eef53b96)
- **fix(tools): video_gen picker reflects active xAI selection and runs xai_grok post_setup** (e4d7a5dff)
- **feat(xai-oauth): add xAI Grok OAuth (SuperGrok Subscription) provider** (b62c99797)
- **fix(tui): restrict fast-echo bypass to ASCII so Vietnamese/CJK/IME input renders correctly (#26011)** (9fb40e6a3)
- **fix(tui): autonomous background process completion notifications (#26071) (#26327)** (d5416284f)
- **fix(langfuse): complete observability fix — trace I/O, tool outputs, placeholder credentials (closes #22342, #22763) (#26320)** (db84a78e6)
- **chore(release): map brian@dralth.com to btorresgil for #22345 salvage (#26319)** (f199cd9f8)
- **fix(codex-runtime): de-dup [plugins.X] tables and stop leaking HERMES_HOME into config.toml** (77276070f)
- **fix(codex-runtime): keep migrated root keys top-level** (274217316)
- **fix(tools): wrap browser provider network calls with error handling** (13c72fb48)
- **fix(url-safety): allow only http and https schemes** (6af994232)
- **fix(slack): guard split()[0] against whitespace-only command text** (837395685)
- **chore(release): add AUTHOR_MAP entry for nidhi-singh02** (94bdc63ff)
- **fix(tools): add return_exceptions to asyncio.gather in web_tools** (eacb398f7)
- **chore(release): add AUTHOR_MAP entry for nidhi-singh02** (5301cc212)
- **fix(cli): log swallowed exception in runtime model auto-detection** (c4a21d783)
- **chore(release): add AUTHOR_MAP entry for amethystani** (59c7cc64f)
- **fix(mcp): pre-compile env-var regex and unify interpolation** (55f3262e7)
- **fix(providers): set User-Agent on ProviderProfile.fetch_models** (5360b5424)
- **chore(release): add AUTHOR_MAP entries for InB4DevOps** (647cc0bb0)
- **perf(run_agent): accumulate length-continuation prefix via list+join** (4f8aaf104)
- **feat(cli): show YOLO mode warning in banner and status bar** (b6e07417c)
- **chore: wire simplex docs into sidebar + AUTHOR_MAP** (47614dbfc)
- **feat(gateway): add SimpleX Chat platform plugin** (09d9724a0)
- **feat(acp): hermes acp --setup-browser bootstraps browser tools for registry installs** (85782a4ed)
- **chore(release): add AUTHOR_MAP entry for buntingszn** (9f57f2286)
- **feat(cron): support name-based lookup for job operations** (6682f91b8)
- **docs(cron): worked recipes for the wakeAgent pre-run gate (#26229)** (05d9f641c)
- **feat(image-gen): actionable setup message when no FAL backend is reachable (#26222)** (9329e0669)
- **security(deps): add upper bounds to 5 loose deps + document supply chain policy (#24226)** (04b1fdaec)
- **fix(whatsapp): fail fast when Baileys sendMessage hangs** (681778a0b)
- **chore(release): add AUTHOR_MAP entry for CoinTheHat** (0161d4bb6)
- **fix: clean stale conversation mappings on response eviction/deletion** (814c60092)
- **fix(gateway): isinstance-guard string-form 429 error body** (23ac522d3)
- **fix(session): persist auto-reset state across gateway restarts** (e0e7397c3)
- **feat(skills-hub): add huggingface/skills as trusted default tap (#2549)** (e0e4856d4)
- **refactor(yuanbao): improve quote media fallback — move to DispatchMiddleware, tighten conditions** (0086cdaf9)
- **fix(yuanbao): resolve quoted file/image via transcript lookup when quote desc lacks ybres** (fc2754dbd)
- **feat(yuanbao): prioritize quote media refs over history backfill in DispatchMiddleware** (3df26b925)
- **feat(yuanbao): add quote_media_refs extraction to QuoteContextMiddleware** (80efe664c)
- **feat(yuanbao): add _parse_resource_id and update _extract_text for ybres anchors** (d57a4b3eb)
- **ci: add PyPI publish workflow (salvaged from #25901) (#26148)** (6bdad1f3b)
- **fix(goals): raise judge max_tokens 200 → 4096, make configurable** (f9ad7400e)
- **revert(cli): drop scrollback box width clamp (#25975), restore full-width borders (#26163)** (965ae7fa9)
- **test(cli): cover light-mode detection + SkinConfig.get_color remap** (cbd1f8e4b)
- **fix(cli): kill resize scrollback duplication + light-mode visibility** (f8745f59c)
- **fix(deps): pin brotlicffi so aiohttp can decode Discord's Brotli attachments** (bcca5ed34)
- **feat(acp-registry): switch to uvx distribution, drop npm launcher** (c8c6ce173)
- **chore: remove Atropos RL environments and tinker-atropos integration (#26106)** (5af672c75)
- **chore(release): bump ACP Registry assets in lockstep with pyproject** (d36413211)
- **feat: add ACP registry metadata for Zed** (4c9439620)
- **fix(aux): surface Nous auth-unavailable warning in auxiliary client** (e8b9f5ff9)
- **chore(release): add AUTHOR_MAP entry for outdoorsea** (d3d591608)
- **fix(cli): fall back to SelectSelector when kqueue can't watch stdin** (eabd8c1fd)
- **test(run-agent): isolate Nous provider parity model** (e8a4c85e8)
- **test(e2e): fix Discord mock exception surface** (ad7d3bc84)
- **fix(browser): honor pre-set AGENT_BROWSER_ARGS and document the bypass** (4695d2716)
- **fix(browser): use correct env var for --no-sandbox bypass** (8ed2ef6f4)
- **Merge pull request #25957 from stephenschoettler/fix/main-ci-unblocker-after-21012** (1702a94c8)
- **chore(release): map phil.thomas@gametime.co -> explainanalyze** (55622b552)
- **chore(release): map phil.thomas@gametime.co -> explainanalyze** (74e47c081)
- **fix(cli): wire /sessions slash command in the classic CLI** (d6c488f2d)
- **fix(proxy): suppress false-positive windows-footgun on guarded add_signal_handler** (09d970160)
- **chore(release): map agorgianitisj@hotmail.com -> johnisag** (db82c453b)
- **fix(web): handle non-UTF8 Windows console encodings in _build_web_ui** (38ea2a57a)
- **fix(web): cross-platform sync-assets + surface build errors on failure** (085464053)
- **fix(lsp): shift baseline diagnostics into post-edit coordinates (#25978)** (19071529f)
- **fix(web): make sync-assets script cross-platform** (ed84637d1)
- **feat(discord): default history backfill on, expand to per-user + threads** (4abfb6bc2)
- **feat(discord): channel history backfill for multi-user sessions** (e84fe483b)
- **feat(proxy): local OpenAI-compatible proxy for OAuth providers (#25969)** (ccb5aae0d)
- **chore(release): map @luoyuctl in AUTHOR_MAP** (34fc94d1f)
- **fix(ui-tui): heal same-dimension alt-screen resize drift** (4813aaf0b)
- **fix(cli): clamp scrollback box widths + suppress status bar after resize (#25975)** (2844c888f)
- **chore(release): map @LeonSGP43 commit email in AUTHOR_MAP** (f491b07cb)
- **fix: preserve ansi output history on resize replay** (ac64d0c2c)
- **fix(voice): remove per-tool-call beep in CLI voice mode (#25967)** (624453568)
- **chore(release): map @1000Delta in AUTHOR_MAP** (7bf66a07b)
- **fix(cli): batch resize history replay** (06c6c1f0f)
- **fix(codex-app-server): attach redacted stderr tail to generic failures (#25929)** (fe83c4001)
- **fix(agent): keep image tool results from poisoning text-only sessions** (a28add199)
- **fix(gateway): prevent duplicate final send when only cosmetic edit failed** (bc42e62b1)
- **fix(gateway): load streaming config from nested gateway.streaming key** (b4b8509fe)
- **fix(telegram): set REQUIRES_EDIT_FINALIZE so final MarkdownV2 edit is not skipped** (d44dafdb4)
- **fix(ci): stabilize shared test state after 21012** (5ce0067c0)
- **Merge pull request #21012 from stephenschoettler/fix/ci-pr-check-unblock** (cd64bed55)
- **fix(whatsapp): drop status broadcasts and channel newsletters before agent dispatch (#25845)** (9ed751b96)
- **skill(comfyui): add template-integrity reference from @purzbeats (#25828)** (b08f53a75)
- **fix(install): support non-sudo service-user installs on apt distros (#25814)** (78b842c99)
- **fix(agent/gemini-cloudcode): seed delta defaults for reasoning-only stream chunks** (26933c2f5)
- **fix(update): refresh lazy-installed backends on hermes update (#25766)** (72b5dd865)
- **test(toolsets): lock web search into default platform coverage** (436a0a271)
- **chore(release): map oswaldb22 noreply email for AUTHOR_MAP** (529ec85c7)
- **fix(terminal): prevent safety filter false positives on keywords inside quoted strings** (364ddd45e)
- **fix(gateway): forward image attachments to background agent tasks** (3adde245b)
- **fix: restrict .env file permissions to 0600** (a952ca3ff)
- **fix(gateway): enable text-intercept for multi-choice clarify fallback (#25567)** (f26098e22)
- **fix: stop retrying initial MCP auth failures** (1247ff2dc)
- **docs: clarify media impact on session context** (1dd33988e)
- **fix: use AUTOINCREMENT id for message ordering instead of timestamp** (c03acca50)
- **fix: read approvals.timeout from config in CLI approval callback** (8ae65d5c8)
- **chore(release): add AUTHOR_MAP entries for second new-contributor batch** (d8fdec16d)
- **fix(codex-runtime): retire wedged sessions + post-tool watchdog + OAuth refresh classify (#25769)** (12f755c9e)
- **fix(memory): skip OpenViking upload symlinks** (63991bbd9)
- **fix(telegram): restore model-switch success path + author map** (26deeea83)
- **fix(telegram): escape dynamic markdown in callback flows** (a69404052)
- **fix(install.ps1): pin uv sync to venv\, verify baseline imports on Windows (#25755)** (524490a40)
- **fix(cli): allow rotating broken OpenRouter / AI Gateway key in `hermes model` flow (#25750)** (17e0e9d17)
- **feat(discord): render clarify choices as buttons** (1dca6a696)
- **fix(install): preserve pip entry point when re-running on symlinked install** (c75e1a03f)
- **docs: update NovitaAI provider positioning (#25532)** (ddb8d8fa8)
- **test(novita): cache pricing, add provider test coverage, AUTHOR_MAP entry** (0f0e20ef8)
- **docs: update NovitaAI description to "90+ models, pay-per-use"** (1551ce46a)
- **feat: add NovitaAI as LLM provider** (c76e87957)
- **fix(background-review): silence memory provider teardown output leak** (55ba02bef)
- **fix(auxiliary): forward custom_providers to compression model context-length detection** (7becb19ea)
- **fix(gateway): keep QQBot reconnect loop alive** (8199ec380)
- **fix: do not inherit api_mode when delegating across providers** (f0e46c5e9)
- **fix(gateway): make Feishu ws connect override sync to preserve context manager** (71191b7e8)
- **fix: show context compaction status** (00ad3d3c9)
- **feat(whatsapp): surface quoted reply metadata** (bd33a48a5)
- **fix: gateway PID detection fails on Windows (two issues)** (fd9c1504d)
- **fix(auxiliary): skip providers without credentials immediately** (057f5a31d)
- **fix(discord): handle forwarded messages via message_snapshots** (b59ed9c6b)
- **fix(agent): add Xiaomi MiMo to reasoning_content echo-back providers** (efa97af7e)
- **docs(lsp): replace "git worktree" with "git repository" in LSP docs** (8de26e280)
- **docs(user-guide): point tirith link to correct repo** (796c8a2d6)
- **chore(release): add AUTHOR_MAP entries for 25-PR new-contributor batch** (2ff744ae2)
- **chore(release): add AUTHOR_MAP entry for mrshu** (16796acc8)
- **fix: simplify ACP approval bridging** (31b472179)
- **fix(tests): correct skin engine test API call** (35ce94a2f)
- **fix(cli): harden skin yaml parsing for invalid section types** (5f234d405)
- **feat(goals): /subgoal — user-added criteria appended to active /goal (#25449)** (8f19078c6)
- **fix(clipboard): only read PNG signature bytes, not entire file** (d110ce449)
- **fix(clipboard): reject non-png clipboard images when png normalization fails** (8db544b4d)
- **fix(tests): exercise profile-mode HERMES_HOME for honcho fallback** (c872f07c4)
- **fix(honcho): respect HOME-anchored default profile fallback** (d18618f48)
- **fix(web): preserve top-level error envelope on unconfigured systems** (4ca5e7244)
- **fix(web): align _LEGACY_PREFERENCE with legacy 7-provider order + doc cleanup** (657e6d87c)
- **feat(web): firecrawl plugin natively supports crawl; delete legacy inline path** (21e3a863b)
- **test(plugins): tests/plugins/web/ — coverage for the 7-plugin migration** (e8cee87e8)
- **refactor(web): delete legacy tools/web_providers/ directory + migrate ABC tests** (39b4ebfce)
- **refactor(tools): drop hardcoded web picker rows + skiplist; plugins are sole source** (24fe60faa)
- **refactor(web): delete inline vendor helpers, re-export from plugins** (748f3e016)
- **fix(web): preserve firecrawl crawl + website-policy gate after migration** (5e54330e2)
- **refactor(web): dispatch all three tools through web_search_registry** (b05253cee)
- **feat(web): firecrawl plugin — largest migration (search + async extract + dual auth)** (143184e94)
- **feat(web): tavily plugin — first three-capability plugin (search + extract + crawl)** (31fcde876)
- **feat(web): parallel plugin — first async-extract plugin** (481664610)
- **feat(web): exa plugin — first multi-capability migration (search + extract)** (ec8449e9c)
- **feat(web): extend ABC with supports_crawl and async-extract semantics** (e3f0a8889)
- **fix(plugins): filter resolution by is_available() in web + image_gen registries** (0a7cbd334)
- **refactor(web): remove legacy in-tree provider modules** (6b219f5af)
- **feat(tools): mirror image_gen plugin-injection in Web Search picker** (714630110)
- **refactor(web): dispatch brave-free/ddgs/searxng via web_search_registry** (6bd16a645)
- **feat(web): searxng plugin (search-only, third migration)** (0d085d945)
- **feat(web): ddgs plugin (second migration)** (5c7d098be)
- **feat(web): brave_free plugin (first migration from tools/web_providers/)** (d403cf018)
- **feat(plugins): add ctx.register_web_search_provider() facade** (f29f02a73)
- **feat(web): add web search provider registry mirroring image_gen pattern** (007a630b1)
- **feat(web): add WebSearchProvider ABC mirroring image_gen template** (2cea98e14)
- **refactor(cli): route /model picker through shared inventory module** (563077a47)
- **refactor(inventory): extract shared ConfigContext + build_models_payload** (efc32ab63)
- **fix(compression): keep default protect_first_n at 3 + align ABC** (4ceab1689)
- **feat(compression): make protect_first_n configurable** (dee71a31e)
- **chore(release): map jake@nousresearch.com → simpolism** (ffbc21100)
- **feat(discord): add thread_require_mention for multi-bot threads** (d863773c8)
- **fix(discord): keep free-response channels inline** (d55754456)
- **refactor(plugins): add apply_yaml_config_fn registry hook** (3633c8690)
- **feat(codex-runtime): skip unavailable plugins during migration (#25437)** (d5775fe98)
- **feat(dashboard): hide token/cost analytics behind config flag (default off) (#25438)** (f7ad2f111)
- **chore(release): map jake@nousresearch.com and simpolism@gmail.com to @simpolism** (e90508103)
- **test(memory): cover cache-parity + runtime whitelist on background review fork** (8c6b0c9ec)
- **fix(memory): pin session_start + session_id on background review fork** (07349ce4d)
- **chore(release): map WorldWriter for PR #17276 salvage** (95d074cdb)
- **fix(memory): hit prefix cache in background review fork** (5fe067226)
- **feat(plugins): add thread-local tool whitelist to pre_tool_call gate** (3a30c605b)
- **fix(gateway): complete lazy-install rebind for slack/feishu/matrix + add ensure_and_bind helper (#25038)** (d898e0eb7)
- **fix(install): skip browser download when system chromium exists** (52521c937)
- **fix(tts): align MiniMax TTS defaults with current API and add GroupId support** (7f08cb594)
- **fix(tts): update MiniMax default model to speech-02 and correct API endpoint** (c875c0dc1)
- **feat(slack): support !cmd as alternate prefix for slash commands in threads (#25355)** (6122a79aa)
- **perf(tools): cache get_nous_auth_status() and load_env() to fix slow `hermes tools` menus (#25341)** (3f13d7808)
- **test(ci): stabilize shared optional dependency baselines** (3c106c89a)
- **fix(tools-config): write video_gen.provider on Reconfigure tool path (#25307)** (dd5a9502e)
- **docs: close in-tree memory plugins to new PRs and codify skill standards (#25302)** (ef98e3f9e)
- **chore(skills/evm): tighten SKILL.md to modern format** (66c70966c)
- **feat(skills): merge blockchain/base into blockchain/evm; salvage PR #2010** (e3fc08149)
- **feat: add EVM multi-chain skill (8 chains, 14 commands)** (aa1e2edd3)
- **feat(codex-runtime): optional codex app-server runtime for OpenAI/Codex models (#24182)** (091d8e103)
- **feat(video_gen): unified video_generate tool with pluggable provider backends (#25126)** (9d42c2c28)
- **chore(release): map mgongzai author for PR #25183 salvage** (b833d8501)
- **test(gateway): make queued follow-up regression generic** (cc64a04f6)
- **fix(gateway): preserve queued follow-up transcript history** (9a815b6c8)
- **tui: make URLs clickable + hover-highlight in any terminal (#25071)** (08671d877)
- **fix(cli): preserve startup banner on terminal resize** (e2b2d4861)
- **fix(tools): refuse skill_view name collisions instead of guessing** (59da8ec4e)
- **fix(setup): drop post-setup chat handoff (#25067)** (256bedb63)
- **feat(custom): prompt and persist explicit api_mode for custom providers** (6f2d1c88b)
- **chore(release): map iuyup author for PR #6155 salvage** (1979ef580)
- **fix(security): reduce unnecessary shell=True in subprocess calls** (d6c9711ba)
- **chore(release): map anton.kuenzi@gmail.com -> ZeterMordio** (a9b8254e5)
- **refactor(profiles): remove dead generate_bash_completion / generate_zsh_completion** (a43d7e67b)
- **test(cli): strengthen zsh completion regression coverage** (6d30b4a7e)
- **fix(cli): repair broken zsh completion generation** (8c4bec615)
- **Merge pull request #25045 from NousResearch/hermes/hermes-852727b9** (4fdfdf674)
- **ci(docker): split :latest (releases only) from :main (main HEAD)** (1149e75db)
- **fix(gateway): add lazy_deps.ensure() to slack, matrix, dingtalk, feishu adapters (#25014)** (5d90386ba)
- **refactor: import FILE_MUTATING_TOOL_NAMES from shared module** (c3094b46e)
- **fix: classify landed file mutations with diagnostics** (da0ddbf88)
- **fix(cli): add 'lsp' to _BUILTIN_SUBCOMMANDS so plugin discovery is skipped** (71c6dd0dc)
- **fix(docker): chown .venv to hermes so lazy_deps can install platform packages (#24841)** (942adf617)
- **feat(providers): rename Alibaba Cloud to Qwen Cloud, reorder picker (#24835)** (1e01b25e7)
- **feat(nous): unified client=hermes-client-v<version> tag on every Portal request (#24779)** (486b692dd)
- **fix(cache): kill long-lived prefix layout — system prompt is now byte-static within a session (#24778)** (b06e99930)
- **fix: approval DELETE pattern DOTALL flag allows newline bypass** (80374d4dd)
- **fix(agent): clear stale config context_length on model switch** (8ac351407)
- **fix(test): use i18n t() for restart drain assertion** (a4289d74a)
- **fix(gateway): make WhatsApp npm install timeout configurable** (1a4e8f704)
- **fix(tools): forward thread_id via metadata in _send_via_adapter live path** (420762f86)
- **fix(wecom): update connection status after WebSocket reconnection** (e77fd75c4)
- **fix(line): use build_source instead of nonexistent create_source** (7c6709732)
- **fix(prompt_builder): inject tool-use enforcement for GLM models** (afa5b8191)
- **fix(telegram): use thread fallback helper in slash-confirm result send** (e474130c4)
- **fix(install): use stash@{0} instead of git rev-parse refs/stash for autostash recovery Autostash creates refs/stash as a pointer to the latest stash commit, but git stash apply/drop expect the symbolic ref format like stash@{0}, not the raw commit SHA. Using the commit SHA causes: error: 'X is not a stash reference'** (327b8cee9)
- **fix(gateway): add chat_id to hook_ctx for message source tracking** (dd1d4e9c5)
- **docs(lsp): document follow-up fixes from #24630 (#24709)** (80c4b2743)
- **fix(tui): use TERMINAL_CWD in _session_info for accurate status line path** (557deece6)
- **fix(voice_mode): detect audio in WSL when sd.query_devices() returns empty list but PULSE_SERVER is set** (081f9368b)
- **fix(signal): handle group messages from linked devices in syncMessage path** (e71393237)
- **fix(retry): use float() for Retry-After header to handle sub-second values** (4c825554c)
- **fix(cache): drop ttl=1h on Portal Qwen — Alibaba upstream is 5m-only (#24702)** (2a18b6283)
- **fix(cron): include whatsapp in _HOME_TARGET_ENV_VARS** (d8c4460fe)
- **fix(web): add Bearer auth header for Tavily /crawl endpoint** (6f92a2192)
- **fix(doctor): skip /models health check for providers that don't support it** (0c233e70f)
- **fix(send_message): recognize XMPP JIDs as explicit targets** (a54d4b0e4)
- **fix(gateway): reduce systemd restart delay** (0bc5f7b23)
- **fix(ci): bump e2e job timeout to 15 minutes** (8d553056c)
- **fix(ci): install ripgrep in e2e job** (1beb578fd)
- **docs(gateway): mention Weixin in gateway help and docstrings** (a694a2633)
- **fix(lsp): typescript SDK install + tsc-missing skip + shellcheck warning (#24630)** (29c9ff9ba)
- **fix(telegram): clear in-progress reaction on cancelled processing (#24628)** (6f285efb8)
- **chore(release): add AUTHOR_MAP entries for JamesX88** (413990c94)
- **fix(cli): @-file completion crash on Windows when paths aren't cp1252-decodable** (a33ec1087)
- **chore(release): add AUTHOR_MAP entries for NorethSea** (c7cfad5d9)
- **fix(cli): use display-width for response box header label to support CJK** (7a4ad5ccb)
- **chore(release): add AUTHOR_MAP entries for laoli-no1** (b7bd0f77f)
- **fix(tui): clear scrollback buffer on startup to prevent tmux scrollback leakage** (d33deb7cb)
- **fix(dashboard): rescan plugins when cached directory is removed** (2a3140a81)
- **chore(release): add AUTHOR_MAP entries for aqilaziz** (6ec89d885)
- **fix(dashboard): display real config path on Config page** (80375cbe2)
- **chore(release): add AUTHOR_MAP entries for AllynSheep** (782e3f516)
- **fix(dashboard): skip browser-open on headless Linux to prevent process exit** (e3858772d)
- **chore(release): add AUTHOR_MAP entry for hookinglau** (b3ca6362a)
- **fix(auxiliary): pass cfg_base_url and cfg_api_key when resolving task provider** (d68a0ec38)
- **chore(release): add AUTHOR_MAP entry for ryptotalent** (389c707e4)
- **fix: include arg-taking commands in Telegram menu** (9b2488af2)
- **feat(gateway): wire clarify tool with inline keyboard buttons on Telegram (#24199)** (29d7c244c)
- **chore: AUTHOR_MAP entry for AhmetArif0 (PR #24600)** (76bbb94be)
- **fix(gateway): consult lock record argv when cmdline unreadable in scoped-lock stale check** (f9559c39c)
- **chore(release): add AUTHOR_MAP entries for zccyman and Osraka** (24e2151cd)
- **fix(pricing): add deepseek-v4-pro to official docs pricing table** (88ede807c)
- **feat(lsp): semantic diagnostics from real language servers in write_file/patch (#24168)** (83b93898c)
- **fix(daytona): migrate legacy-sandbox lookup to cursor-based list() (#24587)** (d89553c2d)
- **docs(camofox): expand externally-managed sessions section (#24584)** (38441a7d7)
- **chore(camofox): document new env vars + AUTHOR_MAP entry** (f63d52049)
- **feat(browser): support externally managed Camofox sessions** (62fd90534)
- **fix(install): use `--extra all` not `--all-extras`; drop lazy-covered extras from [all] (#24515)** (3955aefce)
- **fix(gateway): enqueue SSE EOS sentinel on task completion** (4bb0a82a2)
- **chore(release): add AUTHOR_MAP entry for luarss** (4fa5f7b76)
- **fix(docs): correct broken internal links to webhooks and mlops skill pages** (1189ed785)
- **📝 docs(kanban): clarify dependent task gating** (71198b9e1)
- **chore(release): map kyanam.preetham@gmail.com → pkyanam** (954e854cc)
- **test(gateway): patch _pid_exists instead of os.kill for scoped-lock tests** (629c33c63)
- **fix(gateway): detect stale scoped locks via cmdline when start_time is absent on macOS** (653d30429)
- **Merge pull request #24161 from NousResearch/austin/fix/dashboard** (642768c5c)
- **fix(cli): parse positional insights days** (a34998ee2)
- **union paid recs from nous portal with static list (#24509)** (c23a87bc1)
- **fix(install): surface uv install + uv.lock sync errors instead of silently hanging (#24504)** (d186186e1)
- **Use nous portal as model metadata authority (#24502)** (2863e9484)
- **feat(agent): per-turn file-mutation verifier footer (#24498)** (c594a2304)
- **fix(dashboard): UI polish — modals, layout, consistency, test fixes** (fc3fd6bb6)
- **docs: remove public advisory page (handle community comms separately) (#24253)** (dd0923bb8)
- **feat(security): supply-chain advisory checker + lazy-install framework + tiered install fallback (#24220)** (c1eb2dcda)
- **fix(deps): unbreak [all] install — drop mistralai while PyPI quarantined (#24205)** (99ad2d137)
- **fix(docs): repair Voice & TTS provider table** (407683b72)
- **add client marker tag on aux inference requests** (94d9db72b)
- **fix(minimax): harden OAuth dashboard and runtime** (58e2109f1)
- **fix comment** (32abe742f)
- **remove comments** (f0c2964f0)
- **fix guard** (057fc7b07)
- **fix kimi** (528bba673)
- **fix(cache): route Nous Portal Qwen through Portal-Claude cache pathway (#24151)** (7993e03c0)
- **fix(tui-clipboard): skip native safety net on OSC52-capable terminals (#20954)** (3c23b15f8)
- **fix(nous): surface Portal-flagged free models in picker even when curated list is stale (#24082)** (e85592591)
- **feat(computer-use): refresh cua-driver on `hermes update` + add `install --upgrade` (#24063)** (ced1990c1)
- **chore(release): add AUTHOR_MAP entry for ahmedbadr3** (97a0e69df)
- **fix(dashboard): MiniMax 'Login' button launched Claude OAuth (#22832)** (05bad7b1e)
- **fix(cli): vertical fallback for markdown tables wider than terminal (#23948)** (ea1d0462c)
- **Merge pull request #18036 from NousResearch/fix/bundle-size** (825bd50e6)
- **feat(ui-tui): resolve markdown links to readable page titles (#24013)** (75b428c85)
- **refactor(tui): simplify TUI build logic, remove stale staleness checks** (c6ca11618)
- **chore: add nicoechaniz to AUTHOR_MAP** (9a63b5f16)
- **fix(model-metadata): skip OpenRouter for known providers, add kimi/moonshot to PROVIDER_TO_MODELS_DEV** (e2b713cce)
- **fix: correct context-length resolution for kimi-k2.6 on Ollama Cloud and Kimi Coding** (91eef6255)
- **Merge remote-tracking branch 'origin/main' into fix/bundle-size** (3197b4de6)
- **feat: expose HERMES_SESSION_ID to agent tools via ContextVar + env (#23847)** (271883447)
- **chore: ruff auto-fix C401, C416, C408, PLR1722 (#23940)** (ce0f529cd)
- **feat(prompt-cache): cross-session 1h prefix cache for Claude on Anthropic / OpenRouter / Nous Portal (#23828)** (7b7636655)
- **chore: ruff auto-fix PLR6201 — tuple → set in membership tests (#23937)** (2ec8d2b42)
- **chore(release): add AUTHOR_MAP entry for wuli666** (8c1171031)
- **fix(auxiliary): evict async wrappers on poisoned client (follow-up to #23482)** (111b859e4)
- **fix(cli,tui): align CJK / wide-char markdown tables (#23863)** (1d0071675)
- **chore: ruff auto-fixes — collapsible-else-if, if-stmt-min-max, dict.fromkeys (#23926)** (657874460)
- **fix(/model): surface Nous Portal models from remote catalog manifest (#23912)** (8e2eb4b51)
- **fix(cli): defensive _slash_confirm_state access + AUTHOR_MAP** (cc9e788c1)
- **fix: use TUI modal for slash confirmations** (054f56857)
- **rebuild model catalog** (e155f2aca)
- **fix(dashboard): validate dist exists when --skip-build is set** (283381b1c)
- **fix(dashboard): fallback to stale dist, retry build, add --skip-build flag** (7085f4e23)
- **chore: AUTHOR_MAP entry for VinceZcrikl noreply (#23647)** (88a2ce4ae)
- **fix: make web UI build output decoding robust on Windows** (a479ec01e)
- **fix(agent): catch ChatGPT-account Codex data-URL rejection so images are stripped instead of cascading to compression (#23602)** (7026af4e2)
- **revert: roll back /goal checklist + /subgoal feature stack (#23813)** (3e7145e0b)
- **chore: AUTHOR_MAP entries for sudo-hardening salvage contributors** (1d4a4997b)
- **fix(approval): catch sudo with stdin/askpass/shell privilege flags** (976d8e27a)
- **fix(terminal): block sudo -S password guessing when SUDO_PASSWORD is not set** (9520a1ccd)
- **chore: remove unused sentinel in test_send_message_tool** (494824fb1)
- **fix: guard resolve_profile_env against missing profile dirs** (571248348)
- **chore: add salvage contributors to AUTHOR_MAP** (708770221)
- **fix(kanban): treat archived parent tasks as terminal for dependency resolution** (a1854ac07)
- **fix(kanban): use localized column label in select-all aria label** (27cfe7254)
- **test(send_message): cover _check_send_message gating paths** (379e7dd01)
- **fix(send_message): allow kanban workers to call send_message** (8ac998cb0)
- **fix(kanban): inject HERMES_HOME into worker subprocess env** (5af315c4c)
- **fix(kanban): restore HERMES_KANBAN_BOARD after scoped slash override** (641e40c4b)
- **fix(kanban): call kanban_block on iteration-budget exhaustion to prevent protocol violation** (2b3bf17df)
- **fix(kanban): route gateway create auto-subscribe to explicit board** (f6d4f3c37)
- **fix(nix): replace chown -R with targeted find in container entrypoint (#23633)** (64145a199)
- **feat(nix): add extraDependencyGroups for sealed venv extras (#21817)** (560625885)
- **feat(deps): add hindsight-client as optional dependency (#21818)** (d992fd9aa)
- **feat(terminal,cli): docker_extra_args + display.timestamps** (ebf2ea584)
- **fix(auxiliary): cache 402'd providers as unhealthy with TTL to stop per-call retry storms (#23597)** (228b7d27b)
- **fix(discord): typing indicator task not cleaned up after API error** (ace1c4ea8)
- **chore(release): AUTHOR_MAP entry for Mibayy clawhub email** (0458d99f2)
- **chore(skills/stocks): tighten SKILL.md to modern format** (952604070)
- **chore(skills/stocks): relocate to optional-skills/finance/stocks/** (2ea957fc4)
- **feat: add stocks & finance skill (Yahoo Finance, no API key)** (896a7ce26)
- **Merge pull request #20317 from NousResearch/meta/security-policy** (bf2cc8b31)
- **fix(config): warn loudly on YAML parse failure instead of silent default fallback (#23585)** (228a4d11a)
- **fix(misc): three small defensive fixes from PR #1974** (3af3c4eb8)
- **chore: AUTHOR_MAP entry for wilsen0** (482d49cf9)
- **test(telegram): cover env-clamped helper + adaptive text-batch tiers** (edb4a2bda)
- **perf(gateway): tune Telegram cadence + adaptive fast-path for short replies** (ac95b8cdb)
- **rename(skills): api-testing -> rest-graphql-debug (#23589)** (e3b88a8fe)
- **chore(release): AUTHOR_MAP entry for Hugo-SEQUIER** (5f767879e)
- **chore(skills/hyperliquid): tighten SKILL.md to modern format** (1f899393d)
- **Add unit tests for hyperliquid skill functionality** (f2e8ed240)
- **test: stabilize quick-command redaction test against xdist ordering** (28b4fe600)
- **fix(security): sanitize env and redact output in quick commands + remove write-only _pending_messages** (f6736ced8)
- **feat(skills): add api-testing optional skill (#1800)** (4c57a5b31)
- **chore: AUTHOR_MAP entry for kjames2001 (James Huang)** (6c1af45b7)
- **test(telegram): regression coverage for edit overflow split-and-deliver** (82352e54c)
- **fix(telegram): split-and-deliver oversized edits instead of silent truncation** (bf1f40996)
- **feat(kanban): stranded_in_ready diagnostic for unclaimed tasks (#23578)** (3b122cc1a)
- **chore(release): map @eloklam tailnet email** (bf5b8a7d6)
- **fix(kanban): merge dashboard batch QOL with i18n + collapse + assignee-casing** (b8bf2f817)
- **test(kanban): remove stale t.summary assertion from search test** (b60462a20)
- **kanban dashboard: fix shift-click range selection, column select-all toggle, and bulk action optimistic UI** (3df7e3024)
- **kanban dashboard: remove redundant t.summary from search haystack** (69053832e)
- **kanban dashboard: multi-card drag visual feedback** (a88f201cd)
- **kanban dashboard: fix batch QOL oracle blockers** (98c499b23)
- **feat(kanban): dashboard batch QOL upgrade** (0ea234e09)
- **feat(kanban): add reclaim_first support to bulk reassign endpoint** (518d37f6a)
- **fix(goals): force judge to use tool calls instead of JSON-text replies (#23547)** (a63a2b7c7)
- **fix(goals): forward standing /goal state on auto-compression session rotation (#23530)** (4a080b1d5)
- **fix(kanban): keep '--created-by' default as 'user'** (68d081f57)
- **fix(gateway): route kanban notifications to creator profile** (ba5640fa1)
- **chore: AUTHOR_MAP entry for NivOO5** (9e005d677)
- **test(telegram): native-draft transport coverage + docs** (7f90141c6)
- **feat(telegram): native draft streaming via sendMessageDraft (Bot API 9.5+)** (4ed293b38)
- **fix(achievements): use canonical X-Hermes-Session-Token header** (80bb5f294)
- **fix(achievements): inject Authorization header in plugin API calls** (da2ed478b)
- **test(conftest): plug every gateway-kill leak path (#23486)** (771b8c4a3)
- **fix(auxiliary): evict cached client on timeout/connection error (#23482)** (e5bce320d)
- **docs(kanban): worker lane contract page + review-required convention** (ae83a54be)
- **chore: AUTHOR_MAP entry for rahimsais** (666b75153)
- **fix(telegram): normalize dm threads and retry control sends** (737314fe9)
- **feat(goals): /goal checklist + /subgoal user controls (#23456)** (404640a2b)
- **chore: AUTHOR_MAP entry for Freeman-Consulting** (c0bbdec85)
- **test(stream-consumer): add UTF-16 overflow regression tests for #11170** (121bbe038)
- **fix: use UTF-16 length for Telegram stream consumer message splitting** (c0da5d09a)
- **fix(cli): drive _prompt_text_input directly when off main thread (#23454)** (c5f1f863a)
- **fix(tools): clarify kanban_complete phantom-card retry guidance** (62cfe79e9)
- **fix(telegram): pass source.thread_id explicitly on auto-reset notice (carve-out of #7404)** (2f00559d9)
- **fix(tui): right-click copies selection, only pastes when no selection** (a2920b176)
- **chore: AUTHOR_MAP entry for konsisumer noreply (#23071)** (59d3f24f1)
- **fix(kanban): extend stale claim instead of killing live worker** (88588b615)
- **docs(user-stories): add 116 stories from the Hermes Discord archive (#23436)** (3974a137c)
- **fix(xai): omit reasoning.effort for grok models that reject it (#23435)** (d6e1fadbf)
- **chore: AUTHOR_MAP entry for hrygo (黄飞虹)** (cc2a0c674)
- **test(thread-routing): handle both lark-SDK-present and absent paths** (f9e0d60a9)
- **fix(stream-consumer): preserve thread routing on overflow first-send path** (e164a9c1e)
- **fix(gateway): stream consumer first message drops thread context** (ff14666cd)
- **fix(gateway): only mark final response sent when split-overflow chunks actually land (#23420)** (6636fecd4)
- **chore: AUTHOR_MAP entry for jelrod27 (#21398)** (b38b10010)
- **test(kanban): cover redeliver-on-cycle + flip stale unsub-on-abnormal-event tests** (787e3c368)
- **fix: deduplicate kanban notifications for blocked/gave_up states** (a96dd5487)
- **chore: AUTHOR_MAP entry for HuangYuChuh** (04e18160a)
- **fix(gateway): align fallback delete with sibling style + add regression tests** (ec1fad344)
- **fix(gateway): delete partial message after fallback send on flood control** (4eb8479eb)
- **test(conftest): block tests from killing the live hermes-gateway (#23397)** (cdb6e5e52)
- **ci: skip lint comment on fork PRs** (6062c24fd)
- **test(kanban): cover send-exception rewind + drop noisy success log to debug** (9c68d1207)
- **fix: dedupe kanban notifier delivery claims** (861ce7c0b)
- **docs(sessions): document /handoff cross-platform session transfer (#23400)** (373c4d664)
- **fix(windows): unbreak install + update on Windows (#23394)** (4d9dcbc47)
- **feat(session): make /handoff actually transfer the session live** (00ce5f04d)
- **feat(session): add /handoff command for cross-platform session transfer** (878611a79)
- **refactor(kanban-orchestrator): drop hardcoded specialist roster, add Step-0 profile discovery** (6e5c49bdc)
- **feat(gateway): per-platform admin/user split for slash commands (salvage of #4443) (#23373)** (a28243430)
- **fix(xai): drop models being retired May 15, 2026 from pickers (#23291)** (594209389)
- **chore: AUTHOR_MAP entry for guglielmofonda (#21505)** (d62808c37)
- **docs(kanban): document max_spawn as live concurrency cap (not per-tick budget)** (3fbbf5885)
- **fix(kanban): cap dispatch by running workers** (845be254e)
- **feat(gateway): shutdown forensics — non-blocking diag, per-phase timing, stale-unit warning (#23285)** (cede61298)
- **feat(kanban): aggregate all toolset-name typos in skills before raising** (1f5983c4c)
- **fix(kanban): reject toolset names in task skills** (673418dfa)
- **feat(kanban-dashboard): native <details> collapse + skip empty metadata** (a91e5a875)
- **fix(kanban-dashboard): tone down completed-run metadata panel (#19548)** (0e0ddaac8)
- **perf(browser): route browser_console eval through supervisor's persistent CDP WS (180x faster) (#23226)** (d4b26df89)
- **test(kanban-dashboard): pin assignee-casing static-asset regressions + AUTHOR_MAP** (08c5b35a7)
- **fix(kanban): preserve assignee casing in dashboard** (b308dd7d7)
- **test(kanban): cover task_age safe-int guards + AUTHOR_MAP entry** (40a4bfa71)
- **fix(kanban): guard task_age against corrupt created_at values like '%s'** (061a18300)
- **feat(i18n): localize all gateway commands + web dashboard, add 8 new locales (16 total) (#22914)** (c39168453)
- **fix(kanban): correct dispatcher spawn module name + PATH-first lookup** (62b1c74cb)
- **fix(kanban): use sys.executable -m hermes for dispatcher spawn** (d3db6724d)
- **feat(plugins): run any LLM call from inside a plugin via ctx.llm (#23194)** (5aa755e4e)
- **test(security): broaden plugin API auth coverage + correct stale docstring** (ae4b09ce1)
- **fix(security): require dashboard auth for plugin API routes** (ec9329ec4)
- **feat(curator): hint at `hermes curator pin` in the rename block (#23212)** (7312f7f84)
- **feat(gateway): add LINE Messaging API platform plugin (#23197)** (50f9fee98)
- **docs(web-search): explain auxiliary-model summarization for web_extract (#23211)** (9cdcf31ca)
- **docs(user-stories): add 4 entries from @emmagine79 thread (#23204)** (3d4297a59)
- **chore: AUTHOR_MAP entry for kallidean (#20568)** (ce374bc1b)
- **fix(kanban): restrict board routing tools to orchestrators** (2704e7b67)
- **fix(kanban): parse triage flag explicitly** (50d281495)
- **fix(kanban): parse include_archived explicitly** (26bf45f8c)
- **feat(kanban): add orchestrator board tools** (236cbe16b)
- **fix(codex-spark): defensive 128k entry in DEFAULT_CONTEXT_LENGTHS + clarify validation test docstring** (44cdf555a)
- **test(codex-spark): add live-API regression and make picker test deterministic** (826e7171e)
- **docs(codex-spark): document ChatGPT Pro entitlement gating** (9ee9a4297)
- **chore: add codex-spark salvage contributors to AUTHOR_MAP** (6b5e0119b)
- **fix: surface Codex CLI-only models** (945764439)
- **fix(model-metadata): set codex-spark fallback context to 128k** (c6dc295a3)
- **fix(model-metadata): restore gpt-5.3-codex-spark fallback context** (2a6f3deb5)
- **feat(codex): add gpt-5.3-codex-spark model** (dcc8de83a)
- **fix(review): tell background reviewer not to capture transient env failures as skills (#23004)** (e5af1dd63)
- **feat(stream-retry): add upstream + timing diagnostics to drop log (#23005)** (126cbffb8)
- **chore: AUTHOR_MAP entry for tymrtn (#21794)** (5a70d9b6b)
- **fix(kanban): /kanban slash command emits argparse garbage instead of help** (d1fc748de)
- **chore(models): refresh OpenRouter + Nous fallback lists (#23001)** (3d2bfc502)
- **chore: AUTHOR_MAP entry for li0near gmail (#21378)** (e2ce89a8a)
- **fix(kanban): drop redundant init_db() in gateway watchers (#21378)** (6f2d60559)
- **fix(stream-retry): collapse two-line drop status, name provider, and let agent.log capture diagnostics (#22993)** (68e44642c)
- **feat(vision): vision_analyze returns pixels to vision-capable models, not aux text (#22955)** (3800972dd)
- **docs(user-stories): add 18 verified social entries (99 → 117) (#22920)** (e62250453)
- **chore(test): comment of test case rewrite to english** (998676dd0)
- **fix(kanban): remove blocked kind from unsub** (a4036654f)
- **test(kanban): assert re-block notification is delivered after unblock cycle** (dd49d5038)
- **fix(kanban): request default board explicitly (#21819)** (8954537f9)
- **chore: AUTHOR_MAP entry for eloklam (#22898)** (eb3db231d)
- **docs(skills): clarify kanban fan-out decomposition** (d04a0b81e)
- **fix(tool-result-storage): persist via stdin to bypass 128 KB exec-arg cap (#22913)** (08ec60277)
- **chore(skills): move heavy training skills + outlines to optional-skills (#22912)** (ded194eb6)
- **feat(curator): show rename map in user-visible summary (#22910)** (4375b82cd)
- **perf(cli): skip welcome banner on `chat -q` single-query mode (#22904)** (b67ea7ff4)
- **feat(docs): richer info panels on the Skills Hub for built-in + optional skills (#22905)** (5971a4e09)
- **chore: add ming1523 to AUTHOR_MAP** (da086a015)
- **fix(cli): preserve config comments on setting writes** (85383c636)
- **chore: add v1b3coder to AUTHOR_MAP** (de5461872)
- **fix: use credential_pool for custom endpoint model listing probes** (4fdaf0b4d)
- **chore: add DanielLSM to AUTHOR_MAP** (f93b8c28e)
- **fix(gateway): pass max_total_size_mb and max_file_size_mb to CheckpointManager** (1fb9f7c68)
- **test(gateway): stub /proc unavailability in find_gateway_pids fallback test** (4ca7c2104)
- **fix(gateway): detect gateway process via /proc in Docker without procps** (6bf7ac318)
- **fix(test_gateway): stop run_gateway() tests from rewriting the dev's installed systemd unit (#22900)** (2ffef1567)
- **fix(error_classifier): classify generic-typed timeout messages as transient (carve-out of #22664)** (4f8d8ad91)
- **fix(fallback): resolve api_key_env in fallback chain entries (carve-out of #22665)** (6ddc48b05)
- **fix(gateway): degrade gracefully when all platform adapters are missing** (246c676c2)
- **fix(terminal): bridge docker_env config to TERMINAL_DOCKER_ENV** (116a1446a)
- **fix(process_registry): kill orphaned Popen on post-spawn setup failure** (53ec32819)
- **fix(install): also patch psutil on Termux fresh-install path** (c179bdab3)
- **fix(update): use termux-all uv fallback path on Termux** (6d5d467d3)
- **fix(update): prebuild psutil on Termux Android via Linux path shim** (3863d6d34)
- **fix(checkpoint): guard _touch_project against non-dict project metadata** (2245879af)
- **fix(session): route OR-combined short CJK tokens to LIKE fallback (#20494)** (058c50816)
- **fix(context_compressor): treat streaming premature-close as transient error** (35f773c45)
- **fix(skills-hub): cover remaining SSRF fetch paths after #10029** (0c5c4d1b8)
- **chore: add kidonng to AUTHOR_MAP** (af9df4652)
- **fix(gateway): finalize final stream edit on done** (1321bcf5f)
- **perf(image_gen): defer fal_client import to first generation request (#22859)** (c1cc3d4ea)
- **docs: round 2 audit — messaging, developer-guide, guides, integrations (#22858)** (fef1a4124)
- **docs(openrouter): document auxiliary.<task>.extra_body for OR routing and Pareto (#22844)** (0bcc327ca)
- **fix(gateway): preserve reasoning_content, codex_message_items, finish_reason on transcript replay (#22839)** (70bfd429e)
- **feat(openrouter): wire Pareto Code router with min_coding_score knob (#22838)** (c7f0aab94)
- **fix(acp): honor task cwd for foreground terminal commands** (b349ae1e4)
- **perf(teams): defer httpx import to first webhook call (#22831)** (550f6e2ef)
- **fix: make session search initialize session db** (840ebe063)
- **fix(gateway): preserve Ctrl+C for Windows foreground runs** (9c26297c8)
- **chore: add Ninso112 to AUTHOR_MAP** (bfc84bdc6)
- **fix(openrouter): add x-grok-conv-id header for Grok models to improve prompt cache hit rates (carve-out of #22708)** (883e11f0a)
- **chore: add mbac to AUTHOR_MAP** (5e2eba87e)
- **fix(gateway): adopt unit's HERMES_HOME for --system CLI ops** (1508dcb9c)
- **fix(telegram): default notifications to 'important' (silence intermediate)** (448c11f16)
- **chore: add CalmProton to AUTHOR_MAP** (b4d3092f6)
- **feat(gateway): add Telegram notification mode to suppress intermediate push notifications** (236f3b052)
- **fix(delegate): add explicit do-not-use guidance to acp_command/acp_args schema (carve-out of #22680)** (ca1399321)
- **fix(model-metadata): align hy3-preview static fallback + delete change-detector test (#22805)** (1c9ffb177)
- **fix(completion): use valid zsh _arguments exclusion-group syntax** (fe61d95b4)
- **fix(doctor): normalize provider name and aliases before dedicated-skip check** (6e848f60e)
- **fix(doctor): skip pluggable provider profiles when a dedicated check exists (#22346)** (1dd079065)
- **fix(kanban): make _migrate_add_optional_columns idempotent on concurrent open** (78698381a)
- **fix(agent): extract thinking from content-list blocks for DeepSeek V4 Pro** (68854cdcd)
- **fix(deps): declare youtube-transcript-api in pyproject.toml [youtube] extra** (98e94beb1)
- **fix(email): use real hermes version in IMAP ID command** (a671d8a27)
- **fix(email): send IMAP ID extension to support 163/NetEase mailbox** (3fd4ccbd8)
- **fix(browser_tool): fall through to autodetect on config read failure** (48bf0ea24)
- **fix(browser_tool): do not cache transient None cloud provider resolution** (3170c8d44)
- **chore: add Qwinty to AUTHOR_MAP** (5a0021146)
- **fix(auxiliary): rotate pooled auth after quota failures** (17d891485)
- **perf(models_dev): cache-first lookup, skip network when disk cache is fresh (#22808)** (775c0e22c)
- **feat(transports/codex): pass reasoning.effort to xAI Responses API** (cd712b176)
- **docs: deep audit — fix stale config keys, missing commands, and registry drift (#22784)** (252d68fd4)
- **perf(gateway): defer QQAdapter and YuanbaoAdapter imports via PEP 562 (#22790)** (ea2d66ddc)
- **test(xai-image): regression-guard literal '1k'/'2k' resolution payload** (dcff23a25)
- **chore: add A-kamal to AUTHOR_MAP for PR #18678** (5b32c9fc6)
- **fix: send correct resolution param to xAI image generation API** (13b474c56)
- **perf(doctor): parallelize API connectivity checks and disable IMDS (#22766)** (e612c3d6f)
- **fix(tools): install cua-driver when Computer Use is enabled via 'hermes tools' (#22765)** (8f711f79a)
- **fix(memory): tighten MEMORY_GUIDANCE against ephemeral PR/issue/SHA notes (#22781)** (6e5489c9f)
- **fix(fallback): skip chain entries matching current provider/model/base_url (#22780)** (e7c0d6ee5)
- **fix(cli): make Ctrl+Enter insert newline on WSL/SSH/Windows Terminal (#22777)** (70bc52e40)
- **fix(api-server): emit length/error finish_reason for truncation/failure (#22775)** (2124ad72a)
- **fix(agent): hydrate memory-nudge counters from conversation_history (#22774)** (86f69e8c2)
- **fix(kanban): sanitize comment author rendering in build_worker_context (#22769)** (ade598142)
- **fix(tests): harden run_tests.sh — uv-aware bootstrap + scrub HERMES_CRON_SESSION (#22767)** (f00dc6d7a)
- **fix(agent): notify context engine on commit_memory_session (#22764)** (e90aa7f28)
- **fix: follow-up for salvaged PR #22263** (dae94fa65)
- **feat(gateway): add Telegram guest mention mode** (55f518e52)
- **chore: add wali-reheman to AUTHOR_MAP** (369cee018)
- **fix: move pytest.importorskip below pytest import in skip-guarded tests** (b959cfa05)
- **tests: add Windows skip guards for UNIX-only stdlib imports** (4e8b8573c)
- **fix(cron): allow quoted URL in github auth-header allowlist** (b6ff96c05)
- **fix(cron): keep auth-header exfiltration blocked** (691778a08)
- **fix(cron): avoid github skill false positives in scanner** (783d11717)
- **feat(mcp): add codex preset for built-in MCP server discovery** (9aefa74a9)
- **fix(dingtalk): align override signatures with base + guard Optional[error] in tests** (684fd14db)
- **fix(dingtalk): clarify webhook media behavior** (c705c7ac9)
- **fix(profiles): honour active_profile when HERMES_HOME points to hermes root** (a33c63b9f)
- **fix(telegram): honor message.quote for partial-quote reply context** (854c2ce30)
- **chore: add xieNniu to AUTHOR_MAP** (78b8155ec)
- **fix(plugins): resolve Git binary for installs under minimal PATH** (c8ede8aa1)
- **fix(gateway): refresh runtime argv metadata** (124fbb0af)
- **fix(cli): expand composite toolset when mixed with configurables in platform_toolsets** (7d276bfbe)
- **feat(delegate): show user's actual concurrency / spawn-depth limits in tool description (#22694)** (1f4200deb)
- **chore: add SiliconID to AUTHOR_MAP** (000ddb8a9)
- **fix(kanban): gate claim + unblock on parent completion** (cda20eec0)
- **feat(plugins): HERMES_PLUGINS_DEBUG=1 surfaces plugin discovery logs (#22684)** (79694018f)
- **perf(google_chat): defer heavy google-cloud imports to first adapter use (#22681)** (8f83046f6)
- **chore: add wesleysimplicio to AUTHOR_MAP** (0d9800743)
- **fix(kanban): call recompute_ready after unlink_tasks removes a dependency** (0c22434f0)
- **feat: confirm prompt for destructive slash commands (#4069) (#22687)** (b9c001116)
- **Merge pull request #22510 from novax635/fix/gateway-slash-confirm-boundary-cleanup** (0cafe7d50)
- **Merge pull request #22610 from uzunkuyruk/fix/telegram-table-row-label-duplicate-bullet** (f1f42a7b9)
- **fix(telegram): exclude row-label column from bullet items in table rendering** (8fdaf4d3d)
- **chore: add nik1t7n to AUTHOR_MAP** (f6d45e5df)
- **feat(gateway): stream Telegram edits safely** (1ac8deb3c)
- **fix(gateway): clear slash-confirm state during session boundary cleanup** (8b6501786)
- **fix(banner): resolve update-check repo from running code, not profile-scoped path** (cca2869d7)
- **fix(profiles): exclude infrastructure artifacts when cloning with --clone-all** (f7e514d4a)
- **feat(plugins): add standalone_sender_fn for out-of-process cron delivery** (93e25ceb1)
- **fix(tests): pin UTF-8 encoding when reading source files on Windows** (3801825ef)
- **chore(release): add KvnGz to AUTHOR_MAP (#22458)** (5d2a75ddf)
- **fix(async): replace get_event_loop() with get_running_loop() in async contexts** (4a1840e68)
- **chore(release): add Zhekinmaksim to AUTHOR_MAP (#22449)** (b7d8e280e)
- **feat(feishu): add native update prompt cards** (7e578f02c)
- **test(kanban): cover kanban_comment author hardening + cross-task policy** (e3ebaa19b)
- **fix(security): drop caller-controlled author override in kanban_comment** (9bbad3cc1)
- **chore(release): add heathley email to AUTHOR_MAP for PR #21911 salvage (#22446)** (e3cd4e401)
- **test(google-chat): cover relay-declared sender_type honoring** (8578f898c)
- **fix(security): honor relay-declared sender_type in Google Chat adapter to prevent BOT filter bypass** (c38640004)
- **fix(transports): use PEP 604 annotation for ToolCall.extra_content** (0f1d41a88)
- **fix(webui): clarify MEDIA absolute-path hint** (2c8c48fbc)
- **fix(webui): add platform hint for MEDIA rendering** (aad5490e7)
- **fix(model_tools): log warnings for failed JSON-array coercion** (7330183d0)
- **fix(delegate): accept JSON string batch tasks** (326ca754a)
- **chore(release): add uzunkuyruk to AUTHOR_MAP (#22434)** (4632be123)
- **fix(sqlite): fall back to journal_mode=DELETE on NFS/SMB/FUSE (#22043)** (2a7047c2e)
- **fix(send_message): map Telegram General topic id to None for forum groups (#22423)** (ae005ec58)
- **fix: always send tenant headers in OpenViking _headers() when account/user are set** (8fb3e2d63)
- **fix(context): handle JSON decode errors in compression — salvage of #22248 (#22416)** (c7e8add12)
- **fix(telegram): skip send_chat_action for DM topic reply-fallback lanes** (aef297a45)
- **fix(telegram): preserve DM topic routing via reply fallback** (b3239572f)
- **chore(release): add leehack to AUTHOR_MAP for PR #22053 salvage (#22409)** (28b5bd7e9)
- **fix(cron): use getJobState helper in handlePauseResume** (96dc27262)
- **Fix cron dashboard rendering for partial jobs** (e57273727)
- **fix(cron): normalize partial job records** (e407376c5)
- **chore(release): add oferlaor to AUTHOR_MAP for PR #22356 salvage** (f2afa68a4)
- **fix(cron): avoid delivery origin as sender identity** (dbafa083b)
- **fix(tui): trim markdown wrap spaces (#22062)** (a7e7921db)
- **fix(gateway): also catch restart TimeoutExpired; friendly message** (78b0008f4)
- **fix(gateway): cap adapter disconnect during stop** (dccf1fb6e)
- **chore(release): add dandacompany to AUTHOR_MAP for salvaged PR #20503** (524cbabd8)
- **fix(slack): enable writable app home DMs in manifest** (24d321617)
- **test(patch-tool): collapse 9 schema-shape tests into 2 invariants** (8e4f3ba4d)
- **fix(patch-tool): advertise per-mode required params in schema descriptions** (3adcc6441)
- **fix: harden termux update path with uv bootstrap and env guard** (7c174e65f)
- **fix: keep tui /quit behavior aligned with cli exit flow** (6f7b698a0)
- **perf(cli): cut ~19s from 'hermes' cold start (skills cache + lazy Feishu + no Nous HTTP) (#22138)** (0ec052ca2)
- **docs(cli): call out Ctrl+Enter for Windows Terminal users** (d606df812)
- **feat(cli): recognise Shift+Enter as a newline key** (f5b635f6a)
- **fix(google-chat): repair setup prompt imports** (cacb98473)
- **Merge pull request #22080 from NousResearch/fix/faster-docker** (d10d19ebb)
- **fix(update): bypass systemd RestartSec after graceful drain (#22101)** (d971b26bf)
- **perf(cli): skip eager plugin discovery on known built-in subcommands (#22120)** (508959668)
- **docs(windows): label native Windows support as early beta (#22115)** (7a4d5c123)
- **ci: run docker build on PRs + smoke test arm64** (93679ef27)
- **ci: add blocking uv.lock check** (758c40135)
- **fix(ci): update uv.lock** (0a51863f5)
- **docker: split python dep install into cached layer above COPY . .** (afc186fa4)
- **ci: split docker-publish into per-arch native runners** (bf80508d6)
- **fix(setup): offer gateway service install on Windows (#22099)** (a54cae60d)
- **test: remove 50 stale/broken tests to unblock CI (#22098)** (66320de52)
- **fix(entry-points): guard hermes_bootstrap import so partial updates don't brick hermes (#22091)** (26bac67ef)
- **docs(windows): add native Windows guide + install one-liner on landing page (#22089)** (3299be6bd)
- **ci(lint): add blocking ruff-check + windows-footguns jobs to lint.yml** (d3120aeab)
- **test: migrate stale os.kill monkeypatches to gateway.status._pid_exists** (f5ee78012)
- **fix(skills): move platforms key out of folded description: > scalars** (291a15844)
- **fix(install.ps1): strip UTF-8 BOM that broke [scriptblock]::Create** (59fbcd5cc)
- **feat(windows uninstall): clean up User env, PATH, Scheduled Task, and portable tooling** (35fce7699)
- **fix(windows): gateway status dedup + install.ps1 platform-SDK bootstrap** (0548facc5)
- **feat(cross-platform): psutil for PID/process management + Windows footgun checker** (cc38282b0)
- **fix(windows): os.kill(pid, 0) is NOT a no-op on Windows — route through new _pid_exists helper** (324567c93)
- **feat(windows): gateway as a Scheduled Task + Startup-folder fallback** (9c263fbf8)
- **fix(windows installer): UTF-8 BOM, tiered extras, skip tinker-atropos by default** (52e497ce7)
- **fix(windows): browser tool + spurious SIGINT from subprocess spawning** (0ba1e12ab)
- **auth: use get_default_hermes_root() for shared nous_auth.json path** (62b4ebb7d)
- **feat(skills): declare platforms frontmatter for all 79 undeclared built-in skills** (98db898c0)
- **feat(optional-skills): declare platforms frontmatter for all 63 undeclared skills** (db22efbe8)
- **feat(skills): gate 7 Linux/macOS-only skills from Windows via platforms frontmatter** (b18b17f9c)
- **fix(windows): auto-install Playwright Chromium + surface it in doctor** (03566e512)
- **docs: add Windows-Specific Quirks section to hermes-agent skill + keystroke diagnostic** (b63f9645f)
- **feat: Ctrl+Enter inserts newline on Windows Terminal** (d1838041e)
- **feat: enrich system-prompt environment hints with host + terminal-backend info** (40e7a71c3)
- **lint: enable PLW1514 as a blocking ruff rule** (3be853a9b)
- **codebase: add encoding='utf-8' to all bare open() calls (PLW1514)** (cbce5e93f)
- **hermes_bootstrap: Windows-only UTF-8 stdio shim for all entry points** (d94fb4771)
- **execute_code: set PYTHONIOENCODING=utf-8 + PYTHONUTF8=1 in child env** (107de0321)
- **tests: skip POSIX-venv-layout tests on Windows** (e614e8795)
- **execute_code: write sandbox files as UTF-8 on Windows** (da184439d)
- **tests: lock in POSIX-equivalence guard for execute_code env scrubber** (3b9cd5820)
- **execute_code: pass through Windows OS-essential env vars** (5c859e571)
- **fix(windows): prefer npm.cmd over npm.ps1, skip .py argv0 in relaunch** (a2efad6be)
- **fix(windows): enable execute_code — stale AF_UNIX gate was blocking the tool** (21efeb51b)
- **fix(windows): %1 install error, patch CRLF false-negative, SOUL.md BOM** (8f91d7bfa)
- **fix(install.ps1): step out of $InstallDir before touching it + harden repo probe** (d52e54170)
- **fix(install.ps1): validate existing repo via git itself + clean up broken stubs** (c469a05ce)
- **fix(windows): quote cache paths in bash + augment PATH so rg/bash resolve on first launch** (fc918867b)
- **fix(windows): use PortableGit (not MinGit), fix relaunch os.execvp crash, surface npm errors** (3601e20f4)
- **feat(windows): close remaining POSIX-only landmines — TUI crash, kanban waitpid, AF_UNIX sandbox, /bin/bash, npm .cmd shims, cwd tracking, detach flags** (e93bfc6c9)
- **fix(windows-editor): default EDITOR=notepad so /edit and Ctrl+X Ctrl+E work** (b53bd12fe)
- **feat(windows-install): bundle portable MinGit instead of relying on winget** (b7fe7ed7b)
- **feat(windows): close native-Windows install gaps — crash-free startup, UTF-8 stdio, tzdata dep, docs** (9de893e3b)
- **fix(profiles): pass encoding=utf-8 to distribution.yaml open (#22083)** (ea2cc4f90)
- **docs(teams-pipeline): cron renewal recipe, sidebar wiring, skill rewrite** (242da9db9)
- **fix(teams-pipeline): add skill asset and fix async test env** (729a659a3)
- **docs(teams): split meetings setup from operator runbook** (b79ef8827)
- **feat(tui): support attaching to an existing gateway (#21978)** (1997b3baf)
- **docs(teams): meeting summary delivery section + env var reference** (968082707)
- **fix(teams-pipeline): fill in missing delivery URL in adapter-reuse test** (5e8dfc9f6)
- **refactor(teams): remove redundant delivery-mode branch** (d36ccc29c)
- **feat(teams): add pipeline outbound delivery via existing adapter** (397f750bb)
- **fix(teams-pipeline): drop-scheduler fallback + test wiring for enablement gate** (a99547740)
- **feat(teams-pipeline): add plugin runtime and operator cli** (07bbd9333)
- **docs(profiles): full user guide for profile distributions (#22017)** (ea86714cc)
- **docs(computer-use): add to sidebar nav under Media and Web** (a735b7213)
- **fix(computer-use): harden image-rejection fallback + AUTHOR_MAP** (d0aad4b02)
- **fix(computer-use): unwrap _multimodal tool results to content list for non-Anthropic providers** (2937f9bef)
- **feat(computer-use): background focus-safe backend — set_value, structured windows, MIME detection** (e31f3b3c5)
- **feat(computer-use): cua-driver backend, universal any-model schema** (850413f12)
- **docs(msgraph): webhook listener setup page + env var reference** (474d1e812)
- **fix(msgraph_webhook): harden auth surface + IP allowlisting + response hygiene** (b8d7e0e6d)
- **fix(msgraph): normalize webhook dedupe and resource matching** (26a59e4f6)
- **fix(msgraph): bound webhook receipt dedupe cache** (2a215de9a)
- **feat(msgraph): add webhook listener platform** (46a6f3902)
- **feat(profile): shareable profile distributions via git (#20831)** (f209a3585)
- **docs(msgraph): add Azure app registration walkthrough + env var reference** (cf648a9b7)
- **fix(msgraph): stream download_to_file body instead of buffering** (45d860d42)
- **test(msgraph): cover concurrent token cache reuse** (b878f89f6)
- **feat(msgraph): add auth and client foundation** (a152c706b)
- **feat(skills): watchers skill — poll RSS / HTTP JSON / GitHub via cron no-agent (#21881)** (ea8e60882)
- **fix(approval): cron jobs must not be treated as gateway context** (839cdd1b0)
- **feat(api-server): expose run approval events** (526c0e018)
- **feat(google-workspace): Drive write ops + Docs/Sheets create/append (#21895)** (e43d2fe52)
- **fix(goals): Ctrl+C during /goal loop auto-pauses the goal (#21888)** (674fad148)
- **feat(docker): bootstrap auth.json from env on first boot** (5643c2979)
- **fix(cron): clean up job output dir in remove_job** (f4e621f7d)
- **Merge pull request #19830 from NousResearch/austin/fix/pluralization** (a3131862b)
- **feat(tui): segment turns with rule above non-first user msgs; trim ticker dead space (#21846)** (42f9234da)
- **fix: include terminal backend in quick setup wizard (#21842)** (7190e20e0)
- **fix(google-workspace): cleanup for --check-live salvage** (83c23e886)
- **fix: correct docstring syntax error in check_auth_live** (617ac0535)
- **fix(google-workspace): detect disabled_client in --check and add --check-live** (5fa493a2c)
- **test(auth): assert Nous refresh rotation payload** (80775d758)
- **fix(auth): send Nous refresh token via header** (b32461f6e)
- **feat(cron): routing intent — deliver=all fans out to every connected channel (#21495)** (486b14b42)
- **refactor(gmi): move User-Agent to profile.default_headers** (81928f03a)
- **Add AUTHOR_MAP entry for Isaac Huang** (5d1bdf11b)
- **fix(model-switch): prevent stale Ollama credentials after provider switch (#21703)** (7338e5d9b)
- **docs(web): fix SearXNG env configuration** (faa13e49f)
- **chore(release): add BennetYrWang to AUTHOR_MAP** (1bdacb697)
- **Serialize Hermes config access** (34f729735)
- **fix(goals): auto-pause when judge model returns unparseable output** (307c85e5c)
- **fix(gateway): defer goal status notices until after response delivery** (03ddff889)
- **feat(kanban): add tooltips and docs link across dashboard (#21541)** (7d66d30d7)
- **Merge origin/main and resolve conflict in nix/tui.nix** (901eccc88)
- **Merge pull request #20942 from NousResearch/austin/fix/personality** (7f92e5506)
- **Merge pull request #20805 from NousResearch/austin-feat-sessions-skills-menu** (b0393af38)
- **chore(release): add hllqkb to AUTHOR_MAP for PR #21288 salvage** (7f369bfe5)
- **fix(installer): set UV_NO_CONFIG=1 to avoid permission denied under sudo -u** (c80fa728b)
- **fix(mcp): unwrap platforms key in channels_list** (292f46836)
- **fix(analytics): prevent silent token loss and add Claude 4.5–4.7 pricing (#21455)** (d87c7b99e)
- **docs: register triage_specifier in the aux-models enumerations (#21494)** (cff821e2d)
- **chore: fix AUTHOR_MAP for johnsonblake1@gmail.com → voteblake** (2214ab107)
- **fix(agent): keep Nous GPT-5 fallback on chat completions** (9076a2e74)
- **feat(kanban): add `specify` — auxiliary LLM fleshes out triage tasks (#21435)** (24d48ffb8)
- **feat: add termux doctor fallback guidance for blocked extras** (732a6c45f)
- **fix: add termux-all install profile and safe fallbacks** (dc5ef1ac8)
- **fix: strengthen termux install network prerequisites** (da18fd084)
- **fix(update): add heartbeat during dependency install** (54c0b10d1)
- **feat(web): add Brave Search (free tier) and DDGS search providers** (04193cf71)
- **test(hermes_constants): cover parse_reasoning_effort()** (cdc0a47dd)
- **feat(acp): pass image file attachments through as image_url parts** (7e2af0c2e)
- **fix(acp): inline file attachment resources** (733e297b8)
- **chore: release v0.13.0 (2026.5.7) (#21406)** (498bfc7bc)
- **fix(telegram): preserve thread_id=1 for forum General typing indicator (#21390)** (2564132a1)
- **fix(run_agent): break permanent empty-response loop from orphan tool-tail (#21385)** (812ce0b98)
- **fix(update): reset-failed before every fallback restart so the gateway can't get stranded (#21371)** (1d2029b2b)
- **fix(cron): initialize MCP servers before constructing the cron AIAgent (#21354)** (04918345e)
- **feat(qqbot): wire native tool-approval UX via inline keyboards** (4de3ef38b)
- **fix(cron): scan assembled prompt including skill content (#3968) (#21350)** (a1fe5f473)
- **chore(release): map maciekczech noreply email** (bbff2f634)
- **fix(kanban): filter dashboard board by selected tenant** (162ad3dd1)
- **test(kanban): cover dashboard select filter wiring** (f4de3810e)
- **fix(mcp): gate utility stubs on server-advertised capabilities (#21347)** (74c9c0eec)
- **fix(webhook): widen INSECURE_NO_AUTH loopback check + tests + docs** (898b6d7d5)
- **fix: block INSECURE_NO_AUTH on non-localhost webhook bindings** (fb4f95356)
- **docs(platforms): document env_enablement_fn + cron_deliver_env_var hooks (#21331)** (5c08b851d)
- **feat(qqbot): process attachments in quoted (reply) messages** (5b121c6e3)
- **feat(qqbot): add inline-keyboard approvals and update prompts** (de584cd1d)
- **feat(qqbot): add chunked upload with structured error types** (9feaeb632)
- **feat(kanban): per-task max_retries override (#20263 follow-up, supersedes #20972) (#21330)** (ac51c4c1a)
- **docs(readme): prefer .venv to match AGENTS.md and scripts/run_tests.sh (#21334)** (ff0985323)
- **fix(pairing): enforce lockout on approve_code, not just generate_code (#10195) (#21325)** (145e8ec23)
- **chore(release): add qWaitCrypto to AUTHOR_MAP for PR #21055 salvage** (1baab8771)
- **fix(mcp): coerce numeric tool args defensively** (62c2f5d8d)
- **chore(release): map donramon77 to AUTHOR_MAP for PR #18425 salvage** (43cf72a45)
- **refactor(plugins/platforms): migrate IRC + Teams to new env_enablement + cron_deliver hooks** (be87a9629)
- **feat(plugins/google_chat): Google Chat platform adapter as a bundled plugin** (44cd79e79)
- **feat(gateway): generic plugin hooks for env enablement + cron delivery** (af9336d57)
- **fix(mcp): surface image tool results as MEDIA tags instead of dropping them (#21328)** (c8e3e3918)
- **fix(mcp): forward OAuth auth and bump sse_read_timeout on SSE transport (#21323)** (dd2dc2bdd)
- **chore(release): map tuancanhnguyen706@gmail.com → xxxigm** (4ee6c3349)
- **fix(tests): avoid asyncio DeprecationWarning in event loop fixture on 3.12+** (d5fcc8392)
- **fix(dashboard): finish resumeId -> resumeParam rename in ChatPage (#21317)** (12a0f5901)
- **fix(mcp): re-raise CancelledError explicitly in MCPServerTask.run (#21318)** (e0a2b0876)
- **fix(memory): remove dead allOf schema block at the source** (5a3e5b23d)
- **fix: strip Codex-hostile top-level schema combinators** (3924cb408)
- **feat(gateway): add allowed_{chats,channels,rooms} whitelist to Telegram, Mattermost, Matrix, DingTalk** (69d025e4a)
- **chore(release): add CashWilliams to AUTHOR_MAP** (f5c9bb582)
- **feat(slack): add allowed_channels whitelist config** (cd3ef685c)
- **fix(whatsapp): reject strangers by default, never respond in self-chat (#8389) (#21291)** (6a4ecc0a9)
- **fix(kanban): make code/pre styling theme-immune across all themes (#21086) (#21247)** (76d2dcdc8)
- **fix(compressor): soften summary prompt for content filters** (fc88eec92)
- **fix(delegate): expand composite toolsets before intersection in delegate_task** (e795b7e3a)
- **fix(agent): honor configured model max tokens** (a78e622df)
- **feat(dashboard): support serving under URL prefix via X-Forwarded-Prefix** (52e277782)
- **chore: AUTHOR_MAP entry for @glesperance** (6769060ae)
- **fix(tui): render structured content on resume** (ec9d0e26d)
- **chore: correct AUTHOR_MAP for oluwadareab12 (was mismapped to bennytimz)** (30c999017)
- **fix(cli): replace get_event_loop() with get_running_loop() to silence RuntimeWarning in process_loop thread (#19285)** (edbbc96b5)
- **feat(models): add paid tencent/hy3-preview route on OpenRouter (#21077)** (2c1921241)
- **fix(mcp): include exception type in error messages when str(exc) is empty** (f9b4b8af3)
- **chore(release): add subtract0 to AUTHOR_MAP for PR #19935 salvage** (f481395d4)
- **fix(mcp): retry stale pipe transport failures** (a1f85ef2b)
- **fix(models): add alibaba-coding-plan to _PROVIDER_MODELS curated list** (8ad117a3d)
- **chore: AUTHOR_MAP entry for @paul-tian** (33563df02)
- **fix(gateway): honor configured goal turn budget** (4d4807585)
- **fix(gateway): consolidate runtime-status writes + rate-limit failure logs** (0efc54796)
- **fix(gateway): log platform status write failures instead of silently swallowing** (5d9061148)
- **chore: AUTHOR_MAP entry for @LucianoSP** (755b74fc2)
- **fix: use configured model for gateway auth fallback** (f7b71aa0d)
- **chore(release): add masonjames to AUTHOR_MAP for PR #10439 salvage** (8aa30407c)
- **fix(mcp): report configured timeout in MCP call errors** (80548f9a4)
- **chore: AUTHOR_MAP entry for @hedirman** (25187ca05)
- **Fix WhatsApp long message splitting** (a9ebee5f0)
- **fix(gateway): include exception detail in bootstrap warning output** (4d32f4030)
- **fix(gateway): surface bootstrap failures to stderr instead of silently swallowing** (926402dd1)
- **fix(security): support SRI integrity verification for dashboard plugin scripts** (5909526a0)
- **chore(release): add AJV20 to AUTHOR_MAP for PR #10287 salvage** (46d1fc16a)
- **fix(mcp): clear stale thread interrupt before MCP discovery** (9575bce6c)
- **chore: AUTHOR_MAP entry for wabrent** (b7a97cd44)
- **fix(gateway): log agent task failures instead of silently losing usage data** (98ca0694d)
- **chore: AUTHOR_MAP entry for @kowenhaoai** (fcd619cae)
- **feat(image-gen): honor image_gen.model from config.yaml in plugin dispatch** (a9c7bdaea)
- **fix(security): require explicit allowlist or TEAMS_ALLOW_ALL_USERS opt-in for Teams approval buttons** (b739fcdfc)
- **chore: AUTHOR_MAP entry for @acc001k** (cfe019c78)
- **fix(auxiliary): enforce Codex Responses stream timeout** (5533ad764)
- **chore: AUTHOR_MAP entry for @agilejava** (fd13b7d2b)
- **fix(vision): Z.AI vision model compatibility — endpoint routing and max_tokens handling** (6ea4a6a74)
- **fix(kanban): restore Enter=submit, Shift+Enter=newline in inline-create textarea** (fa582749e)
- **feat(kanban): convert inline-create title input to multiline textarea** (b93c9f639)
- **fix(docker): chown runtime node_modules trees to hermes user (#18800)** (498c01406)
- **fix: add dashboard to CLI help epilogue and Docker CI smoke test** (2f2f65448)
- **fix(auth): shorten credential 401 cooldown** (4876959a1)
- **fix: use max_completion_tokens for GitHub Copilot** (f648c2e3a)
- **fix(skills): lock usage telemetry updates** (d12be46df)
- **fix(windows): terminal drain and cwd path conversion for native Windows** (c2d6b385f)
- **fix(weixin): wrap long copy-unfriendly lines** (7244a1f0d)
- **fix(tui): avoid main-screen scrollback reset loops** (a494a614d)
- **fix(matrix): defer reaction cleanup redactions** (31f22890e)
- **chore: AUTHOR_MAP entry for @stevenchouai** (8cef14913)
- **fix(update): migrate config in non-interactive updates** (9442a8fa2)
- **fix(docker): refuse root gateway runs in official image** (84287b0de)
- **chore: AUTHOR_MAP entry for @shashwatgokhe** (afbcca0f0)
- **fix(image-routing): sniff magic bytes for image MIME, ignore misleading suffix** (5cf703245)
- **fix(doctor): retry DashScope China endpoint** (5ead12670)
- **fix(models): prefer image modalities for vision routing** (14f38822f)
- **fix(tui): surface backend error as visible text when final_response is empty (#21245)** (6e46f99e7)
- **fix(auth): keep Spotify logout from resetting model config** (8dcdc3cbc)
- **fix(agent): drop terminal empty-response sentinels** (2021c1865)
- **fix(agent): avoid persisting empty-response recovery scaffolding** (e73508979)
- **fix(discord): route DM role-auth opt-in through config.yaml (not env var)** (80717a157)
- **fix(discord): extend role-scope fix to slash surface + fixture update** (5c045b8f6)
- **fix(discord): scope DISCORD_ALLOWED_ROLES to originating guild (CVSS 8.1)** (ef1e56557)
- **fix(gateway): preserve max turns after env reload** (8308d1833)
- **fix(tui): refresh scroll height at cached bottom** (2c14d3b9b)
- **fix: require memory schema fields by action** (5b24c0fa8)
- **feat(curator): add `hermes curator list-archived` command (#21236)** (ae1f058b3)
- **test+docs: cover transform_llm_output hook + release author map** (47bf5d7ec)
- **feat: add transform_llm_output plugin hook** (c3be6ec18)
- **fix(openviking): add Bearer auth header and omit empty/legacy tenant headers (#21232)** (6e250a55d)
- **Follow latest child session on dashboard resume** (b12a5a72b)
- **fix: avoid unsupported anthropic context beta by default** (e9685a5cf)
- **fix(kanban): make dashboard board pin authoritative over server current file (#21230)** (b9f1ac8c1)
- **docs(contributing): align tool discovery and test runner with AGENTS.md** (647f95b42)
- **fix: WhatsApp bridge process leak and disable config asymmetry** (0d3593e51)
- **fix(browser): enforce cloud-metadata SSRF floor in hybrid routing (#16234) (#21228)** (0214858ef)
- **feat: add SSE transport support for MCP client** (12289c263)
- **fix(mcp-oauth): persist OAuth server metadata across process restarts (#21226)** (c4a799231)
- **feat(gateway): add `hermes gateway list` to show all profiles' gateway status** (3c439ec68)
- **fix(model_tools): log plugin hook exceptions instead of silently swallowing them** (61d9e3366)
- **test(kanban): regression for CancelledError swallow in stream_events** (fe4748ede)
- **chore(release): map SandroHub013 email** (a5f116fc3)
- **fix(kanban): treat dashboard event-stream cancellation as normal shutdown** (36ad97337)
- **docs: clarify API server tool execution locality** (43a664571)
- **fix(install): remove uv exclude-newer cutoff** (d8d57fb2f)
- **docs(curator): update CLI docs for synchronous-by-default manual run** (6b3a9b4bf)
- **fix(curator): make manual runs synchronous** (6b9f7140b)
- **chore(release): map altriatree@gmail.com -> @TruaShamu** (bda7b240b)
- **feat(tui): surface compression count in Ink status bar** (3a82172dd)
- **refactor: replace 'cmp' text with 🗜️ emoji in status bar** (f5a232af8)
- **feat(cli): show context compression count in status bar** (103e11926)
- **fix(credential_pool): resolve key mix-up when custom providers share base_url** (e38ea3807)
- **chore: AUTHOR_MAP entry for @GinWU05** (3c8154e62)
- **fix(cli): honor positive tool preview length** (6d9b30632)
- **chore: AUTHOR_MAP entry for @nouseman666** (eef23354a)
- **fix(dashboard): route browser wheel into inner TUI scrolling** (7cbef2bd4)
- **fix(dashboard): let embedded chat use a single scroll system** (8aceef539)
- **fix(dashboard): stabilize embedded chat resume and scrollback** (a0758cd1e)
- **fix(kanban): auto-block workers that exit without completing (#20894) (#21214)** (fdb9e0f6a)
- **docs(readme): drop misleading RL install-extras claim, defer to CONTRIBUTING** (699c770e5)
- **chore(release): add AUTHOR_MAP entries for ggnnggez and ehz0ah** (aa9a2091f)
- **fix(memory): harden OpenViking local path uploads** (2b6345cee)
- **test(memory): harden OpenViking local upload coverage** (187951ec6)
- **fix(memory): support OpenViking local resource uploads** (7137cccbd)
- **fix(model_switch): live model discovery for custom_providers in /model picker** (abe5a3c93)
- **chore: AUTHOR_MAP entry for @leon7609** (4e27e4e05)
- **test: update send_message_tool mocks for force_document kwarg** (e82f3b0c4)
- **feat(gateway): support [[as_document]] directive for skill media routing** (d34f03c32)
- **fix(bedrock): preserve reasoningContent across converse normalization** (8d363f8d5)
- **chore: add discodirector email to AUTHOR_MAP** (f0dd5b9c1)
- **fix(mcp): give 'mcp add --command' a distinct argparse dest** (4f364c4e9)
- **fix(gateway): cap cached session sources with LRU eviction** (333598cb0)
- **fix(gateway): preserve thread routing from cached live session sources** (176b93575)
- **fix: exclude hidden and archive dirs from _find_skill rglob** (5bf12eb44)
- **fix(delegate): correct ACP docs — Claude Code CLI has no --acp flag** (69692039e)
- **fix(security): close TOCTOU window in hermes_cli/auth.py credential writers (#21194)** (042eb930e)
- **chore: AUTHOR_MAP entry for @likejudy** (991df4ef8)
- **feat: add Discord message deletion action** (8b32a9d0f)
- **feat(security): enable secret redaction by default (#17691, #20785) (#21193)** (fb1ce793e)
- **chore: AUTHOR_MAP entry for chenlinfeng@ruije / @noOne-list** (d856f4535)
- **test(weixin): update timeout assertion for asyncio.wait_for migration** (ecaafe5f2)
- **fix(weixin): replace all aiohttp ClientTimeout with asyncio.wait_for()** (3a0d52d57)
- **fix(oauth,gateway): monotonic deadlines for polling/timeout loops** (2e00bcaaa)
- **fix(gateway): use monotonic deadlines in QR onboarding flows** (6e8f1e09a)
- **chore: add AUTHOR_MAP entries for thelumiereguy and counterposition** (73d637176)
- **fix(gateway): avoid duplicated responses history** (8a96fa48c)
- **refactor(auth): dedupe file-lock helper; document Nous lock order** (429e78589)
- **fix(auth): sync shared Nous refresh tokens** (a84e56d4c)
- **refactor(gateway): simplify auto-resume + extend to crash recovery** (38b1c7dce)
- **fix(gateway): preserve resume marker on interrupted restart** (961a3535f)
- **feat(gateway): auto-resume interrupted sessions after restart** (fad684b1f)
- **chore(release): map mwnickerson noreply email** (233bfd362)
- **fix: auto-block repeated kanban retries** (411cfa26e)
- **chore(release): map sonic-netizen noreply email** (595e90669)
- **fix(kanban): reap completed worker children in dispatch_once** (b49a3f847)
- **fix(kanban): stop reclaimed workers before retry** (06f24351c)
- **chore(release): map stephen0110 noreply email** (63bd690a5)
- **fix(kanban): heartbeat tool extends claim TTL, not just last_heartbeat_at** (40b51c93a)
- **feat(gateway): opt-in cleanup of temporary progress bubbles (#21186)** (bf843adf0)
- **fix(gateway): translate inbound document host paths to container paths for Docker backend** (7c0766e06)
- **test(skills): cover additional rescan paths in skill_commands cache (#14536)** (d4de7d417)
- **feat(optional-skills): port Anthropic financial-services skills as optional finance bundle (#21180)** (fce58cbe2)
- **fix(image-routing): expose attached image paths in native multimodal text part** (11b9b146f)
- **test(update): teach restart-mocks about the post-update survivor sweep** (1f27ca638)
- **chore(release): add Gutslabs to AUTHOR_MAP for PR #21148 salvage** (aa5690342)
- **fix(security): close TOCTOU window when saving MCP OAuth credentials** (7d36e8346)
- **fix(web): force light color-scheme on docs iframe** (a5c9c83b7)
- **test(update): patch isatty on real streams to fix xdist-flaky --yes tests** (595bcc89f)
- **test(docker): align Dockerfile contract tests with simplified TUI flow** (033e533d0)
- **chore: AUTHOR_MAP entry for mrcoferland** (e7eb07cec)
- **fix: route Telegram image documents through photo handling** (bd0c54d17)
- **feat(profiles): --no-skills flag for empty profile creation (#20986)** (51f9953e6)
- **docs(kanban): fix worker skill setup instructions too (#20960)** (49c3c2e0d)
- **docs(kanban): fix orchestrator skill setup instructions (#20958)** (45cbf9389)
- **fix(discord): narrow rate-limit catch and move sync state under gateway/** (5a3cadf6e)
- **fix(gateway): wait for systemd restart readiness** (d797755a1)
- **fix(tui): preserve session when switching personality** (65c762b2e)
- **fix(gateway): don't dead-end setup wizard when only system-scope unit is installed** (3cdbf334d)
- **fix(tui): restore voice push-to-talk parity (#20897)** (04cf4788c)
- **fix(tui): steady transcript scrollbar (#20917)** (5ccab51fa)
- **Merge pull request #20890 from NousResearch/fix/docker-push** (53a024994)
- **fix(tui): honor skin highlight colors (#20895)** (f1a8e9994)
- **fix(tui): refresh virtual offsets after row resize (#20898)** (da6019820)
- **fix(cli): submit LF enter in thin PTYs (#20896)** (5044e1cbf)
- **chore: add guillaumemeyer to AUTHOR_MAP** (d8b85bfd1)
- **feat(gateway): also gate pre-restart "Gateway restarting" notification** (7df611519)
- **feat(gateway): per-platform gateway_restart_notification flag** (b71f80e6c)
- **fix(auth): fall back to global-root auth.json for providers missing in profile** (33bf5f629)
- **docs(tool-gateway): rewrite as pitch-first marketing page (#20827)** (d514dd405)
- **ci(docker): don't cancel overlapping builds, guard :latest** (f4031df05)
- **fix(tui): bound virtual history offset searches** (946ef0ea1)
- **Merge pull request #19908 from NousResearch/typecheck** (a345f7b6e)
- **chore: follow-up cleanup for Kanban migration fix** (a2ff19305)
- **fix(kanban): avoid fragile failure-column renames** (b1d420e75)
- **chore: follow-up cleanup for Feishu topic thread fix** (28299afc2)
- **fix(feishu): keep topic replies in threads** (441ef75d1)
- **docs: add Web Search + Extract feature page with SearXNG setup guide** (48c241840)
- **docs+skill: add searxng-search optional skill and documentation** (94016dd1a)
- **feat(web): add SearXNG as a native search-only backend** (5c906d702)
- **refactor(web): per-capability backend selection for search/extract split** (cd2cbc73b)
- **feat(dashboard): add 'default-large' built-in theme with 18px base size (#20820)** (6388aafbd)
- **fix(opencode-go): keep users on opencode-go instead of hijacking to native providers (#20802)** (a24789d73)
- **feat(tui): add /sessions slash command for browsing and resuming previous sessions** (09a491464)
- **docs(plugins): close the gaps \u2014 image-gen-provider-plugin guide + publishing a skill tap (#20800)** (773cf48c5)
- **feat(skills/linear): add Documents support + Python helper script (#20752)** (ad7aad251)
- **feat(ci): add typecheck (warnings only in CI)** (9627ee70e)
- **change: enable ruff/ty** (63c51d896)
- **docs: pluggable surfaces coverage — model-provider guide, full plugin map, opt-in fix (#20749)** (b62a82e0c)
- **docs(wsl2): expand Windows (WSL2) guide — filesystem, networking, services, pitfalls (#20748)** (90a7adcb2)
- **chore(release): map cleo@edaphic.xyz → curiouscleo** (3ce1233ae)
- **fix(cli): catch OSError in _resolve_attachment_path to prevent ENAMETOOLONG dropping long slash commands** (906881c38)
- **feat(checkpoints): v2 single-store rewrite with real pruning + disk guardrails (#20709)** (a0fedfbb1)
- **feat(skills): add shop-app personal shopping assistant (optional) (#20702)** (b045e7a2b)
- **fix(cli): recover classic CLI output after resize** (76074d9ee)
- **fix(kanban): reset code element background inside board** (17687911b)
- **chore(release): map liuguangyong@hellobike -> liuguangyong93** (b1e0ef82f)
- **fix(tui): restore gap before duration when verb segment is hidden** (a0556b861)
- **fix(tui): stabilize FaceTicker elapsed width to prevent composer drift** (ca5febfed)
- **fix(ui): reduce status-line jitter while scrolling** (e45df2e81)
- **chore: AUTHOR_MAP entry for adybag14-cyber** (a869a523e)
- **fix: harden install.sh against inherited Python env leakage** (043a118d4)
- **fix(cli): guard logger.debug in signal handler (#13710 regression) (#20673)** (e70e49016)
- **fix(update): drop pip --quiet so slow installs don't look hung (#20679)** (a6f5f9c48)
- **fix(gateway): preserve model picker current context** (466f3a11d)
- **fix(browser): tighten Lightpanda fallback edge cases** (629d8b843)
- **fix(tui): collapse long system messages in transcript with expand toggle** (68162eb18)
- **feat(tui): collapsible sections in startup banner (skills, system prompt, MCP)** (d78c34928)
- **fix(browser): surface Lightpanda Chrome fallback warnings** (3ebdd2644)
- **feat(browser): add Lightpanda engine support with automatic Chrome fallback** (395dbcc87)
- **fix: salvage batch — compaction guidance, memory authority, cache eviction after compression** (aa88dcc57)
- **changes from feedback** (0d1cbc2dd)
- **feat(models): add x-ai/grok-4.3 to OpenRouter + Nous Portal curated lists (#20497)** (f27fcb6a8)
- **feat(models): add deepseek/deepseek-v4-pro to OpenRouter + Nous Portal curated lists (#20495)** (477e4a2fe)
- **docs: document custom model aliases for /model command (#20475)** (e598e1852)
- **docs(security): rewrite policy around OS-level isolation as the boundary** (401aadb5b)
- **fix(nix): refresh hermes-tui npmDepsHash for ui-tui lockfile** (b162f9ef9)
- **fix: pluralization** (05bec0ac7)
- **fix(tui): update README** (9d645d98c)
- **fix(tui): don't hardcode /home/bb** (242659f5a)
- **fix(tui): update comments** (42df7ec59)
- **refactor(docker): drop manual @hermes/ink build, rely on esbuild bundle** (42e166c7e)
- **fix(nix): refresh npm lockfile hashes** (279504d5b)
- **refactor(tui): bundle with esbuild, drop runtime node_modules** (42627b4ea)

## Changed files

```
 .env.example                                       |    89 +-
 .github/actions/hermes-smoke-test/action.yml       |    47 +
 .github/workflows/docker-publish.yml               |   517 +-
 .github/workflows/history-check.yml                |    58 +
 .github/workflows/lint.yml                         |   202 +
 .github/workflows/supply-chain-audit.yml           |    66 +
 .github/workflows/tests.yml                        |     5 +-
 .github/workflows/upload_to_pypi.yml               |   163 +
 .github/workflows/uv-lockfile-check.yml            |   119 +
 .gitignore                                         |     3 +
 .gitmodules                                        |     3 -
 AGENTS.md                                          |   153 +-
 CONTRIBUTING.md                                    |   302 +-
 Dockerfile                                         |    42 +-
 README.md                                          |    29 +-
 README.zh-CN.md                                    |     8 +-
 RELEASE_v0.13.0.md                                 |   641 +
 RELEASE_v0.14.0.md                                 |   479 +
 SECURITY.md                                        |   357 +-
 acp_adapter/auth.py                                |    48 +-
 .../bootstrap}/__init__.py                         |     0
 acp_adapter/bootstrap/bootstrap_browser_tools.ps1  |   288 +
 acp_adapter/bootstrap/bootstrap_browser_tools.sh   |   399 +
 acp_adapter/entry.py                               |   156 +-
 acp_adapter/events.py                              |    77 +-
 acp_adapter/permissions.py                         |   122 +-
 acp_adapter/server.py                              |   481 +-
 acp_adapter/session.py                             |     1 +
 acp_adapter/tools.py                               |     5 +-
 acp_registry/agent.json                            |    20 +-
 acp_registry/icon.svg                              |    31 +-
 agent/account_usage.py                             |     2 +-
 agent/agent_init.py                                |  1469 +++
 agent/agent_runtime_helpers.py                     |  2134 ++++
 agent/anthropic_adapter.py                         |   202 +-
 agent/async_utils.py                               |    68 +
 agent/auxiliary_client.py                          |  1071 +-
 agent/background_review.py                         |   570 +
 agent/bedrock_adapter.py                           |    29 +-
 agent/browser_provider.py                          |   175 +
 agent/browser_registry.py                          |   223 +
 agent/chat_completion_helpers.py                   |  2051 ++++
 agent/codex_responses_adapter.py                   |    95 +-
 agent/codex_runtime.py                             |   448 +
 agent/context_compressor.py                        |   349 +-
 agent/context_engine.py                            |     5 +
 agent/conversation_compression.py                  |   556 +
 agent/conversation_loop.py                         |  4018 +++++++
 agent/copilot_acp_client.py                        |    43 +-
 agent/credential_pool.py                           |   212 +-
 agent/credential_sources.py                        |    30 +
 agent/curator.py                                   |   109 +-
 agent/display.py                                   |    37 +-
 agent/error_classifier.py                          |    38 +-
 agent/gemini_cloudcode_adapter.py                  |    10 +-
 agent/gemini_native_adapter.py                     |     6 +
 agent/i18n.py                                      |    33 +-
 agent/image_gen_registry.py                        |    37 +-
 agent/image_routing.py                             |    93 +-
 agent/iteration_budget.py                          |    62 +
 agent/lsp/__init__.py                              |   106 +
 agent/lsp/cli.py                                   |   308 +
 agent/lsp/client.py                                |   930 ++
 agent/lsp/eventlog.py                              |   213 +
 agent/lsp/install.py                               |   376 +
 agent/lsp/manager.py                               |   644 +
 agent/lsp/protocol.py                              |   196 +
 agent/lsp/range_shift.py                           |   149 +
 agent/lsp/reporter.py                              |    78 +
 agent/lsp/servers.py                               |  1040 ++
 agent/lsp/workspace.py                             |   223 +
 agent/markdown_tables.py                           |   309 +
 agent/memory_manager.py                            |     9 +-
 agent/message_sanitization.py                      |   444 +
 agent/model_metadata.py                            |   436 +-
 agent/models_dev.py                                |   112 +-
 agent/moonshot_schema.py                           |    35 +-
 agent/nous_rate_guard.py                           |     2 +-
 agent/plugin_llm.py                                |  1046 ++
 agent/portal_tags.py                               |    64 +
 agent/process_bootstrap.py                         |   167 +
 agent/prompt_builder.py                            |   278 +-
 agent/prompt_caching.py                            |    25 +-
 agent/redact.py                                    |    15 +-
 agent/shell_hooks.py                               |    32 +-
 agent/skill_commands.py                            |     4 +-
 agent/skill_utils.py                               |    42 +-
 agent/stream_diag.py                               |   280 +
 agent/system_prompt.py                             |   333 +
 agent/tool_dispatch_helpers.py                     |   336 +
 agent/tool_executor.py                             |   920 ++
 agent/tool_guardrails.py                           |     3 +
 agent/tool_result_classification.py                |    26 +
 agent/transports/chat_completions.py               |    21 +-
 agent/transports/codex.py                          |    51 +-
 agent/transports/codex_app_server.py               |   368 +
 agent/transports/codex_app_server_session.py       |   810 ++
 agent/transports/codex_event_projector.py          |   312 +
 agent/transports/hermes_tools_mcp_server.py        |   233 +
 agent/transports/types.py                          |     2 +-
 agent/usage_pricing.py                             |   184 +-
 agent/video_gen_provider.py                        |   299 +
 agent/video_gen_registry.py                        |   117 +
 agent/web_search_provider.py                       |   221 +
 agent/web_search_registry.py                       |   262 +
 batch_runner.py                                    |    17 +-
 cli-config.yaml.example                            |    62 +-
 cli.py                                             |  2559 +++-
 cron/jobs.py                                       |   155 +-
 cron/scheduler.py                                  |   308 +-
 docker-compose.yml                                 |    12 +
 docker/entrypoint.sh                               |    18 +
 environments/README.md                             |   324 -
 environments/__init__.py                           |    36 -
 environments/agent_loop.py                         |   534 -
 environments/agentic_opd_env.py                    |  1214 --
 environments/benchmarks/tblite/README.md           |    73 -
 environments/benchmarks/tblite/default.yaml        |    39 -
 environments/benchmarks/tblite/local.yaml          |    38 -
 environments/benchmarks/tblite/local_vllm.yaml     |    40 -
 environments/benchmarks/tblite/run_eval.sh         |    42 -
 environments/benchmarks/tblite/tblite_env.py       |   119 -
 .../benchmarks/terminalbench_2/default.yaml        |    42 -
 .../benchmarks/terminalbench_2/run_eval.sh         |    42 -
 .../terminalbench_2/terminalbench2_env.py          |  1016 --
 environments/benchmarks/yc_bench/README.md         |   115 -
 environments/benchmarks/yc_bench/__init__.py       |     0
 environments/benchmarks/yc_bench/default.yaml      |    43 -
 environments/benchmarks/yc_bench/run_eval.sh       |    34 -
 environments/benchmarks/yc_bench/yc_bench_env.py   |   848 --
 environments/hermes_base_env.py                    |   714 --
 environments/hermes_swe_env/__init__.py            |     0
 environments/hermes_swe_env/default.yaml           |    34 -
 environments/hermes_swe_env/hermes_swe_env.py      |   229 -
 environments/patches.py                            |    35 -
 environments/terminal_test_env/__init__.py         |     0
 environments/terminal_test_env/default.yaml        |    34 -
 .../terminal_test_env/terminal_test_env.py         |   292 -
 environments/tool_call_parsers/__init__.py         |   120 -
 .../tool_call_parsers/deepseek_v3_1_parser.py      |    72 -
 .../tool_call_parsers/deepseek_v3_parser.py        |    89 -
 environments/tool_call_parsers/glm45_parser.py     |   109 -
 environments/tool_call_parsers/glm47_parser.py     |    35 -
 environments/tool_call_parsers/hermes_parser.py    |    75 -
 environments/tool_call_parsers/kimi_k2_parser.py   |    93 -
 environments/tool_call_parsers/llama_parser.py     |    96 -
 environments/tool_call_parsers/longcat_parser.py   |    69 -
 environments/tool_call_parsers/mistral_parser.py   |   137 -
 .../tool_call_parsers/qwen3_coder_parser.py        |   163 -
 environments/tool_call_parsers/qwen_parser.py      |    19 -
 environments/tool_context.py                       |   473 -
 environments/web_research_env.py                   |   719 --
 gateway/__init__.py                                |     2 +-
 gateway/config.py                                  |   348 +-
 gateway/display_config.py                          |    16 +-
 gateway/memory_monitor.py                          |   230 +
 gateway/pairing.py                                 |    13 +-
 gateway/platform_registry.py                       |    50 +-
 gateway/platforms/ADDING_A_PLATFORM.md             |    52 +-
 gateway/platforms/__init__.py                      |    28 +-
 gateway/platforms/api_server.py                    |   450 +-
 gateway/platforms/base.py                          |   490 +-
 gateway/platforms/bluebubbles.py                   |     2 +-
 gateway/platforms/dingtalk.py                      |   115 +-
 gateway/platforms/discord.py                       |  1106 +-
 gateway/platforms/email.py                         |    29 +-
 gateway/platforms/feishu.py                        |   338 +-
 gateway/platforms/feishu_comment.py                |     6 +-
 gateway/platforms/feishu_comment_rules.py          |     2 +-
 gateway/platforms/helpers.py                       |     6 +-
 gateway/platforms/homeassistant.py                 |     4 +-
 gateway/platforms/matrix.py                        |   219 +-
 gateway/platforms/mattermost.py                    |    38 +-
 gateway/platforms/msgraph_webhook.py               |   397 +
 gateway/platforms/qqbot/__init__.py                |    36 +
 gateway/platforms/qqbot/adapter.py                 |   756 +-
 gateway/platforms/qqbot/chunked_upload.py          |   602 +
 gateway/platforms/qqbot/keyboards.py               |   473 +
 gateway/platforms/signal.py                        |    26 +-
 gateway/platforms/slack.py                         |   131 +-
 gateway/platforms/sms.py                           |     2 +
 gateway/platforms/telegram.py                      |  1560 ++-
 gateway/platforms/telegram_network.py              |     2 +-
 gateway/platforms/webhook.py                       |    47 +-
 gateway/platforms/wecom.py                         |    15 +-
 gateway/platforms/weixin.py                        |   111 +-
 gateway/platforms/whatsapp.py                      |   226 +-
 gateway/platforms/yuanbao.py                       |   192 +-
 gateway/platforms/yuanbao_media.py                 |     4 +-
 gateway/platforms/yuanbao_proto.py                 |     2 +-
 gateway/run.py                                     |  3782 ++++--
 gateway/session.py                                 |    25 +-
 gateway/session_context.py                         |     2 +
 gateway/shutdown_forensics.py                      |   462 +
 gateway/slash_access.py                            |   229 +
 gateway/status.py                                  |   176 +-
 gateway/stream_consumer.py                         |   308 +-
 hermes_bootstrap.py                                |   129 +
 hermes_cli/__init__.py                             |     4 +-
 hermes_cli/_parser.py                              |     3 +
 hermes_cli/_subprocess_compat.py                   |   175 +
 hermes_cli/auth.py                                 |  1817 ++-
 hermes_cli/auth_commands.py                        |    48 +-
 hermes_cli/backup.py                               |    16 +-
 hermes_cli/banner.py                               |    83 +-
 hermes_cli/checkpoints.py                          |   244 +
 hermes_cli/claw.py                                 |    32 +-
 hermes_cli/clipboard.py                            |    21 +-
 hermes_cli/codex_models.py                         |    33 +-
 hermes_cli/codex_runtime_plugin_migration.py       |   757 ++
 hermes_cli/codex_runtime_switch.py                 |   266 +
 hermes_cli/commands.py                             |    44 +-
 hermes_cli/completion.py                           |     8 +-
 hermes_cli/config.py                               |   862 +-
 hermes_cli/copilot_auth.py                         |     6 +-
 hermes_cli/cron.py                                 |    12 +-
 hermes_cli/curator.py                              |    60 +-
 hermes_cli/curses_ui.py                            |    24 +-
 hermes_cli/dep_ensure.py                           |   106 +
 hermes_cli/dingtalk_auth.py                        |     2 +-
 hermes_cli/doctor.py                               |   813 +-
 hermes_cli/env_loader.py                           |     2 +-
 hermes_cli/fallback_cmd.py                         |     6 +-
 hermes_cli/gateway.py                              |  1112 +-
 hermes_cli/gateway_windows.py                      |   691 ++
 hermes_cli/goals.py                                |   301 +-
 hermes_cli/hooks.py                                |     8 +-
 hermes_cli/inventory.py                            |   240 +
 hermes_cli/kanban.py                               |   270 +-
 hermes_cli/kanban_db.py                            |  1014 +-
 hermes_cli/kanban_diagnostics.py                   |   147 +-
 hermes_cli/kanban_specify.py                       |   266 +
 hermes_cli/main.py                                 |  2184 +++-
 hermes_cli/mcp_config.py                           |    30 +-
 hermes_cli/memory_setup.py                         |    13 +-
 hermes_cli/model_catalog.py                        |     4 +-
 hermes_cli/model_normalize.py                      |    23 +-
 hermes_cli/model_switch.py                         |    62 +-
 hermes_cli/models.py                               |   402 +-
 hermes_cli/nous_subscription.py                    |    19 +-
 hermes_cli/oneshot.py                              |    21 +-
 hermes_cli/pairing.py                              |    18 +
 hermes_cli/plugins.py                              |   267 +-
 hermes_cli/plugins_cmd.py                          |   166 +-
 hermes_cli/profile_distribution.py                 |   702 ++
 hermes_cli/profiles.py                             |   299 +-
 hermes_cli/providers.py                            |    19 +
 hermes_cli/proxy/__init__.py                       |    20 +
 hermes_cli/proxy/adapters/__init__.py              |    35 +
 hermes_cli/proxy/adapters/base.py                  |    94 +
 hermes_cli/proxy/adapters/nous_portal.py           |   137 +
 hermes_cli/proxy/cli.py                            |   141 +
 hermes_cli/proxy/server.py                         |   265 +
 hermes_cli/pt_input_extras.py                      |    83 +
 hermes_cli/pty_bridge.py                           |    19 +-
 hermes_cli/relaunch.py                             |    64 +-
 hermes_cli/runtime_provider.py                     |   109 +-
 hermes_cli/security_advisories.py                  |   451 +
 hermes_cli/send_cmd.py                             |   445 +
 hermes_cli/session_recap.py                        |   316 +
 hermes_cli/setup.py                                |   257 +-
 hermes_cli/skills_hub.py                           |    14 +-
 hermes_cli/skin_engine.py                          |    46 +-
 hermes_cli/slack_cli.py                            |     6 +
 hermes_cli/status.py                               |    25 +-
 hermes_cli/stdio.py                                |   252 +
 hermes_cli/tips.py                                 |     2 +-
 hermes_cli/tools_config.py                         |  1092 +-
 hermes_cli/uninstall.py                            |   221 +-
 hermes_cli/voice.py                                |   184 +-
 hermes_cli/web_server.py                           |   542 +-
 hermes_cli/webhook.py                              |     6 +-
 hermes_constants.py                                |     4 +-
 hermes_state.py                                    |   355 +-
 hermes_time.py                                     |     2 +-
 locales/af.yaml                                    |   350 +
 locales/de.yaml                                    |   326 +
 locales/en.yaml                                    |   330 +
 locales/es.yaml                                    |   326 +
 locales/fr.yaml                                    |   326 +
 locales/ga.yaml                                    |   354 +
 locales/hu.yaml                                    |   350 +
 locales/it.yaml                                    |   350 +
 locales/ja.yaml                                    |   326 +
 locales/ko.yaml                                    |   350 +
 locales/pt.yaml                                    |   350 +
 locales/ru.yaml                                    |   350 +
 locales/tr.yaml                                    |   326 +
 locales/uk.yaml                                    |   326 +
 locales/zh-hant.yaml                               |   350 +
 locales/zh.yaml                                    |   326 +
 mcp_serve.py                                       |    42 +-
 model_tools.py                                     |   102 +-
 nix/checks.nix                                     |    24 +-
 nix/hermes-agent.nix                               |     7 +-
 nix/nixosModules.nix                               |    29 +-
 nix/tui.nix                                        |    12 +-
 .../autonomous-ai-agents/blackbox/SKILL.md         |     1 +
 .../autonomous-ai-agents/honcho/SKILL.md           |     1 +
 optional-skills/blockchain/base/SKILL.md           |   231 -
 .../blockchain/base/scripts/base_client.py         |  1008 --
 optional-skills/blockchain/evm/SKILL.md            |   211 +
 .../blockchain/evm/scripts/evm_client.py           |  1508 +++
 optional-skills/blockchain/hyperliquid/SKILL.md    |   211 +
 .../hyperliquid/scripts/hyperliquid_client.py      |  1660 +++
 optional-skills/blockchain/solana/SKILL.md         |     1 +
 .../communication/one-three-one-rule/SKILL.md      |     1 +
 optional-skills/creative/blender-mcp/SKILL.md      |     1 +
 optional-skills/creative/concept-diagrams/SKILL.md |     1 +
 optional-skills/creative/hyperframes/SKILL.md      |     1 +
 .../creative/kanban-video-orchestrator/SKILL.md    |     1 +
 optional-skills/creative/meme-generation/SKILL.md  |     1 +
 .../meme-generation/scripts/generate_meme.py       |     4 +-
 optional-skills/devops/cli/SKILL.md                |     1 +
 optional-skills/devops/docker-management/SKILL.md  |     1 +
 optional-skills/devops/pinggy-tunnel/SKILL.md      |   309 +
 optional-skills/devops/watchers/SKILL.md           |   112 +
 .../devops/watchers/scripts/_watermark.py          |   148 +
 .../devops/watchers/scripts/watch_github.py        |   168 +
 .../devops/watchers/scripts/watch_http_json.py     |   131 +
 .../devops/watchers/scripts/watch_rss.py           |   121 +
 .../dogfood/adversarial-ux-test/SKILL.md           |     1 +
 optional-skills/email/agentmail/SKILL.md           |     1 +
 optional-skills/finance/3-statement-model/SKILL.md |   433 +
 .../3-statement-model/references/formatting.md     |   118 +
 .../3-statement-model/references/formulas.md       |   292 +
 .../3-statement-model/references/sec-filings.md    |   125 +
 optional-skills/finance/comps-analysis/SKILL.md    |   662 +
 optional-skills/finance/dcf-model/SKILL.md         |  1270 ++
 .../finance/dcf-model/TROUBLESHOOTING.md           |    40 +
 optional-skills/finance/dcf-model/requirements.txt |     7 +
 .../finance/dcf-model/scripts/validate_dcf.py      |   292 +
 optional-skills/finance/excel-author/SKILL.md      |   244 +
 .../finance/excel-author/scripts/recalc.py         |    88 +
 optional-skills/finance/lbo-model/SKILL.md         |   291 +
 optional-skills/finance/merger-model/SKILL.md      |   144 +
 optional-skills/finance/pptx-author/SKILL.md       |   173 +
 optional-skills/finance/stocks/SKILL.md            |    95 +
 .../finance/stocks/scripts/stocks_client.py        |   755 ++
 optional-skills/health/fitness-nutrition/SKILL.md  |     1 +
 .../health/fitness-nutrition/scripts/body_calc.py  |     6 +-
 optional-skills/health/neuroskill-bci/SKILL.md     |     1 +
 optional-skills/mcp/fastmcp/SKILL.md               |     1 +
 optional-skills/mcp/mcporter/SKILL.md              |     1 +
 .../migration/openclaw-migration/SKILL.md          |     1 +
 .../scripts/openclaw_to_hermes.py                  |    20 +-
 optional-skills/mlops/accelerate/SKILL.md          |     1 +
 optional-skills/mlops/chroma/SKILL.md              |     1 +
 optional-skills/mlops/clip/SKILL.md                |     1 +
 optional-skills/mlops/faiss/SKILL.md               |     1 +
 optional-skills/mlops/flash-attention/SKILL.md     |     1 +
 optional-skills/mlops/guidance/SKILL.md            |     1 +
 .../mlops/hermes-atropos-environments/SKILL.md     |   302 -
 .../references/agentresult-fields.md               |    59 -
 .../references/atropos-base-env.md                 |    65 -
 .../references/usage-patterns.md                   |   199 -
 .../mlops/huggingface-tokenizers/SKILL.md          |     1 +
 .../mlops/inference/outlines/SKILL.md              |     1 +
 .../inference/outlines/references/backends.md      |     0
 .../inference/outlines/references/examples.md      |     0
 .../outlines/references/json_generation.md         |     0
 optional-skills/mlops/instructor/SKILL.md          |     1 +
 optional-skills/mlops/lambda-labs/SKILL.md         |     1 +
 optional-skills/mlops/llava/SKILL.md               |     1 +
 optional-skills/mlops/modal/SKILL.md               |     1 +
 optional-skills/mlops/nemo-curator/SKILL.md        |     1 +
 optional-skills/mlops/peft/SKILL.md                |     1 +
 optional-skills/mlops/pinecone/SKILL.md            |     1 +
 optional-skills/mlops/pytorch-fsdp/SKILL.md        |     1 +
 optional-skills/mlops/pytorch-lightning/SKILL.md   |     1 +
 optional-skills/mlops/qdrant/SKILL.md              |     1 +
 optional-skills/mlops/saelens/SKILL.md             |     1 +
 optional-skills/mlops/simpo/SKILL.md               |     1 +
 optional-skills/mlops/slime/SKILL.md               |     1 +
 optional-skills/mlops/stable-diffusion/SKILL.md    |     1 +
 optional-skills/mlops/tensorrt-llm/SKILL.md        |     1 +
 optional-skills/mlops/torchtitan/SKILL.md          |     1 +
 .../mlops/training/axolotl/SKILL.md                |     1 +
 .../mlops/training/axolotl/references/api.md       |     0
 .../training/axolotl/references/dataset-formats.md |     0
 .../mlops/training/axolotl/references/index.md     |     0
 .../mlops/training/axolotl/references/other.md     |     0
 .../mlops/training/trl-fine-tuning/SKILL.md        |     1 +
 .../trl-fine-tuning/references/dpo-variants.md     |     0
 .../trl-fine-tuning/references/grpo-training.md    |     0
 .../trl-fine-tuning/references/online-rl.md        |     0
 .../trl-fine-tuning/references/reward-modeling.md  |     0
 .../trl-fine-tuning/references/sft-training.md     |     0
 .../templates/basic_grpo_training.py               |     0
 .../mlops/training/unsloth/SKILL.md                |     1 +
 .../mlops/training/unsloth/references/index.md     |     0
 .../mlops/training/unsloth/references/llms-full.md |     0
 .../mlops/training/unsloth/references/llms-txt.md  |     0
 .../mlops/training/unsloth/references/llms.md      |     0
 optional-skills/mlops/whisper/SKILL.md             |     1 +
 optional-skills/productivity/canvas/SKILL.md       |     1 +
 optional-skills/productivity/shop-app/SKILL.md     |   340 +
 optional-skills/productivity/shopify/SKILL.md      |     1 +
 optional-skills/productivity/siyuan/SKILL.md       |     1 +
 optional-skills/productivity/telephony/SKILL.md    |     1 +
 .../productivity/telephony/scripts/telephony.py    |     2 +-
 .../research/darwinian-evolver/SKILL.md            |   199 +
 .../darwinian-evolver/scripts/parrot_openrouter.py |   218 +
 .../darwinian-evolver/scripts/show_snapshot.py     |    69 +
 .../templates/custom_problem_template.py           |   240 +
 optional-skills/research/domain-intel/SKILL.md     |     1 +
 .../research/domain-intel/scripts/domain_intel.py  |     2 +-
 optional-skills/research/drug-discovery/SKILL.md   |     1 +
 .../research/duckduckgo-search/SKILL.md            |     1 +
 .../research/gitnexus-explorer/SKILL.md            |     1 +
 .../research/osint-investigation/SKILL.md          |   277 +
 .../references/sources/courtlistener.md            |    98 +
 .../references/sources/gdelt.md                    |   104 +
 .../references/sources/icij-offshore.md            |   104 +
 .../references/sources/nyc-acris.md                |    90 +
 .../references/sources/ofac-sdn.md                 |    92 +
 .../references/sources/opencorporates.md           |   103 +
 .../references/sources/sec-edgar.md                |    83 +
 .../references/sources/senate-ld.md                |    89 +
 .../references/sources/usaspending.md              |    97 +
 .../references/sources/wayback.md                  |    93 +
 .../references/sources/wikipedia.md                |   107 +
 .../research/osint-investigation/scripts/_http.py  |    82 +
 .../osint-investigation/scripts/_normalize.py      |    67 +
 .../osint-investigation/scripts/build_findings.py  |   221 +
 .../scripts/entity_resolution.py                   |   228 +
 .../scripts/fetch_courtlistener.py                 |   149 +
 .../osint-investigation/scripts/fetch_gdelt.py     |   162 +
 .../scripts/fetch_icij_offshore.py                 |   234 +
 .../osint-investigation/scripts/fetch_nyc_acris.py |   203 +
 .../osint-investigation/scripts/fetch_ofac_sdn.py  |   175 +
 .../scripts/fetch_opencorporates.py                |   192 +
 .../osint-investigation/scripts/fetch_sec_edgar.py |   184 +
 .../osint-investigation/scripts/fetch_senate_ld.py |   146 +
 .../scripts/fetch_usaspending.py                   |   170 +
 .../osint-investigation/scripts/fetch_wayback.py   |   142 +
 .../osint-investigation/scripts/fetch_wikipedia.py |   267 +
 .../osint-investigation/scripts/timing_analysis.py |   253 +
 .../templates/source-template.md                   |    59 +
 optional-skills/research/parallel-cli/SKILL.md     |     1 +
 optional-skills/research/scrapling/SKILL.md        |     1 +
 optional-skills/research/searxng-search/SKILL.md   |   212 +
 .../research/searxng-search/scripts/searxng.sh     |    22 +
 optional-skills/security/1password/SKILL.md        |     1 +
 optional-skills/security/oss-forensics/SKILL.md    |     1 +
 optional-skills/security/sherlock/SKILL.md         |     1 +
 .../rest-graphql-debug/SKILL.md                    |   514 +
 .../web-development/page-agent/SKILL.md            |     1 +
 package-lock.json                                  |  2630 ----
 package.json                                       |     1 -
 plugins/browser/browser_use/__init__.py            |    14 +
 plugins/browser/browser_use/plugin.yaml            |     7 +
 .../browser/browser_use/provider.py                |   137 +-
 plugins/browser/browserbase/__init__.py            |    15 +
 plugins/browser/browserbase/plugin.yaml            |     7 +
 .../browser/browserbase/provider.py                |   192 +-
 plugins/browser/firecrawl/__init__.py              |    16 +
 plugins/browser/firecrawl/plugin.yaml              |     7 +
 plugins/browser/firecrawl/provider.py              |   168 +
 plugins/context_engine/__init__.py                 |     2 +-
 plugins/disk-cleanup/__init__.py                   |     2 +-
 plugins/disk-cleanup/disk_cleanup.py               |     2 +-
 plugins/example-dashboard/dashboard/dist/index.js  |   119 -
 plugins/example-dashboard/dashboard/manifest.json  |     4 +-
 plugins/example-dashboard/dashboard/plugin_api.py  |     3 +
 plugins/google_meet/__init__.py                    |     2 +-
 plugins/google_meet/cli.py                         |     6 +-
 plugins/google_meet/meet_bot.py                    |     4 +-
 plugins/google_meet/node/cli.py                    |     2 +-
 plugins/google_meet/process_manager.py             |    15 +-
 plugins/google_meet/realtime/openai_client.py      |     4 +-
 plugins/google_meet/tools.py                       |     4 +-
 .../hermes-achievements/dashboard/dist/index.js    |   198 +-
 plugins/image_gen/xai/__init__.py                  |    58 +-
 plugins/kanban/dashboard/dist/index.js             |  1144 +-
 plugins/kanban/dashboard/dist/style.css            |   240 +-
 plugins/kanban/dashboard/plugin_api.py             |   115 +-
 plugins/memory/__init__.py                         |     4 +-
 plugins/memory/byterover/__init__.py               |     4 +-
 plugins/memory/hindsight/__init__.py               |    32 +-
 plugins/memory/holographic/__init__.py             |     6 +-
 plugins/memory/holographic/store.py                |     6 +-
 plugins/memory/honcho/__init__.py                  |     4 +-
 plugins/memory/honcho/cli.py                       |    30 +-
 plugins/memory/honcho/client.py                    |    25 +-
 plugins/memory/openviking/__init__.py              |   212 +-
 plugins/memory/supermemory/__init__.py             |     8 +-
 plugins/model-providers/deepseek/__init__.py       |    84 +-
 plugins/model-providers/gmi/__init__.py            |     5 +
 plugins/model-providers/kimi-coding/__init__.py    |     2 +-
 plugins/model-providers/nous/__init__.py           |     3 +-
 plugins/model-providers/novita/__init__.py         |    27 +
 plugins/model-providers/novita/plugin.yaml         |     5 +
 plugins/model-providers/openrouter/__init__.py     |    33 +-
 plugins/model-providers/xiaomi/__init__.py         |     1 +
 plugins/observability/langfuse/README.md           |    10 +-
 plugins/observability/langfuse/__init__.py         |   176 +-
 plugins/observability/langfuse/plugin.yaml         |     2 +-
 plugins/platforms/google_chat/__init__.py          |     3 +
 plugins/platforms/google_chat/adapter.py           |  3342 +++++
 plugins/platforms/google_chat/oauth.py             |   638 +
 plugins/platforms/google_chat/plugin.yaml          |    39 +
 plugins/platforms/irc/adapter.py                   |   297 +-
 plugins/platforms/irc/plugin.yaml                  |    47 +-
 plugins/platforms/line/__init__.py                 |     3 +
 plugins/platforms/line/adapter.py                  |  1638 +++
 plugins/platforms/line/plugin.yaml                 |    65 +
 plugins/platforms/simplex/__init__.py              |     3 +
 plugins/platforms/simplex/adapter.py               |   746 ++
 plugins/platforms/simplex/plugin.yaml              |    37 +
 plugins/platforms/teams/adapter.py                 |   498 +-
 plugins/platforms/teams/plugin.yaml                |    41 +-
 plugins/strike-freedom-cockpit/README.md           |    70 -
 .../strike-freedom-cockpit/dashboard/dist/index.js |   309 -
 .../strike-freedom-cockpit/dashboard/manifest.json |    14 -
 .../theme/strike-freedom.yaml                      |   126 -
 plugins/teams_pipeline/__init__.py                 |    23 +
 plugins/teams_pipeline/cli.py                      |   462 +
 plugins/teams_pipeline/meetings.py                 |   333 +
 plugins/teams_pipeline/models.py                   |   350 +
 plugins/teams_pipeline/pipeline.py                 |   691 ++
 plugins/teams_pipeline/plugin.yaml                 |     9 +
 plugins/teams_pipeline/runtime.py                  |   135 +
 plugins/teams_pipeline/store.py                    |   193 +
 plugins/teams_pipeline/subscriptions.py            |   249 +
 plugins/video_gen/fal/__init__.py                  |   523 +
 plugins/video_gen/fal/plugin.yaml                  |     7 +
 plugins/video_gen/xai/__init__.py                  |   441 +
 plugins/video_gen/xai/plugin.yaml                  |     7 +
 plugins/web/__init__.py                            |     7 +
 plugins/web/brave_free/__init__.py                 |    14 +
 plugins/web/brave_free/plugin.yaml                 |     7 +
 plugins/web/brave_free/provider.py                 |   137 +
 plugins/web/ddgs/__init__.py                       |    15 +
 plugins/web/ddgs/plugin.yaml                       |     7 +
 plugins/web/ddgs/provider.py                       |   104 +
 plugins/web/exa/__init__.py                        |    15 +
 plugins/web/exa/plugin.yaml                        |     7 +
 plugins/web/exa/provider.py                        |   212 +
 plugins/web/firecrawl/__init__.py                  |    28 +
 plugins/web/firecrawl/plugin.yaml                  |     7 +
 plugins/web/firecrawl/provider.py                  |   773 ++
 plugins/web/parallel/__init__.py                   |    16 +
 plugins/web/parallel/plugin.yaml                   |     7 +
 plugins/web/parallel/provider.py                   |   291 +
 plugins/web/searxng/__init__.py                    |    15 +
 plugins/web/searxng/plugin.yaml                    |     7 +
 plugins/web/searxng/provider.py                    |   140 +
 plugins/web/tavily/__init__.py                     |    15 +
 plugins/web/tavily/plugin.yaml                     |     7 +
 plugins/web/tavily/provider.py                     |   285 +
 providers/base.py                                  |    19 +
 pyproject.toml                                     |   263 +-
 rl_cli.py                                          |   446 -
 run_agent.py                                       | 12040 ++-----------------
 scripts/benchmark_browser_eval.py                  |   138 +
 scripts/build_model_catalog.py                     |     2 +-
 scripts/build_skills_index.py                      |     4 +-
 scripts/check-windows-footguns.py                  |   632 +
 scripts/contributor_audit.py                       |     4 +-
 scripts/discord-voice-doctor.py                    |     2 +-
 scripts/install.ps1                                |  1529 ++-
 scripts/install.sh                                 |   615 +-
 scripts/install_psutil_android.py                  |   117 +
 scripts/keystroke_diagnostic.py                    |    81 +
 scripts/lint_diff.py                               |   207 +
 scripts/profile-tui.py                             |    17 +-
 scripts/release.py                                 |   389 +-
 scripts/run_tests.sh                               |    27 +-
 scripts/setup_open_webui.sh                        |     4 +-
 scripts/tests/test-install-ps1-stage-protocol.ps1  |   134 +
 scripts/whatsapp-bridge/allowlist.js               |     6 +-
 scripts/whatsapp-bridge/allowlist.test.mjs         |    21 +
 scripts/whatsapp-bridge/bridge.js                  |   157 +-
 setup-hermes.sh                                    |   111 +-
 skills/apple/DESCRIPTION.md                        |     5 +-
 skills/apple/macos-computer-use/SKILL.md           |   201 +
 skills/autonomous-ai-agents/claude-code/SKILL.md   |     1 +
 skills/autonomous-ai-agents/codex/SKILL.md         |     1 +
 skills/autonomous-ai-agents/hermes-agent/SKILL.md  |   131 +-
 skills/autonomous-ai-agents/opencode/SKILL.md      |     1 +
 skills/creative/architecture-diagram/SKILL.md      |     1 +
 skills/creative/ascii-art/SKILL.md                 |     1 +
 skills/creative/ascii-video/SKILL.md               |     1 +
 skills/creative/baoyu-comic/SKILL.md               |     1 +
 skills/creative/baoyu-infographic/SKILL.md         |     1 +
 skills/creative/claude-design/SKILL.md             |     1 +
 skills/creative/comfyui/SKILL.md                   |    10 +-
 .../comfyui/references/template-integrity.md       |   243 +
 skills/creative/comfyui/scripts/_common.py         |    10 +-
 skills/creative/comfyui/scripts/extract_schema.py  |     6 +-
 skills/creative/comfyui/scripts/fetch_logs.py      |     2 +-
 skills/creative/comfyui/scripts/hardware_check.py  |     2 +-
 skills/creative/comfyui/scripts/run_workflow.py    |     6 +-
 skills/creative/comfyui/scripts/ws_monitor.py      |     2 +-
 .../comfyui/tests/test_cloud_integration.py        |     2 +-
 .../creative/comfyui/tests/test_extract_schema.py  |     2 +-
 skills/creative/creative-ideation/SKILL.md         |     1 +
 skills/creative/design-md/SKILL.md                 |     1 +
 skills/creative/excalidraw/SKILL.md                |     1 +
 skills/creative/humanizer/SKILL.md                 |     1 +
 skills/creative/manim-video/SKILL.md               |     1 +
 skills/creative/p5js/SKILL.md                      |     1 +
 skills/creative/pixel-art/SKILL.md                 |     1 +
 skills/creative/popular-web-designs/SKILL.md       |     1 +
 skills/creative/pretext/SKILL.md                   |     1 +
 skills/creative/sketch/SKILL.md                    |     1 +
 skills/creative/songwriting-and-ai-music/SKILL.md  |     1 +
 skills/creative/touchdesigner-mcp/SKILL.md         |     1 +
 skills/data-science/jupyter-live-kernel/SKILL.md   |     1 +
 skills/devops/kanban-orchestrator/SKILL.md         |   117 +-
 skills/devops/kanban-worker/SKILL.md               |    24 +
 skills/devops/webhook-subscriptions/SKILL.md       |     1 +
 skills/dogfood/SKILL.md                            |     1 +
 skills/email/himalaya/SKILL.md                     |     1 +
 skills/gaming/minecraft-modpack-server/SKILL.md    |     1 +
 skills/gaming/pokemon-player/SKILL.md              |     1 +
 skills/github/codebase-inspection/SKILL.md         |     1 +
 skills/github/github-auth/SKILL.md                 |     1 +
 skills/github/github-code-review/SKILL.md          |     1 +
 skills/github/github-issues/SKILL.md               |     1 +
 skills/github/github-pr-workflow/SKILL.md          |     1 +
 skills/github/github-repo-management/SKILL.md      |     1 +
 skills/mcp/native-mcp/SKILL.md                     |     1 +
 skills/media/gif-search/SKILL.md                   |     1 +
 skills/media/heartmula/SKILL.md                    |     1 +
 skills/media/songsee/SKILL.md                      |     1 +
 skills/media/spotify/SKILL.md                      |     1 +
 skills/media/youtube-content/SKILL.md              |     1 +
 .../evaluation/lm-evaluation-harness/SKILL.md      |     1 +
 .../mlops/evaluation/weights-and-biases/SKILL.md   |     1 +
 skills/mlops/huggingface-hub/SKILL.md              |     1 +
 skills/mlops/inference/llama-cpp/SKILL.md          |     1 +
 skills/mlops/inference/obliteratus/SKILL.md        |     1 +
 skills/mlops/inference/vllm/SKILL.md               |     1 +
 skills/mlops/models/audiocraft/SKILL.md            |     1 +
 skills/mlops/models/segment-anything/SKILL.md      |     1 +
 skills/mlops/research/dspy/SKILL.md                |     1 +
 skills/note-taking/obsidian/SKILL.md               |     1 +
 skills/productivity/airtable/SKILL.md              |     1 +
 skills/productivity/google-workspace/SKILL.md      |    55 +-
 .../google-workspace/scripts/google_api.py         |   363 +-
 .../productivity/google-workspace/scripts/setup.py |    57 +-
 skills/productivity/linear/SKILL.md                |    85 +-
 skills/productivity/linear/scripts/linear_api.py   |   445 +
 skills/productivity/maps/SKILL.md                  |     1 +
 skills/productivity/maps/scripts/maps_client.py    |    10 +-
 skills/productivity/nano-pdf/SKILL.md              |     1 +
 skills/productivity/notion/SKILL.md                |   355 +-
 skills/productivity/ocr-and-documents/SKILL.md     |     1 +
 .../ocr-and-documents/scripts/extract_marker.py    |     2 +-
 .../ocr-and-documents/scripts/extract_pymupdf.py   |     2 +-
 skills/productivity/powerpoint/SKILL.md            |     1 +
 .../productivity/teams-meeting-pipeline/SKILL.md   |   116 +
 skills/red-teaming/godmode/SKILL.md                |     1 +
 skills/research/arxiv/SKILL.md                     |     1 +
 skills/research/arxiv/scripts/search_arxiv.py      |     2 +-
 skills/research/blogwatcher/SKILL.md               |     1 +
 skills/research/llm-wiki/SKILL.md                  |     1 +
 skills/research/polymarket/SKILL.md                |     1 +
 skills/research/polymarket/scripts/polymarket.py   |     2 +-
 skills/smart-home/openhue/SKILL.md                 |     1 +
 .../debugging-hermes-tui-commands/SKILL.md         |     1 +
 .../hermes-agent-skill-authoring/SKILL.md          |     1 +
 .../node-inspect-debugger/SKILL.md                 |     1 +
 skills/software-development/plan/SKILL.md          |     1 +
 .../software-development/python-debugpy/SKILL.md   |     1 +
 .../requesting-code-review/SKILL.md                |     1 +
 skills/software-development/spike/SKILL.md         |     1 +
 .../subagent-driven-development/SKILL.md           |     1 +
 .../systematic-debugging/SKILL.md                  |     1 +
 .../test-driven-development/SKILL.md               |     1 +
 skills/software-development/writing-plans/SKILL.md |     1 +
 skills/yuanbao/SKILL.md                            |     1 +
 tests/acp/test_auth.py                             |    48 +-
 tests/acp/test_entry.py                            |   178 +-
 tests/acp/test_events.py                           |    97 +-
 tests/acp/test_permissions.py                      |   224 +-
 tests/acp/test_registry_manifest.py                |    90 +
 tests/acp/test_server.py                           |   396 +-
 tests/acp/test_tools.py                            |    10 +
 tests/acp_adapter/test_acp_commands.py             |    50 +-
 tests/acp_adapter/test_acp_images.py               |   125 +-
 tests/agent/lsp/__init__.py                        |     1 +
 tests/agent/lsp/_mock_lsp_server.py                |   159 +
 tests/agent/lsp/test_backend_gate.py               |   108 +
 tests/agent/lsp/test_broken_set.py                 |   213 +
 tests/agent/lsp/test_client_e2e.py                 |   143 +
 tests/agent/lsp/test_delta_key.py                  |   262 +
 tests/agent/lsp/test_diagnostics_field.py          |   146 +
 tests/agent/lsp/test_eventlog.py                   |   199 +
 tests/agent/lsp/test_install_and_lint_fixes.py     |   279 +
 tests/agent/lsp/test_lifecycle.py                  |   144 +
 tests/agent/lsp/test_protocol.py                   |   197 +
 tests/agent/lsp/test_reporter.py                   |    94 +
 tests/agent/lsp/test_service.py                    |   178 +
 tests/agent/lsp/test_workspace.py                  |   139 +
 tests/agent/test_anthropic_adapter.py              |    48 +-
 tests/agent/test_anthropic_oauth_pkce.py           |   170 +
 tests/agent/test_async_utils.py                    |   157 +
 tests/agent/test_auxiliary_client.py               |   738 ++
 tests/agent/test_auxiliary_config_bridge.py        |    14 +-
 tests/agent/test_auxiliary_main_first.py           |     2 +-
 tests/agent/test_bedrock_1m_context.py             |    41 -
 tests/agent/test_bedrock_adapter.py                |    21 +-
 tests/agent/test_bedrock_integration.py            |    24 +-
 tests/agent/test_compressor_historical_media.py    |   266 +
 tests/agent/test_context_compressor.py             |   356 +-
 .../test_context_compressor_summary_continuity.py  |     2 +
 tests/agent/test_copilot_acp_deprecation.py        |    77 +
 tests/agent/test_credential_pool.py                |    73 +
 tests/agent/test_curator_classification.py         |   237 +
 tests/agent/test_deepseek_anthropic_thinking.py    |     2 +-
 tests/agent/test_display.py                        |    70 +
 tests/agent/test_error_classifier.py               |    22 +
 tests/agent/test_external_skills_dirs_cache.py     |   149 +
 tests/agent/test_gemini_cloudcode.py               |    29 +
 tests/agent/test_i18n.py                           |     7 +-
 tests/agent/test_image_routing.py                  |    85 +-
 tests/agent/test_markdown_tables.py                |   312 +
 tests/agent/test_model_metadata.py                 |   294 +-
 tests/agent/test_models_dev.py                     |   112 +-
 tests/agent/test_moonshot_schema.py                |   163 +
 tests/agent/test_plugin_llm.py                     |   991 ++
 tests/agent/test_portal_tags.py                    |    61 +
 tests/agent/test_prompt_builder.py                 |   103 +-
 tests/agent/test_shell_hooks.py                    |    24 +
 tests/agent/test_skill_commands.py                 |   139 +
 tests/agent/test_tool_guardrails.py                |    16 +
 tests/agent/test_tool_result_classification.py     |    30 +
 tests/agent/test_unsupported_parameter_retry.py    |    59 -
 tests/agent/test_usage_pricing.py                  |    34 +
 tests/agent/test_video_gen_registry.py             |   114 +
 tests/agent/transports/test_bedrock_transport.py   |    18 +
 tests/agent/transports/test_chat_completions.py    |    66 +-
 .../transports/test_codex_app_server_runtime.py    |   243 +
 .../transports/test_codex_app_server_session.py    |  1024 ++
 .../agent/transports/test_codex_event_projector.py |   303 +
 tests/agent/transports/test_codex_transport.py     |   191 +
 .../transports/test_hermes_tools_mcp_server.py     |   135 +
 tests/cli/test_cli_approval_ui.py                  |     1 +
 tests/cli/test_cli_background_status_indicator.py  |   104 +
 tests/cli/test_cli_file_drop.py                    |    31 +
 tests/cli/test_cli_force_redraw.py                 |   122 +-
 tests/cli/test_cli_goal_interrupt.py               |   221 +
 tests/cli/test_cli_init.py                         |   147 +-
 tests/cli/test_cli_insights_command.py             |    43 +
 tests/cli/test_cli_light_mode.py                   |   154 +
 tests/cli/test_cli_markdown_rendering.py           |    31 +-
 tests/cli/test_cli_new_session.py                  |     5 +
 tests/cli/test_cli_provider_resolution.py          |    61 +-
 tests/cli/test_cli_save_config_value.py            |    62 +-
 tests/cli/test_cli_shift_enter_newline.py          |    88 +
 tests/cli/test_cli_status_bar.py                   |   170 +
 tests/cli/test_cprint_bg_thread.py                 |   102 +
 tests/cli/test_ctrl_enter_newline.py               |   105 +
 tests/cli/test_destructive_slash_confirm.py        |   211 +
 tests/cli/test_exit_delete_session.py              |   119 +
 tests/cli/test_prompt_text_input_thread_safety.py  |   101 +
 tests/cli/test_quick_commands.py                   |    41 +
 tests/cli/test_reasoning_command.py                |     8 +-
 tests/cli/test_resume_display.py                   |    16 +
 tests/conftest.py                                  |   424 +-
 tests/cron/test_cron_no_agent.py                   |     4 +-
 tests/cron/test_cron_prompt_injection_skill.py     |   236 +
 tests/cron/test_cron_script.py                     |    13 -
 tests/cron/test_jobs.py                            |   107 +
 tests/cron/test_scheduler.py                       |    94 +
 tests/cron/test_scheduler_mcp_init.py              |    54 +
 tests/e2e/conftest.py                              |     6 +
 .../benchmarks/test_terminalbench2_env_security.py |   164 -
 tests/gateway/conftest.py                          |    10 +-
 tests/gateway/restart_test_helpers.py              |     9 +
 tests/gateway/test_active_session_text_merge.py    |   152 +
 tests/gateway/test_agent_cache.py                  |    61 +-
 tests/gateway/test_allowed_channels_widening.py    |   364 +
 tests/gateway/test_allowlist_startup_check.py      |     4 +-
 tests/gateway/test_api_server.py                   |   563 +-
 tests/gateway/test_api_server_runs.py              |    52 +
 tests/gateway/test_background_command.py           |    83 +
 .../test_background_process_notifications.py       |    34 +
 tests/gateway/test_base_topic_sessions.py          |     4 +-
 tests/gateway/test_bluebubbles.py                  |     5 +
 tests/gateway/test_config.py                       |    74 +-
 tests/gateway/test_config_cwd_bridge.py            |     4 +-
 tests/gateway/test_destructive_slash_confirm.py    |   261 +
 tests/gateway/test_dingtalk.py                     |   122 +-
 tests/gateway/test_discord_clarify_buttons.py      |   408 +
 tests/gateway/test_discord_connect.py              |   187 +
 tests/gateway/test_discord_document_handling.py    |   145 +
 tests/gateway/test_discord_free_response.py        |   410 +-
 tests/gateway/test_discord_roles_dm_scope.py       |   355 +
 tests/gateway/test_discord_send.py                 |    59 +
 tests/gateway/test_discord_slash_auth.py           |     6 +-
 tests/gateway/test_discord_system_messages.py      |     2 +-
 tests/gateway/test_display_config.py               |    75 +-
 tests/gateway/test_dm_topics.py                    |    41 +-
 tests/gateway/test_duplicate_reply_suppression.py  |    56 +
 tests/gateway/test_email.py                        |    75 +
 tests/gateway/test_feishu.py                       |    39 +
 tests/gateway/test_feishu_approval_buttons.py      |   258 +
 tests/gateway/test_feishu_bot_admission.py         |    31 +-
 tests/gateway/test_feishu_onboard.py               |    29 +-
 tests/gateway/test_goal_max_turns_config.py        |    62 +
 tests/gateway/test_goal_status_notice.py           |   147 +
 tests/gateway/test_goal_verdict_send.py            |    26 +-
 tests/gateway/test_google_chat.py                  |  2868 +++++
 tests/gateway/test_irc_adapter.py                  |   222 +
 tests/gateway/test_kanban_notifier.py              |   236 +
 tests/gateway/test_line_plugin.py                  |   644 +
 tests/gateway/test_matrix.py                       |   265 +-
 tests/gateway/test_memory_monitor.py               |   122 +
 tests/gateway/test_msgraph_webhook.py              |   430 +
 tests/gateway/test_pairing.py                      |    36 +
 tests/gateway/test_platform_base.py                |    31 +
 tests/gateway/test_platform_connected_checkers.py  |     7 +-
 tests/gateway/test_platform_reconnect.py           |   228 +-
 tests/gateway/test_platform_registry.py            |   314 +
 .../test_post_delivery_callback_chaining.py        |   113 +
 tests/gateway/test_qqbot.py                        |  1184 ++
 tests/gateway/test_replay_entry_fields.py          |   254 +
 tests/gateway/test_restart_drain.py                |    46 +-
 tests/gateway/test_restart_notification.py         |    96 +
 tests/gateway/test_restart_resume_pending.py       |   228 +-
 tests/gateway/test_run_cleanup_progress.py         |   367 +
 tests/gateway/test_run_progress_topics.py          |    44 +
 tests/gateway/test_runner_fatal_adapter.py         |    12 +-
 tests/gateway/test_runner_startup_failures.py      |    58 +-
 .../test_runtime_env_reload_config_authority.py    |    53 +
 tests/gateway/test_safe_adapter_disconnect.py      |    20 +
 tests/gateway/test_session.py                      |    71 +
 tests/gateway/test_session_boundary_hooks.py       |     2 +-
 .../test_session_boundary_security_state.py        |    15 +
 .../gateway/test_session_model_override_routing.py |    55 +
 tests/gateway/test_session_reset_notify.py         |    75 +
 tests/gateway/test_shutdown_forensics.py           |   250 +
 tests/gateway/test_signal.py                       |   159 +
 tests/gateway/test_simplex_plugin.py               |   347 +
 tests/gateway/test_slack.py                        |    88 +
 tests/gateway/test_slack_mention.py                |   139 +-
 tests/gateway/test_slash_access.py                 |   289 +
 tests/gateway/test_slash_access_dispatch.py        |   558 +
 tests/gateway/test_status.py                       |   164 +-
 tests/gateway/test_stream_consumer.py              |   288 +
 tests/gateway/test_stream_consumer_draft.py        |   318 +
 .../gateway/test_stream_consumer_thread_routing.py |   229 +
 tests/gateway/test_teams.py                        |   320 +-
 .../gateway/test_teams_pipeline_runtime_wiring.py  |   197 +
 tests/gateway/test_telegram_approval_buttons.py    |   101 +-
 tests/gateway/test_telegram_clarify_buttons.py     |   451 +
 tests/gateway/test_telegram_documents.py           |    37 +
 tests/gateway/test_telegram_format.py              |   198 +
 tests/gateway/test_telegram_group_gating.py        |    59 +
 tests/gateway/test_telegram_model_picker.py        |   179 +
 tests/gateway/test_telegram_reactions.py           |    49 +-
 tests/gateway/test_telegram_reply_quote.py         |   144 +
 tests/gateway/test_telegram_text_batch_perf.py     |   133 +
 tests/gateway/test_telegram_thread_fallback.py     |   726 +-
 tests/gateway/test_telegram_topic_mode.py          |    71 +-
 tests/gateway/test_transcript_offset.py            |    61 +-
 tests/gateway/test_tts_media_routing.py            |    18 +-
 tests/gateway/test_update_streaming.py             |    10 +
 tests/gateway/test_verbose_command.py              |    14 +-
 tests/gateway/test_voice_command.py                |    31 +
 tests/gateway/test_webhook_adapter.py              |    79 +-
 tests/gateway/test_webhook_deliver_only.py         |     2 +-
 tests/gateway/test_wecom.py                        |    44 +-
 tests/gateway/test_weixin.py                       |    57 +-
 tests/gateway/test_whatsapp_connect.py             |    90 +
 tests/gateway/test_whatsapp_formatting.py          |    72 +
 tests/gateway/test_whatsapp_group_gating.py        |    75 +
 tests/hermes_cli/test_api_key_providers.py         |   153 +
 tests/hermes_cli/test_apply_profile_override.py    |   141 +
 tests/hermes_cli/test_auth_commands.py             |    44 +
 tests/hermes_cli/test_auth_loopback_ssh_hint.py    |    95 +
 tests/hermes_cli/test_auth_nous_provider.py        |   127 +-
 tests/hermes_cli/test_auth_profile_fallback.py     |   360 +
 tests/hermes_cli/test_auth_toctou_file_modes.py    |   202 +
 tests/hermes_cli/test_auth_xai_oauth_provider.py   |  1605 +++
 tests/hermes_cli/test_banner_pip_update.py         |    35 +
 tests/hermes_cli/test_bedrock_model_picker.py      |    19 +-
 tests/hermes_cli/test_cmd_update.py                |    99 +-
 tests/hermes_cli/test_codex_cli_model_picker.py    |    31 +
 tests/hermes_cli/test_codex_models.py              |    54 +-
 .../test_codex_runtime_plugin_migration.py         |   865 ++
 tests/hermes_cli/test_codex_runtime_switch.py      |   238 +
 tests/hermes_cli/test_commands.py                  |    19 +-
 tests/hermes_cli/test_completion.py                |    48 +
 tests/hermes_cli/test_config.py                    |    75 +
 tests/hermes_cli/test_curator_recent_run_notice.py |   162 +
 tests/hermes_cli/test_curator_run.py               |    87 +
 tests/hermes_cli/test_curator_status.py            |    25 +
 .../test_dashboard_profiles_nav_label.py           |     7 +-
 tests/hermes_cli/test_debug.py                     |    25 +-
 tests/hermes_cli/test_dep_ensure.py                |    43 +
 .../test_destructive_slash_confirm_gate.py         |    86 +
 tests/hermes_cli/test_doctor.py                    |   401 +
 .../test_doctor_dedicated_provider_skip.py         |    50 +
 tests/hermes_cli/test_env_load_cache.py            |   193 +
 tests/hermes_cli/test_gateway.py                   |   139 +-
 tests/hermes_cli/test_gateway_platform_gating.py   |    61 +
 tests/hermes_cli/test_gateway_proc_fallback.py     |   138 +
 tests/hermes_cli/test_gateway_service.py           |   450 +-
 tests/hermes_cli/test_gateway_service_paths.py     |    31 +
 tests/hermes_cli/test_gmi_provider.py              |    16 +
 tests/hermes_cli/test_goals.py                     |   416 +-
 tests/hermes_cli/test_image_gen_picker.py          |    27 +
 tests/hermes_cli/test_install_cua_driver.py        |   115 +
 tests/hermes_cli/test_inventory.py                 |   378 +
 tests/hermes_cli/test_kanban_cli.py                |   116 +
 tests/hermes_cli/test_kanban_core_functionality.py |   724 +-
 tests/hermes_cli/test_kanban_db.py                 |   637 +-
 tests/hermes_cli/test_kanban_diagnostics.py        |   184 +-
 tests/hermes_cli/test_kanban_notify.py             |   481 +
 tests/hermes_cli/test_kanban_specify.py            |   337 +
 tests/hermes_cli/test_kanban_specify_db.py         |   184 +
 tests/hermes_cli/test_list_picker_providers.py     |    49 +-
 tests/hermes_cli/test_managed_installs.py          |     3 +-
 tests/hermes_cli/test_mcp_add_command_dest.py      |    87 +
 tests/hermes_cli/test_mcp_config.py                |    10 +-
 tests/hermes_cli/test_memory_reset.py              |     4 +-
 tests/hermes_cli/test_model_catalog.py             |   101 +
 .../hermes_cli/test_model_provider_persistence.py  |    89 +-
 .../test_model_switch_custom_providers.py          |    61 +
 tests/hermes_cli/test_model_validation.py          |     9 -
 tests/hermes_cli/test_models.py                    |   269 +-
 tests/hermes_cli/test_nous_auth_status_cache.py    |   144 +
 .../test_openai_codex_model_validation_fallback.py |    15 +-
 .../hermes_cli/test_opencode_go_flat_namespace.py  |   159 +
 tests/hermes_cli/test_opencode_go_in_model_list.py |     2 +-
 tests/hermes_cli/test_pip_install_detection.py     |    37 +
 tests/hermes_cli/test_plugins.py                   |   287 +
 tests/hermes_cli/test_plugins_cmd.py               |   176 +
 tests/hermes_cli/test_post_setup_gating.py         |    71 +
 tests/hermes_cli/test_profile_distribution.py      |   584 +
 tests/hermes_cli/test_profiles.py                  |   207 +-
 tests/hermes_cli/test_proxy.py                     |   512 +
 tests/hermes_cli/test_redact_config_bridge.py      |    12 +-
 tests/hermes_cli/test_relaunch.py                  |   133 +-
 .../hermes_cli/test_runtime_provider_resolution.py |    36 +
 tests/hermes_cli/test_security_advisories.py       |   330 +
 tests/hermes_cli/test_send_cmd.py                  |   400 +
 tests/hermes_cli/test_session_handoff.py           |   202 +
 tests/hermes_cli/test_session_recap.py             |   180 +
 tests/hermes_cli/test_set_config_value.py          |     2 -
 tests/hermes_cli/test_setup.py                     |    42 -
 tests/hermes_cli/test_setup_hermes_script.py       |     1 -
 tests/hermes_cli/test_setup_openclaw_migration.py  |     3 -
 tests/hermes_cli/test_setup_reconfigure.py         |     1 -
 tests/hermes_cli/test_skin_engine.py               |    31 +
 tests/hermes_cli/test_slack_cli.py                 |    30 +
 tests/hermes_cli/test_spotify_auth.py              |    45 +
 tests/hermes_cli/test_startup_plugin_gating.py     |   180 +
 tests/hermes_cli/test_status.py                    |   223 +
 tests/hermes_cli/test_suppress_eio_on_interrupt.py |   120 +
 tests/hermes_cli/test_teams_pipeline_plugin_cli.py |   214 +
 tests/hermes_cli/test_tencent_tokenhub_provider.py |    25 +-
 tests/hermes_cli/test_tools_config.py              |   147 +
 tests/hermes_cli/test_tui_bundled.py               |    21 +
 tests/hermes_cli/test_tui_npm_install.py           |    20 +-
 tests/hermes_cli/test_tui_resume_flow.py           |    94 +
 tests/hermes_cli/test_update_autostash.py          |    73 +-
 tests/hermes_cli/test_update_check.py              |     7 +-
 tests/hermes_cli/test_update_gateway_restart.py    |   360 +-
 tests/hermes_cli/test_update_stale_dashboard.py    |     2 +-
 tests/hermes_cli/test_update_yes_flag.py           |    54 +-
 tests/hermes_cli/test_video_gen_picker.py          |   237 +
 tests/hermes_cli/test_voice_wrapper.py             |   219 +-
 tests/hermes_cli/test_web_oauth_dispatch.py        |   178 +
 tests/hermes_cli/test_web_server.py                |   121 +-
 tests/hermes_cli/test_web_ui_build.py              |    91 +-
 tests/hermes_cli/test_whatsapp_setup_ordering.py   |   140 +
 tests/honcho_plugin/test_client.py                 |    49 +-
 tests/honcho_plugin/test_session.py                |     2 +-
 .../tblite => tests/plugins/browser}/__init__.py   |     0
 tests/plugins/browser/check_parity_vs_main.py      |   273 +
 .../browser/test_browser_provider_plugins.py       |   379 +
 tests/plugins/image_gen/test_xai_provider.py       |    31 +-
 tests/plugins/memory/test_openviking_provider.py   |   362 +-
 .../model_providers/test_deepseek_profile.py       |   207 +
 tests/plugins/test_achievements_plugin.py          |     2 +-
 tests/plugins/test_kanban_dashboard_plugin.py      |   310 +
 tests/plugins/test_langfuse_plugin.py              |   538 +-
 tests/plugins/test_teams_pipeline_plugin.py        |   468 +
 tests/plugins/video_gen/__init__.py                |     1 +
 tests/plugins/video_gen/test_fal_plugin.py         |   314 +
 tests/plugins/video_gen/test_xai_plugin.py         |   113 +
 .../video_gen/test_xai_plugin_integration.py       |   191 +
 .../plugins/web}/__init__.py                       |     0
 .../web/test_web_search_provider_plugins.py        |   475 +
 tests/providers/test_plugin_discovery.py           |     6 +-
 tests/providers/test_profile_wiring.py             |     3 +-
 tests/providers/test_provider_profiles.py          |    93 +-
 tests/providers/test_transport_parity.py           |     3 +-
 tests/run_agent/test_413_compression.py            |    26 +
 tests/run_agent/test_agent_loop.py                 |   505 -
 tests/run_agent/test_agent_loop_tool_calling.py    |   552 -
 tests/run_agent/test_agent_loop_vllm.py            |   359 -
 .../test_anthropic_prompt_cache_policy.py          |    40 +
 .../test_anthropic_truncation_continuation.py      |     6 +-
 tests/run_agent/test_async_httpx_del_neuter.py     |     2 +-
 tests/run_agent/test_background_review.py          |    51 +
 .../test_background_review_cache_parity.py         |   185 +
 .../test_background_review_toolset_restriction.py  |    96 +-
 .../run_agent/test_codex_app_server_integration.py |   418 +
 .../run_agent/test_codex_multimodal_tool_result.py |   173 +
 tests/run_agent/test_codex_xai_oauth_recovery.py   |   544 +
 .../test_commit_memory_session_context_engine.py   |   102 +
 tests/run_agent/test_compression_feasibility.py    |    14 +
 tests/run_agent/test_concurrent_interrupt.py       |   118 -
 .../test_empty_response_recovery_persistence.py    |    98 +
 tests/run_agent/test_fallback_model.py             |   104 +
 tests/run_agent/test_file_mutation_verifier.py     |   358 +
 tests/run_agent/test_image_rejection_fallback.py   |   267 +
 tests/run_agent/test_jsondecodeerror_retryable.py  |    13 +-
 .../run_agent/test_materialize_data_url_cleanup.py |    54 +
 .../test_memory_nudge_counter_hydration.py         |   141 +
 tests/run_agent/test_message_sequence_repair.py    |   201 +
 tests/run_agent/test_primary_runtime_restore.py    |    20 +
 .../run_agent/test_provider_attribution_headers.py |    93 +
 tests/run_agent/test_provider_fallback.py          |    85 +
 tests/run_agent/test_provider_parity.py            |     8 +-
 tests/run_agent/test_review_prompt_class_first.py  |    44 +
 tests/run_agent/test_run_agent.py                  |   366 +-
 tests/run_agent/test_run_agent_codex_responses.py  |   205 +-
 tests/run_agent/test_session_id_env.py             |    61 +
 tests/run_agent/test_stream_drop_logging.py        |   247 +
 tests/run_agent/test_streaming.py                  |   223 +
 tests/run_agent/test_streaming_tool_call_repair.py |     2 +-
 tests/run_agent/test_switch_model_context.py       |    15 +-
 tests/run_agent/test_token_persistence_non_cli.py  |    34 +-
 .../test_tool_executor_contextvar_propagation.py   |    31 +-
 tests/scripts/test_release_acp_registry.py         |   113 +
 tests/skills/test_darwinian_evolver_skill.py       |   102 +
 tests/skills/test_fetch_transcript.py              |    87 +
 tests/skills/test_hyperliquid_skill.py             |   358 +
 tests/skills/test_openclaw_migration.py            |     2 +-
 tests/stress/test_atypical_scenarios.py            |     8 +-
 tests/stress/test_concurrency_parent_gate.py       |   183 +
 tests/test_gateway_streaming_nested_config.py      |    46 +
 tests/test_hermes_bootstrap.py                     |   314 +
 tests/test_hermes_constants.py                     |    62 +-
 tests/test_hermes_state.py                         |    33 +
 tests/test_hermes_state_wal_fallback.py            |   305 +
 tests/test_install_sh_browser_install.py           |    60 +
 tests/test_install_sh_pythonpath_sanitization.py   |    30 +
 tests/test_install_sh_symlink_stomp.py             |   123 +
 tests/test_install_sh_termux_network_prereqs.py    |    22 +
 tests/test_lint_config.py                          |   115 +
 tests/test_live_system_guard_self_test.py          |   295 +
 tests/test_mcp_serve.py                            |   146 +-
 tests/test_minimax_oauth.py                        |    74 +
 tests/test_model_tools.py                          |     2 +-
 tests/test_package_json_lazy_deps.py               |    85 +
 tests/test_process_loop_event_loop_warning.py      |   131 +
 tests/test_project_metadata.py                     |    75 +-
 tests/test_sanitize_tool_error.py                  |   137 +
 tests/test_termux_all_extra_compat.py              |    23 +
 tests/test_timezone.py                             |     2 +-
 tests/test_toolsets.py                             |     8 +
 tests/test_transform_llm_output_hook.py            |   159 +
 tests/test_tui_gateway_server.py                   |   370 +-
 tests/tools/test_approval.py                       |   340 +
 tests/tools/test_approval_heartbeat.py             |   146 -
 tests/tools/test_approval_plugin_hooks.py          |   103 -
 tests/tools/test_browser_camofox_persistence.py    |   112 +
 tests/tools/test_browser_camofox_state.py          |     5 +-
 tests/tools/test_browser_chromium_check.py         |    78 +-
 tests/tools/test_browser_cloud_provider_cache.py   |   125 +
 tests/tools/test_browser_eval_supervisor_path.py   |   363 +
 tests/tools/test_browser_homebrew_paths.py         |    22 +-
 tests/tools/test_browser_lightpanda.py             |   636 +
 tests/tools/test_browser_orphan_reaper.py          |    81 +-
 tests/tools/test_browser_ssrf_local.py             |    82 +
 tests/tools/test_browser_supervisor.py             |    77 +
 tests/tools/test_checkpoint_manager.py             |   906 +-
 tests/tools/test_clarify_gateway.py                |   227 +
 tests/tools/test_clipboard.py                      |    47 +-
 tests/tools/test_code_execution.py                 |    10 +-
 tests/tools/test_code_execution_modes.py           |    34 +-
 tests/tools/test_code_execution_windows_env.py     |   698 ++
 tests/tools/test_command_guards.py                 |    43 -
 tests/tools/test_computer_use.py                   |   681 ++
 tests/tools/test_credential_pool_env_fallback.py   |    13 -
 tests/tools/test_cron_approval_mode.py             |    74 +
 tests/tools/test_cronjob_tools.py                  |    68 +
 tests/tools/test_daytona_environment.py            |    26 +-
 tests/tools/test_delegate.py                       |   372 +-
 tests/tools/test_delegate_composite_toolsets.py    |    46 +
 tests/tools/test_discord_tool.py                   |    23 +-
 tests/tools/test_dockerfile_node_modules_perms.py  |    39 +
 tests/tools/test_dockerfile_pid1_reaping.py        |    30 +-
 tests/tools/test_file_sync_back.py                 |     3 +-
 tests/tools/test_file_tools.py                     |    24 +
 tests/tools/test_hardline_blocklist.py             |    88 +
 tests/tools/test_hidden_dir_filter.py              |     2 +-
 tests/tools/test_image_generation_env.py           |    59 +
 tests/tools/test_kanban_tools.py                   |   495 +-
 tests/tools/test_lazy_deps.py                      |   407 +
 tests/tools/test_local_env_windows_msys.py         |   200 +
 tests/tools/test_managed_browserbase_and_modal.py  |   103 +-
 tests/tools/test_managed_modal_environment.py      |     2 +-
 tests/tools/test_managed_server_tool_support.py    |   178 -
 .../tools/test_mcp_cancelled_error_propagation.py  |    92 +
 tests/tools/test_mcp_empty_error_message.py        |    89 +
 tests/tools/test_mcp_image_content.py              |   138 +
 tests/tools/test_mcp_invalid_url.py                |   125 +
 tests/tools/test_mcp_oauth.py                      |    94 +
 tests/tools/test_mcp_oauth_metadata.py             |   213 +
 tests/tools/test_mcp_probe.py                      |    12 +-
 tests/tools/test_mcp_sse_transport.py              |   209 +
 tests/tools/test_mcp_stability.py                  |     9 +-
 tests/tools/test_mcp_structured_content.py         |     3 +-
 tests/tools/test_mcp_tool.py                       |   356 +-
 tests/tools/test_mcp_tool_session_expired.py       |    11 +
 tests/tools/test_mcp_utility_capability_gating.py  |   175 +
 tests/tools/test_memory_tool_schema.py             |    49 +
 tests/tools/test_microsoft_graph_auth.py           |   179 +
 tests/tools/test_microsoft_graph_client.py         |   257 +
 tests/tools/test_process_registry.py               |   249 +-
 tests/tools/test_registry.py                       |    45 +-
 tests/tools/test_rl_training_tool.py               |   142 -
 tests/tools/test_schema_sanitizer.py               |    58 +
 tests/tools/test_send_message_tool.py              |   438 +-
 tests/tools/test_session_search.py                 |    22 +-
 tests/tools/test_singularity_preflight.py          |     2 +-
 tests/tools/test_skill_manager_tool.py             |     2 +-
 tests/tools/test_skill_provenance.py               |     6 -
 tests/tools/test_skill_usage.py                    |    33 +
 tests/tools/test_skills_hub.py                     |    37 +-
 tests/tools/test_skills_hub_clawhub.py             |    45 +-
 tests/tools/test_skills_tool.py                    |   165 +
 tests/tools/test_terminal_config_env_sync.py       |    16 +
 tests/tools/test_terminal_task_cwd.py              |    74 +
 tests/tools/test_tirith_security.py                |   214 +
 tests/tools/test_tool_call_parsers.py              |   274 -
 tests/tools/test_tool_result_storage.py            |    27 +-
 tests/tools/test_transcription.py                  |    11 +-
 tests/tools/test_transcription_dotenv_fallback.py  |    21 +-
 tests/tools/test_transcription_tools.py            |    77 +-
 tests/tools/test_tts_dotenv_fallback.py            |     7 +-
 tests/tools/test_tts_kittentts.py                  |     3 +-
 tests/tools/test_tts_mistral.py                    |    23 +-
 tests/tools/test_tts_speed.py                      |   120 +-
 tests/tools/test_url_safety.py                     |    75 +
 tests/tools/test_vercel_sandbox_environment.py     |    17 -
 tests/tools/test_video_generation_dispatch.py      |   126 +
 .../tools/test_video_generation_dynamic_schema.py  |   153 +
 .../test_video_generation_tool_surface_matrix.py   |   253 +
 tests/tools/test_vision_native_fast_path.py        |   213 +
 tests/tools/test_web_providers.py                  |   334 +
 tests/tools/test_web_providers_brave_free.py       |   275 +
 tests/tools/test_web_providers_ddgs.py             |   246 +
 tests/tools/test_web_providers_searxng.py          |   337 +
 tests/tools/test_web_tools_config.py               |    37 +-
 tests/tools/test_website_policy.py                 |    42 +-
 tests/tools/test_windows_native_support.py         |   873 ++
 tests/tools/test_x_search_tool.py                  |   438 +
 tests/tui_gateway/test_entry_sys_path.py           |    10 +-
 tinker-atropos                                     |     1 -
 tools/approval.py                                  |   182 +-
 tools/browser_camofox.py                           |   114 +-
 tools/browser_cdp_tool.py                          |    16 +-
 tools/browser_providers/__init__.py                |    10 -
 tools/browser_providers/base.py                    |    59 -
 tools/browser_providers/firecrawl.py               |   107 -
 tools/browser_supervisor.py                        |   109 +-
 tools/browser_tool.py                              |  1298 +-
 tools/budget_config.py                             |     1 -
 tools/checkpoint_manager.py                        |  1278 +-
 tools/clarify_gateway.py                           |   278 +
 tools/code_execution_tool.py                       |   276 +-
 tools/computer_use/__init__.py                     |    43 +
 tools/computer_use/backend.py                      |   150 +
 tools/computer_use/cua_backend.py                  |   682 ++
 tools/computer_use/schema.py                       |   191 +
 tools/computer_use/tool.py                         |   521 +
 tools/computer_use_tool.py                         |    39 +
 tools/credential_files.py                          |    28 +
 tools/cronjob_tools.py                             |    92 +-
 tools/delegate_tool.py                             |   321 +-
 tools/discord_tool.py                              |    12 +
 tools/environments/base.py                         |    87 +-
 tools/environments/daytona.py                      |    21 +-
 tools/environments/docker.py                       |    11 +
 tools/environments/file_sync.py                    |     2 +-
 tools/environments/local.py                        |   160 +-
 tools/environments/modal.py                        |    20 +-
 tools/environments/vercel_sandbox.py               |    20 +-
 tools/feishu_doc_tool.py                           |    13 +-
 tools/feishu_drive_tool.py                         |     8 +-
 tools/file_operations.py                           |   330 +-
 tools/file_tools.py                                |    49 +-
 tools/fuzzy_match.py                               |     3 +-
 tools/image_generation_tool.py                     |   112 +-
 tools/kanban_tools.py                              |   332 +-
 tools/lazy_deps.py                                 |   608 +
 tools/mcp_oauth.py                                 |    86 +-
 tools/mcp_oauth_manager.py                         |    51 +
 tools/mcp_tool.py                                  |   510 +-
 tools/memory_tool.py                               |    11 +-
 tools/microsoft_graph_auth.py                      |   245 +
 tools/microsoft_graph_client.py                    |   408 +
 tools/mixture_of_agents_tool.py                    |     3 +-
 tools/osv_check.py                                 |     4 +-
 tools/patch_parser.py                              |     4 +-
 tools/process_registry.py                          |   151 +-
 tools/registry.py                                  |    64 +-
 tools/rl_training_tool.py                          |  1396 ---
 tools/schema_sanitizer.py                          |    41 +
 tools/send_message_tool.py                         |   194 +-
 tools/session_search_tool.py                       |     9 +-
 tools/skill_manager_tool.py                        |     6 +-
 tools/skill_usage.py                               |    82 +-
 tools/skills_guard.py                              |     6 +-
 tools/skills_hub.py                                |    89 +-
 tools/skills_sync.py                               |     2 +-
 tools/skills_tool.py                               |   111 +-
 tools/slash_confirm.py                             |     7 +-
 tools/terminal_tool.py                             |    75 +-
 tools/tirith_security.py                           |   107 +-
 tools/todo_tool.py                                 |     2 +-
 tools/tool_result_storage.py                       |    22 +-
 tools/transcription_tools.py                       |    59 +-
 tools/tts_tool.py                                  |   258 +-
 tools/url_safety.py                                |   103 +-
 tools/video_generation_tool.py                     |   561 +
 tools/vision_tools.py                              |   275 +-
 tools/voice_mode.py                                |     9 +-
 tools/web_tools.py                                 |  1382 +--
 tools/x_search_tool.py                             |   424 +
 tools/xai_http.py                                  |    71 +
 tools/yuanbao_tools.py                             |     2 +-
 toolsets.py                                        |    65 +-
 trajectory_compressor.py                           |     4 +-
 tui_gateway/entry.py                               |    36 +-
 tui_gateway/server.py                              |   491 +-
 tui_gateway/ws.py                                  |     6 +-
 ui-tui/README.md                                   |     2 +-
 ui-tui/package-lock.json                           |     1 +
 ui-tui/package.json                                |     4 +-
 ui-tui/packages/hermes-ink/index.d.ts              |     2 +
 ui-tui/packages/hermes-ink/src/entry-exports.ts    |     2 +
 .../packages/hermes-ink/src/ink/components/App.tsx |    17 +-
 .../src/ink/components/CursorAdvanceContext.ts     |    35 +
 .../hermes-ink/src/ink/components/Link.tsx         |    65 +-
 .../hermes-ink/src/ink/hooks/use-cursor-advance.ts |    33 +
 .../packages/hermes-ink/src/ink/hyperlinkHover.ts  |    52 +
 .../hermes-ink/src/ink/ink-cursor-advance.test.ts  |   234 +
 .../packages/hermes-ink/src/ink/ink-resize.test.ts |    50 +
 ui-tui/packages/hermes-ink/src/ink/ink.tsx         |   264 +-
 .../packages/hermes-ink/src/ink/log-update.test.ts |    88 +-
 ui-tui/packages/hermes-ink/src/ink/log-update.ts   |    22 +-
 .../hermes-ink/src/ink/render-node-to-output.ts    |    41 +-
 ui-tui/packages/hermes-ink/src/ink/root.ts         |    22 +-
 .../packages/hermes-ink/src/ink/termio/osc.test.ts |   142 +-
 ui-tui/packages/hermes-ink/src/ink/termio/osc.ts   |   101 +-
 .../packages/hermes-ink/src/ink/wrap-text.test.ts  |    17 +
 ui-tui/packages/hermes-ink/src/ink/wrap-text.ts    |    28 +-
 ui-tui/packages/hermes-ink/src/utils/env.ts        |    25 +
 ui-tui/scripts/build.mjs                           |    61 +
 ui-tui/src/__tests__/approvalAction.test.ts        |    50 +
 .../__tests__/createGatewayEventHandler.test.ts    |    55 +
 ui-tui/src/__tests__/createSlashHandler.test.ts    |     8 +
 ui-tui/src/__tests__/cursorDriftRegression.test.ts |   114 +
 ui-tui/src/__tests__/externalLink.test.ts          |   138 +
 ui-tui/src/__tests__/forceTruecolor.test.ts        |    68 +
 ui-tui/src/__tests__/gatewayClient.test.ts         |   386 +
 ui-tui/src/__tests__/markdown.test.ts              |   158 +-
 ui-tui/src/__tests__/precisionWheel.test.ts        |    44 +
 ui-tui/src/__tests__/scroll.test.ts                |    46 +-
 ui-tui/src/__tests__/spawnHistoryStore.test.ts     |    46 +
 ui-tui/src/__tests__/statusBarTicker.test.ts       |    18 +
 ui-tui/src/__tests__/text.test.ts                  |    43 +
 .../__tests__/textInputCursorSourceOfTruth.test.ts |    50 +
 ui-tui/src/__tests__/textInputFastEcho.test.ts     |   185 +
 ui-tui/src/__tests__/textInputRightClick.test.ts   |    48 +
 ui-tui/src/__tests__/textInputWrap.test.ts         |    68 +-
 ui-tui/src/__tests__/theme.test.ts                 |    28 +
 ui-tui/src/__tests__/useInputHandlers.test.ts      |    77 +
 ui-tui/src/__tests__/viewportStore.test.ts         |    33 +-
 ui-tui/src/__tests__/virtualHeights.test.ts        |     8 +
 .../__tests__/virtualHistoryOffsetCache.test.ts    |   155 +
 ui-tui/src/app/createGatewayEventHandler.ts        |    29 +-
 ui-tui/src/app/scroll.ts                           |    20 +-
 ui-tui/src/app/slash/commands/session.ts           |    15 +-
 ui-tui/src/app/spawnHistoryStore.ts                |    24 +-
 ui-tui/src/app/useInputHandlers.ts                 |   142 +-
 ui-tui/src/app/useMainApp.ts                       |    10 +-
 ui-tui/src/components/agentsOverlay.tsx            |    19 +-
 ui-tui/src/components/appChrome.tsx                |    35 +-
 ui-tui/src/components/appLayout.tsx                |    15 +
 ui-tui/src/components/appOverlays.tsx              |    12 +-
 ui-tui/src/components/branding.tsx                 |   215 +-
 ui-tui/src/components/markdown.tsx                 |   434 +-
 ui-tui/src/components/messageLine.tsx              |    42 +-
 ui-tui/src/components/prompts.tsx                  |    71 +-
 ui-tui/src/components/streamingMarkdown.tsx        |    11 +-
 ui-tui/src/components/textInput.tsx                |   215 +-
 ui-tui/src/components/thinking.tsx                 |     6 +-
 ui-tui/src/entry.tsx                               |    19 +-
 ui-tui/src/gatewayClient.ts                        |   455 +-
 ui-tui/src/gatewayTypes.ts                         |     6 +-
 ui-tui/src/hooks/useVirtualHistory.ts              |    19 +-
 ui-tui/src/lib/externalLink.ts                     |   429 +
 ui-tui/src/lib/forceTruecolor.ts                   |    30 +
 ui-tui/src/lib/inputMetrics.ts                     |   139 +-
 ui-tui/src/lib/openExternalUrl.test.ts             |   217 +
 ui-tui/src/lib/openExternalUrl.ts                  |   158 +
 ui-tui/src/lib/precisionWheel.ts                   |    48 +
 ui-tui/src/lib/text.ts                             |    36 +-
 ui-tui/src/lib/viewportStore.ts                    |    50 +
 ui-tui/src/lib/virtualHeights.ts                   |    18 +-
 ui-tui/src/theme.ts                                |    24 +-
 ui-tui/src/types.ts                                |     8 +-
 ui-tui/src/types/hermes-ink.d.ts                   |     2 +
 utils.py                                           |    64 +
 uv.lock                                            |  2212 +---
 web/package.json                                   |     2 +-
 web/scripts/sync-assets.mjs                        |    27 +
 web/src/App.tsx                                    |    29 +-
 web/src/components/ChatSidebar.tsx                 |     9 +-
 web/src/components/LanguageSwitcher.tsx            |   104 +-
 web/src/components/OAuthProvidersCard.tsx          |    20 +-
 web/src/components/ui/checkbox.tsx                 |    61 +
 web/src/hooks/useModalBehavior.ts                  |    44 +
 web/src/i18n/af.ts                                 |   696 ++
 web/src/i18n/context.tsx                           |    64 +-
 web/src/i18n/de.ts                                 |   695 ++
 web/src/i18n/en.ts                                 |   273 +-
 web/src/i18n/es.ts                                 |   695 ++
 web/src/i18n/fr.ts                                 |   695 ++
 web/src/i18n/ga.ts                                 |   696 ++
 web/src/i18n/hu.ts                                 |   696 ++
 web/src/i18n/index.ts                              |     2 +-
 web/src/i18n/it.ts                                 |   695 ++
 web/src/i18n/ja.ts                                 |   696 ++
 web/src/i18n/ko.ts                                 |   696 ++
 web/src/i18n/pt.ts                                 |   696 ++
 web/src/i18n/ru.ts                                 |   696 ++
 web/src/i18n/tr.ts                                 |   696 ++
 web/src/i18n/types.ts                              |   267 +-
 web/src/i18n/uk.ts                                 |   696 ++
 web/src/i18n/zh-hant.ts                            |   696 ++
 web/src/i18n/zh.ts                                 |   268 +
 web/src/lib/api.ts                                 |    45 +-
 web/src/lib/gatewayClient.ts                       |     4 +-
 web/src/lib/resolve-page-title.ts                  |     7 +
 web/src/main.tsx                                   |     3 +-
 web/src/pages/AnalyticsPage.tsx                    |   114 +-
 web/src/pages/ChatPage.tsx                         |   156 +-
 web/src/pages/ConfigPage.tsx                       |    35 +-
 web/src/pages/CronPage.tsx                         |   391 +-
 web/src/pages/DocsPage.tsx                         |    10 +-
 web/src/pages/EnvPage.tsx                          |    78 +-
 web/src/pages/ModelsPage.tsx                       |   545 +-
 web/src/pages/PluginsPage.tsx                      |    30 +-
 web/src/pages/ProfilesPage.tsx                     |   135 +-
 web/src/plugins/types.ts                           |     6 +
 web/src/plugins/usePlugins.ts                      |    16 +-
 web/src/themes/presets.ts                          |    22 +
 website/docs/developer-guide/acp-internals.md      |     8 +-
 .../developer-guide/adding-platform-adapters.md    |   297 +-
 website/docs/developer-guide/adding-providers.md   |     2 +-
 website/docs/developer-guide/agent-loop.md         |     4 +-
 website/docs/developer-guide/architecture.md       |    26 +-
 website/docs/developer-guide/browser-supervisor.md |     7 +-
 website/docs/developer-guide/contributing.md       |    13 +-
 website/docs/developer-guide/creating-skills.md    |     2 +-
 website/docs/developer-guide/environments.md       |   520 -
 website/docs/developer-guide/gateway-internals.md  |    13 +-
 .../developer-guide/image-gen-provider-plugin.md   |   288 +
 .../docs/developer-guide/model-provider-plugin.md  |   267 +
 website/docs/developer-guide/plugin-llm-access.md  |   465 +
 .../developer-guide/programmatic-integration.md    |   126 +
 website/docs/developer-guide/provider-runtime.md   |    27 +-
 .../developer-guide/video-gen-provider-plugin.md   |   231 +
 website/docs/getting-started/installation.md       |    89 +-
 website/docs/getting-started/nix-setup.md          |    37 +-
 website/docs/getting-started/quickstart.md         |    25 +-
 website/docs/getting-started/termux.md             |     4 +-
 website/docs/getting-started/updating.md           |    42 +-
 website/docs/guides/automate-with-cron.md          |     5 +-
 website/docs/guides/automation-templates.md        |    10 +-
 website/docs/guides/build-a-hermes-plugin.md       |   366 +-
 website/docs/guides/cron-script-only.md            |     7 +-
 website/docs/guides/cron-troubleshooting.md        |     2 +-
 website/docs/guides/local-ollama-setup.md          |     8 +-
 .../guides/microsoft-graph-app-registration.md     |   180 +
 website/docs/guides/minimax-oauth.md               |    16 +-
 website/docs/guides/oauth-over-ssh.md              |   137 +
 .../docs/guides/operate-teams-meeting-pipeline.md  |   288 +
 website/docs/guides/pipe-script-output.md          |   249 +
 website/docs/guides/python-library.md              |     3 +-
 website/docs/guides/tips.md                        |     2 +-
 website/docs/guides/use-mcp-with-hermes.md         |     2 +-
 website/docs/guides/xai-grok-oauth.md              |   233 +
 website/docs/index.md                              |    24 +-
 website/docs/integrations/index.md                 |    13 +-
 website/docs/integrations/providers.md             |    90 +-
 website/docs/reference/cli-commands.md             |   152 +-
 website/docs/reference/environment-variables.md    |    95 +-
 website/docs/reference/faq.md                      |     6 +-
 website/docs/reference/mcp-config-reference.md     |     2 +
 website/docs/reference/optional-skills-catalog.md  |    35 +-
 website/docs/reference/profile-commands.md         |   165 +-
 website/docs/reference/skills-catalog.md           |    10 +-
 website/docs/reference/slash-commands.md           |    53 +-
 website/docs/reference/tools-reference.md          |    75 +-
 website/docs/reference/toolsets-reference.md       |    12 +-
 .../docs/user-guide/checkpoints-and-rollback.md    |   183 +-
 website/docs/user-guide/cli.md                     |    21 +-
 website/docs/user-guide/configuration.md           |   103 +-
 website/docs/user-guide/configuring-models.md      |    31 +-
 website/docs/user-guide/docker.md                  |     4 +
 website/docs/user-guide/features/acp.md            |    88 +-
 website/docs/user-guide/features/api-server.md     |    21 +-
 website/docs/user-guide/features/browser.md        |    62 +
 .../docs/user-guide/features/built-in-plugins.md   |    15 +-
 .../features/codex-app-server-runtime.md           |   444 +
 website/docs/user-guide/features/computer-use.md   |   196 +
 website/docs/user-guide/features/cron.md           |    95 +
 website/docs/user-guide/features/curator.md        |     4 +-
 website/docs/user-guide/features/delegation.md     |     1 +
 .../user-guide/features/extending-the-dashboard.md |    13 +-
 .../docs/user-guide/features/fallback-providers.md |     5 +-
 website/docs/user-guide/features/honcho.md         |    26 +-
 website/docs/user-guide/features/hooks.md          |    44 +
 .../docs/user-guide/features/kanban-tutorial.md    |     4 +-
 .../user-guide/features/kanban-worker-lanes.md     |   114 +
 website/docs/user-guide/features/kanban.md         |    48 +-
 website/docs/user-guide/features/lsp.md            |   254 +
 website/docs/user-guide/features/mcp.md            |    18 +
 .../docs/user-guide/features/memory-providers.md   |     6 +-
 website/docs/user-guide/features/plugins.md        |   103 +-
 website/docs/user-guide/features/rl-training.md    |   234 -
 website/docs/user-guide/features/skills.md         |   116 +-
 website/docs/user-guide/features/skins.md          |     2 +
 website/docs/user-guide/features/spotify.md        |    20 +-
 .../docs/user-guide/features/subscription-proxy.md |   203 +
 website/docs/user-guide/features/tool-gateway.md   |   205 +-
 website/docs/user-guide/features/tools.md          |     3 +-
 website/docs/user-guide/features/web-dashboard.md  |     8 +-
 website/docs/user-guide/features/web-search.md     |   392 +
 website/docs/user-guide/features/x-search.md       |   117 +
 website/docs/user-guide/messaging/discord.md       |   126 +-
 website/docs/user-guide/messaging/feishu.md        |     2 +
 website/docs/user-guide/messaging/google_chat.md   |   370 +
 website/docs/user-guide/messaging/index.md         |    43 +-
 website/docs/user-guide/messaging/line.md          |   198 +
 website/docs/user-guide/messaging/matrix.md        |    17 +
 .../docs/user-guide/messaging/msgraph-webhook.md   |   137 +
 website/docs/user-guide/messaging/open-webui.md    |    38 +-
 website/docs/user-guide/messaging/qqbot.md         |     4 +-
 website/docs/user-guide/messaging/simplex.md       |    99 +
 website/docs/user-guide/messaging/slack.md         |    16 +
 website/docs/user-guide/messaging/sms.md           |     2 +-
 .../docs/user-guide/messaging/teams-meetings.md    |   233 +
 website/docs/user-guide/messaging/teams.md         |    38 +
 website/docs/user-guide/messaging/telegram.md      |    85 +-
 website/docs/user-guide/messaging/webhooks.md      |     2 +
 website/docs/user-guide/profile-distributions.md   |   573 +
 website/docs/user-guide/profiles.md                |    14 +
 website/docs/user-guide/security.md                |    22 +-
 website/docs/user-guide/sessions.md                |    75 +
 .../bundled/apple/apple-macos-computer-use.md      |   217 +
 .../autonomous-ai-agents-claude-code.md            |     1 +
 .../autonomous-ai-agents-codex.md                  |     1 +
 .../autonomous-ai-agents-hermes-agent.md           |   267 +-
 .../autonomous-ai-agents-opencode.md               |     1 +
 .../creative/creative-architecture-diagram.md      |     1 +
 .../skills/bundled/creative/creative-ascii-art.md  |     1 +
 .../bundled/creative/creative-ascii-video.md       |     1 +
 .../bundled/creative/creative-baoyu-comic.md       |     1 +
 .../bundled/creative/creative-baoyu-infographic.md |     1 +
 .../bundled/creative/creative-claude-design.md     |     1 +
 .../skills/bundled/creative/creative-comfyui.md    |    10 +-
 .../bundled/creative/creative-creative-ideation.md |     1 +
 .../skills/bundled/creative/creative-design-md.md  |     1 +
 .../skills/bundled/creative/creative-excalidraw.md |     1 +
 .../skills/bundled/creative/creative-humanizer.md  |     1 +
 .../bundled/creative/creative-manim-video.md       |     1 +
 .../skills/bundled/creative/creative-p5js.md       |     1 +
 .../skills/bundled/creative/creative-pixel-art.md  |     1 +
 .../creative/creative-popular-web-designs.md       |     1 +
 .../skills/bundled/creative/creative-pretext.md    |     1 +
 .../skills/bundled/creative/creative-sketch.md     |     1 +
 .../creative/creative-songwriting-and-ai-music.md  |     1 +
 .../bundled/creative/creative-touchdesigner-mcp.md |     1 +
 .../data-science-jupyter-live-kernel.md            |     1 +
 .../bundled/devops/devops-kanban-orchestrator.md   |   127 +-
 .../skills/bundled/devops/devops-kanban-worker.md  |    50 +
 .../bundled/devops/devops-webhook-subscriptions.md |     1 +
 .../skills/bundled/dogfood/dogfood-dogfood.md      |     1 +
 .../skills/bundled/email/email-himalaya.md         |    23 +-
 .../gaming/gaming-minecraft-modpack-server.md      |     1 +
 .../skills/bundled/gaming/gaming-pokemon-player.md |     1 +
 .../bundled/github/github-codebase-inspection.md   |     1 +
 .../skills/bundled/github/github-github-auth.md    |     1 +
 .../bundled/github/github-github-code-review.md    |     1 +
 .../skills/bundled/github/github-github-issues.md  |     1 +
 .../bundled/github/github-github-pr-workflow.md    |     1 +
 .../github/github-github-repo-management.md        |     1 +
 .../skills/bundled/mcp/mcp-native-mcp.md           |     1 +
 .../skills/bundled/media/media-gif-search.md       |     1 +
 .../skills/bundled/media/media-heartmula.md        |     1 +
 .../skills/bundled/media/media-songsee.md          |     1 +
 .../skills/bundled/media/media-spotify.md          |     1 +
 .../skills/bundled/media/media-youtube-content.md  |     1 +
 .../mlops-evaluation-lm-evaluation-harness.md      |     1 +
 .../mlops/mlops-evaluation-weights-and-biases.md   |     1 +
 .../skills/bundled/mlops/mlops-huggingface-hub.md  |     1 +
 .../bundled/mlops/mlops-inference-llama-cpp.md     |     1 +
 .../bundled/mlops/mlops-inference-obliteratus.md   |     1 +
 .../skills/bundled/mlops/mlops-inference-vllm.md   |     1 +
 .../bundled/mlops/mlops-models-audiocraft.md       |     1 +
 .../bundled/mlops/mlops-models-segment-anything.md |     1 +
 .../skills/bundled/mlops/mlops-research-dspy.md    |     1 +
 .../bundled/note-taking/note-taking-obsidian.md    |     1 +
 .../bundled/productivity/productivity-airtable.md  |     1 +
 .../productivity/productivity-google-workspace.md  |    55 +-
 .../bundled/productivity/productivity-linear.md    |    85 +-
 .../bundled/productivity/productivity-maps.md      |     1 +
 .../bundled/productivity/productivity-nano-pdf.md  |     1 +
 .../bundled/productivity/productivity-notion.md    |   355 +-
 .../productivity/productivity-ocr-and-documents.md |     1 +
 .../productivity/productivity-powerpoint.md        |     1 +
 .../productivity-teams-meeting-pipeline.md         |   127 +
 .../bundled/red-teaming/red-teaming-godmode.md     |     1 +
 .../skills/bundled/research/research-arxiv.md      |     1 +
 .../bundled/research/research-blogwatcher.md       |     1 +
 .../skills/bundled/research/research-llm-wiki.md   |     1 +
 .../skills/bundled/research/research-polymarket.md |     1 +
 .../bundled/smart-home/smart-home-openhue.md       |     1 +
 ...re-development-debugging-hermes-tui-commands.md |     1 +
 ...are-development-hermes-agent-skill-authoring.md |     1 +
 .../software-development-node-inspect-debugger.md  |     1 +
 .../software-development-plan.md                   |     1 +
 .../software-development-python-debugpy.md         |     1 +
 .../software-development-requesting-code-review.md |     1 +
 .../software-development-spike.md                  |     1 +
 ...ware-development-subagent-driven-development.md |     1 +
 .../software-development-systematic-debugging.md   |     1 +
 ...software-development-test-driven-development.md |     1 +
 .../software-development-writing-plans.md          |     1 +
 .../skills/bundled/yuanbao/yuanbao-yuanbao.md      |     1 +
 .../autonomous-ai-agents-blackbox.md               |     1 +
 .../autonomous-ai-agents-honcho.md                 |     1 +
 .../skills/optional/blockchain/blockchain-base.md  |   248 -
 .../skills/optional/blockchain/blockchain-evm.md   |   227 +
 .../optional/blockchain/blockchain-hyperliquid.md  |   228 +
 .../optional/blockchain/blockchain-solana.md       |     1 +
 .../communication-one-three-one-rule.md            |     1 +
 .../optional/creative/creative-blender-mcp.md      |     1 +
 .../optional/creative/creative-concept-diagrams.md |     1 +
 .../optional/creative/creative-hyperframes.md      |   205 +
 .../creative/creative-kanban-video-orchestrator.md |   219 +
 .../optional/creative/creative-meme-generation.md  |     1 +
 .../skills/optional/devops/devops-cli.md           |     1 +
 .../optional/devops/devops-docker-management.md    |     1 +
 .../skills/optional/devops/devops-pinggy-tunnel.md |   327 +
 .../skills/optional/devops/devops-watchers.md      |   126 +
 .../dogfood/dogfood-adversarial-ux-test.md         |     1 +
 .../skills/optional/email/email-agentmail.md       |     1 +
 .../optional/finance/finance-3-statement-model.md  |   451 +
 .../optional/finance/finance-comps-analysis.md     |   682 ++
 .../skills/optional/finance/finance-dcf-model.md   |  1288 ++
 .../optional/finance/finance-excel-author.md       |   262 +
 .../skills/optional/finance/finance-lbo-model.md   |   309 +
 .../optional/finance/finance-merger-model.md       |   162 +
 .../skills/optional/finance/finance-pptx-author.md |   191 +
 .../skills/optional/finance/finance-stocks.md      |   112 +
 .../optional/health/health-fitness-nutrition.md    |     1 +
 .../optional/health/health-neuroskill-bci.md       |     1 +
 .../user-guide/skills/optional/mcp/mcp-fastmcp.md  |     1 +
 .../user-guide/skills/optional/mcp/mcp-mcporter.md |     1 +
 .../migration/migration-openclaw-migration.md      |     1 +
 .../skills/optional/mlops/mlops-accelerate.md      |     1 +
 .../skills/optional/mlops/mlops-chroma.md          |     1 +
 .../user-guide/skills/optional/mlops/mlops-clip.md |     1 +
 .../skills/optional/mlops/mlops-faiss.md           |     1 +
 .../skills/optional/mlops/mlops-flash-attention.md |     5 +-
 .../skills/optional/mlops/mlops-guidance.md        |     1 +
 .../mlops/mlops-hermes-atropos-environments.md     |   322 -
 .../optional/mlops/mlops-huggingface-tokenizers.md |     1 +
 .../mlops/mlops-inference-outlines.md              |     5 +-
 .../skills/optional/mlops/mlops-instructor.md      |     1 +
 .../skills/optional/mlops/mlops-lambda-labs.md     |     1 +
 .../skills/optional/mlops/mlops-llava.md           |     1 +
 .../skills/optional/mlops/mlops-modal.md           |     1 +
 .../skills/optional/mlops/mlops-nemo-curator.md    |     1 +
 .../user-guide/skills/optional/mlops/mlops-peft.md |     1 +
 .../skills/optional/mlops/mlops-pinecone.md        |     1 +
 .../skills/optional/mlops/mlops-pytorch-fsdp.md    |     1 +
 .../optional/mlops/mlops-pytorch-lightning.md      |     1 +
 .../skills/optional/mlops/mlops-qdrant.md          |     1 +
 .../skills/optional/mlops/mlops-saelens.md         |     1 +
 .../skills/optional/mlops/mlops-simpo.md           |     1 +
 .../skills/optional/mlops/mlops-slime.md           |     1 +
 .../optional/mlops/mlops-stable-diffusion.md       |     1 +
 .../skills/optional/mlops/mlops-tensorrt-llm.md    |     1 +
 .../skills/optional/mlops/mlops-torchtitan.md      |     1 +
 .../mlops/mlops-training-axolotl.md                |     5 +-
 .../mlops/mlops-training-trl-fine-tuning.md        |    17 +-
 .../mlops/mlops-training-unsloth.md                |     5 +-
 .../skills/optional/mlops/mlops-whisper.md         |     1 +
 .../optional/productivity/productivity-canvas.md   |     1 +
 .../optional/productivity/productivity-shop-app.md |   354 +
 .../optional/productivity/productivity-shopify.md  |     1 +
 .../optional/productivity/productivity-siyuan.md   |     1 +
 .../productivity/productivity-telephony.md         |     1 +
 .../research/research-darwinian-evolver.md         |   217 +
 .../optional/research/research-domain-intel.md     |     1 +
 .../optional/research/research-drug-discovery.md   |     1 +
 .../research/research-duckduckgo-search.md         |     1 +
 .../research/research-gitnexus-explorer.md         |     1 +
 .../research/research-osint-investigation.md       |   294 +
 .../optional/research/research-parallel-cli.md     |     1 +
 .../skills/optional/research/research-scrapling.md |     1 +
 .../optional/research/research-searxng-search.md   |   229 +
 .../skills/optional/security/security-1password.md |     1 +
 .../optional/security/security-oss-forensics.md    |     1 +
 .../skills/optional/security/security-sherlock.md  |     1 +
 .../software-development-rest-graphql-debug.md     |   531 +
 .../web-development/web-development-page-agent.md  |     1 +
 website/docs/user-guide/tui.md                     |     9 +-
 website/docs/user-guide/windows-native.md          |   301 +
 website/docs/user-guide/windows-wsl-quickstart.md  |   332 +-
 website/package.json                               |     2 +-
 website/scripts/extract-skills.py                  |    93 +-
 website/scripts/generate-llms-txt.py               |     2 +-
 website/scripts/generate-skill-docs.py             |   105 +-
 website/sidebars.ts                                |   502 +-
 .../src/components/UserStoriesCollage/index.tsx    |     2 +
 website/src/data/userStories.json                  |  2986 +++--
 website/src/pages/skills/index.tsx                 |    53 +-
 website/src/pages/skills/styles.module.css         |    91 +
 website/static/api/model-catalog.json              |   124 +-
 1638 files changed, 226605 insertions(+), 45101 deletions(-)
```

## Full diff (for reference)

diff --git a/.env.example b/.env.example
index 589978e6b..812986dca 100644
--- a/.env.example
+++ b/.env.example
@@ -14,6 +14,14 @@
 # LLM_MODEL is no longer read from .env — this line is kept for reference only.
 # LLM_MODEL=anthropic/claude-opus-4.6
 
+# =============================================================================
+# LLM PROVIDER (NovitaAI)
+# =============================================================================
+# NovitaAI — 90+ models, pay-per-use
+# Get your key at: https://novita.ai/settings/key-management
+# NOVITA_API_KEY=
+# NOVITA_BASE_URL=https://api.novita.ai/openai/v1  # Override default base URL
+
 # =============================================================================
 # LLM PROVIDER (Google AI Studio / Gemini)
 # =============================================================================
@@ -143,6 +151,18 @@
 # Also requires ~/.honcho/config.json with enabled=true (see README).
 # HONCHO_API_KEY=
 
+# =============================================================================
+# HYPERLIQUID OPTIONAL SKILL
+# =============================================================================
+# Optional defaults for the Hyperliquid skill in optional-skills/blockchain/hyperliquid
+#
+# Hyperliquid API base URL override
+# Default: https://api.hyperliquid.xyz
+# HYPERLIQUID_API_URL=https://api.hyperliquid-testnet.xyz
+#
+# Default address for account-level commands like state, fills, orders, and review
+# HYPERLIQUID_USER_ADDRESS=0x0000000000000000000000000000000000000000
+
 # =============================================================================
 # TERMINAL TOOL CONFIGURATION
 # =============================================================================
@@ -244,6 +264,15 @@ BROWSERBASE_PROXIES=true
 # Uses custom Chromium build to avoid bot detection altogether
 BROWSERBASE_ADVANCED_STEALTH=false
 
+# Browser engine for local mode (default: auto = Chrome)
+# "auto"       — use Chrome (don't pass --engine flag)
+# "lightpanda" — use Lightpanda (1.3-5.8x faster navigation, no screenshots)
+# "chrome"     — explicitly request Chrome
+# Requires agent-browser v0.25.3+. Lightpanda commands that fail or return
+# empty results are automatically retried with Chrome.
+# Also configurable via browser.engine in config.yaml.
+# AGENT_BROWSER_ENGINE=auto
+
 # Browser session timeout in seconds (default: 300)
 # Sessions are cleaned up after this duration of inactivity
 BROWSER_SESSION_TIMEOUT=300
@@ -252,6 +281,27 @@ BROWSER_SESSION_TIMEOUT=300
 # Browser sessions are automatically closed after this period of no activity
 BROWSER_INACTIVITY_TIMEOUT=120
 
+# Extra Chromium launch flags passed to agent-browser, comma- or newline-separated.
+# Hermes auto-injects "--no-sandbox,--disable-dev-shm-usage" when it detects root
+# or AppArmor-restricted unprivileged user namespaces (Ubuntu 23.10+, DGX Spark,
+# many container images), so leave this unset unless you need extra flags.
+# Setting this disables the auto-injection.
+# AGENT_BROWSER_ARGS=--no-sandbox
+
+# Camofox local anti-detection browser (Camoufox-based Firefox).
+# Set CAMOFOX_URL to route the browser tools through a local Camofox server
+# instead of agent-browser/Browserbase. See docs/user-guide/features/browser.md.
+# CAMOFOX_URL=http://localhost:9377
+
+# Externally managed Camofox sessions — when another app owns the visible
+# Camofox browser, set these so Hermes shares the same userId/profile instead
+# of creating its own isolated session.
+# CAMOFOX_USER_ID=
+# CAMOFOX_SESSION_KEY=
+# Set to true to reuse an already-open Camofox tab for this identity before
+# creating a new one (useful for gateway restarts).
+# CAMOFOX_ADOPT_EXISTING_TAB=false
+
 # =============================================================================
 # SESSION LOGGING
 # =============================================================================
@@ -344,24 +394,6 @@ IMAGE_TOOLS_DEBUG=false
 # CONTEXT_COMPRESSION_THRESHOLD=0.85      # Compress at 85% of context limit
 # Model is set via compression.summary_model in config.yaml (default: google/gemini-3-flash-preview)
 
-# =============================================================================
-# RL TRAINING (Tinker + Atropos)
-# =============================================================================
-# Run reinforcement learning training on language models using the Tinker API.
-# Requires the rl-server to be running (from tinker-atropos package).
-
-# Tinker API Key - RL training service
-# Get at: https://tinker-console.thinkingmachines.ai/keys
-# TINKER_API_KEY=
-
-# Weights & Biases API Key - Experiment tracking and metrics
-# Get at: https://wandb.ai/authorize
-# WANDB_API_KEY=
-
-# RL API Server URL (default: http://localhost:8080)
-# Change if running the rl-server on a different host/port
-# RL_API_URL=http://localhost:8080
-
 # =============================================================================
 # SKILLS HUB (GitHub integration for skill search/install/publish)
 # =============================================================================
@@ -414,3 +446,24 @@ IMAGE_TOOLS_DEBUG=false
 # TEAMS_HOME_CHANNEL=                  # Default channel/chat ID for cron delivery
 # TEAMS_HOME_CHANNEL_NAME=             # Display name for the home channel
 # TEAMS_PORT=3978                      # Webhook listen port (Bot Framework default)
+
+# =============================================================================
+# GOOGLE CHAT INTEGRATION
+# =============================================================================
+# Connects via Cloud Pub/Sub pull subscription (no public URL required).
+# Setup walkthrough: website/docs/user-guide/messaging/google_chat.md.
+# 1. Create a GCP project, enable the Google Chat API and Cloud Pub/Sub.
+# 2. Create a Service Account with roles/pubsub.subscriber on the
+#    subscription (NOT project-wide); download the JSON key.
+# 3. Configure your Chat app at console.cloud.google.com/apis/credentials
+#    → Google Chat API → Configuration → Cloud Pub/Sub topic.
+# 4. (Optional, for native attachment delivery) Each user runs
+#    `/setup-files` once in their own DM after Pub/Sub is wired up.
+#
+# GOOGLE_CHAT_PROJECT_ID=                       # GCP project hosting the topic (or set GOOGLE_CLOUD_PROJECT)
+# GOOGLE_CHAT_SUBSCRIPTION_NAME=                # Full path: projects/<id>/subscriptions/<name>
+# GOOGLE_CHAT_SERVICE_ACCOUNT_JSON=             # Path to SA JSON (or set GOOGLE_APPLICATION_CREDENTIALS)
+# GOOGLE_CHAT_ALLOWED_USERS=                    # Comma-separated emails allowed to talk to the bot
+# GOOGLE_CHAT_ALLOW_ALL_USERS=false             # Set true to skip the allowlist
+# GOOGLE_CHAT_HOME_CHANNEL=                     # Default space (spaces/XXXX) for cron delivery
+# GOOGLE_CHAT_HOME_CHANNEL_NAME=                # Display name for the home channel
diff --git a/.github/actions/hermes-smoke-test/action.yml b/.github/actions/hermes-smoke-test/action.yml
new file mode 100644
index 000000000..08b9f9363
--- /dev/null
+++ b/.github/actions/hermes-smoke-test/action.yml
@@ -0,0 +1,47 @@
+name: Hermes smoke test
+description: >
+  Run the image's built-in entrypoint against `--help` and `dashboard --help`
+  to catch basic runtime regressions before publishing.  Requires the image
+  to already be loaded into the local Docker daemon under `image`.
+
+  Works identically on amd64 and arm64 runners.
+
+inputs:
+  image:
+    description: Fully-qualified image tag (e.g. nousresearch/hermes-agent:test)
+    required: true
+
+runs:
+  using: composite
+  steps:
+    - name: Ensure /tmp/hermes-test is hermes-writable
+      shell: bash
+      run: |
+        # The image runs as the hermes user (UID 10000).  GitHub Actions
+        # creates /tmp/hermes-test root-owned by default, which hermes
+        # can't write to — chown it to match the in-container UID before
+        # bind-mounting.  Real users doing `docker run -v ~/.hermes:...`
+        # with their own UID hit the same issue and have their own
+        # remediations (HERMES_UID env var, or chown locally).
+        mkdir -p /tmp/hermes-test
+        sudo chown -R 10000:10000 /tmp/hermes-test
+
+    - name: hermes --help
+      shell: bash
+      run: |
+        docker run --rm \
+          -v /tmp/hermes-test:/opt/data \
+          --entrypoint /opt/hermes/docker/entrypoint.sh \
+          "${{ inputs.image }}" --help
+
+    - name: hermes dashboard --help
+      shell: bash
+      run: |
+        # Regression guard for #9153: dashboard was present in source but
+        # missing from the published image.  If this fails, something in
+        # the Dockerfile is excluding the dashboard subcommand from the
+        # installed package.
+        docker run --rm \
+          -v /tmp/hermes-test:/opt/data \
+          --entrypoint /opt/hermes/docker/entrypoint.sh \
+          "${{ inputs.image }}" dashboard --help
diff --git a/.github/workflows/docker-publish.yml b/.github/workflows/docker-publish.yml
index 228ee3396..cccb8f3b4 100644
--- a/.github/workflows/docker-publish.yml
+++ b/.github/workflows/docker-publish.yml
@@ -10,37 +10,60 @@ on:
       - 'Dockerfile'
       - 'docker/**'
       - '.github/workflows/docker-publish.yml'
+      - '.github/actions/hermes-smoke-test/**'
+  pull_request:
+    branches: [main]
+    paths:
+      - '**/*.py'
+      - 'pyproject.toml'
+      - 'uv.lock'
+      - 'Dockerfile'
+      - 'docker/**'
+      - '.github/workflows/docker-publish.yml'
+      - '.github/actions/hermes-smoke-test/**'
   release:
     types: [published]
 
 permissions:
   contents: read
 
+# Concurrency: push/release runs are NEVER cancelled so every merge gets its
+# own SHA-tagged image; :main and :latest are guarded separately by the
+# move-main and move-latest jobs.  PR runs reuse a PR-scoped group with
+# cancel-in-progress: true so rapid pushes to the same PR collapse to the
+# latest commit.
 concurrency:
-  group: docker-${{ github.ref }}
-  cancel-in-progress: true
+  group: docker-${{ github.event.pull_request.number || github.ref }}
+  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
+
+env:
+  IMAGE_NAME: nousresearch/hermes-agent
 
 jobs:
-  build-and-push:
+  # ---------------------------------------------------------------------------
+  # Build amd64 natively.  This job also runs the smoke tests (basic --help
+  # and the dashboard subcommand regression guard from #9153), because amd64
+  # is the only arch we can `load` into the local daemon on an amd64 runner.
+  # ---------------------------------------------------------------------------
+  build-amd64:
     # Only run on the upstream repository, not on forks
     if: github.repository == 'NousResearch/hermes-agent'
     runs-on: ubuntu-latest
-    timeout-minutes: 60
+    timeout-minutes: 45
+    outputs:
+      digest: ${{ steps.push.outputs.digest }}
     steps:
       - name: Checkout code
         uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5  # v4
         with:
           submodules: recursive
 
-      - name: Set up QEMU
-        uses: docker/setup-qemu-action@c7c53464625b32c7a7e944ae62b3e17d2b600130  # v3
-
       - name: Set up Docker Buildx
         uses: docker/setup-buildx-action@8d2750c68a42422c14e847fe6c8ac0403b4cbd6f  # v3
 
-      # Build amd64 only so we can `load` the image for smoke testing.
-      # `load: true` cannot export a multi-arch manifest to the local daemon.
-      # The multi-arch build follows on push to main / release.
+      # Build once, load into the local daemon for smoke testing.  Cached
+      # to gha with a per-arch scope; the push step below reuses every
+      # layer from this build.
       - name: Build image (amd64, smoke test)
         uses: docker/build-push-action@10e90e3645eae34f1e60eeb005ba3a3d33f178e8  # v6
         with:
@@ -48,24 +71,14 @@ jobs:
           file: Dockerfile
           load: true
           platforms: linux/amd64
-          tags: nousresearch/hermes-agent:test
-          cache-from: type=gha
-          cache-to: type=gha,mode=max
+          tags: ${{ env.IMAGE_NAME }}:test
+          cache-from: type=gha,scope=docker-amd64
+          cache-to: type=gha,mode=max,scope=docker-amd64
 
-      - name: Test image starts
-        run: |
-          # The image runs as the hermes user (UID 10000).  GitHub Actions
-          # creates /tmp/hermes-test root-owned by default, which hermes
-          # can't write to — chown it to match the in-container UID before
-          # bind-mounting.  Real users doing `docker run -v ~/.hermes:...`
-          # with their own UID hit the same issue and have their own
-          # remediations (HERMES_UID env var, or chown locally).
-          mkdir -p /tmp/hermes-test
-          sudo chown -R 10000:10000 /tmp/hermes-test
-          docker run --rm \
-            -v /tmp/hermes-test:/opt/data \
-            --entrypoint /opt/hermes/docker/entrypoint.sh \
-            nousresearch/hermes-agent:test --help
+      - name: Smoke test image
+        uses: ./.github/actions/hermes-smoke-test
+        with:
+          image: ${{ env.IMAGE_NAME }}:test
 
       - name: Log in to Docker Hub
         if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'release'
@@ -74,26 +87,448 @@ jobs:
           username: ${{ secrets.DOCKERHUB_USERNAME }}
           password: ${{ secrets.DOCKERHUB_TOKEN }}
 
-      - name: Push multi-arch image (main branch)
-        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
+      # Push amd64 by digest only (no tag).  The merge job assembles the
+      # tagged manifest list.  `push-by-digest=true` is docker's recommended
+      # pattern for multi-runner multi-platform builds.
+      #
+      # We apply the OCI revision label here (and again on arm64) because
+      # the move-main / move-latest jobs read it off the linux/amd64
+      # sub-manifest config of the floating tag to decide whether it's safe
+      # to advance.  The label must be on each per-arch image — manifest
+      # lists themselves don't carry image config labels.
+      - name: Push amd64 by digest
+        id: push
+        if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'release'
         uses: docker/build-push-action@10e90e3645eae34f1e60eeb005ba3a3d33f178e8  # v6
         with:
           context: .
           file: Dockerfile
-          push: true
-          platforms: linux/amd64,linux/arm64
-          tags: nousresearch/hermes-agent:latest
-          cache-from: type=gha
-          cache-to: type=gha,mode=max
+          platforms: linux/amd64
+          labels: |
+            org.opencontainers.image.revision=${{ github.sha }}
+          outputs: type=image,name=${{ env.IMAGE_NAME }},push-by-digest=true,name-canonical=true,push=true
+          cache-from: type=gha,scope=docker-amd64
+          cache-to: type=gha,mode=max,scope=docker-amd64
 
-      - name: Push multi-arch image (release)
-        if: github.event_name == 'release'
+      # Write the digest to a file and upload it as an artifact so the
+      # merge job can stitch both per-arch digests into a manifest list.
+      - name: Export digest
+        if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'release'
+        run: |
+          mkdir -p /tmp/digests
+          digest="${{ steps.push.outputs.digest }}"
+          touch "/tmp/digests/${digest#sha256:}"
+
+      - name: Upload digest artifact
+        if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'release'
+        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4
+        with:
+          name: digest-amd64
+          path: /tmp/digests/*
+          if-no-files-found: error
+          retention-days: 1
+
+  # ---------------------------------------------------------------------------
+  # Build arm64 natively on GitHub's free arm64 runner.  This replaces the
+  # previous QEMU-emulated arm64 build, which was ~5-10x slower and shared
+  # a cache scope with amd64.  Matches the amd64 job's shape: build+load,
+  # smoke test, then on push/release push by digest.
+  # ---------------------------------------------------------------------------
+  build-arm64:
+    if: github.repository == 'NousResearch/hermes-agent'
+    runs-on: ubuntu-24.04-arm
+    timeout-minutes: 45
+    outputs:
+      digest: ${{ steps.push.outputs.digest }}
+    steps:
+      - name: Checkout code
+        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5  # v4
+        with:
+          submodules: recursive
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@8d2750c68a42422c14e847fe6c8ac0403b4cbd6f  # v3
+
+      # Build once, load into the local daemon for smoke testing.  Cached
+      # to gha with a per-arch scope; the push step below reuses every
+      # layer from this build.
+      - name: Build image (arm64, smoke test)
         uses: docker/build-push-action@10e90e3645eae34f1e60eeb005ba3a3d33f178e8  # v6
         with:
           context: .
           file: Dockerfile
-          push: true
-          platforms: linux/amd64,linux/arm64
-          tags: nousresearch/hermes-agent:${{ github.event.release.tag_name }}
-          cache-from: type=gha
-          cache-to: type=gha,mode=max
+          load: true
+          platforms: linux/arm64
+          tags: ${{ env.IMAGE_NAME }}:test
+          cache-from: type=gha,scope=docker-arm64
+          cache-to: type=gha,mode=max,scope=docker-arm64
+
+      - name: Smoke test image
+        uses: ./.github/actions/hermes-smoke-test
+        with:
+          image: ${{ env.IMAGE_NAME }}:test
+
+      - name: Log in to Docker Hub
+        if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'release'
+        uses: docker/login-action@c94ce9fb468520275223c153574b00df6fe4bcc9  # v3
+        with:
+          username: ${{ secrets.DOCKERHUB_USERNAME }}
+          password: ${{ secrets.DOCKERHUB_TOKEN }}
+
+      - name: Push arm64 by digest
+        id: push
+        if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'release'
+        uses: docker/build-push-action@10e90e3645eae34f1e60eeb005ba3a3d33f178e8  # v6
+        with:
+          context: .
+          file: Dockerfile
+          platforms: linux/arm64
+          labels: |
+            org.opencontainers.image.revision=${{ github.sha }}
+          outputs: type=image,name=${{ env.IMAGE_NAME }},push-by-digest=true,name-canonical=true,push=true
+          cache-from: type=gha,scope=docker-arm64
+          cache-to: type=gha,mode=max,scope=docker-arm64
+
+      - name: Export digest
+        if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'release'
+        run: |
+          mkdir -p /tmp/digests
+          digest="${{ steps.push.outputs.digest }}"
+          touch "/tmp/digests/${digest#sha256:}"
+
+      - name: Upload digest artifact
+        if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'release'
+        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4
+        with:
+          name: digest-arm64
+          path: /tmp/digests/*
+          if-no-files-found: error
+          retention-days: 1
+
+  # ---------------------------------------------------------------------------
+  # Stitch both per-arch digests into a single tagged multi-arch manifest.
+  # This is a registry-side operation — no building, no layer re-push —
+  # so it runs in ~30 seconds.  On main pushes it produces :sha-<sha>.
+  # On releases it produces :<release_tag_name>.
+  # ---------------------------------------------------------------------------
+  merge:
+    if: github.repository == 'NousResearch/hermes-agent' && (github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'release')
+    runs-on: ubuntu-latest
+    needs: [build-amd64, build-arm64]
+    timeout-minutes: 10
+    outputs:
+      pushed_sha_tag: ${{ steps.mark_pushed.outputs.pushed }}
+      pushed_release_tag: ${{ steps.mark_release_pushed.outputs.pushed }}
+      release_tag: ${{ steps.tag.outputs.tag }}
+    steps:
+      - name: Download digests
+        uses: actions/download-artifact@d3f86a106a0bac45b974a628896c90dbdf5c8093  # v4
+        with:
+          path: /tmp/digests
+          pattern: digest-*
+          merge-multiple: true
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@8d2750c68a42422c14e847fe6c8ac0403b4cbd6f  # v3
+
+      - name: Log in to Docker Hub
+        uses: docker/login-action@c94ce9fb468520275223c153574b00df6fe4bcc9  # v3
+        with:
+          username: ${{ secrets.DOCKERHUB_USERNAME }}
+          password: ${{ secrets.DOCKERHUB_TOKEN }}
+
+      # Compute the tag for this run.  Main pushes use sha-<sha> (so every
+      # commit gets its own immutable tag); releases use the release tag name.
+      - name: Compute tag
+        id: tag
+        run: |
+          if [ "${{ github.event_name }}" = "release" ]; then
+            echo "tag=${{ github.event.release.tag_name }}" >> "$GITHUB_OUTPUT"
+          else
+            echo "tag=sha-${{ github.sha }}" >> "$GITHUB_OUTPUT"
+          fi
+
+      - name: Create manifest list and push
+        working-directory: /tmp/digests
+        run: |
+          set -euo pipefail
+          # Build the arg array from each digest file (filename = the digest
+          # hex, with no sha256: prefix; empty file content, only the name
+          # matters).  Using an array avoids shellcheck SC2046 and keeps
+          # every digest a single argv token even under pathological names.
+          args=()
+          for digest_file in *; do
+            args+=("${IMAGE_NAME}@sha256:${digest_file}")
+          done
+          docker buildx imagetools create \
+            -t "${IMAGE_NAME}:${TAG}" \
+            "${args[@]}"
+        env:
+          IMAGE_NAME: ${{ env.IMAGE_NAME }}
+          TAG: ${{ steps.tag.outputs.tag }}
+
+      - name: Inspect image
+        run: |
+          docker buildx imagetools inspect "${IMAGE_NAME}:${TAG}"
+        env:
+          IMAGE_NAME: ${{ env.IMAGE_NAME }}
+          TAG: ${{ steps.tag.outputs.tag }}
+
+      # Signal to move-main that the SHA tag is live.  Only on main pushes;
+      # releases set pushed_release_tag instead.
+      - name: Mark SHA tag pushed
+        id: mark_pushed
+        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
+        run: echo "pushed=true" >> "$GITHUB_OUTPUT"
+
+      # Signal to move-latest that the release tag is live.
+      - name: Mark release tag pushed
+        id: mark_release_pushed
+        if: github.event_name == 'release'
+        run: echo "pushed=true" >> "$GITHUB_OUTPUT"
+
+  # ---------------------------------------------------------------------------
+  # Move :main to point at the SHA tag the merge job pushed.
+  #
+  # :main is the floating tag that tracks the tip of the main branch.  Every
+  # merge to main retags :main forward.  Users who want "latest dev build"
+  # pull :main; users who want stable releases pull :latest.
+  #
+  # The real serialization guarantee comes from the top-level concurrency
+  # group (`docker-${{ github.ref }}` with `cancel-in-progress: false`),
+  # which ensures at most one workflow run for this ref executes at a time.
+  # That means two move-main steps for the same ref cannot overlap.
+  #
+  # This job has its own concurrency group as defense-in-depth: if the
+  # top-level group is ever loosened, queued move-mains will run serially
+  # in arrival order, each one running the ancestor check below and either
+  # advancing :main or skipping.  `cancel-in-progress: false` matches the
+  # top-level setting — we don't want rapid pushes to cancel a queued
+  # move-main, because the ancestor check is the real safety mechanism
+  # and queueing is cheap (move-main is a ~30s registry op).
+  #
+  # Combined with the ancestor check, this means :main only ever moves
+  # forward in git history.
+  # ---------------------------------------------------------------------------
+  move-main:
+    if: |
+      github.repository == 'NousResearch/hermes-agent'
+      && github.event_name == 'push'
+      && github.ref == 'refs/heads/main'
+      && needs.merge.outputs.pushed_sha_tag == 'true'
+    needs: merge
+    runs-on: ubuntu-latest
+    timeout-minutes: 10
+    concurrency:
+      group: docker-move-main-${{ github.ref }}
+      cancel-in-progress: false
+    steps:
+      - name: Checkout code
+        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5  # v4
+        with:
+          fetch-depth: 1000
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@8d2750c68a42422c14e847fe6c8ac0403b4cbd6f  # v3
+
+      - name: Log in to Docker Hub
+        uses: docker/login-action@c94ce9fb468520275223c153574b00df6fe4bcc9  # v3
+        with:
+          username: ${{ secrets.DOCKERHUB_USERNAME }}
+          password: ${{ secrets.DOCKERHUB_TOKEN }}
+
+      # Read the git revision label off the current :main manifest, then
+      # use `git merge-base --is-ancestor` to check whether our commit is a
+      # descendant of it.  If :main doesn't exist yet, or its label is
+      # missing, we treat that as "safe to publish".  If another run already
+      # advanced :main past us (or diverged), we skip and leave it alone.
+      - name: Decide whether to move :main
+        id: main_check
+        run: |
+          set -euo pipefail
+          image=nousresearch/hermes-agent
+
+          # Pull the JSON for the linux/amd64 sub-manifest's config and extract
+          # the OCI revision label with jq — Go template field access can't
+          # handle dots in map keys, so using json+jq is the robust route.
+          image_json=$(
+            docker buildx imagetools inspect "${image}:main" \
+              --format '{{ json (index .Image "linux/amd64") }}' \
+              2>/dev/null || true
+          )
+
+          if [ -z "${image_json}" ]; then
+            echo "No existing :main (or inspect failed) — safe to publish."
+            echo "push_main=true" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
+
+          current_sha=$(
+            printf '%s' "${image_json}" \
+              | jq -r '.config.Labels."org.opencontainers.image.revision" // ""'
+          )
+
+          if [ -z "${current_sha}" ]; then
+            echo "Registry :main has no revision label — safe to publish."
+            echo "push_main=true" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
+
+          echo "Registry :main is at ${current_sha}"
+          echo "This run is at      ${GITHUB_SHA}"
+
+          if [ "${current_sha}" = "${GITHUB_SHA}" ]; then
+            echo ":main already points at our SHA — nothing to do."
+            echo "push_main=false" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
+
+          # Make sure we have the :main commit locally for merge-base.
+          if ! git cat-file -e "${current_sha}^{commit}" 2>/dev/null; then
+            git fetch --no-tags --prune origin \
+              "+refs/heads/main:refs/remotes/origin/main" \
+              || true
+          fi
+
+          if ! git cat-file -e "${current_sha}^{commit}" 2>/dev/null; then
+            echo "Registry :main points at an unknown commit (${current_sha}); refusing to overwrite."
+            echo "push_main=false" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
+
+          # Our SHA must be a descendant of the current :main to be safe.
+          if git merge-base --is-ancestor "${current_sha}" "${GITHUB_SHA}"; then
+            echo "Our commit is a descendant of :main — safe to advance."
+            echo "push_main=true" >> "$GITHUB_OUTPUT"
+          else
+            echo "Another run advanced :main past us (or diverged) — leaving it alone."
+            echo "push_main=false" >> "$GITHUB_OUTPUT"
+          fi
+
+      # Retag the already-pushed SHA manifest as :main.  This is a registry-
+      # side operation — no rebuild, no layer re-push — so it's quick and
+      # atomic per-tag.  The ancestor check above plus the cancel-in-progress
+      # concurrency on this job together guarantee we only ever move :main
+      # forward in git history.
+      - name: Move :main to this SHA
+        if: steps.main_check.outputs.push_main == 'true'
+        run: |
+          set -euo pipefail
+          image=nousresearch/hermes-agent
+          docker buildx imagetools create \
+            --tag "${image}:main" \
+            "${image}:sha-${GITHUB_SHA}"
+
+  # ---------------------------------------------------------------------------
+  # Move :latest to point at the release tag the merge job pushed.
+  #
+  # :latest is the floating tag that tracks the most recent stable release.
+  # Only `release: published` events advance it — never main pushes.
+  #
+  # We still run an ancestor check against the existing :latest so that a
+  # backport release on an older branch (e.g. patching v1.1.5 after v1.2.3
+  # is out) doesn't drag :latest backwards.  The check is the same shape as
+  # move-main: read the OCI revision label off the current :latest, look up
+  # that commit in git, and only advance if our release commit is a strict
+  # descendant.
+  # ---------------------------------------------------------------------------
+  move-latest:
+    if: |
+      github.repository == 'NousResearch/hermes-agent'
+      && github.event_name == 'release'
+      && needs.merge.outputs.pushed_release_tag == 'true'
+    needs: merge
+    runs-on: ubuntu-latest
+    timeout-minutes: 10
+    concurrency:
+      group: docker-move-latest
+      cancel-in-progress: false
+    steps:
+      - name: Checkout code
+        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5  # v4
+        with:
+          fetch-depth: 1000
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@8d2750c68a42422c14e847fe6c8ac0403b4cbd6f  # v3
+
+      - name: Log in to Docker Hub
+        uses: docker/login-action@c94ce9fb468520275223c153574b00df6fe4bcc9  # v3
+        with:
+          username: ${{ secrets.DOCKERHUB_USERNAME }}
+          password: ${{ secrets.DOCKERHUB_TOKEN }}
+
+      - name: Decide whether to move :latest
+        id: latest_check
+        run: |
+          set -euo pipefail
+          image=nousresearch/hermes-agent
+
+          image_json=$(
+            docker buildx imagetools inspect "${image}:latest" \
+              --format '{{ json (index .Image "linux/amd64") }}' \
+              2>/dev/null || true
+          )
+
+          if [ -z "${image_json}" ]; then
+            echo "No existing :latest (or inspect failed) — safe to publish."
+            echo "push_latest=true" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
+
+          current_sha=$(
+            printf '%s' "${image_json}" \
+              | jq -r '.config.Labels."org.opencontainers.image.revision" // ""'
+          )
+
+          if [ -z "${current_sha}" ]; then
+            echo "Registry :latest has no revision label — safe to publish."
+            echo "push_latest=true" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
+
+          echo "Registry :latest is at ${current_sha}"
+          echo "This release is at  ${GITHUB_SHA}"
+
+          if [ "${current_sha}" = "${GITHUB_SHA}" ]; then
+            echo ":latest already points at our SHA — nothing to do."
+            echo "push_latest=false" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
+
+          # Make sure we have the :latest commit locally for merge-base.
+          # Releases can be cut from any branch, so fetch broadly.
+          if ! git cat-file -e "${current_sha}^{commit}" 2>/dev/null; then
+            git fetch --no-tags --prune origin \
+              "+refs/heads/main:refs/remotes/origin/main" \
+              || true
+          fi
+
+          if ! git cat-file -e "${current_sha}^{commit}" 2>/dev/null; then
+            echo "Registry :latest points at an unknown commit (${current_sha}); refusing to overwrite."
+            echo "push_latest=false" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
+
+          # Our release SHA must be a descendant of the current :latest.
+          # Backport releases on older branches won't satisfy this and will
+          # be left alone — :latest stays on the newer release.
+          if git merge-base --is-ancestor "${current_sha}" "${GITHUB_SHA}"; then
+            echo "Our release commit is a descendant of :latest — safe to advance."
+            echo "push_latest=true" >> "$GITHUB_OUTPUT"
+          else
+            echo "Existing :latest is newer than this release (likely a backport) — leaving it alone."
+            echo "push_latest=false" >> "$GITHUB_OUTPUT"
+          fi
+
+      # Retag the already-pushed release manifest as :latest.
+      - name: Move :latest to this release tag
+        if: steps.latest_check.outputs.push_latest == 'true'
+        env:
+          RELEASE_TAG: ${{ needs.merge.outputs.release_tag }}
+        run: |
+          set -euo pipefail
+          image=nousresearch/hermes-agent
+          docker buildx imagetools create \
+            --tag "${image}:latest" \
+            "${image}:${RELEASE_TAG}"
diff --git a/.github/workflows/history-check.yml b/.github/workflows/history-check.yml
new file mode 100644
index 000000000..bd66f1940
--- /dev/null
+++ b/.github/workflows/history-check.yml
@@ -0,0 +1,58 @@
+name: History Check
+
+# Rejects PRs whose branch has no common ancestor with main.
+#
+# In May 2026 PR #25045 was merged from a branch that had been disconnected
+# from main's history (likely an accidental `git checkout --orphan` or
+# `.git/` re-init).  GitHub's merge UI does not refuse merges of unrelated
+# histories, so the PR landed cleanly with the intended one-file change —
+# but its parent-less root commit (413990c94) got grafted into main as a
+# second root, and ~1500 files' worth of `git blame` history collapsed
+# onto that single commit.
+#
+# This check catches the failure mode by requiring `git merge-base` between
+# the PR head and main to be non-empty.
+
+on:
+  pull_request:
+    branches: [main]
+
+permissions:
+  contents: read
+
+jobs:
+  check-common-ancestor:
+    runs-on: ubuntu-latest
+    steps:
+      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5  # v4
+        with:
+          fetch-depth: 0  # full history both sides for merge-base
+
+      - name: Reject PRs with no common ancestor on main
+        run: |
+          # `git merge-base` exits non-zero AND prints nothing when the two
+          # commits share no ancestor.  We check both conditions explicitly
+          # so the failure message is clear regardless of which signal fires
+          # first.
+          if ! BASE=$(git merge-base origin/main HEAD 2>/dev/null) || [ -z "$BASE" ]; then
+            echo ""
+            echo "::error::This PR has no common ancestor with main."
+            echo ""
+            echo "Your branch's history is disconnected from main.  Common causes:"
+            echo "  - the branch was created with 'git checkout --orphan'"
+            echo "  - '.git/' was re-initialized at some point during the work"
+            echo "  - the branch was force-pushed from an unrelated repository"
+            echo ""
+            echo "Merging an unrelated-history PR grafts a parent-less root commit"
+            echo "into main and collapses git blame for every file in that snapshot."
+            echo "Reference: PR #25045 caused this and re-rooted blame on ~1500"
+            echo "files to a single orphan commit."
+            echo ""
+            echo "To fix, rebase your changes onto current main:"
+            echo "  git fetch origin main"
+            echo "  git checkout -b fix-branch origin/main"
+            echo "  # re-apply your changes (cherry-pick, copy files, etc.)"
+            echo "  git push -f origin fix-branch"
+            exit 1
+          fi
+          echo "::notice::Common ancestor with main: $BASE"
diff --git a/.github/workflows/lint.yml b/.github/workflows/lint.yml
new file mode 100644
index 000000000..807d5b6b6
--- /dev/null
+++ b/.github/workflows/lint.yml
@@ -0,0 +1,202 @@
+name: Lint (ruff + ty)
+
+# Two things here:
+#   1. Advisory diff — ruff + ty diagnostics as a diff vs the target branch.
+#      Posts a Markdown summary and a PR comment. Exit zero always.
+#   2. Blocking ``ruff check .`` — enforces the explicit rules in
+#      ``[tool.ruff.lint.select]`` (currently PLW1514). Failure blocks merge.
+#      Separate job so the advisory diff still runs and posts even when
+#      enforcement fails.
+
+on:
+  push:
+    branches: [main]
+    paths-ignore:
+      - "**/*.md"
+      - "docs/**"
+      - "website/**"
+  pull_request:
+    branches: [main]
+    paths-ignore:
+      - "**/*.md"
+      - "docs/**"
+      - "website/**"
+
+permissions:
+  contents: read
+  pull-requests: write # needed to post/update PR comments
+
+concurrency:
+  group: lint-${{ github.ref }}
+  cancel-in-progress: true
+
+jobs:
+  lint-diff:
+    name: ruff + ty diff
+    runs-on: ubuntu-latest
+    timeout-minutes: 10
+    steps:
+      - name: Checkout code
+        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
+        with:
+          fetch-depth: 0 # need full history for merge-base + worktree
+
+      - name: Install uv
+        uses: astral-sh/setup-uv@d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86 # v5
+
+      - name: Install ruff + ty
+        run: |
+          uv tool install ruff
+          uv tool install ty
+
+      - name: Determine base ref
+        id: base
+        run: |
+          # For PRs, diff against the merge base with the target branch.
+          # For pushes to main, diff against the previous commit on main.
+          if [ "${{ github.event_name }}" = "pull_request" ]; then
+            BASE_SHA=$(git merge-base "origin/${{ github.base_ref }}" HEAD)
+            BASE_REF="origin/${{ github.base_ref }}"
+          else
+            BASE_SHA=$(git rev-parse HEAD~1 2>/dev/null || git rev-parse HEAD)
+            BASE_REF="HEAD~1"
+          fi
+          echo "sha=${BASE_SHA}" >> "$GITHUB_OUTPUT"
+          echo "ref=${BASE_REF}" >> "$GITHUB_OUTPUT"
+          echo "Base SHA: ${BASE_SHA}"
+          echo "Base ref: ${BASE_REF}"
+
+      - name: Run ruff + ty on HEAD
+        run: |
+          mkdir -p .lint-reports/head
+          ruff check --output-format json --exit-zero \
+            > .lint-reports/head/ruff.json || true
+          ty check --output-format gitlab --exit-zero \
+            > .lint-reports/head/ty.json || true
+          echo "HEAD ruff: $(wc -c < .lint-reports/head/ruff.json) bytes"
+          echo "HEAD ty:   $(wc -c < .lint-reports/head/ty.json) bytes"
+
+      - name: Run ruff + ty on base (via git worktree)
+        run: |
+          mkdir -p .lint-reports/base
+          # Use a worktree so we don't clobber the main checkout. If the basex
+          # SHA is identical to HEAD (e.g. first commit), skip and leave the
+          # base reports empty — the diff script handles missing files.
+          HEAD_SHA=$(git rev-parse HEAD)
+          BASE_SHA="${{ steps.base.outputs.sha }}"
+          if [ "$BASE_SHA" = "$HEAD_SHA" ]; then
+            echo "Base SHA == HEAD SHA, skipping base scan."
+            echo '[]' > .lint-reports/base/ruff.json
+            echo '[]' > .lint-reports/base/ty.json
+          else
+            git worktree add --detach /tmp/lint-base "$BASE_SHA"
+            (
+              cd /tmp/lint-base
+              ruff check --output-format json --exit-zero \
+                > "$GITHUB_WORKSPACE/.lint-reports/base/ruff.json" || true
+              ty check --output-format gitlab --exit-zero \
+                > "$GITHUB_WORKSPACE/.lint-reports/base/ty.json" || true
+            )
+            git worktree remove --force /tmp/lint-base
+          fi
+          echo "base ruff: $(wc -c < .lint-reports/base/ruff.json) bytes"
+          echo "base ty:   $(wc -c < .lint-reports/base/ty.json) bytes"
+
+      - name: Generate diff summary
+        run: |
+          python scripts/lint_diff.py \
+            --base-ruff .lint-reports/base/ruff.json \
+            --head-ruff .lint-reports/head/ruff.json \
+            --base-ty   .lint-reports/base/ty.json \
+            --head-ty   .lint-reports/head/ty.json \
+            --base-ref  "${{ steps.base.outputs.ref }}" \
+            --head-ref  "${{ github.event_name == 'pull_request' && github.head_ref || github.ref_name }}" \
+            --output    .lint-reports/summary.md
+          cat .lint-reports/summary.md >> "$GITHUB_STEP_SUMMARY"
+
+      - name: Upload reports as artifact
+        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4
+        with:
+          name: lint-reports
+          path: .lint-reports/
+          retention-days: 14
+
+      - name: Post / update PR comment
+        if: github.event_name == 'pull_request' && github.event.pull_request.head.repo.full_name == github.repository
+        continue-on-error: true
+        uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7
+        with:
+          script: |
+            const fs = require('fs');
+            const body = fs.readFileSync('.lint-reports/summary.md', 'utf8');
+            const marker = '<!-- lint-diff-summary -->';
+            const fullBody = marker + '\n' + body;
+
+            const { data: comments } = await github.rest.issues.listComments({
+              owner: context.repo.owner,
+              repo:  context.repo.repo,
+              issue_number: context.issue.number,
+            });
+            const existing = comments.find(c => c.body && c.body.includes(marker));
+            if (existing) {
+              await github.rest.issues.updateComment({
+                owner: context.repo.owner,
+                repo:  context.repo.repo,
+                comment_id: existing.id,
+                body: fullBody,
+              });
+            } else {
+              await github.rest.issues.createComment({
+                owner: context.repo.owner,
+                repo:  context.repo.repo,
+                issue_number: context.issue.number,
+                body: fullBody,
+              });
+            }
+
+
+  ruff-blocking:
+    # Enforce the rules in pyproject.toml [tool.ruff.lint.select]. Currently
+    # PLW1514 (unspecified-encoding) — catches bare ``open()`` /
+    # ``read_text()`` / ``write_text()`` calls that default to locale
+    # encoding on Windows. Failure here blocks merge; the advisory
+    # ``lint-diff`` job above runs independently so reviewers still get
+    # the diff comment even when enforcement fails.
+    name: ruff enforcement (blocking)
+    runs-on: ubuntu-latest
+    timeout-minutes: 5
+    steps:
+      - name: Checkout code
+        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
+
+      - name: Install uv
+        uses: astral-sh/setup-uv@d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86 # v5
+
+      - name: Install ruff
+        run: uv tool install ruff
+
+      - name: ruff check .
+        # No --exit-zero, no || true. Exit code propagates to the job,
+        # which propagates to the required-check gate.
+        run: |
+          ruff check .
+
+  windows-footguns:
+    # Static guardrails on Windows-unsafe Python primitives — os.kill(pid, 0),
+    # os.killpg, os.setsid, signal.SIGKILL without getattr fallback,
+    # shebang scripts via subprocess, bare open() without encoding=, etc.
+    # See scripts/check-windows-footguns.py for the full rule list.
+    name: Windows footguns (blocking)
+    runs-on: ubuntu-latest
+    timeout-minutes: 5
+    steps:
+      - name: Checkout code
+        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
+
+      - name: Set up Python
+        uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b # v5
+        with:
+          python-version: "3.11"
+
+      - name: Run footgun checker
+        run: python scripts/check-windows-footguns.py --all
diff --git a/.github/workflows/supply-chain-audit.yml b/.github/workflows/supply-chain-audit.yml
index 417e7b21f..69a9a115c 100644
--- a/.github/workflows/supply-chain-audit.yml
+++ b/.github/workflows/supply-chain-audit.yml
@@ -11,6 +11,7 @@ on:
       - '**/sitecustomize.py'
       - '**/usercustomize.py'
       - '**/__init__.pth'
+      - 'pyproject.toml'
 
 permissions:
   pull-requests: write
@@ -137,3 +138,68 @@ jobs:
         run: |
           echo "::error::CRITICAL supply chain risk patterns detected in this PR. See the PR comment for details."
           exit 1
+
+  dep-bounds:
+    name: Check PyPI dependency upper bounds
+    runs-on: ubuntu-latest
+    if: contains(github.event.pull_request.changed_files_url, 'pyproject.toml') || true
+    steps:
+      - name: Checkout
+        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5  # v4
+        with:
+          fetch-depth: 0
+
+      - name: Check for unbounded PyPI deps
+        id: bounds
+        run: |
+          set -euo pipefail
+
+          BASE="${{ github.event.pull_request.base.sha }}"
+          HEAD="${{ github.event.pull_request.head.sha }}"
+
+          # Only check added lines in pyproject.toml
+          ADDED=$(git diff "$BASE".."$HEAD" -- pyproject.toml | grep '^+' | grep -v '^+++' || true)
+
+          if [ -z "$ADDED" ]; then
+            echo "found=false" >> "$GITHUB_OUTPUT"
+            exit 0
+          fi
+
+          # Match PyPI dep specs that have >= but no < ceiling.
+          # Pattern: "package>=version" without a following ",<" bound.
+          # Excludes git+ URLs (which use commit SHAs) and comments.
+          UNBOUNDED=$(echo "$ADDED" | grep -oE '"[a-zA-Z0-9_-]+(\[[^\]]*\])?>=[ 0-9.]+"' | grep -v ',<' || true)
+
+          if [ -n "$UNBOUNDED" ]; then
+            echo "found=true" >> "$GITHUB_OUTPUT"
+            echo "$UNBOUNDED" > /tmp/unbounded.txt
+          else
+            echo "found=false" >> "$GITHUB_OUTPUT"
+          fi
+
+      - name: Post unbounded dep warning
+        if: steps.bounds.outputs.found == 'true'
+        env:
+          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
+        run: |
+          BODY="## ⚠️ Unbounded PyPI Dependency Detected
+
+          This PR adds PyPI dependencies without a \`<next_major\` upper bound. Per our [supply chain policy](../blob/main/CONTRIBUTING.md#dependency-pinning-policy-supply-chain-hardening), all PyPI deps must be pinned as \`>=floor,<next_major\`.
+
+          **Unbounded specs found:**
+          \`\`\`
+          $(cat /tmp/unbounded.txt)
+          \`\`\`
+
+          **Fix:** Add an upper bound, e.g. \`\"package>=1.2.0,<2\"\`
+
+          ---
+          *See PR #2810 and CONTRIBUTING.md for the full policy rationale.*"
+
+          gh pr comment "${{ github.event.pull_request.number }}" --body "$BODY" || echo "::warning::Could not post PR comment (expected for fork PRs)"
+
+      - name: Fail on unbounded deps
+        if: steps.bounds.outputs.found == 'true'
+        run: |
+          echo "::error::PyPI dependencies without upper bounds detected. Add <next_major ceiling per CONTRIBUTING.md policy."
+          exit 1
diff --git a/.github/workflows/tests.yml b/.github/workflows/tests.yml
index a92afdfa4..be14f14c8 100644
--- a/.github/workflows/tests.yml
+++ b/.github/workflows/tests.yml
@@ -55,11 +55,14 @@ jobs:
 
   e2e:
     runs-on: ubuntu-latest
-    timeout-minutes: 10
+    timeout-minutes: 15
     steps:
       - name: Checkout code
         uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5  # v4
 
+      - name: Install system dependencies
+        run: sudo apt-get update && sudo apt-get install -y ripgrep
+
       - name: Install uv
         uses: astral-sh/setup-uv@d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86  # v5
 
diff --git a/.github/workflows/upload_to_pypi.yml b/.github/workflows/upload_to_pypi.yml
new file mode 100644
index 000000000..95477ccf0
--- /dev/null
+++ b/.github/workflows/upload_to_pypi.yml
@@ -0,0 +1,163 @@
+name: Publish to PyPI
+
+# Triggered by CalVer tag pushes from scripts/release.py (e.g. v2026.5.15)
+# Can also be triggered manually from the Actions tab as an escape hatch.
+on:
+  push:
+    tags:
+      - 'v20*'  # CalVer tags: v2026.5.15, v2026.5.15.2, etc.
+  workflow_dispatch:
+    inputs:
+      confirm_tag:
+        description: 'Tag to publish (e.g. v2026.5.15). Must already exist.'
+        required: true
+        type: string
+
+# Restrict default token to read-only; each job escalates as needed.
+permissions:
+  contents: read
+
+# Prevent overlapping publishes (e.g. two same-day tags pushed quickly).
+concurrency:
+  group: pypi-publish
+  cancel-in-progress: false
+
+jobs:
+  build:
+    name: Build distribution 📦
+    runs-on: ubuntu-latest
+    steps:
+      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5  # v4
+        with:
+          persist-credentials: false
+          # On workflow_dispatch, check out the confirmed tag.
+          ref: ${{ inputs.confirm_tag || github.ref }}
+          fetch-tags: true
+
+      - name: Validate tag exists
+        if: github.event_name == 'workflow_dispatch'
+        run: |
+          if ! git tag -l "${{ inputs.confirm_tag }}" | grep -q .; then
+            echo "::error::Tag '${{ inputs.confirm_tag }}' does not exist in the repo"
+            exit 1
+          fi
+
+      - name: Set up Python
+        uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065  # v5
+        with:
+          python-version: '3.13'
+
+      - name: Install uv
+        uses: astral-sh/setup-uv@d0cc045d04ccac9d8b7881df0226f9e82c39688e  # v6
+
+      - name: Set up Node.js
+        uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020  # v4
+        with:
+          node-version: '22'
+
+      - name: Build web dashboard
+        run: cd web && npm ci && npm run build
+
+      - name: Build TUI bundle
+        run: cd ui-tui && npm ci && npm run build
+
+      - name: Bundle TUI into hermes_cli
+        run: |
+          mkdir -p hermes_cli/tui_dist
+          cp ui-tui/dist/entry.js hermes_cli/tui_dist/entry.js
+
+      - name: Verify frontend assets exist
+        run: |
+          test -f hermes_cli/web_dist/index.html || { echo "ERROR: web_dist not built"; exit 1; }
+          test -f hermes_cli/tui_dist/entry.js || { echo "ERROR: tui_dist not built"; exit 1; }
+
+      - name: Bundle install.sh into wheel
+        run: |
+          mkdir -p hermes_cli/scripts
+          cp scripts/install.sh hermes_cli/scripts/install.sh
+
+      - name: Build wheel and sdist
+        run: uv build --sdist --wheel
+
+      - name: Upload distribution artifacts
+        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4
+        with:
+          name: python-package-distributions
+          path: dist/
+
+  publish:
+    name: Publish to PyPI
+    needs: build
+    runs-on: ubuntu-latest
+    environment:
+      name: pypi
+      url: https://pypi.org/p/hermes-agent
+    permissions:
+      id-token: write  # OIDC trusted publishing
+
+    steps:
+      - name: Download distribution artifacts
+        uses: actions/download-artifact@d3f86a106a0bac45b974a628896c90dbdf5c8093  # v4
+        with:
+          name: python-package-distributions
+          path: dist/
+
+      - name: Publish to PyPI
+        uses: pypa/gh-action-pypi-publish@cef221092ed1bacb1cc03d23a2d87d1d172e277b  # v1.14.0
+        with:
+          skip-existing: true
+
+  sign:
+    name: Sign and attach to GitHub Release
+    # Only runs on tag pushes — release.py creates the GitHub Release,
+    # and workflow_dispatch won't have a matching release to attach to.
+    if: startsWith(github.ref, 'refs/tags/')
+    needs: publish
+    runs-on: ubuntu-latest
+    permissions:
+      contents: write   # attach assets to the existing release
+      id-token: write   # sigstore signing
+
+    steps:
+      - name: Download distribution artifacts
+        uses: actions/download-artifact@d3f86a106a0bac45b974a628896c90dbdf5c8093  # v4
+        with:
+          name: python-package-distributions
+          path: dist/
+
+      - name: Wait for GitHub Release to exist
+        env:
+          GITHUB_TOKEN: ${{ github.token }}
+        # release.py creates the GitHub Release after pushing the tag,
+        # but this workflow starts from the tag push — wait for it.
+        run: |
+          for i in $(seq 1 30); do
+            if gh release view "$GITHUB_REF_NAME" --repo "$GITHUB_REPOSITORY" >/dev/null 2>&1; then
+              echo "Release $GITHUB_REF_NAME found"
+              exit 0
+            fi
+            echo "Waiting for release... ($i/30)"
+            sleep 10
+          done
+          echo "::warning::Release $GITHUB_REF_NAME not found after 5 minutes — skipping signature upload"
+          echo "skip_sign=true" >> "$GITHUB_ENV"
+
+      - name: Sign with Sigstore
+        if: env.skip_sign != 'true'
+        uses: sigstore/gh-action-sigstore-python@f514d46b907ebcd5bedc05145c03b69c1edd8b46  # v3.0.0
+        with:
+          inputs: >-
+            ./dist/*.tar.gz
+            ./dist/*.whl
+
+      - name: Attach signed artifacts to GitHub Release
+        if: env.skip_sign != 'true'
+        env:
+          GITHUB_TOKEN: ${{ github.token }}
+        # release.py already created the GitHub Release — just upload
+        # the Sigstore signatures alongside the existing assets.
+        run: >-
+          gh release upload
+          "$GITHUB_REF_NAME" dist/*.sigstore.json
+          --repo "$GITHUB_REPOSITORY"
+          --clobber
diff --git a/.github/workflows/uv-lockfile-check.yml b/.github/workflows/uv-lockfile-check.yml
new file mode 100644
index 000000000..190a16253
--- /dev/null
+++ b/.github/workflows/uv-lockfile-check.yml
@@ -0,0 +1,119 @@
+name: uv.lock check
+
+# Verify uv.lock is in sync with pyproject.toml.  Blocking check — PRs
+# that modify pyproject.toml without regenerating uv.lock (or vice versa)
+# must not merge, because the Docker build's `uv sync --frozen` step will
+# fail on a stale lockfile and we'd rather catch it here than in the
+# docker-publish workflow on main.
+#
+# ─────────────────────────────────────────────────────────────────────────
+# IMPORTANT: this check runs against the MERGED state, not just your branch
+# ─────────────────────────────────────────────────────────────────────────
+#
+# For `pull_request` events, GitHub checks out `refs/pull/<N>/merge` by
+# default — a synthetic commit that merges your PR branch into the CURRENT
+# state of `main`.  That means the pyproject.toml evaluated here is
+# `main's pyproject.toml + your PR's changes to pyproject.toml`, not just
+# what's on your branch.
+#
+# Failure mode this creates: if `main` has advanced since you branched
+# (e.g. someone merged a PR that added a dep to pyproject.toml + its
+# corresponding uv.lock entries), your branch's uv.lock is missing those
+# new entries.  `uv lock --check` resolves against the merged pyproject
+# and sees a lockfile that doesn't cover all the current deps → fails
+# with "The lockfile at uv.lock needs to be updated."
+#
+# This can be confusing: `uv lock --check` passes locally (your branch
+# is internally consistent) but fails in CI (merged state isn't).
+#
+# Fix is to sync your branch with main and regenerate the lockfile:
+#
+#     git fetch origin main
+#     git rebase origin/main      # or merge, whatever the repo prefers
+#     uv lock                     # regenerates uv.lock against new pyproject.toml
+#     git add uv.lock
+#     git commit -m "chore: refresh uv.lock after rebase onto main"
+#     git push --force-with-lease # if you rebased
+#
+# If you also changed pyproject.toml in your PR, `uv lock` handles that
+# at the same time — one regeneration covers both your changes and the
+# drift from main.
+#
+# This is the correct behavior!  The check is protecting main's Docker
+# build: a post-merge build would see the same merged state and fail
+# the same way.  Better to catch it here than after merge.
+
+on:
+  push:
+    branches: [main]
+    paths:
+      - 'pyproject.toml'
+      - 'uv.lock'
+      - '.github/workflows/uv-lockfile-check.yml'
+  pull_request:
+    branches: [main]
+    paths:
+      - 'pyproject.toml'
+      - 'uv.lock'
+      - '.github/workflows/uv-lockfile-check.yml'
+
+permissions:
+  contents: read
+
+concurrency:
+  group: uv-lockfile-check-${{ github.event.pull_request.number || github.ref }}
+  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
+
+jobs:
+  check:
+    name: uv lock --check
+    runs-on: ubuntu-latest
+    timeout-minutes: 5
+    steps:
+      - name: Checkout code
+        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5  # v4
+
+      - name: Install uv
+        uses: astral-sh/setup-uv@d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86  # v5
+
+      # `uv lock --check` re-resolves the project from pyproject.toml and
+      # compares the result to uv.lock, exiting non-zero if they disagree.
+      # No network writes, no file modifications.
+      #
+      # On PRs this runs against the merge commit (see comment at the top
+      # of this file) — failures often mean "your branch is behind main,
+      # rebase and regenerate uv.lock."
+      - name: Verify uv.lock is up-to-date
+        run: |
+          if ! uv lock --check; then
+            cat <<'EOF' >> "$GITHUB_STEP_SUMMARY"
+          ## ❌ uv.lock is out of sync with pyproject.toml
+
+          **If this is a PR:** this check runs against the merged state
+          (your branch + current `main`), not just your branch.  If
+          `uv lock --check` passes locally, your branch is likely behind
+          `main` — recent changes to `pyproject.toml` on `main` aren't
+          reflected in your branch's `uv.lock` yet.
+
+          To fix, sync with main and regenerate the lockfile:
+
+          ```bash
+          git fetch origin main
+          git rebase origin/main   # or `git merge origin/main`
+          uv lock                  # regenerate against new pyproject.toml
+          git add uv.lock
+          git commit -m "chore: refresh uv.lock after syncing with main"
+          git push --force-with-lease  # drop --force-with-lease if you merged
+          ```
+
+          **If you only changed pyproject.toml:** run `uv lock` locally
+          and commit the result.
+
+          This check is blocking because the Docker image build uses
+          `uv sync --frozen --extra all`, which rejects stale lockfiles
+          — catching it here avoids a ~15 min failed docker-publish run
+          on `main` post-merge.
+          EOF
+            echo "::error title=uv.lock out of sync::Run \`uv lock\` locally and commit the result. If on a PR, sync with main first."
+            exit 1
+          fi
diff --git a/.gitignore b/.gitignore
index 6ae86265a..37b1f602c 100644
--- a/.gitignore
+++ b/.gitignore
@@ -70,3 +70,6 @@ mini-swe-agent/
 result
 website/static/api/skills-index.json
 models-dev-upstream/
+hermes_cli/tui_dist/*
+hermes_cli/scripts/
+docs/superpowers/*
\ No newline at end of file
diff --git a/.gitmodules b/.gitmodules
deleted file mode 100644
index 76580d6e8..000000000
--- a/.gitmodules
+++ /dev/null
@@ -1,3 +0,0 @@
-[submodule "tinker-atropos"]
-	path = tinker-atropos
-	url = https://github.com/nousresearch/tinker-atropos
diff --git a/AGENTS.md b/AGENTS.md
index b77a1d269..7c324f503 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -42,6 +42,7 @@ hermes-agent/
 ├── plugins/              # Plugin system (see "Plugins" section below)
 │   ├── memory/           # Memory-provider plugins (honcho, mem0, supermemory, ...)
 │   ├── context_engine/   # Context-engine plugins
+│   ├── model-providers/  # Inference backend plugins (openrouter, anthropic, gmi, ...)
 │   ├── kanban/           # Multi-agent board dispatcher + worker plugin
 │   ├── hermes-achievements/  # Gamified achievement tracking
 │   ├── observability/    # Metrics / traces / logs plugin
@@ -55,7 +56,6 @@ hermes-agent/
 ├── tui_gateway/          # Python JSON-RPC backend for the TUI
 ├── acp_adapter/          # ACP server (VS Code / Zed / JetBrains integration)
 ├── cron/                 # Scheduler — jobs.py, scheduler.py
-├── environments/         # RL training environments (Atropos)
 ├── scripts/              # run_tests.sh, release.py, auxiliary scripts
 ├── website/              # Docusaurus docs site
 └── tests/                # Pytest suite (~17k tests across ~900 files as of May 2026)
@@ -308,6 +308,29 @@ The registry handles schema collection, dispatch, availability checking, and err
 
 ---
 
+## Dependency Pinning Policy
+
+All dependencies must have upper bounds to limit supply-chain attack surface.
+This policy was established after the litellm compromise (PR #2796, #2810) and
+reinforced after the Mini Shai-Hulud worm campaign (May 2026).
+
+| Source type | Treatment | Example |
+|---|---|---|
+| PyPI package | `>=floor,<next_major` | `"httpx>=0.28.1,<1"` |
+| Git URL | Commit SHA | `git+https://...@<40-char-sha>` |
+| GitHub Actions | Commit SHA + comment | `uses: actions/checkout@<sha>  # v4` |
+| CI-only pip | `==exact` | `pyyaml==6.0.2` |
+
+**When adding a new dependency to `pyproject.toml`:**
+1. Pin to `>=current_version,<next_major` for post-1.0 (e.g. `>=1.5.0,<2`).
+2. For pre-1.0 packages, use `<0.(current_minor + 2)` (e.g. `>=0.29,<0.32`).
+3. Never commit a bare `>=X.Y.Z` without a ceiling — CI and reviewers will reject it.
+4. Run `uv lock` to regenerate `uv.lock` with hashes.
+
+Reference: #2810 (bounds pass), #9801 (SHA pinning + audit CI).
+
+---
+
 ## Adding Configuration
 
 ### config.yaml options:
@@ -512,12 +535,52 @@ generic plugin surface (new hook, new ctx method) — never hardcode
 plugin-specific logic into core. PR #5295 removed 95 lines of hardcoded
 honcho argparse from `main.py` for exactly this reason.
 
+**No new in-tree memory providers (policy, May 2026):** the set of
+built-in memory providers under `plugins/memory/` is closed. New memory
+backends must ship as **standalone plugin repos** that users install
+into `~/.hermes/plugins/` (or via pip entry points) — they implement
+the same `MemoryProvider` ABC, register through the same discovery
+path, and integrate via `hermes memory setup` / `post_setup()` without
+landing in this tree. PRs that add a new directory under
+`plugins/memory/` will be closed with a pointer to publish the
+provider as its own repo. Existing in-tree providers stay; bug fixes
+to them are welcome.
+
+### Model-provider plugins (`plugins/model-providers/<name>/`)
+
+Every inference backend (openrouter, anthropic, gmi, deepseek, nvidia, …)
+ships as a plugin here. Each plugin's `__init__.py` calls
+`providers.register_provider(ProviderProfile(...))` at module load.
+`providers/__init__.py._discover_providers()` is a **lazy, separate
+discovery system** — scanned on first `get_provider_profile()` or
+`list_providers()` call, NOT by the general PluginManager.
+
+Scan order:
+1. Bundled: `<repo>/plugins/model-providers/<name>/`
+2. User: `$HERMES_HOME/plugins/model-providers/<name>/`
+3. Legacy: `<repo>/providers/<name>.py` (back-compat)
+
+User plugins of the same name override bundled ones — `register_provider()`
+is last-writer-wins. This lets third parties swap out any built-in
+profile without a repo patch.
+
+The general PluginManager records `kind: model-provider` manifests but does
+NOT import them (would double-instantiate `ProviderProfile`). Plugins
+without an explicit `kind:` get auto-coerced via a source-text heuristic
+(`register_provider` + `ProviderProfile` in `__init__.py`).
+
+Full authoring guide: `website/docs/developer-guide/model-provider-plugin.md`.
+
 ### Dashboard / context-engine / image-gen plugin directories
 
-`plugins/context_engine/`, `plugins/image_gen/`, `plugins/example-dashboard/`,
-etc. follow the same pattern (ABC + orchestrator + per-plugin directory).
-Context engines plug into `agent/context_engine.py`; image-gen providers
-into `agent/image_gen_provider.py`.
+`plugins/context_engine/`, `plugins/image_gen/`, etc. follow the same
+pattern (ABC + orchestrator + per-plugin directory). Context engines
+plug into `agent/context_engine.py`; image-gen providers into
+`agent/image_gen_provider.py`. Reference / docs-companion plugins
+(`example-dashboard`, `strike-freedom-cockpit`, `plugin-llm-example`,
+`plugin-llm-async-example`) live in the
+[`hermes-example-plugins`](https://github.com/NousResearch/hermes-example-plugins)
+companion repo, not in this tree.
 
 ---
 
@@ -550,6 +613,86 @@ during setup, injected at load time).
 Top-level `tags:` and `category:` are also accepted and mirrored from
 `metadata.hermes.*` by the loader.
 
+### Skill authoring standards (HARDLINE)
+
+Every new or modernized skill — bundled, optional, or contributed —
+must meet these standards before merge. Reviewers reject PRs that
+violate them.
+
+1. **`description` ≤ 60 characters, one sentence, ends with a period.**
+   Long descriptions bloat skill listings and dilute the model's
+   attention when many skills are loaded. State the capability, not
+   the implementation. No marketing words ("powerful",
+   "comprehensive", "seamless", "advanced"). Don't repeat the skill
+   name. Verify with:
+   ```python
+   import re, pathlib
+   m = re.search(r'^description: (.*)$',
+                 pathlib.Path('skills/<cat>/<name>/SKILL.md').read_text(),
+                 re.MULTILINE)
+   assert len(m.group(1)) <= 60, len(m.group(1))
+   ```
+
+2. **Tools referenced in SKILL.md prose must be native Hermes tools or
+   MCP servers the skill explicitly expects.** When the skill needs a
+   capability, point at the proper tool by name in backticks
+   (`` `terminal` ``, `` `web_extract` ``, `` `read_file` ``,
+   `` `patch` ``, `` `search_files` ``, `` `vision_analyze` ``,
+   `` `browser_navigate` ``, `` `delegate_task` ``, etc.). Do NOT
+   name shell utilities the agent already has wrapped — `grep` →
+   `search_files`, `cat`/`head`/`tail` → `read_file`, `sed`/`awk` →
+   `patch`, `find`/`ls` → `search_files target='files'`. If the skill
+   depends on an MCP server, name the MCP server and document the
+   expected setup in `## Prerequisites`. Anything else (third-party
+   CLIs, shell pipelines, etc.) is fair game inside script files but
+   should not be the headline interaction surface in the prose.
+
+3. **`platforms:` gating audited against actual script imports.**
+   Skills that use POSIX-only primitives (`fcntl`, `termios`,
+   `os.setsid`, `os.kill(pid, 0)` for liveness, `/proc`, `/tmp`
+   hardcoded, `signal.SIGKILL`, bash heredocs, `osascript`, `apt`,
+   `systemctl`) must declare their supported platforms. Default
+   posture: try to fix it cross-platform first — `tempfile.gettempdir`,
+   `pathlib.Path`, `psutil.pid_exists`, Python-level filtering instead
+   of `grep`. Gate to a narrower set only when the dependency is
+   genuinely platform-bound.
+
+4. **`author` credits the human contributor first.** For external
+   contributions, the contributor's real name + GitHub handle goes
+   first; "Hermes Agent" is the secondary collaborator. If the
+   contributor's commit shows "Hermes Agent" as author (because they
+   used Hermes to draft the skill), replace it with their actual name
+   — credit the human, not the tool.
+
+5. **SKILL.md body uses the modern section order.** `# <Skill> Skill`
+   title, 2-3 sentence intro stating what it does and doesn't do,
+   `## When to Use`, `## Prerequisites`, `## How to Run`,
+   `## Quick Reference`, `## Procedure`, `## Pitfalls`,
+   `## Verification`. Target ~200 lines for a complex skill,
+   ~100 lines for a simple one. Cut redundant intro fluff, marketing
+   prose, and re-explanations of env vars already in
+   `## Prerequisites`.
+
+6. **Scripts go in `scripts/`, references in `references/`,
+   templates in `templates/`.** Don't expect the model to inline-write
+   parsers, XML walkers, or non-trivial logic every call — ship a
+   helper script. Reference it from SKILL.md by path relative to the
+   skill directory.
+
+7. **Tests live at `tests/skills/test_<skill>_skill.py`** and use only
+   stdlib + pytest + `unittest.mock`. No live network calls. Run via
+   `scripts/run_tests.sh tests/skills/test_<skill>_skill.py -q`.
+
+8. **`.env.example` additions are isolated to a clearly delimited
+   block.** Don't touch the surrounding file — contributor-supplied
+   `.env.example` versions are usually stale and edits outside the
+   skill's own block must be dropped during salvage.
+
+The full salvage / modernization checklist for external skill PRs
+lives in the `hermes-agent-dev` skill at
+`references/new-skill-pr-salvage.md` — load it before polishing
+contributor skill PRs.
+
 ---
 
 ## Toolsets
diff --git a/CONTRIBUTING.md b/CONTRIBUTING.md
index 30d171543..36b1e9df2 100644
--- a/CONTRIBUTING.md
+++ b/CONTRIBUTING.md
@@ -49,6 +49,24 @@ If your skill is specialized, community-contributed, or niche, it's better suite
 
 ---
 
+## Memory Providers: Ship as a Standalone Plugin
+
+**We are no longer accepting new memory providers into this repo.** The set of built-in providers under `plugins/memory/` (honcho, mem0, supermemory, byterover, hindsight, holographic, openviking, retaindb) is closed. If you want to add a new memory backend, publish it as a **standalone plugin repo** that users install into `~/.hermes/plugins/` (or via a pip entry point).
+
+Standalone memory plugins:
+
+- Implement the same `MemoryProvider` ABC (`agent/memory_provider.py`) — `sync_turn`, `prefetch`, `shutdown`, and optionally `post_setup(hermes_home, config)` for setup-wizard integration
+- Use the same discovery system — `discover_memory_providers()` picks them up from user/project plugin directories and pip entry points
+- Integrate with `hermes memory setup` via `post_setup()` — no need to touch core code
+- Can register their own CLI subcommands via `register_cli(subparser)` in a `cli.py` file
+- Get all the same lifecycle hooks and config plumbing as in-tree providers
+
+PRs that add a new directory under `plugins/memory/` will be closed with a pointer to publish the provider as its own repo. Existing in-tree providers stay; bug fixes to them are welcome.
+
+This isn't a quality bar — it's a coupling-and-maintenance decision. Memory providers are the most common plugin type and they shouldn't all live in this tree.
+
+---
+
 ## Development Setup
 
 ### Prerequisites
@@ -73,9 +91,6 @@ export VIRTUAL_ENV="$(pwd)/venv"
 # Install with all extras (messaging, cron, CLI menus, dev tools)
 uv pip install -e ".[all,dev]"
 
-# Optional: RL training submodule
-# git submodule update --init tinker-atropos && uv pip install -e "./tinker-atropos"
-
 # Optional: browser tools
 npm install
 ```
@@ -106,6 +121,11 @@ hermes chat -q "Hello"
 ### Run tests
 
 ```bash
+# Preferred — matches CI (hermetic env, 4 xdist workers); see AGENTS.md
+scripts/run_tests.sh
+
+# Alternative (activate the venv first). The wrapper is still recommended
+# for parity with GitHub Actions before you open a PR:
 pytest tests/ -v
 ```
 
@@ -173,7 +193,6 @@ hermes-agent/
 │
 ├── skills/                   # Bundled skills (copied to ~/.hermes/skills/ on install)
 ├── optional-skills/          # Official optional skills (discoverable via hub, not activated by default)
-├── environments/             # RL training environments (Atropos integration)
 ├── tests/                    # Test suite
 ├── website/                  # Documentation site (hermes-agent.nousresearch.com)
 │
@@ -286,16 +305,18 @@ registry.register(
 )
 ```
 
-Then add the import to `model_tools.py` in the `_modules` list:
+**Wire into a toolset (required):** Built-in tools are auto-discovered: any
+`tools/*.py` file that contains a top-level `registry.register(...)` call is
+imported by `discover_builtin_tools()` in `tools/registry.py` when `model_tools`
+loads. There is **no** manual import list in `model_tools.py` to maintain.
 
-```python
-_modules = [
-    # ... existing modules ...
-    "tools.my_tool",
-]
-```
+You must still add the tool name to the appropriate list in `toolsets.py`
+(for example `_HERMES_CORE_TOOLS` or a dedicated toolset); otherwise the tool
+registers but is never exposed to the agent. If you introduce a new toolset,
+add it in `toolsets.py` and wire it into the relevant platform presets.
 
-If it's a new toolset, add it to `toolsets.py` and to the relevant platform presets.
+See `AGENTS.md` (section **Adding New Tools**) for profile-aware paths and
+plugin vs core guidance.
 
 ---
 
@@ -454,6 +475,58 @@ Gateway and messaging sessions never collect secrets in-band; they instruct the
 
 See `skills/gifs/gif-search/` and `skills/email/himalaya/` for examples.
 
+### Skill authoring standards (HARDLINE)
+
+Every new or modernized skill — bundled, optional, or contributed — must meet these standards before merge. Reviewers reject PRs that violate them.
+
+1. **`description` ≤ 60 characters, one sentence, ends with a period.** Long descriptions bloat the skill listing UI and dilute the model's attention when many skills are loaded. State the capability, not the implementation. No marketing words ("powerful", "comprehensive", "seamless", "advanced"). Don't repeat the skill name. Verify with:
+   ```python
+   import re, pathlib
+   m = re.search(r'^description: (.*)$',
+                 pathlib.Path('skills/<cat>/<name>/SKILL.md').read_text(),
+                 re.MULTILINE)
+   assert len(m.group(1)) <= 60, len(m.group(1))
+   ```
+
+   Good: `Search arXiv papers by keyword, author, category, or ID.`
+   Bad: `A powerful and comprehensive skill that allows the agent to search arXiv for relevant academic papers using various criteria including keywords, authors, and categories.`
+
+2. **Tools referenced in SKILL.md prose must be native Hermes tools or MCP servers the skill explicitly expects.** When the skill needs a capability, point at the proper tool by name in backticks: `` `terminal` ``, `` `web_extract` ``, `` `web_search` ``, `` `read_file` ``, `` `write_file` ``, `` `patch` ``, `` `search_files` ``, `` `vision_analyze` ``, `` `browser_navigate` ``, `` `delegate_task` ``, `` `image_generate` ``, `` `text_to_speech` ``, `` `cronjob` ``, `` `memory` ``, `` `skill_view` ``, `` `todo` ``, `` `execute_code` ``.
+
+   Do NOT name shell utilities the agent already has wrapped:
+
+   | Don't say | Say |
+   |---|---|
+   | `grep`, `rg` | `search_files` |
+   | `cat`, `head`, `tail` | `read_file` |
+   | `sed`, `awk` | `patch` |
+   | `find`, `ls` | `search_files` (with `target='files'`) |
+   | `curl` for content extraction | `web_extract` |
+   | `echo > file`, `cat <<EOF` | `write_file` |
+
+   If the skill depends on an MCP server, name the MCP server and document its setup in `## Prerequisites`. Third-party CLIs (e.g. `ffmpeg`, `gh`, a specific SDK) are fine to invoke from inside script files, but the prose should frame the interaction as "invoke through the `terminal` tool", not as a manual shell session.
+
+3. **`platforms:` gating audited against actual script imports.** Skills that use POSIX-only primitives (`fcntl`, `termios`, `os.setsid`, `os.kill(pid, 0)` for liveness, `/proc`, hardcoded `/tmp` paths, `signal.SIGKILL`, bash heredocs, `osascript`, `apt`, `systemctl`) must declare their supported platforms via the `platforms:` frontmatter. Default posture is to fix it cross-platform first — `tempfile.gettempdir()`, `pathlib.Path`, `psutil.pid_exists()`, Python-level filtering instead of `grep`. Gate to a narrower set only when the dependency is genuinely platform-bound (e.g. `osascript` is macOS-only, `/proc` is Linux-only).
+
+4. **`author` credits the human contributor first.** For external contributions, the contributor's real name + GitHub handle goes first (`Jane Doe (jane-doe)`); "Hermes Agent" is the secondary collaborator. If the contributor's commit shows "Hermes Agent" as author because they used Hermes to draft the skill, replace it with their actual name — credit the human, not the tool.
+
+5. **SKILL.md body uses the modern section order.** `# <Skill> Skill` title, 2-3 sentence intro stating what it does and what it doesn't do, then:
+   - `## When to Use` — trigger conditions
+   - `## Prerequisites` — env vars, install steps, MCP setup, API key sourcing
+   - `## How to Run` — canonical invocation through the `terminal` tool
+   - `## Quick Reference` — flat command/API reference
+   - `## Procedure` — numbered steps with copy-paste commands
+   - `## Pitfalls` — known limits, rate limits, things that look broken but aren't
+   - `## Verification` — single command that proves the skill works
+
+   Target ~200 lines for a complex skill, ~100 lines for a simple one. Cut redundant intro fluff, marketing prose, and re-explanations of env vars already documented in `## Prerequisites`.
+
+6. **Scripts go in `scripts/`, references in `references/`, templates in `templates/`.** Don't expect the model to inline-write parsers, XML walkers, or non-trivial logic every call — ship a helper script. Reference scripts from SKILL.md by path relative to the skill directory.
+
+7. **Tests live at `tests/skills/test_<skill>_skill.py`** and use only stdlib + pytest + `unittest.mock`. No live network calls. Run via `scripts/run_tests.sh tests/skills/test_<skill>_skill.py -q`. Must pass under the hermetic CI env (no API keys leaking through). Use `monkeypatch` and `tmp_path` for any env-var or filesystem dependencies.
+
+8. **`.env.example` additions are isolated to a clearly delimited block.** Don't touch the surrounding file — contributor-supplied `.env.example` versions are usually stale, and edits outside the skill's own block will be dropped during salvage. Comment all values with `#` (it's documentation, not live config).
+
 ### Skill guidelines
 
 - **No external dependencies unless absolutely necessary.** Prefer stdlib Python, curl, and existing Hermes tools (`web_extract`, `terminal`, `read_file`).
@@ -515,11 +588,57 @@ See `hermes_cli/skin_engine.py` for the full schema and existing skins as exampl
 
 ## Cross-Platform Compatibility
 
-Hermes runs on Linux, macOS, and WSL2 on Windows. When writing code that touches the OS:
+Hermes runs on Linux, macOS, and native Windows (plus WSL2). When writing code
+that touches the OS, assume *any* platform can hit your code path.
+
+> **Before you PR:** run `scripts/check-windows-footguns.py` to catch the
+> common Windows-unsafe patterns in your diff. It's grep-based and cheap;
+> CI runs it on every PR too.
 
 ### Critical rules
 
-1. **`termios` and `fcntl` are Unix-only.** Always catch both `ImportError` and `NotImplementedError`:
+1. **Never call `os.kill(pid, 0)` for liveness checks.** `os.kill(pid, 0)`
+   is a standard POSIX idiom to check "is this PID alive" — the signal 0
+   is a no-op permission check. **On Windows it is NOT a no-op.** Python's
+   Windows `os.kill` maps `sig=0` to `CTRL_C_EVENT` (they collide at the
+   integer value 0) and routes it through `GenerateConsoleCtrlEvent(0, pid)`,
+   which broadcasts Ctrl+C to the **entire console process group** containing
+   the target PID. "Probe if alive" silently becomes "kill the target and
+   often unrelated processes sharing its console." See [bpo-14484](https://bugs.python.org/issue14484)
+   (open since 2012 — will never be fixed for compat reasons).
+
+   **Preferred:** use `psutil` (a core dependency — always available):
+
+   ```python
+   import psutil
+   if psutil.pid_exists(pid):
+       # process is alive — safe on every platform
+       ...
+   ```
+
+   If you specifically need the hermes wrapper (it has a stdlib fallback
+   for scaffold-phase imports before pip install finishes), use
+   `gateway.status._pid_exists(pid)`. It calls `psutil.pid_exists` first
+   and falls back to a hand-rolled `OpenProcess + WaitForSingleObject`
+   dance on Windows only when psutil is somehow missing.
+
+   Audit grep for new callsites: `rg "os\.kill\([^,]+,\s*0\s*\)"`. Any hit
+   in non-test code is presumptively a Windows silent-kill bug.
+
+2. **Use `shutil.which()` before shelling out — don't assume Windows has
+   tools Linux has.** `wmic` was removed in Windows 10 21H1 and later. `ps`,
+   `kill`, `grep`, `awk`, `fuser`, `lsof`, `pgrep`, and most POSIX CLI tools
+   simply don't exist on Windows. Test availability with
+   `shutil.which("tool")` and fall back to a Windows-native equivalent —
+   usually PowerShell via `subprocess.run(["powershell", "-NoProfile",
+   "-Command", ...])`.
+
+   For process enumeration: PowerShell's `Get-CimInstance Win32_Process` is
+   the modern replacement for `wmic process`. See
+   `hermes_cli/gateway.py::_scan_gateway_pids` for the pattern.
+
+3. **`termios` and `fcntl` are Unix-only.** Always catch both `ImportError`
+   and `NotImplementedError`:
    ```python
    try:
        from simple_term_menu import TerminalMenu
@@ -532,24 +651,126 @@ Hermes runs on Linux, macOS, and WSL2 on Windows. When writing code that touches
        idx = int(input("Choice: ")) - 1
    ```
 
-2. **File encoding.** Windows may save `.env` files in `cp1252`. Always handle encoding errors:
+4. **File encoding.** Windows may save `.env` files in `cp1252`. Always
+   handle encoding errors:
    ```python
    try:
        load_dotenv(env_path)
    except UnicodeDecodeError:
        load_dotenv(env_path, encoding="latin-1")
    ```
+   Config files (`config.yaml`) may be saved with a UTF-8 BOM by Notepad and
+   similar editors — use `encoding="utf-8-sig"` when reading files that
+   could have been touched by a Windows GUI editor.
 
-3. **Process management.** `os.setsid()`, `os.killpg()`, and signal handling differ on Windows. Use platform checks:
+5. **Process management.** `os.setsid()`, `os.killpg()`, `os.fork()`,
+   `os.getuid()`, and POSIX signal handling differ on Windows. Guard with
+   `platform.system()`, `sys.platform`, or `hasattr(os, "setsid")`:
    ```python
-   import platform
    if platform.system() != "Windows":
        kwargs["preexec_fn"] = os.setsid
+   else:
+       kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    ```
 
-4. **Path separators.** Use `pathlib.Path` instead of string concatenation with `/`.
+   **Preferred:** for killing a process AND its children (what `os.killpg`
+   does on POSIX), use `psutil` — it works on every platform:
+   ```python
+   import psutil
+   try:
+       parent = psutil.Process(pid)
+       # Kill children first (leaf-up), then the parent.
+       for child in parent.children(recursive=True):
+           child.kill()
+       parent.kill()
+   except psutil.NoSuchProcess:
+       pass
+   ```
 
-5. **Shell commands in installers.** If you change `scripts/install.sh`, check if the equivalent change is needed in `scripts/install.ps1`.
+6. **Signals that don't exist on Windows: `SIGALRM`, `SIGCHLD`, `SIGHUP`,
+   `SIGUSR1`, `SIGUSR2`, `SIGPIPE`, `SIGQUIT`, `SIGKILL`.** Python's
+   `signal` module raises `AttributeError` at import time if you reference
+   them on Windows. Use `getattr(signal, "SIGKILL", signal.SIGTERM)` or
+   gate the whole block behind a platform check. `loop.add_signal_handler`
+   raises `NotImplementedError` on Windows — always catch it.
+
+7. **Path separators.** Use `pathlib.Path` instead of string concatenation
+   with `/`. Forward slashes work almost everywhere on Windows, but
+   `subprocess.run(["cmd.exe", "/c", ...])` and other shell contexts can
+   require backslashes — convert with `str(path)` at the subprocess boundary,
+   not inside Python logic.
+
+8. **Symlinks need elevated privileges on Windows** (unless Developer Mode is
+   on). Tests that create symlinks need `@pytest.mark.skipif(sys.platform ==
+   "win32", reason="Symlinks require elevated privileges on Windows")`.
+
+9. **POSIX file modes (0o600, 0o644, etc.) are NOT enforced on NTFS** by
+   default. Tests that assert on `stat().st_mode & 0o777` must skip on
+   Windows — the concept doesn't translate. Use ACLs (`icacls`, `pywin32`)
+   for Windows secret-file protection if needed.
+
+10. **Detached background daemons on Windows need `pythonw.exe`, NOT
+    `python.exe`.** `python.exe` always allocates or attaches to a console,
+    which makes it vulnerable to `CTRL_C_EVENT` broadcasts from any sibling
+    process. `pythonw.exe` is the no-console variant. Combine with
+    `CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP |
+    CREATE_BREAKAWAY_FROM_JOB` in `subprocess.Popen(creationflags=...)`.
+    See `hermes_cli/gateway_windows.py::_spawn_detached` for the reference
+    implementation.
+
+11. **`subprocess.Popen` with `.cmd` or `.bat` shims needs `shutil.which`
+    to resolve.** Passing `"agent-browser"` to `Popen` on Windows finds
+    the extensionless POSIX shebang shim in `node_modules/.bin/`, which
+    `CreateProcessW` can't execute — you'll get `WinError 193 "not a valid
+    Win32 application"`. Use `shutil.which("agent-browser", path=local_bin)`
+    which honors PATHEXT and picks the `.CMD` variant on Windows.
+
+12. **Don't use shell shebangs as a way to run Python.** `#!/usr/bin/env
+    python` only works when the file is executed through a Unix shell.
+    `subprocess.run(["./myscript.py"])` on Windows fails even if the file
+    has a shebang line. Always invoke Python explicitly:
+    `[sys.executable, "myscript.py"]`.
+
+13. **Shell commands in installers.** If you change `scripts/install.sh`,
+    make the equivalent change in `scripts/install.ps1`. The two scripts
+    are the canonical example of "works on Linux does not mean works on
+    Windows" and have drifted multiple times — keep them in lockstep.
+
+14. **Known paths that are OneDrive-redirected on Windows:** Desktop,
+    Documents, Pictures, Videos. The "real" path when OneDrive Backup is
+    enabled is `%USERPROFILE%\OneDrive\Desktop` (etc.), NOT
+    `%USERPROFILE%\Desktop` (which exists as an empty husk). Resolve the
+    real location via `ctypes` + `SHGetKnownFolderPath` or by reading the
+    `Shell Folders` registry key — never assume `~/Desktop`.
+
+15. **CRLF vs LF in generated scripts.** Windows `cmd.exe` and `schtasks`
+    parse line-by-line; mixed or LF-only line endings can break multi-line
+    `.cmd` / `.bat` files. Use `open(path, "w", encoding="utf-8",
+    newline="\r\n")` — or `open(path, "wb")` + explicit bytes — when
+    generating scripts Windows will execute.
+
+16. **Two different quoting schemes in one command line.** `subprocess.run
+    (["schtasks", "/TR", some_cmd])` → schtasks itself parses `/TR`, AND
+    the `some_cmd` string is re-parsed by `cmd.exe` when the task fires.
+    Different parsers, different escape rules. Use two separate quoting
+    helpers and never cross them. See `hermes_cli/gateway_windows.py::
+    _quote_cmd_script_arg` and `_quote_schtasks_arg` for the reference
+    pair.
+
+### Testing cross-platform
+
+Tests that use POSIX-only syscalls need a skip marker. Common ones:
+- Symlinks → `@pytest.mark.skipif(sys.platform == "win32", ...)`
+- `0o600` file modes → `@pytest.mark.skipif(sys.platform.startswith("win"), ...)`
+- `signal.SIGALRM` → Unix-only (see `tests/conftest.py::_enforce_test_timeout`)
+- `os.setsid` / `os.fork` → Unix-only
+- Live Winsock / Windows-specific regression tests →
+  `@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific regression")`
+
+If you monkeypatch `sys.platform` for cross-platform tests, also patch
+`platform.system()` / `platform.release()` / `platform.mac_ver()` — each
+re-reads the real OS independently, so half-patched tests still route
+through the wrong branch on a Windows runner.
 
 ---
 
@@ -579,6 +800,47 @@ Hermes has terminal access. Security matters.
 
 If your PR affects security, note it explicitly in the description.
 
+### Dependency pinning policy (supply chain hardening)
+
+After the [litellm supply chain compromise](https://github.com/BerriAI/litellm/issues/24512) in March 2026 and the [Mini Shai-Hulud worm campaign](https://socket.dev/blog/tanstack-npm-packages-compromised-mini-shai-hulud-supply-chain-attack) in May 2026, all dependencies must follow these rules:
+
+| Source type | Required treatment | Rationale |
+|---|---|---|
+| **PyPI package** | `>=floor,<next_major` | PyPI versions are immutable once published, but new versions can be pushed into your range. A `<next_major` ceiling stops a 1.x install from upgrading to a malicious 2.0.0. |
+| **Git URL** (atroposlib, tinker, yc-bench, Baileys) | Full commit SHA | Branches and tags are mutable refs; SHA is content-addressed. |
+| **GitHub Actions** | Full commit SHA + version comment | Action tags are mutable refs (e.g. tj-actions/changed-files March 2025). Pin as `uses: owner/action@<sha>  # vX.Y.Z` |
+| **CI-only pip installs** | `==exact` | Hermetic CI builds; churn is acceptable. |
+
+**Every new PyPI dependency in a PR must have a `<next_major` upper bound.** PRs adding unbounded `>=X.Y.Z` specs will be rejected by reviewers. The `supply-chain-audit.yml` CI workflow also flags dependency manifest changes for manual review.
+
+**How to determine the ceiling:**
+- If the package is at version `1.x.y`, use `<2`.
+- If the package is at version `0.x.y` (pre-1.0), use `<0.(current_minor + 2)` — e.g. if current is `0.29.x`, use `<0.32`. This gives ~2 minor versions of headroom while keeping the window small enough that a hostile takeover version is unlikely to land inside it.
+- Exception: packages with very stable APIs (e.g. `aiohttp-socks`) can use `<1` at reviewer discretion.
+
+**Examples:**
+```toml
+# ✅ Correct — post-1.0
+"openai>=2.21.0,<3"
+"pydantic>=2.12.5,<3"
+
+# ✅ Correct — pre-1.0 (tight minor window)
+"asyncpg>=0.29,<0.32"
+"aiosqlite>=0.20,<0.23"
+"hindsight-client>=0.4.22,<0.5"
+
+# ❌ Rejected — no upper bound
+"some-package>=1.2.3"
+
+# ❌ Rejected — too tight (blocks legitimate patches)
+"some-package==1.2.3"
+
+# ❌ Rejected — too loose for pre-1.0 (allows 80 minor versions)
+"some-package>=0.20,<1"
+```
+
+**Reference PRs:** #2796 (litellm removal), #2810 (upper bounds pass), #9801 (SHA pinning + supply-chain-audit CI).
+
 ---
 
 ## Pull Request Process
@@ -595,7 +857,7 @@ refactor/description   # Code restructuring
 
 ### Before submitting
 
-1. **Run tests**: `pytest tests/ -v`
+1. **Run tests**: `scripts/run_tests.sh` (recommended; same as CI) or `pytest tests/ -v` with the project venv activated
 2. **Test manually**: Run `hermes` and exercise the code path you changed
 3. **Check cross-platform impact**: If you touch file I/O, process management, or terminal handling, consider macOS, Linux, and WSL2
 4. **Keep PRs focused**: One logical change per PR. Don't mix a bug fix with a refactor with a new feature.
diff --git a/Dockerfile b/Dockerfile
index 08a5b6a27..8655c51f3 100644
--- a/Dockerfile
+++ b/Dockerfile
@@ -55,6 +55,29 @@ RUN npm install --prefer-offline --no-audit && \
     (cd ui-tui && npm install --prefer-offline --no-audit) && \
     npm cache clean --force
 
+# ---------- Layer-cached Python dependency install ----------
+# Copy only pyproject.toml + uv.lock so the Python dep resolve + wheel
+# download + native-extension compile layer is cached unless those inputs
+# change.  Before this split the Python install sat after `COPY . .`, so
+# every source-only commit re-did ~4-5 min of dep work on cold builds.
+#
+# README.md is referenced by pyproject.toml's `readme =` field, but it's
+# excluded from the build context by .dockerignore's `*.md`.  uv's build
+# frontend stats the readme path during dep resolution, so we `touch` an
+# empty placeholder — the real README is restored by `COPY . .` below.
+#
+# `uv sync --frozen --no-install-project --extra all` installs only the
+# deps reachable through the composite `[all]` extra (handpicked set
+# intended for the production image).  We do NOT use `--all-extras`:
+# that would pull in `[rl]` (atroposlib + tinker + torch + wandb from
+# git), `[yc-bench]` (another git dep), and `[termux-all]` (Android
+# redundancy), none of which belong in the published container.
+#
+# The editable link is created after the source copy below.
+COPY pyproject.toml uv.lock ./
+RUN touch ./README.md
+RUN uv sync --frozen --no-install-project --extra all
+
 # ---------- Source code ----------
 # .dockerignore excludes node_modules, so the installs above survive.
 COPY --chown=hermes:hermes . .
@@ -66,14 +89,25 @@ RUN cd web && npm run build && \
 # ---------- Permissions ----------
 # Make install dir world-readable so any HERMES_UID can read it at runtime.
 # The venv needs to be traversable too.
+# node_modules trees additionally need to be writable by the hermes user
+# so the runtime `npm install` triggered by _tui_need_npm_install() in
+# hermes_cli/main.py succeeds (see #18800). /opt/hermes/web is build-time
+# only (HERMES_WEB_DIST points at hermes_cli/web_dist) and is intentionally
+# not chowned here.
+# The .venv MUST be hermes-writable so lazy_deps.py can install platform
+# packages (discord.py, telegram, slack, etc.) at first gateway boot.
+# Without this, `uv pip install` fails with EACCES and all messaging
+# adapters silently fail to load.  See tools/lazy_deps.py.
 USER root
-RUN chmod -R a+rX /opt/hermes
+RUN chmod -R a+rX /opt/hermes && \
+    chown -R hermes:hermes /opt/hermes/.venv /opt/hermes/ui-tui /opt/hermes/node_modules
 # Start as root so the entrypoint can usermod/groupmod + gosu.
 # If HERMES_UID is unset, the entrypoint drops to the default hermes user (10000).
 
-# ---------- Python virtualenv ----------
-RUN uv venv && \
-    uv pip install --no-cache-dir -e ".[all]"
+# ---------- Link hermes-agent itself (editable) ----------
+# Deps are already installed in the cached layer above; `--no-deps` makes
+# this a fast (~1s) egg-link creation with no resolution or downloads.
+RUN uv pip install --no-cache-dir --no-deps -e "."
 
 # ---------- Runtime ----------
 ENV HERMES_WEB_DIST=/opt/hermes/hermes_cli/web_dist
diff --git a/README.md b/README.md
index 2674cabe7..abdc66245 100644
--- a/README.md
+++ b/README.md
@@ -14,7 +14,7 @@
 
 **The self-improving AI agent built by [Nous Research](https://nousresearch.com).** It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM.
 
-Use any model you want — [Nous Portal](https://portal.nousresearch.com), [OpenRouter](https://openrouter.ai) (200+ models), [NVIDIA NIM](https://build.nvidia.com) (Nemotron), [Xiaomi MiMo](https://platform.xiaomimimo.com), [z.ai/GLM](https://z.ai), [Kimi/Moonshot](https://platform.moonshot.ai), [MiniMax](https://www.minimax.io), [Hugging Face](https://huggingface.co), OpenAI, or your own endpoint. Switch with `hermes model` — no code changes, no lock-in.
+Use any model you want — [Nous Portal](https://portal.nousresearch.com), [OpenRouter](https://openrouter.ai) (200+ models), [NovitaAI](https://novita.ai) (AI-native cloud for Model API, Agent Sandbox, and GPU Cloud), [NVIDIA NIM](https://build.nvidia.com) (Nemotron), [Xiaomi MiMo](https://platform.xiaomimimo.com), [z.ai/GLM](https://z.ai), [Kimi/Moonshot](https://platform.moonshot.ai), [MiniMax](https://www.minimax.io), [Hugging Face](https://huggingface.co), OpenAI, or your own endpoint. Switch with `hermes model` — no code changes, no lock-in.
 
 <table>
 <tr><td><b>A real terminal interface</b></td><td>Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output.</td></tr>
@@ -23,22 +23,36 @@ Use any model you want — [Nous Portal](https://portal.nousresearch.com), [Open
 <tr><td><b>Scheduled automations</b></td><td>Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — all in natural language, running unattended.</td></tr>
 <tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns.</td></tr>
 <tr><td><b>Runs anywhere, not just your laptop</b></td><td>Seven terminal backends — local, Docker, SSH, Singularity, Modal, Daytona, and Vercel Sandbox. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster.</td></tr>
-<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, Atropos RL environments, trajectory compression for training the next generation of tool-calling models.</td></tr>
+<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, trajectory compression for training the next generation of tool-calling models.</td></tr>
 </table>
 
 ---
 
 ## Quick Install
 
+### Linux, macOS, WSL2, Termux
+
 ```bash
 curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
 ```
 
-Works on Linux, macOS, WSL2, and Android via Termux. The installer handles the platform-specific setup for you.
+### Windows (native, PowerShell) — Early Beta
+
+> **Heads up:** Native Windows support is **early beta**. It installs and runs, but hasn't been road-tested as broadly as our Linux/macOS/WSL2 paths. Please [file issues](https://github.com/NousResearch/hermes-agent/issues) when you hit rough edges. For the most battle-tested Windows setup today, run the Linux/macOS one-liner above inside **WSL2**.
+
+Run this in PowerShell:
+
+```powershell
+irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex
+```
+
+The installer handles everything: uv, Python 3.11, Node.js, ripgrep, ffmpeg, **and a portable Git Bash** (MinGit, unpacked to `%LOCALAPPDATA%\hermes\git` — no admin required, completely isolated from any system Git install).  Hermes uses this bundled Git Bash to run shell commands.
+
+If you already have Git installed, the installer detects it and uses that instead.  Otherwise a ~45MB MinGit download is all you need — it won't touch or interfere with any system Git.
 
 > **Android / Termux:** The tested manual path is documented in the [Termux guide](https://hermes-agent.nousresearch.com/docs/getting-started/termux). On Termux, Hermes installs a curated `.[termux]` extra because the full `.[all]` extra currently pulls Android-incompatible voice dependencies.
 >
-> **Windows:** Native Windows is not supported. Please install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run the command above.
+> **Windows:** Native Windows is supported as an **early beta** — the PowerShell one-liner above installs everything, but expect rough edges and please file issues when you hit them. If you'd rather use WSL2 (our most battle-tested Windows path), the Linux command works there too. Native Windows install lives under `%LOCALAPPDATA%\hermes`; WSL2 installs under `~/.hermes` as on Linux.  The only Hermes feature that currently needs WSL2 specifically is the browser-based dashboard chat pane (it uses a POSIX PTY — classic CLI and gateway both run natively).
 
 After installation:
 
@@ -155,14 +169,12 @@ Manual path (equivalent to the above):
 
 ```bash
 curl -LsSf https://astral.sh/uv/install.sh | sh
-uv venv venv --python 3.11
-source venv/bin/activate
+uv venv .venv --python 3.11
+source .venv/bin/activate
 uv pip install -e ".[all,dev]"
 scripts/run_tests.sh
 ```
 
-> **RL Training (optional):** The RL/Atropos integration (`environments/`) ships via the `atroposlib` and `tinker` dependencies pulled in by `.[all,dev]` — no submodule setup required.
-
 ---
 
 ## Community
@@ -170,6 +182,7 @@ scripts/run_tests.sh
 - 💬 [Discord](https://discord.gg/NousResearch)
 - 📚 [Skills Hub](https://agentskills.io)
 - 🐛 [Issues](https://github.com/NousResearch/hermes-agent/issues)
+- 🔌 [computer-use-linux](https://github.com/avifenesh/computer-use-linux) — Linux desktop-control MCP server for Hermes and other MCP hosts, with AT-SPI accessibility trees, Wayland/X11 input, screenshots, and compositor window targeting.
 - 🔌 [HermesClaw](https://github.com/AaronWong1999/hermesclaw) — Community WeChat bridge: Run Hermes Agent and OpenClaw on the same WeChat account.
 
 ---
diff --git a/README.zh-CN.md b/README.zh-CN.md
index ea7fea8dc..9a9645744 100644
--- a/README.zh-CN.md
+++ b/README.zh-CN.md
@@ -23,7 +23,7 @@
 <tr><td><b>定时自动化</b></td><td>内置 cron 调度器，支持向任何平台投递。日报、夜间备份、周审计——全部用自然语言描述，无人值守运行。</td></tr>
 <tr><td><b>委派与并行</b></td><td>生成隔离子代理处理并行工作流。编写 Python 脚本通过 RPC 调用工具，将多步管道压缩为零上下文开销的轮次。</td></tr>
 <tr><td><b>随处运行</b></td><td>六种终端后端——本地、Docker、SSH、Daytona、Singularity 和 Modal。Daytona 和 Modal 提供 Serverless 持久化——代理环境空闲时休眠、按需唤醒，空闲期间几乎零成本。$5 VPS 或 GPU 集群都能跑。</td></tr>
-<tr><td><b>研究就绪</b></td><td>批量轨迹生成、Atropos RL 环境、轨迹压缩——用于训练下一代工具调用模型。</td></tr>
+<tr><td><b>研究就绪</b></td><td>批量轨迹生成、轨迹压缩——用于训练下一代工具调用模型。</td></tr>
 </table>
 
 ---
@@ -161,12 +161,6 @@ uv pip install -e ".[all,dev]"
 python -m pytest tests/ -q
 ```
 
-> **RL 训练（可选）：** 如需参与 RL/Tinker-Atropos 集成开发：
-> ```bash
-> git submodule update --init tinker-atropos
-> uv pip install -e "./tinker-atropos"
-> ```
-
 ---
 
 ## 社区
diff --git a/RELEASE_v0.13.0.md b/RELEASE_v0.13.0.md
new file mode 100644
index 000000000..7efcb7aee
--- /dev/null
+++ b/RELEASE_v0.13.0.md
@@ -0,0 +1,641 @@
+# Hermes Agent v0.13.0 (v2026.5.7)
+
+**Release Date:** May 7, 2026
+**Since v0.12.0:** 864 commits · 588 merged PRs · 829 files changed · 128,366 insertions · 282 issues closed (13 P0, 36 P1) · 295 community contributors (including co-authors)
+
+> The Tenacity Release — Hermes Agent now finishes what it starts. Kanban ships as a durable multi-agent board (heartbeat, reclaim, zombie detection, auto-block on incomplete exit, per-task retries, hallucination recovery). `/goal` keeps the agent locked on a target across turns (Ralph loop). Checkpoints v2 rewrites state persistence with real pruning. Gateway auto-resumes interrupted sessions after restart. Cron grows a `no_agent` watchdog mode. A security wave closes 8 P0s — redaction is now ON by default, Discord role-allowlists are guild-scoped, WhatsApp rejects strangers by default, and TOCTOU windows close across auth.json and MCP OAuth. Google Chat becomes the 20th platform. Providers become a pluggable surface. Seven i18n locales ship.
+
+---
+
+## ✨ Highlights
+
+- **Multi-agent Kanban — delegate to an AI team that actually finishes** — Spin up a durable board, drop tasks on it, and let multiple Hermes workers pick them up, hand off, and close them out. Heartbeats, reclaim, zombie detection, retry budgets, and a hallucination gate keep the team honest. One install, many kanbans. ([#17805](https://github.com/NousResearch/hermes-agent/pull/17805), [#19653](https://github.com/NousResearch/hermes-agent/pull/19653), [#20232](https://github.com/NousResearch/hermes-agent/pull/20232), [#20332](https://github.com/NousResearch/hermes-agent/pull/20332), [#21330](https://github.com/NousResearch/hermes-agent/pull/21330), [#21183](https://github.com/NousResearch/hermes-agent/pull/21183), [#21214](https://github.com/NousResearch/hermes-agent/pull/21214))
+
+- **`/goal` — the agent doesn't forget what you asked it to do** — Lock the agent onto a target and it stays on task across turns. The Ralph loop as a first-class primitive. ([#18262](https://github.com/NousResearch/hermes-agent/pull/18262), [#18275](https://github.com/NousResearch/hermes-agent/pull/18275), [#21287](https://github.com/NousResearch/hermes-agent/pull/21287))
+
+- **Show it a video** — new `video_analyze` tool for native video understanding on Gemini and compatible multimodal models. (@alt-glitch) ([#19301](https://github.com/NousResearch/hermes-agent/pull/19301))
+
+- **Clone a voice** — xAI Custom Voices lands as a TTS provider with voice cloning support. (@alt-glitch) ([#18776](https://github.com/NousResearch/hermes-agent/pull/18776))
+
+- **Hermes speaks your language** — static gateway + CLI messages translate to 7 locales: Chinese, Japanese, German, Spanish, French, Ukrainian, and Turkish. Docs site gains a Chinese (zh-Hans) locale. ([#20231](https://github.com/NousResearch/hermes-agent/pull/20231), [#20329](https://github.com/NousResearch/hermes-agent/pull/20329), [#20467](https://github.com/NousResearch/hermes-agent/pull/20467), [#20474](https://github.com/NousResearch/hermes-agent/pull/20474), [#20430](https://github.com/NousResearch/hermes-agent/pull/20430), [#20431](https://github.com/NousResearch/hermes-agent/pull/20431))
+
+- **Google Chat — the 20th messaging platform** — plus a generic platform-plugin hooks surface so third-party adapters drop in without touching core (IRC and Teams migrated). ([#21306](https://github.com/NousResearch/hermes-agent/pull/21306), [#21331](https://github.com/NousResearch/hermes-agent/pull/21331))
+
+- **Sessions survive restarts** — gateway bounces mid-agent, `/update` restarts, source-file reloads — conversations auto-resume when the gateway comes back. ([#21192](https://github.com/NousResearch/hermes-agent/pull/21192))
+
+- **Security wave — 8 P0 closures** — redaction ON by default, Discord role-allowlists guild-scoped (CVSS 8.1 cross-guild DM bypass closed), WhatsApp rejects strangers by default, TOCTOU windows closed across `auth.json` and MCP OAuth, browser enforces cloud-metadata SSRF floor, cron prompt-injection scans assembled skill content, `hermes debug share` redacts at upload. ([#21193](https://github.com/NousResearch/hermes-agent/pull/21193), [#21241](https://github.com/NousResearch/hermes-agent/pull/21241), [#21291](https://github.com/NousResearch/hermes-agent/pull/21291), [#21176](https://github.com/NousResearch/hermes-agent/pull/21176), [#21194](https://github.com/NousResearch/hermes-agent/pull/21194), [#21228](https://github.com/NousResearch/hermes-agent/pull/21228), [#21350](https://github.com/NousResearch/hermes-agent/pull/21350), [#19318](https://github.com/NousResearch/hermes-agent/pull/19318))
+
+- **Checkpoints v2** — state persistence rewritten. Real pruning, disk guardrails, no more orphan shadow repos. ([#20709](https://github.com/NousResearch/hermes-agent/pull/20709))
+
+- **The agent lints its own writes** — post-write delta lint on `write_file` + `patch`. Python, JSON, YAML, TOML. Syntax errors surface immediately instead of shipping downstream. ([#20191](https://github.com/NousResearch/hermes-agent/pull/20191))
+
+- **`no_agent` cron mode — script-only watchdog** — cron jobs can now skip the agent entirely and just run a script. Empty stdout is silent, non-empty gets delivered verbatim. ([#19709](https://github.com/NousResearch/hermes-agent/pull/19709))
+
+- **Platform allowlists everywhere** — `allowed_channels` / `allowed_chats` / `allowed_rooms` config across Slack, Telegram, Mattermost, Matrix, and DingTalk. ([#21251](https://github.com/NousResearch/hermes-agent/pull/21251))
+
+- **Providers are now plugins** — `ProviderProfile` ABC + `plugins/model-providers/`. Drop in third-party providers without touching core. ([#20324](https://github.com/NousResearch/hermes-agent/pull/20324))
+
+- **API server — long-term memory per session** — `X-Hermes-Session-Key` header gives memory providers a stable session identifier. ([#20199](https://github.com/NousResearch/hermes-agent/pull/20199))
+
+- **MCP levels up** — SSE transport with OAuth forwarding, stale-pipe retries, image results surface as MEDIA tags instead of getting dropped, keepalive on long-lived lifecycle waits. ([#21227](https://github.com/NousResearch/hermes-agent/pull/21227), [#21323](https://github.com/NousResearch/hermes-agent/pull/21323), [#21289](https://github.com/NousResearch/hermes-agent/pull/21289), [#21328](https://github.com/NousResearch/hermes-agent/pull/21328), [#20209](https://github.com/NousResearch/hermes-agent/pull/20209))
+
+- **Curator grows subcommands** — `hermes curator archive`, `prune`, `list-archived`. Manual `hermes curator run` is synchronous now — you see results without polling. ([#20200](https://github.com/NousResearch/hermes-agent/pull/20200), [#21236](https://github.com/NousResearch/hermes-agent/pull/21236), [#21216](https://github.com/NousResearch/hermes-agent/pull/21216))
+
+- **ACP — `/steer` and `/queue`** — direct the in-flight agent or queue follow-ups from Zed, VS Code, or JetBrains. Plus atomic session persistence and reasoning-metadata preservation across restarts. (@HenkDz) ([#18114](https://github.com/NousResearch/hermes-agent/pull/18114), [#20279](https://github.com/NousResearch/hermes-agent/pull/20279), [#20296](https://github.com/NousResearch/hermes-agent/pull/20296), [#20433](https://github.com/NousResearch/hermes-agent/pull/20433))
+
+- **TUI glow-up** — `/model` picker matches `hermes model` with inline auth (@austinpickett), collapsible startup banner sections (@kshitijk4poor), context-compression counter in the status bar. ([#18117](https://github.com/NousResearch/hermes-agent/pull/18117), [#20625](https://github.com/NousResearch/hermes-agent/pull/20625), [#21218](https://github.com/NousResearch/hermes-agent/pull/21218))
+
+- **Dashboard grows up** — Plugins page (manage, enable/disable, auth status) (@austinpickett), Profiles management page (@vincez-hms-coder), sortable analytics tables, reverse-proxy support via `X-Forwarded-Prefix`, new `default-large` 18px theme. ([#18095](https://github.com/NousResearch/hermes-agent/pull/18095), [#16419](https://github.com/NousResearch/hermes-agent/pull/16419), [#18192](https://github.com/NousResearch/hermes-agent/pull/18192), [#21296](https://github.com/NousResearch/hermes-agent/pull/21296), [#20820](https://github.com/NousResearch/hermes-agent/pull/20820))
+
+- **SearXNG + split web tools** — SearXNG ships as a native search-only backend; web tools now let you pick different backends per capability (search vs extract vs browse). (@kshitijk4poor) ([#20823](https://github.com/NousResearch/hermes-agent/pull/20823), [#20061](https://github.com/NousResearch/hermes-agent/pull/20061), [#20841](https://github.com/NousResearch/hermes-agent/pull/20841))
+
+- **OpenRouter response caching** — explicit cache control for models that expose it. (@kshitijk4poor) ([#19132](https://github.com/NousResearch/hermes-agent/pull/19132))
+
+- **`[[as_document]]` — skill media-routing directive** — skills can force the gateway to deliver output as a document on platforms that support it. ([#21210](https://github.com/NousResearch/hermes-agent/pull/21210))
+
+- **`transform_llm_output` plugin hook** — new lifecycle hook that lets plugins reshape or filter LLM output before it hits the conversation. Useful for context-window reducers and content filters. ([#21235](https://github.com/NousResearch/hermes-agent/pull/21235))
+
+- **Nous OAuth persists across profiles** — shared token store: sign in once, every profile inherits the session. ([#19712](https://github.com/NousResearch/hermes-agent/pull/19712))
+
+- **QQBot — native approval keyboards** — feature parity with Telegram / Discord approval UX. Chunked upload, quoted attachments. ([#21342](https://github.com/NousResearch/hermes-agent/pull/21342), [#21353](https://github.com/NousResearch/hermes-agent/pull/21353))
+
+- **6 new optional skills** — Shopify (Admin + Storefront GraphQL), here.now, shop-app personal shopping assistant, Anthropic financial-services bundle, kanban-video-orchestrator (@SHL0MS), searxng-search (@kshitijk4poor). ([#18116](https://github.com/NousResearch/hermes-agent/pull/18116), [#18170](https://github.com/NousResearch/hermes-agent/pull/18170), [#20702](https://github.com/NousResearch/hermes-agent/pull/20702), [#21180](https://github.com/NousResearch/hermes-agent/pull/21180), [#19281](https://github.com/NousResearch/hermes-agent/pull/19281), [#20841](https://github.com/NousResearch/hermes-agent/pull/20841))
+
+- **New models** — `deepseek/deepseek-v4-pro`, `x-ai/grok-4.3`, `openrouter/owl-alpha` (free), `tencent/hy3-preview` (@Contentment003111), Arcee Trinity Large Thinking temperature + compression overrides. ([#20495](https://github.com/NousResearch/hermes-agent/pull/20495), [#20497](https://github.com/NousResearch/hermes-agent/pull/20497), [#18071](https://github.com/NousResearch/hermes-agent/pull/18071), [#21077](https://github.com/NousResearch/hermes-agent/pull/21077), [#20473](https://github.com/NousResearch/hermes-agent/pull/20473))
+
+- **100 fresh CLI startup tips** — the random tip banner gets 100 new entries covering cron, kanban, curator, plugins, and lesser-known flags. ([#20168](https://github.com/NousResearch/hermes-agent/pull/20168))
+
+---
+
+## 🧩 Multi-Agent Kanban (Durable)
+
+### New — durable multi-profile collaboration board
+- **`feat(kanban): durable multi-profile collaboration board`** — post-revert reimplementation, multi-profile by design ([#17805](https://github.com/NousResearch/hermes-agent/pull/17805))
+- **Multi-project boards** — one install, many kanbans ([#19653](https://github.com/NousResearch/hermes-agent/pull/19653), [#19679](https://github.com/NousResearch/hermes-agent/pull/19679))
+- **Share board, workspaces, and worker logs across profiles** ([#19378](https://github.com/NousResearch/hermes-agent/pull/19378))
+- **Hallucination gate + recovery UX for worker-created-card claims** (closes #20017) ([#20232](https://github.com/NousResearch/hermes-agent/pull/20232))
+- **Generic diagnostics engine for task distress signals** ([#20332](https://github.com/NousResearch/hermes-agent/pull/20332))
+- **Per-task `max_retries` override** (supersedes #20972) ([#21330](https://github.com/NousResearch/hermes-agent/pull/21330))
+- **Multiline textarea for inline-create title** (salvage of #20970) ([#21243](https://github.com/NousResearch/hermes-agent/pull/21243))
+
+### Kanban Dashboard
+- **Workspace kind + path inputs in inline create form** ([#19679](https://github.com/NousResearch/hermes-agent/pull/19679))
+- **Per-platform home-channel notification toggles** ([#19864](https://github.com/NousResearch/hermes-agent/pull/19864))
+- **Sharper home-channel toggle contrast + drop → running action** ([#19916](https://github.com/NousResearch/hermes-agent/pull/19916))
+- Fix: reject direct status transition to 'running' via dashboard API (salvage of #19554) ([#19705](https://github.com/NousResearch/hermes-agent/pull/19705))
+- Fix: dashboard board pin authoritative over server current file (#20879) ([#21230](https://github.com/NousResearch/hermes-agent/pull/21230))
+- Fix: treat dashboard event-stream cancellation as normal shutdown (#20790) ([#21222](https://github.com/NousResearch/hermes-agent/pull/21222))
+- Fix: filter dashboard board by selected tenant (#19817) ([#21349](https://github.com/NousResearch/hermes-agent/pull/21349))
+- Fix: code/pre styling theme-immune across all themes (#21086) ([#21247](https://github.com/NousResearch/hermes-agent/pull/21247))
+- Fix: reset `<code>` background inside dashboard board ([#20687](https://github.com/NousResearch/hermes-agent/pull/20687))
+- Fix: preserve dashboard completion summaries + add kanban edit (salvages #20016) ([#20195](https://github.com/NousResearch/hermes-agent/pull/20195))
+- Fix: avoid fragile failure-column renames (salvage #20848) (@kshitijk4poor) ([#20855](https://github.com/NousResearch/hermes-agent/pull/20855))
+
+### Worker lifecycle + reliability
+- **Heartbeat + reclaim + zombie + retry-cap fixes** (#21147, #21141, #21169, #20881) ([#21183](https://github.com/NousResearch/hermes-agent/pull/21183))
+- **Auto-block workers that exit without completing + shutdown race** (#20894) ([#21214](https://github.com/NousResearch/hermes-agent/pull/21214))
+- **Detect darwin zombie workers** (salvages #20023) ([#20188](https://github.com/NousResearch/hermes-agent/pull/20188))
+- **Unify failure counter across spawn/timeout/crash outcomes** ([#20410](https://github.com/NousResearch/hermes-agent/pull/20410))
+- **Enforce worker task-ownership on destructive tool calls** ([#19713](https://github.com/NousResearch/hermes-agent/pull/19713))
+- **Drop worker identity claim from KANBAN_GUIDANCE** ([#19427](https://github.com/NousResearch/hermes-agent/pull/19427))
+- Fix: skip dispatch for tasks assigned to non-profile lanes (salvages #20105, #20134) ([#20165](https://github.com/NousResearch/hermes-agent/pull/20165))
+- Fix: include default profile in on-disk assignee enumeration (salvages #20123) ([#20170](https://github.com/NousResearch/hermes-agent/pull/20170))
+- Fix: ignore stale current board pointers (salvages #20063) ([#20183](https://github.com/NousResearch/hermes-agent/pull/20183))
+- Fix: profile discovery ignores HERMES_HOME in custom-root deployments (@jackey8616) ([#19020](https://github.com/NousResearch/hermes-agent/pull/19020))
+- Fix: allow orchestrator profiles to see kanban tools via toolsets config ([#19606](https://github.com/NousResearch/hermes-agent/pull/19606))
+
+### Batch salvages
+- Tier-1 batch — metadata test, max_spawn config, run-id lifecycle guard (salvages #19522 #19556 #19829) ([#20440](https://github.com/NousResearch/hermes-agent/pull/20440))
+- Tier-2 batch — doctor, started_at, parent-guard, latest_summary, selects, linked-children ([#20448](https://github.com/NousResearch/hermes-agent/pull/20448))
+
+### Documentation
+- Backfill multi-board refs in reference docs ([#19704](https://github.com/NousResearch/hermes-agent/pull/19704))
+- Document `/kanban` slash command ([#19584](https://github.com/NousResearch/hermes-agent/pull/19584))
+- Document recommended handoff evidence metadata (salvage #19512) ([#20415](https://github.com/NousResearch/hermes-agent/pull/20415))
+- Fix orchestrator + worker skill setup instructions (@helix4u) ([#20958](https://github.com/NousResearch/hermes-agent/pull/20958), [#20960](https://github.com/NousResearch/hermes-agent/pull/20960))
+
+---
+
+## 🎯 Persistent Goals, Checkpoints & Session Durability
+
+### `/goal` — persistent cross-turn goals (Ralph loop)
+- **`feat: /goal — persistent cross-turn goals`** ([#18262](https://github.com/NousResearch/hermes-agent/pull/18262))
+- **Docs page — Persistent Goals (/goal)** ([#18275](https://github.com/NousResearch/hermes-agent/pull/18275))
+- Fix: honor configured goal turn budget (salvage #19423) ([#21287](https://github.com/NousResearch/hermes-agent/pull/21287))
+
+### Checkpoints v2
+- **Single-store rewrite with real pruning + disk guardrails** ([#20709](https://github.com/NousResearch/hermes-agent/pull/20709))
+
+### Session durability
+- **Auto-resume interrupted sessions after gateway restart** (salvage #20888) ([#21192](https://github.com/NousResearch/hermes-agent/pull/21192))
+- **Preserve pending update prompts across restarts** ([#20160](https://github.com/NousResearch/hermes-agent/pull/20160))
+- **Preserve home-channel thread targets across restart notifications** (salvage #18440) ([#19271](https://github.com/NousResearch/hermes-agent/pull/19271))
+- **Preserve thread routing from cached live session sources** ([#21206](https://github.com/NousResearch/hermes-agent/pull/21206))
+- **Preserve assistant metadata when branching sessions** ([#18222](https://github.com/NousResearch/hermes-agent/pull/18222))
+- **Preserve thread routing for /update progress and prompts** ([#18193](https://github.com/NousResearch/hermes-agent/pull/18193))
+- **Preserve document type when merging queued events** ([#18215](https://github.com/NousResearch/hermes-agent/pull/18215))
+
+---
+
+## 🛡️ Security & Reliability
+
+### Security hardening (8 P0 closures)
+- **Enable secret redaction by default** (#17691, #20785) ([#21193](https://github.com/NousResearch/hermes-agent/pull/21193))
+- **Discord — scope `DISCORD_ALLOWED_ROLES` to originating guild** (#12136, CVSS 8.1) ([#21241](https://github.com/NousResearch/hermes-agent/pull/21241))
+- **WhatsApp — reject strangers by default, never respond in self-chat** (#8389) ([#21291](https://github.com/NousResearch/hermes-agent/pull/21291))
+- **MCP OAuth — close TOCTOU window when saving credentials** ([#21176](https://github.com/NousResearch/hermes-agent/pull/21176))
+- **`hermes_cli/auth.py` — close TOCTOU window in credential writers** ([#21194](https://github.com/NousResearch/hermes-agent/pull/21194))
+- **Browser — enforce cloud-metadata SSRF floor in hybrid routing** (#16234) ([#21228](https://github.com/NousResearch/hermes-agent/pull/21228))
+- **`hermes debug share` — redact log content at upload time** (@GodsBoy) ([#19318](https://github.com/NousResearch/hermes-agent/pull/19318))
+- **Cron — scan assembled prompt including skill content for prompt injection** (#3968) ([#21350](https://github.com/NousResearch/hermes-agent/pull/21350))
+- **Restore .env/auth.json/state.db with 0600 perms** ([#19699](https://github.com/NousResearch/hermes-agent/pull/19699))
+- **SRI integrity for dashboard plugin scripts** (salvage #19389) ([#21277](https://github.com/NousResearch/hermes-agent/pull/21277))
+- **Bind Meet node server to localhost, restrict token file to owner read** ([#19597](https://github.com/NousResearch/hermes-agent/pull/19597))
+- **Extend sensitive-write target to cover shell RC and credential files** ([#19282](https://github.com/NousResearch/hermes-agent/pull/19282))
+- **Harden YOLO mode env parsing against quoted-bool strings** ([#18214](https://github.com/NousResearch/hermes-agent/pull/18214))
+- **OSV-Scanner CI + Dependabot for github-actions only** ([#20037](https://github.com/NousResearch/hermes-agent/pull/20037))
+
+### Reliability — critical bug closures
+- **CLI crash on startup — `Invalid key 'c-S-c'`** (P0, prompt_toolkit doesn't support Shift modifier) ([#19895](https://github.com/NousResearch/hermes-agent/pull/19895), [#19919](https://github.com/NousResearch/hermes-agent/pull/19919))
+- **CLOSE_WAIT fd leak audit** — httpx keepalive + WhatsApp aiohttp leak + Feishu hygiene (#18451) ([#18766](https://github.com/NousResearch/hermes-agent/pull/18766))
+- **Gateway creates AIAgent with empty OpenRouter API key when OPENROUTER_API_KEY is missing** (#20982) — fallback providers correctly honored
+- **Background review + curator protected from overwriting bundled/hub skills** (#20273) ([#20194](https://github.com/NousResearch/hermes-agent/pull/20194))
+- **TUI compression continuation — ghost sessions with incomplete metadata** (#20001)
+- **`hermes mcp add` silently launches chat instead of registering MCP server** (#19785) ([#21204](https://github.com/NousResearch/hermes-agent/pull/21204))
+- **Background review agent runtime propagation** — provider/model/credentials now actually inherit from parent
+- **Inbound document host paths translated to container paths for Docker backend** (salvage #19048) ([#21184](https://github.com/NousResearch/hermes-agent/pull/21184))
+- **Matrix gateway race between auto-redaction and message delivery with high-speed models** (#19075)
+- **`/new` during active agent session never sends response on Telegram** (#18912)
+
+---
+
+## 📱 Messaging Platforms (Gateway)
+
+### New platform
+- **Google Chat — 20th platform** + generic `env_enablement_fn` / `cron_deliver_env_var` platform-plugin hooks (IRC + Teams migrated) ([#21306](https://github.com/NousResearch/hermes-agent/pull/21306), [#21331](https://github.com/NousResearch/hermes-agent/pull/21331))
+
+### Cross-platform
+- **`allowed_{channels,chats,rooms}` whitelist** — Slack (salvage #7401), Telegram, Mattermost, Matrix, DingTalk ([#21251](https://github.com/NousResearch/hermes-agent/pull/21251))
+- **Per-platform `gateway_restart_notification` flag** ([#20892](https://github.com/NousResearch/hermes-agent/pull/20892))
+- **`busy_ack_enabled` config — suppress ack messages** ([#18194](https://github.com/NousResearch/hermes-agent/pull/18194))
+- **Auto-delete slash-command system notices after TTL** ([#18266](https://github.com/NousResearch/hermes-agent/pull/18266))
+- **Opt-in cleanup of temporary progress bubbles** ([#21186](https://github.com/NousResearch/hermes-agent/pull/21186))
+- **`[[as_document]]` directive — skill media routing** (salvage #19069) ([#21210](https://github.com/NousResearch/hermes-agent/pull/21210))
+- **`hermes gateway list` — cross-profile status** (salvage #19129) ([#21225](https://github.com/NousResearch/hermes-agent/pull/21225))
+- **Auto-resume interrupted sessions after restart** (salvage #20888) ([#21192](https://github.com/NousResearch/hermes-agent/pull/21192))
+- **Atomic restart markers + Windows runtime-lock offset** (#17842) ([#18179](https://github.com/NousResearch/hermes-agent/pull/18179))
+- Fix: `config.yaml` wins over `.env` for agent/display/timezone settings ([#18764](https://github.com/NousResearch/hermes-agent/pull/18764))
+- Fix: auto-restart when source files change out from under us (#17648) ([#18409](https://github.com/NousResearch/hermes-agent/pull/18409))
+- Fix: use git HEAD SHA for stale-code check, not file mtimes ([#19740](https://github.com/NousResearch/hermes-agent/pull/19740))
+- Fix: shutdown + restart hygiene — drain timeout, false-fatal, success log ([#18761](https://github.com/NousResearch/hermes-agent/pull/18761))
+- Fix: preserve max_turns after env reload (salvage #19183) ([#21240](https://github.com/NousResearch/hermes-agent/pull/21240))
+- Fix: exclude ancestor PIDs from gateway process scan ([#19586](https://github.com/NousResearch/hermes-agent/pull/19586))
+- Fix: move quick-command alias dispatch before built-ins ([#19588](https://github.com/NousResearch/hermes-agent/pull/19588))
+- Fix: show other profiles in 'gateway status' to prevent confusion ([#19582](https://github.com/NousResearch/hermes-agent/pull/19582))
+- Fix: include external_dirs skills in Telegram/Discord slash commands (salvage #8790) ([#18741](https://github.com/NousResearch/hermes-agent/pull/18741))
+- Fix: match disabled/optional skills by frontmatter slug, not dir name ([#18753](https://github.com/NousResearch/hermes-agent/pull/18753))
+- Fix: read /status token totals from SessionDB (#17158) ([#18206](https://github.com/NousResearch/hermes-agent/pull/18206))
+- Fix: snapshot callback generation after agent binds it, not before ([#18219](https://github.com/NousResearch/hermes-agent/pull/18219))
+- Fix: re-inject topic-bound skill after /new or /reset ([#18205](https://github.com/NousResearch/hermes-agent/pull/18205))
+- Fix: isolate pending native image paths by session ([#18202](https://github.com/NousResearch/hermes-agent/pull/18202))
+- Fix: clear queued reload skills notes on new/resume/branch ([#19431](https://github.com/NousResearch/hermes-agent/pull/19431))
+- Fix: hide required-arg commands from Telegram menu ([#19400](https://github.com/NousResearch/hermes-agent/pull/19400))
+- Fix: bridge top-level `require_mention` to Telegram config ([#19429](https://github.com/NousResearch/hermes-agent/pull/19429))
+- Fix: suppress duplicate voice transcripts ([#19428](https://github.com/NousResearch/hermes-agent/pull/19428))
+- Fix: show friendly error when service is not installed ([#19707](https://github.com/NousResearch/hermes-agent/pull/19707))
+- Fix: read context_length from custom_providers in session info header ([#19708](https://github.com/NousResearch/hermes-agent/pull/19708))
+- Fix: preserve WSL interop PATH in systemd units ([#19867](https://github.com/NousResearch/hermes-agent/pull/19867))
+- Fix: handle planned service stops (salvage #19876) ([#19936](https://github.com/NousResearch/hermes-agent/pull/19936))
+- Fix: keep DoH-confirmed Telegram IPs that match system DNS (salvage #17043) ([#20175](https://github.com/NousResearch/hermes-agent/pull/20175))
+- Fix: load `reply_to_mode` from config.yaml for Discord + Telegram (salvage #17117) ([#20171](https://github.com/NousResearch/hermes-agent/pull/20171))
+- Fix: tolerate malformed HERMES_HUMAN_DELAY_* env vars (salvage #16933) ([#20217](https://github.com/NousResearch/hermes-agent/pull/20217))
+- Fix: deterministic thread eviction preserves newest entries (salvage #13639) ([#20285](https://github.com/NousResearch/hermes-agent/pull/20285))
+- Fix: don't dead-end setup wizard when only system-scope unit is installed ([#20905](https://github.com/NousResearch/hermes-agent/pull/20905))
+- Fix: wait for systemd restart readiness + harden Discord slash-command sync ([#20949](https://github.com/NousResearch/hermes-agent/pull/20949))
+- Fix: avoid duplicated Responses history (salvage #18995) ([#21185](https://github.com/NousResearch/hermes-agent/pull/21185))
+- Fix: surface bootstrap failures to stderr (salvage #21157) ([#21278](https://github.com/NousResearch/hermes-agent/pull/21278))
+- Fix: log agent task failures instead of silently losing usage data (salvage #21159) ([#21274](https://github.com/NousResearch/hermes-agent/pull/21274))
+- Fix: log runtime-status write failures with rate-limiting (salvage #21158) ([#21285](https://github.com/NousResearch/hermes-agent/pull/21285))
+- Fix: reset-failed before every fallback restart so the gateway can't get stranded ([#21371](https://github.com/NousResearch/hermes-agent/pull/21371))
+- Fix: Telegram — preserve `thread_id=1` for forum General typing indicator ([#21390](https://github.com/NousResearch/hermes-agent/pull/21390))
+- Fix: batch critical fixes — session resume, /new race, HA WebSocket scheme (@kshitijk4poor) ([#19182](https://github.com/NousResearch/hermes-agent/pull/19182))
+
+### Telegram
+- **DM user-managed multi-session topics** (salvage of #19185) ([#19206](https://github.com/NousResearch/hermes-agent/pull/19206))
+
+### Discord
+- **Message deletion action** (salvage #19052) ([#21197](https://github.com/NousResearch/hermes-agent/pull/21197))
+- Fix: allow `free_response_channels` to override `DISCORD_IGNORE_NO_MENTION` ([#19629](https://github.com/NousResearch/hermes-agent/pull/19629))
+
+### Slack
+- Fix: ephemeral slash-command ack, private notice delivery, format_message fixes (@kshitijk4poor) ([#18198](https://github.com/NousResearch/hermes-agent/pull/18198))
+
+### WhatsApp
+- Fix: load WhatsApp home channel from env overrides ([#18190](https://github.com/NousResearch/hermes-agent/pull/18190))
+
+### Feishu
+- **Operator-configurable bot admission and mention policy** ([#18208](https://github.com/NousResearch/hermes-agent/pull/18208))
+- Fix: force text mode for markdown tables (salvage of #13723 by @WuTianyi123) ([#20275](https://github.com/NousResearch/hermes-agent/pull/20275))
+
+### Matrix + Email
+- Fix: `/sethome` on Matrix and Email now persists across restarts ([#18272](https://github.com/NousResearch/hermes-agent/pull/18272))
+
+### Teams
+- **Docs + feat: sidebar + threading with group-chat fallback** ([#20042](https://github.com/NousResearch/hermes-agent/pull/20042))
+
+### Weixin
+- Fix: deduplicate Weixin messages by content fingerprint ([#19742](https://github.com/NousResearch/hermes-agent/pull/19742))
+
+### QQBot
+- **Port SDK improvements in-tree — chunked upload, approval keyboards, quoted attachments** ([#21342](https://github.com/NousResearch/hermes-agent/pull/21342))
+- **Wire native tool-approval UX via inline keyboards** ([#21353](https://github.com/NousResearch/hermes-agent/pull/21353))
+
+---
+
+## 🏗️ Core Agent & Architecture
+
+### Provider & Model Support
+
+#### Pluggable providers
+- **ProviderProfile ABC + `plugins/model-providers/`** — inference providers are now a pluggable surface (salvage of #14424) ([#20324](https://github.com/NousResearch/hermes-agent/pull/20324))
+- **`list_picker_providers`** — credential-filtered picker (salvage #13561) ([#20298](https://github.com/NousResearch/hermes-agent/pull/20298))
+- **Remove `/provider` alias for `/model`** ([#20358](https://github.com/NousResearch/hermes-agent/pull/20358))
+- **Shared Hermes dotenv loader across CLI + plugins** (salvage #13660) ([#20281](https://github.com/NousResearch/hermes-agent/pull/20281))
+- **Nous OAuth persisted across profiles via shared token store** ([#19712](https://github.com/NousResearch/hermes-agent/pull/19712))
+
+#### New models
+- `deepseek/deepseek-v4-pro` added to OpenRouter + Nous Portal ([#20495](https://github.com/NousResearch/hermes-agent/pull/20495))
+- `x-ai/grok-4.3` added to OpenRouter + Nous Portal ([#20497](https://github.com/NousResearch/hermes-agent/pull/20497))
+- `openrouter/owl-alpha` (free tier) added to curated OpenRouter list ([#18071](https://github.com/NousResearch/hermes-agent/pull/18071))
+- `tencent/hy3-preview` paid route on OpenRouter (@Contentment003111) ([#21077](https://github.com/NousResearch/hermes-agent/pull/21077))
+- Arcee Trinity Large Thinking — temperature + compression overrides ([#20473](https://github.com/NousResearch/hermes-agent/pull/20473))
+- Rename `x-ai/grok-4.20-beta` to `x-ai/grok-4.20` ([#19640](https://github.com/NousResearch/hermes-agent/pull/19640))
+- Demote Vercel AI Gateway to bottom of provider picker ([#18112](https://github.com/NousResearch/hermes-agent/pull/18112))
+
+#### Provider configuration
+- **OpenRouter — response caching support** (@kshitijk4poor) ([#19132](https://github.com/NousResearch/hermes-agent/pull/19132))
+- **`image_gen.model` from config.yaml honored** (salvage #19376) ([#21273](https://github.com/NousResearch/hermes-agent/pull/21273))
+- Fix: honor runtime default model during delegate provider resolution (@johnncenae) ([#17587](https://github.com/NousResearch/hermes-agent/pull/17587))
+- Fix: avoid Bedrock credential probe in provider picker (@helix4u) ([#18998](https://github.com/NousResearch/hermes-agent/pull/18998))
+- Fix: drop stale env-var override of persisted provider for cron ([#19627](https://github.com/NousResearch/hermes-agent/pull/19627))
+- Fix: auxiliary curator api_key/base_url into runtime resolution ([#19421](https://github.com/NousResearch/hermes-agent/pull/19421))
+
+### Agent Loop & Conversation
+- **`video_analyze` — native video understanding tool** (@alt-glitch) ([#19301](https://github.com/NousResearch/hermes-agent/pull/19301))
+- **Show context compression count in status bar** (CLI + TUI) ([#21218](https://github.com/NousResearch/hermes-agent/pull/21218))
+- **Isolate `get_tool_definitions` quiet_mode cache + dedup LCM injection** (#17335) ([#17889](https://github.com/NousResearch/hermes-agent/pull/17889))
+- Fix: warning-first tool-call loop guardrails ([#18227](https://github.com/NousResearch/hermes-agent/pull/18227))
+- Fix: break permanent empty-response loop from orphan tool-tail ([#21385](https://github.com/NousResearch/hermes-agent/pull/21385))
+- Fix: propagate ContextVars to concurrent tool worker threads (salvage #16660) ([#18123](https://github.com/NousResearch/hermes-agent/pull/18123))
+- Fix: surface self-improvement review summaries across CLI, TUI, and gateway ([#18073](https://github.com/NousResearch/hermes-agent/pull/18073))
+- Fix: serialize concurrent `hermes_tools` RPC calls from `execute_code` ([#17894](https://github.com/NousResearch/hermes-agent/pull/17894), [#17902](https://github.com/NousResearch/hermes-agent/pull/17902))
+- Fix: include system prompt + tool schemas in token estimates for compression ([#18265](https://github.com/NousResearch/hermes-agent/pull/18265))
+
+### Compression
+- Fix: skip non-string tool content in dedup pass to prevent AttributeError ([#19398](https://github.com/NousResearch/hermes-agent/pull/19398))
+- Fix: reset `_summary_failure_cooldown_until` on session reset ([#19622](https://github.com/NousResearch/hermes-agent/pull/19622))
+- Fix: trigger fallback on timeout errors alongside model-unavailable errors ([#19665](https://github.com/NousResearch/hermes-agent/pull/19665))
+- Fix: `_prune_old_tool_results` boundary direction ([#19725](https://github.com/NousResearch/hermes-agent/pull/19725))
+- Fix: soften summary prompt for content filters (salvage #19456) ([#21302](https://github.com/NousResearch/hermes-agent/pull/21302))
+
+### Delegate
+- Fix: inherit parent fallback_chain in `_build_child_agent` ([#19601](https://github.com/NousResearch/hermes-agent/pull/19601))
+- Fix: guard `_load_config()` against `delegation: null` in config.yaml ([#19662](https://github.com/NousResearch/hermes-agent/pull/19662))
+- Fix: inherit parent api_key when `delegation.base_url` set without `delegation.api_key` ([#19741](https://github.com/NousResearch/hermes-agent/pull/19741))
+- Fix: expand composite toolsets before intersection (salvage #19455) ([#21300](https://github.com/NousResearch/hermes-agent/pull/21300))
+- Fix: correct ACP docs — Claude Code CLI has no --acp flag (salvage #19058) ([#21201](https://github.com/NousResearch/hermes-agent/pull/21201))
+
+### Session & Memory
+- **Hindsight — probe API for `update_mode='append'` to dedupe across processes** (@nicoloboschi) ([#20222](https://github.com/NousResearch/hermes-agent/pull/20222))
+
+### Curator
+- **`hermes curator archive` and `prune` subcommands** ([#20200](https://github.com/NousResearch/hermes-agent/pull/20200))
+- **`hermes curator list-archived`** (#20651) ([#21236](https://github.com/NousResearch/hermes-agent/pull/21236))
+- **Synchronous manual `hermes curator run`** (#20555) ([#21216](https://github.com/NousResearch/hermes-agent/pull/21216))
+- Fix: preserve `last_report_path` in state ([#18169](https://github.com/NousResearch/hermes-agent/pull/18169))
+- Fix: rewrite cron job skill refs after consolidation ([#18253](https://github.com/NousResearch/hermes-agent/pull/18253))
+- Fix: defer first run + `--dry-run` preview (#18373) ([#18389](https://github.com/NousResearch/hermes-agent/pull/18389))
+- Fix: authoritative `absorbed_into` on delete + restore cron skill links on rollback (#18671) ([#18731](https://github.com/NousResearch/hermes-agent/pull/18731))
+- Fix: prevent false-positive consolidation from substring matching ([#19573](https://github.com/NousResearch/hermes-agent/pull/19573))
+- Fix: only mark agent-created for background-review sediment ([#19621](https://github.com/NousResearch/hermes-agent/pull/19621))
+- Fix: protect hub skills by frontmatter name ([#20194](https://github.com/NousResearch/hermes-agent/pull/20194))
+
+---
+
+## 🔧 Tool System
+
+### File tools
+- **Post-write delta lint on `write_file` + `patch`** — in-proc linters for Python, JSON, YAML, TOML ([#20191](https://github.com/NousResearch/hermes-agent/pull/20191))
+
+### Cron
+- **`no_agent` mode — script-only cron jobs (watchdog pattern)** ([#19709](https://github.com/NousResearch/hermes-agent/pull/19709))
+- **`context_from` chaining docs** (salvage #15724) ([#20394](https://github.com/NousResearch/hermes-agent/pull/20394))
+- Fix: treat non-dict origin as missing instead of crashing tick ([#19283](https://github.com/NousResearch/hermes-agent/pull/19283))
+- Fix: bump skill usage when cron jobs load skills ([#19433](https://github.com/NousResearch/hermes-agent/pull/19433))
+- Fix: recover null `next_run_at` jobs ([#19576](https://github.com/NousResearch/hermes-agent/pull/19576))
+- Fix: skip AI call when prerun script produces no output ([#19628](https://github.com/NousResearch/hermes-agent/pull/19628))
+- Fix: expand config.yaml refs during job execution ([#19872](https://github.com/NousResearch/hermes-agent/pull/19872))
+- Fix: serialize `get_due_jobs` writes to prevent parallel state corruption ([#19874](https://github.com/NousResearch/hermes-agent/pull/19874))
+- Fix: initialize MCP servers before constructing the cron AIAgent ([#21354](https://github.com/NousResearch/hermes-agent/pull/21354))
+
+### MCP
+- **SSE transport support** (salvage #19135) ([#21227](https://github.com/NousResearch/hermes-agent/pull/21227))
+- **Forward OAuth auth + bump `sse_read_timeout` on SSE transport** ([#21323](https://github.com/NousResearch/hermes-agent/pull/21323))
+- **Retry stale pipe transport failures as session-expired** ([#21289](https://github.com/NousResearch/hermes-agent/pull/21289))
+- **Surface image tool results as MEDIA tags instead of dropping them** ([#21328](https://github.com/NousResearch/hermes-agent/pull/21328))
+- **Periodic keepalive to `_wait_for_lifecycle_event`** (salvage #17016) ([#20209](https://github.com/NousResearch/hermes-agent/pull/20209))
+- Fix: reconnect on terminated sessions ([#19380](https://github.com/NousResearch/hermes-agent/pull/19380))
+- Fix: decouple AnyUrl import from mcp dependency ([#19695](https://github.com/NousResearch/hermes-agent/pull/19695))
+- Fix: `mcp add --command` gets distinct argparse dest ([#21204](https://github.com/NousResearch/hermes-agent/pull/21204))
+- Fix: clear stale thread interrupt before MCP discovery ([#21276](https://github.com/NousResearch/hermes-agent/pull/21276))
+- Fix: report configured timeout in MCP call errors ([#21281](https://github.com/NousResearch/hermes-agent/pull/21281))
+- Fix: include exception type in error messages when str(exc) is empty (salvage #19425) ([#21292](https://github.com/NousResearch/hermes-agent/pull/21292))
+- Fix: re-raise CancelledError explicitly in `MCPServerTask.run` ([#21318](https://github.com/NousResearch/hermes-agent/pull/21318))
+- Fix: coerce numeric tool args defensively in `mcp_serve` ([#21329](https://github.com/NousResearch/hermes-agent/pull/21329))
+- Fix: gate utility stubs on server-advertised capabilities ([#21347](https://github.com/NousResearch/hermes-agent/pull/21347))
+
+### Browser
+- Fix: allow explicit CDP override without local agent-browser ([#19670](https://github.com/NousResearch/hermes-agent/pull/19670))
+- Fix: inject `--no-sandbox` for root + AppArmor userns restrictions ([#19747](https://github.com/NousResearch/hermes-agent/pull/19747))
+- Fix: tighten Lightpanda fallback edge cases (@kshitijk4poor) ([#20672](https://github.com/NousResearch/hermes-agent/pull/20672))
+
+### Web tools
+- **Per-capability backend selection — search/extract split** (@kshitijk4poor) ([#20061](https://github.com/NousResearch/hermes-agent/pull/20061))
+- **SearXNG native search-only backend** (@kshitijk4poor) ([#20823](https://github.com/NousResearch/hermes-agent/pull/20823))
+
+### Approval / Tool gating
+- Fix: wake blocked gateway approvals on session cleanup ([#18171](https://github.com/NousResearch/hermes-agent/pull/18171))
+- Fix: harden YOLO mode env parsing against quoted-bool strings ([#18214](https://github.com/NousResearch/hermes-agent/pull/18214))
+- Fix: extend sensitive write target to cover shell RC and credential files ([#19282](https://github.com/NousResearch/hermes-agent/pull/19282))
+
+---
+
+## 🔌 Plugin System
+
+- **`transform_llm_output` plugin hook** (salvage of #20813) ([#21235](https://github.com/NousResearch/hermes-agent/pull/21235))
+- **Document `env_enablement_fn` + `cron_deliver_env_var` platform-plugin hooks** ([#21331](https://github.com/NousResearch/hermes-agent/pull/21331))
+- **Pluggable surfaces coverage — model-provider guide, full plugin map, opt-in fix** ([#20749](https://github.com/NousResearch/hermes-agent/pull/20749))
+- **Plugin-authoring gaps — image-gen provider guide + publishing a skill tap** ([#20800](https://github.com/NousResearch/hermes-agent/pull/20800))
+
+---
+
+## 🧩 Skills Ecosystem
+
+### New optional skills
+- **Shopify** — Admin + Storefront GraphQL optional skill ([#18116](https://github.com/NousResearch/hermes-agent/pull/18116))
+- **here.now** — optional skill ([#18170](https://github.com/NousResearch/hermes-agent/pull/18170))
+- **shop-app** — personal shopping assistant (optional) ([#20702](https://github.com/NousResearch/hermes-agent/pull/20702))
+- **Anthropic financial-services bundle** — ported as optional finance skills ([#21180](https://github.com/NousResearch/hermes-agent/pull/21180))
+- **kanban-video-orchestrator** — creative optional skill (@SHL0MS) ([#19281](https://github.com/NousResearch/hermes-agent/pull/19281))
+- **searxng-search** — optional skill + Web Search + Extract docs page (@kshitijk4poor) ([#20841](https://github.com/NousResearch/hermes-agent/pull/20841), [#20844](https://github.com/NousResearch/hermes-agent/pull/20844))
+
+### Skill UX
+- **Linear skill — add Documents support + Python helper script** ([#20752](https://github.com/NousResearch/hermes-agent/pull/20752))
+- **Modernize Obsidian skill to use file tools** (salvage #19332) ([#20413](https://github.com/NousResearch/hermes-agent/pull/20413))
+- **Default custom tool creation to plugins** (@kshitijk4poor) ([#19755](https://github.com/NousResearch/hermes-agent/pull/19755))
+- **skill_commands cache — rescan on platform scope changes** (salvage #14570 by @LeonSGP43) ([#18739](https://github.com/NousResearch/hermes-agent/pull/18739))
+- **Skills — additional rescan paths in skill_commands cache** (salvage #19042) ([#21181](https://github.com/NousResearch/hermes-agent/pull/21181))
+- Fix: regression tests for non-dict metadata in `extract_skill_conditions` ([#18213](https://github.com/NousResearch/hermes-agent/pull/18213))
+- Docs: explain restoring bundled skills (salvage #19254) ([#20404](https://github.com/NousResearch/hermes-agent/pull/20404))
+- Docs: document `hermes skills reset` subcommand (salvage #11544) ([#20395](https://github.com/NousResearch/hermes-agent/pull/20395))
+- Docs: himalaya v1.2.0 `folder.aliases` syntax ([#19882](https://github.com/NousResearch/hermes-agent/pull/19882))
+- Point agent at `hermes-agent` skill + docs site sync ([#20390](https://github.com/NousResearch/hermes-agent/pull/20390))
+
+---
+
+## 🖥️ CLI & User Experience
+
+### CLI
+- **`/new` accepts optional session name argument** (salvage of #19555) ([#19637](https://github.com/NousResearch/hermes-agent/pull/19637))
+- **100 new CLI startup tips** ([#20168](https://github.com/NousResearch/hermes-agent/pull/20168))
+- **`display.language` — static message translation** (zh/ja/de/es) ([#20231](https://github.com/NousResearch/hermes-agent/pull/20231))
+- **French (fr) locale** (@Foolafroos) ([#20329](https://github.com/NousResearch/hermes-agent/pull/20329))
+- **Ukrainian (uk) locale** ([#20467](https://github.com/NousResearch/hermes-agent/pull/20467))
+- **Turkish (tr) locale** ([#20474](https://github.com/NousResearch/hermes-agent/pull/20474))
+- Fix: recover classic CLI output after resize (@helix4u) ([#20444](https://github.com/NousResearch/hermes-agent/pull/20444))
+- Fix: complete absolute paths as paths (@helix4u) ([#19930](https://github.com/NousResearch/hermes-agent/pull/19930))
+- Fix: resolve lazy session creation regressions (#18370 fallout) (@alt-glitch) ([#20363](https://github.com/NousResearch/hermes-agent/pull/20363))
+- Fix: local backend CLI always uses launch directory (@alt-glitch) ([#19334](https://github.com/NousResearch/hermes-agent/pull/19334))
+- Refactor: drop dead c-S-c key binding (follow-up to #19895) ([#19919](https://github.com/NousResearch/hermes-agent/pull/19919))
+
+### TUI (Ink)
+- **`/model` picker overhaul to match `hermes model` with inline auth** (@austinpickett) ([#18117](https://github.com/NousResearch/hermes-agent/pull/18117))
+- **Collapsible sections in startup banner** — skills, system prompt, MCP (@kshitijk4poor) ([#20625](https://github.com/NousResearch/hermes-agent/pull/20625))
+- **Show context compression count in status bar** ([#21218](https://github.com/NousResearch/hermes-agent/pull/21218))
+- Perf: reduce overlay render churn with focused selectors (@OutThisLife) ([#20393](https://github.com/NousResearch/hermes-agent/pull/20393))
+- Fix: restore voice push-to-talk parity (salvage of #16189 by @Montbra) (@OutThisLife) ([#20897](https://github.com/NousResearch/hermes-agent/pull/20897))
+- Fix: kanban button (@austinpickett) ([#18358](https://github.com/NousResearch/hermes-agent/pull/18358))
+
+### Dashboard
+- **Plugins page — manage, enable/disable, auth status** (@austinpickett) ([#18095](https://github.com/NousResearch/hermes-agent/pull/18095))
+- **Profiles management page** (@vincez-hms-coder) ([#16419](https://github.com/NousResearch/hermes-agent/pull/16419))
+- **Interactive column sorting in analytics tables** ([#18192](https://github.com/NousResearch/hermes-agent/pull/18192))
+- **`default-large` built-in theme with 18px base size** ([#20820](https://github.com/NousResearch/hermes-agent/pull/20820))
+- **Support serving under URL prefix via `X-Forwarded-Prefix`** (salvage #19450) ([#21296](https://github.com/NousResearch/hermes-agent/pull/21296))
+- **Launch dashboard as side-process via `HERMES_DASHBOARD=1` in Docker** (@benbarclay) ([#19540](https://github.com/NousResearch/hermes-agent/pull/19540))
+- Fix: dashboard theme layout shift (@AllardQuek) ([#17232](https://github.com/NousResearch/hermes-agent/pull/17232))
+- Fix: gateway model picker current context (@helix4u) ([#20513](https://github.com/NousResearch/hermes-agent/pull/20513))
+
+### Update + setup
+- **`hermes update --yes/-y` to skip interactive prompts** ([#18261](https://github.com/NousResearch/hermes-agent/pull/18261))
+- **Restart manual profile gateways after update** ([#18178](https://github.com/NousResearch/hermes-agent/pull/18178))
+
+### Profiles
+- **`--no-skills` flag for empty profile creation** ([#20986](https://github.com/NousResearch/hermes-agent/pull/20986))
+
+---
+
+## 🎵 Voice, Image & Media
+
+- **xAI Custom Voices — voice cloning** (@alt-glitch) ([#18776](https://github.com/NousResearch/hermes-agent/pull/18776))
+- **Achievements — share card render on unlocked badges** ([#19657](https://github.com/NousResearch/hermes-agent/pull/19657))
+- **Refresh systemd unit on gateway boot (not just start/restart)** (@alt-glitch) ([#19684](https://github.com/NousResearch/hermes-agent/pull/19684))
+
+---
+
+## 🔗 API Server & Remote Access
+
+- **`X-Hermes-Session-Key` header for long-term memory scoping** (closes #20060) ([#20199](https://github.com/NousResearch/hermes-agent/pull/20199))
+
+---
+
+## 🧰 ACP Adapter (VS Code / Zed / JetBrains)
+
+- **`/steer` and `/queue` slash commands** (@HenkDz) ([#18114](https://github.com/NousResearch/hermes-agent/pull/18114))
+- Fix: translate Windows cwd for WSL sessions (salvage #18128) ([#18233](https://github.com/NousResearch/hermes-agent/pull/18233))
+- Fix: run `/steer` as a regular prompt on idle sessions ([#18258](https://github.com/NousResearch/hermes-agent/pull/18258))
+- Fix: route Zed thoughts to reasoning + polish tool/context rendering ([#19139](https://github.com/NousResearch/hermes-agent/pull/19139))
+- Fix: atomic session persistence via `replace_messages` (salvage #13675) ([#20279](https://github.com/NousResearch/hermes-agent/pull/20279))
+- Fix: preserve assistant reasoning metadata in session persistence (salvage #13575) ([#20296](https://github.com/NousResearch/hermes-agent/pull/20296))
+- Docs: update VS Code setup for ACP Client extension (salvage #12495) ([#20433](https://github.com/NousResearch/hermes-agent/pull/20433))
+
+---
+
+## 🐳 Docker
+
+- **Launch dashboard as side-process via `HERMES_DASHBOARD=1`** (@benbarclay) ([#19540](https://github.com/NousResearch/hermes-agent/pull/19540))
+- **Refuse root gateway runs in official image** (salvage #19215) ([#21250](https://github.com/NousResearch/hermes-agent/pull/21250))
+- **Chown runtime `node_modules` trees to hermes user** (salvage #19303) ([#21267](https://github.com/NousResearch/hermes-agent/pull/21267))
+- Fix: exclude compose/profile runtime state from build context ([#19626](https://github.com/NousResearch/hermes-agent/pull/19626))
+- CI: don't cancel overlapping builds, guard `:latest` (@ethernet8023) ([#20890](https://github.com/NousResearch/hermes-agent/pull/20890))
+- Test: align Dockerfile contract tests with simplified TUI flow (salvage #19024) ([#21174](https://github.com/NousResearch/hermes-agent/pull/21174))
+- Docs: connect to local inference servers (vLLM, Ollama) (salvage #12335) ([#20407](https://github.com/NousResearch/hermes-agent/pull/20407))
+- Docs: document `API_SERVER_*` env vars (salvage #11758) ([#20409](https://github.com/NousResearch/hermes-agent/pull/20409))
+- Docs: clarify Docker terminal backend is a single persistent container ([#20003](https://github.com/NousResearch/hermes-agent/pull/20003))
+
+---
+
+## 🐛 Notable Bug Fixes
+
+### Agent
+- Fix: recover lazy session creation regressions (#18370 fallout) (@alt-glitch) ([#20363](https://github.com/NousResearch/hermes-agent/pull/20363))
+- Fix: propagate ContextVars to concurrent tool worker threads (salvage #16660) ([#18123](https://github.com/NousResearch/hermes-agent/pull/18123))
+- Fix: warning-first tool-call loop guardrails ([#18227](https://github.com/NousResearch/hermes-agent/pull/18227))
+- Fix: surface self-improvement review summaries across CLI, TUI, and gateway ([#18073](https://github.com/NousResearch/hermes-agent/pull/18073))
+
+### Gateway streaming
+- Fix: harden StreamingConfig bool and numeric coercion (@simbam99) ([#16463](https://github.com/NousResearch/hermes-agent/pull/16463))
+
+### Model
+- Fix: avoid Bedrock credential probe in provider picker (@helix4u) ([#18998](https://github.com/NousResearch/hermes-agent/pull/18998))
+
+### Doctor
+- Fix: check global agent-browser when local install not found ([#19671](https://github.com/NousResearch/hermes-agent/pull/19671))
+- Test: kimi-coding-cn provider validation regression ([#19734](https://github.com/NousResearch/hermes-agent/pull/19734))
+
+### Update
+- Fix: patch `isatty` on real streams to fix xdist-flaky `--yes` tests (salvage #19026) ([#21175](https://github.com/NousResearch/hermes-agent/pull/21175))
+- Fix: teach restart-mocks about the post-update survivor sweep (salvage #19031) ([#21177](https://github.com/NousResearch/hermes-agent/pull/21177))
+
+### Auth
+- Fix: acp preserve assistant reasoning metadata ([#20296](https://github.com/NousResearch/hermes-agent/pull/20296))
+
+### Redact
+- Fix: add `code_file` param to skip false-positive ENV/JSON patterns ([#19715](https://github.com/NousResearch/hermes-agent/pull/19715))
+
+### Email
+- Fix: quoted-relative file-drop paths + Date header on tool email path ([#19646](https://github.com/NousResearch/hermes-agent/pull/19646))
+
+---
+
+## 🧪 Testing
+
+- **ACP — accept prompt persistence kwargs in MCP E2E mocks** (@stephenschoettler) ([#18047](https://github.com/NousResearch/hermes-agent/pull/18047))
+- **Toolsets — include kanban in expected post-#17805 toolset assertions** (@briandevans) ([#18122](https://github.com/NousResearch/hermes-agent/pull/18122))
+- **Agent — cover max-iterations summary message sanitization** ([#19580](https://github.com/NousResearch/hermes-agent/pull/19580))
+- **run_agent — `-inf` and `nan` regression coverage for `_coerce_number`** ([#19703](https://github.com/NousResearch/hermes-agent/pull/19703))
+
+---
+
+## 📚 Documentation
+
+### Major docs additions
+- **`llms.txt` + `llms-full.txt` — agent-friendly ingestion** ([#18276](https://github.com/NousResearch/hermes-agent/pull/18276))
+- **User Stories and Use Cases collage page** ([#18282](https://github.com/NousResearch/hermes-agent/pull/18282))
+- **Persistent Goals (/goal) feature page** ([#18275](https://github.com/NousResearch/hermes-agent/pull/18275))
+- **Windows (WSL2) guide expansion** — filesystem, networking, services, pitfalls ([#20748](https://github.com/NousResearch/hermes-agent/pull/20748))
+- **Chinese (zh-CN) README translation** (salvage #13508) ([#20431](https://github.com/NousResearch/hermes-agent/pull/20431))
+- **zh-Hans Docusaurus locale** + Tool Gateway / image-gen / WSL quickstart translations (salvage #11728) ([#20430](https://github.com/NousResearch/hermes-agent/pull/20430))
+- **Tool Gateway docs restructure** — lead with what it does, config moved to bottom ([#20827](https://github.com/NousResearch/hermes-agent/pull/20827))
+- **Quickstart — Onchain AI Garage Hermes tutorials playlist** ([#20192](https://github.com/NousResearch/hermes-agent/pull/20192))
+- **Open WebUI bootstrap script** (salvage #9566) ([#20427](https://github.com/NousResearch/hermes-agent/pull/20427))
+- **Local Ollama setup guide** (salvage #5842) ([#20426](https://github.com/NousResearch/hermes-agent/pull/20426))
+- **Google Gemini guide** (salvage #17450) ([#20401](https://github.com/NousResearch/hermes-agent/pull/20401))
+- **Custom model aliases for /model command** ([#20475](https://github.com/NousResearch/hermes-agent/pull/20475))
+- **Together/Groq/Perplexity cookbook via `custom_providers`** (salvage #15214) ([#20400](https://github.com/NousResearch/hermes-agent/pull/20400))
+- **Doubao speech integration examples** (TTS + STT) (salvage #18065) ([#20418](https://github.com/NousResearch/hermes-agent/pull/20418))
+- **WSL-to-Windows Chrome MCP bridge** (salvage #8313) ([#20428](https://github.com/NousResearch/hermes-agent/pull/20428))
+- **Hermes skills docs sync** — slash commands + durable-systems section ([#20390](https://github.com/NousResearch/hermes-agent/pull/20390))
+- **AGENTS.md — curator/cron/delegation/toolsets + fix plugin tree** ([#20226](https://github.com/NousResearch/hermes-agent/pull/20226))
+- **Bedrock quickstart entry + fallback comment + deployment link** (salvage #11093) ([#20397](https://github.com/NousResearch/hermes-agent/pull/20397))
+
+### Docs polish
+- Collapse exploding skills tree to a single Skills node ([#18259](https://github.com/NousResearch/hermes-agent/pull/18259))
+- Clarify `session_search` auxiliary model docs ([#19593](https://github.com/NousResearch/hermes-agent/pull/19593))
+- Open WebUI Quick Setup gap fill ([#19654](https://github.com/NousResearch/hermes-agent/pull/19654))
+- Default custom tool creation to plugins (@kshitijk4poor) ([#19755](https://github.com/NousResearch/hermes-agent/pull/19755))
+- Clarify Telegram group chat troubleshooting (salvage #18672) ([#20416](https://github.com/NousResearch/hermes-agent/pull/20416))
+- Codex OAuth auth prerequisite clarification (salvage #18688) ([#20417](https://github.com/NousResearch/hermes-agent/pull/20417))
+- Discord Server Members Intent + SSRC-mapping drift + /voice join slash Choice (salvage #11350) ([#20411](https://github.com/NousResearch/hermes-agent/pull/20411))
+- Document `ctx.dispatch_tool()` (salvage #10955) ([#20391](https://github.com/NousResearch/hermes-agent/pull/20391))
+- Document `hermes webhook subscribe --deliver-only` (salvage #12612) ([#20392](https://github.com/NousResearch/hermes-agent/pull/20392))
+- Document `hermes import` reference (salvage #14711) ([#20396](https://github.com/NousResearch/hermes-agent/pull/20396))
+- Document per-provider TTS `max_text_length` caps (salvage #13825) ([#20389](https://github.com/NousResearch/hermes-agent/pull/20389))
+- Clarify supported prompt customization surfaces (salvage #19987) ([#20383](https://github.com/NousResearch/hermes-agent/pull/20383))
+- Correct `web_extract` summarizer timeout comment (salvage #20051) ([#20381](https://github.com/NousResearch/hermes-agent/pull/20381))
+- Fix fallback provider config paths (salvage #20033) ([#20382](https://github.com/NousResearch/hermes-agent/pull/20382))
+- Fix misleading RL install-extras claim (salvage #19080) ([#21213](https://github.com/NousResearch/hermes-agent/pull/21213))
+- Clarify API server tool execution locality (salvage #19117) ([#21223](https://github.com/NousResearch/hermes-agent/pull/21223))
+- Prefer `.venv` to match AGENTS.md and scripts/run_tests.sh (@xxxigm) ([#21334](https://github.com/NousResearch/hermes-agent/pull/21334))
+- Align tool discovery + test runner with AGENTS.md (@xxxigm) ([#20791](https://github.com/NousResearch/hermes-agent/pull/20791))
+- Align terminal-backend count and naming across docs and code (salvage #19044) ([#20402](https://github.com/NousResearch/hermes-agent/pull/20402))
+- Refresh stale platform counts (salvage #19053) ([#20403](https://github.com/NousResearch/hermes-agent/pull/20403))
+
+---
+
+## 👥 Contributors
+
+### Core
+- **@teknium1** — salvage, triage, review, feature work, and release management
+
+### Top Community Contributors
+
+- **@kshitijk4poor** (21 PRs) — SearXNG native search backend, per-capability backend selection, collapsible TUI startup banner, Slack ephemeral ack + format fixes, Lightpanda fallback hardening, searxng-search optional skill + Web Search + Extract docs, default custom tool creation to plugins, kanban failure-column fix
+- **@alt-glitch** (13 PRs) — video_analyze tool, xAI Custom Voices (voice cloning), local-backend CLI launch-directory fix, lazy-session creation regression recovery, systemd unit refresh on gateway boot
+- **@OutThisLife** (9 PRs) — TUI perf — overlay render churn reduction, voice push-to-talk parity restoration (salvaging @Montbra)
+- **@helix4u** (6 PRs) — Classic CLI output recovery after resize, absolute-path TUI completion, gateway model picker current-context fix, Bedrock credential probe avoidance, kanban docs fixes
+- **@ethernet8023** (3 PRs) — Docker CI — don't cancel overlapping builds, :latest guard
+- **@benbarclay** (3 PRs) — Docker — launch dashboard as side-process via HERMES_DASHBOARD=1
+- **@austinpickett** (3 PRs) — Dashboard Plugins page, TUI /model picker overhaul with inline auth, kanban button fix
+- **@sprmn24** (2 PRs) — Contributor (2 PRs)
+- **@asheriif** (2 PRs) — Contributor (2 PRs)
+- **@xxxigm** (2 PRs) — Contributing docs — .venv preference and test runner alignment with AGENTS.md
+- **@stephenschoettler** (1 PR) — ACP — MCP E2E mock kwargs
+- **@vincez-hms-coder** (1 PR) — Dashboard — Profiles management page
+- **@cdanis** (1 PR) — Contributor
+- **@briandevans** (1 PR) — Toolsets test — kanban assertions post-#17805
+- **@heyitsaamir** (1 PR) — Contributor
+
+### All Contributors
+
+Thanks to everyone who contributed to v0.13.0 — commits, co-authored work, and salvaged PRs. 295 contributors in one week.
+
+@0oAstro, @0xDevNinja, @0xharryriddle, @0xKingBack, @0xsir0000, @0xyg3n, @0z1-ghb, @abhinav11082001-stack,
+@acc001k, @acesjohnny, @adamludwin, @adybag14-cyber, @agentlinker, @agilejava, @ai-ag2026, @AJV20,
+@alanxchen85, @albert748, @AllardQuek, @alt-glitch, @altmazza0-star, @ambition0802, @amitgaur, @amroessam,
+@andrewhosf, @Asce66, @asheriif, @ashermorse, @asimons81, @Aslaaen, @Asunfly, @atongrun, @austinpickett,
+@banditburai, @barteqpl, @Bartok9, @Beandon13, @beardthelion, @beibi9966, @benbarclay, @binhnt92, @bjianhang,
+@BlackJulySnow, @bobashopcashier, @bogerman1, @Bongulielmi, @Brecht-H, @briandevans, @brooklynnicholson,
+@c3115644151, @camaragon, @CashWilliams, @CCClelo, @cdanis, @CES4751, @cg2aigc, @changchun989, @ChanlerDev,
+@CharlieKerfoot, @chengoak, @chenyunbo411, @chinadbo, @CIRWEL, @cixuuz, @cmcgrabby-hue, @colorcross,
+@Contentment003111, @CoreyNoDream, @counterposition, @curiouscleo, @DaniuXie, @deep-name, @dengtaoyuan450-a11y,
+@discodirector, @donramon77, @dpaluy, @ee-blog, @ehz0ah, @el-analista, @elmatadorgh, @EmelyanenkoK,
+@Emidomenge, @emozilla, @Es1la, @EthanGuo-coder, @etherman-os, @ethernet8023, @EvilDrag0n, @exxmen, @Fearvox,
+@Feranmi10, @firefly, @flobo3, @fmercurio, @Foolafroos, @formulahendry, @franksong2702, @ggnnggez, @GinWU05,
+@giwaov, @glesperance, @gnanirahulnutakki, @GodsBoy, @Gosuj, @Grey0202, @guillaumemeyer, @Gutslabs, @h0tp-ftw,
+@haidao1919, @halmisen, @happy5318, @hedirman, @helix4u, @hendrixfreire, @HenkDz, @hex-clawd, @heyitsaamir,
+@hharry11, @Hinotoi-agent, @holynn-q, @hrkzogw, @Hypn0sis, @Hypnus-Yuan, @ideathinklab01-source, @IMHaoyan,
+@Interstellar-code, @ishardo, @jacdevos, @jackey8616, @JanCong, @jasonoutland, @jatingodnani, @JayGwod,
+@jethac, @JezzaHehn, @JiaDe-Wu, @jjjojoj, @jkausel-ai, @John-tip, @johnncenae, @jrusso1020, @jslizar,
+@JTroyerOvermatch, @julysir, @Junass1, @JustinUssuri, @Kailigithub, @keepcalmqqf, @kiala9, @konsisumer,
+@kowenhaoai, @Krionex, @kshitijk4poor, @kyan12, @leavrcn, @leon7609, @LeonSGP43, @leprincep35700, @lhysdl,
+@likejudy, @lisanhu, @liu-collab, @liuguangyong93, @liuhao1024, @LucianoSP, @luoyuctl, @luyao618, @M3RCUR2Y,
+@maciekczech, @Magicray1217, @magicray1217, @MaHaoHao-ch, @malaiwah, @manateelazycat, @masonjames, @megastary,
+@memosr, @MichaelWDanko, @mikeyobrien, @millerc79, @Mind-Dragon, @mioimotoai-lgtm, @misery-hl, @molvikar,
+@momowind, @Montbra, @MottledShadow, @mrbob-git, @mrcharlesiv, @mrcoferland, @ms-alan, @mwnickerson,
+@nazirulhafiy, @nftpoetrist, @nicoloboschi, @nightq, @nikolay-bratanov, @NikolayGusev-astra, @nocturnum91,
+@noOne-list, @nouseman666, @novax635, @npmisantosh, @nudiltoys-cmyk, @olisikh, @oluwadareab12, @Oxidane-bot,
+@pama0227, @pander, @pasevin, @paul-tian, @pdonizete, @perlowja, @pingchesu, @PratikRai0101, @priveperfumes,
+@probepark, @QifengKuang, @quocanh261997, @qWaitCrypto, @qxxaa, @r266-tech, @rames-jusso, @revaraver,
+@Ricardo-M-L, @rob-maron, @Roy-oss1, @rxdxxxx, @SandroHub013, @Sanjays2402, @Sertug17, @shashwatgokhe,
+@shellybotmoyer, @SHL0MS, @SimbaKingjoe, @simbam99, @simplenamebox-ops, @socrates1024, @sonic-netizen,
+@sprmn24, @steezkelly, @stephen0110, @stephenschoettler, @stevenchanin, @stevenchouai, @stormhierta,
+@subtract0, @suncokret12, @swithek, @taeng0204, @TakeshiSawaguchi, @tangyuanjc, @TheEpTic, @thelumiereguy,
+@Tkander1715, @tmdgusya, @Tranquil-Flow, @TruaShamu, @UgwujaGeorge, @valda, @vincez-hms-coder, @VinVC,
+@vominh1919, @wabrent, @WadydX, @wanazhar, @WanderWang, @warabe1122, @web-dev0521, @WideLee, @willy-scr,
+@wmagev, @WuTianyi123, @wxst, @wysie, @Wysie, @xsfX20, @xxxigm, @xyiy001, @YanzhongSu, @ygd58, @Yoimex,
+@yuehei, @Yukipukii1, @yuqianma, @YX234, @zeejaytan, @zhanggttry, @zhao0112, @zng8418, @zons-zhaozhy, @Zyproth
+
+---
+
+**Full Changelog**: [v2026.4.30...v2026.5.7](https://github.com/NousResearch/hermes-agent/compare/v2026.4.30...v2026.5.7)
diff --git a/RELEASE_v0.14.0.md b/RELEASE_v0.14.0.md
new file mode 100644
index 000000000..30ab4189a
--- /dev/null
+++ b/RELEASE_v0.14.0.md
@@ -0,0 +1,479 @@
+# Hermes Agent v0.14.0 (v2026.5.16)
+
+**Release Date:** May 16, 2026
+**Since v0.13.0:** 808 commits · 633 merged PRs · 1393 files changed · 165,061 insertions · 545 issues closed (12 P0, 50 P1) · 215 community contributors (including co-authors)
+
+> The Foundation Release — Hermes installs and runs anywhere, ships with the things you actually want to use, and stops shipping the things you don't. xAI Grok lands as a SuperGrok OAuth provider with grok-4.3 bumped to a 1M context window. A new OpenAI-compatible local proxy turns any OAuth-authed Hermes provider — Claude Pro, ChatGPT Pro, SuperGrok — into an endpoint that Codex / Aider / Cline / Continue can hit. `x_search` lands as a first-class X (Twitter) search tool with OAuth-or-API-key auth. The Microsoft Teams stack is wired end-to-end (Graph auth + webhook listener + pipeline runtime + outbound delivery). A debloating wave makes installs dramatically lighter — heavyweight backends now lazy-install on first use, the `[all]` extras drop everything covered by lazy-deps, and a tiered install falls back when a wheel rejects on your platform. `pip install hermes-agent` works from PyPI. The cold-start wave shaves ~19 seconds off `hermes` launch. Browser CDP calls are 180x faster. Two new messaging platforms (LINE + SimpleX Chat) bring the total to 22. Cross-session 1-hour Claude prompt caching, `/handoff` that actually transfers sessions live, native button UI for `clarify` on Telegram and Discord, Discord channel history backfill, LSP semantic diagnostics on every write, a unified pluggable `video_generate`, a `computer_use` cua-driver backend that finally works with non-Anthropic providers, clickable URLs in any terminal, Zed ACP Registry integration via `uvx`, native Windows beta, 9 new optional skills, OpenRouter Pareto Code router, huggingface/skills as a trusted default tap. 12 P0 + 50 P1 closures.
+
+---
+
+## ✨ Highlights
+
+- **xAI Grok via SuperGrok OAuth — and grok-4.3 jumps to a 1M context window** — If you pay for SuperGrok, you can now use Grok inside Hermes by signing in with your xAI account — no API key, no separate billing. The wire-through also bumps grok-4.3 to a 1M token context window, so you can drop whole codebases or research corpora into a single prompt. Includes proper handling for entitlement errors and an SSH-to-tunnel docs page for when you're SSH'd into a remote box and need to complete the OAuth flow. ([#26534](https://github.com/NousResearch/hermes-agent/pull/26534), [#26664](https://github.com/NousResearch/hermes-agent/pull/26664), [#26644](https://github.com/NousResearch/hermes-agent/pull/26644), [#26592](https://github.com/NousResearch/hermes-agent/pull/26592))
+
+- **OpenAI-compatible local proxy for OAuth providers** — Run `hermes proxy` and you get a `http://localhost:port` endpoint that speaks the OpenAI API but is backed by whichever OAuth provider you're signed into — Claude Pro, ChatGPT Pro, SuperGrok. Now any tool that expects an OpenAI-compatible endpoint (Codex CLI, Aider, Cline, Continue, your custom scripts) just works with your existing subscription, no API key required. One subscription, every tool. ([#25969](https://github.com/NousResearch/hermes-agent/pull/25969))
+
+- **`x_search` — first-class X (Twitter) search tool** — The agent can now search X directly without installing a skill or wiring up a custom integration. Search the timeline, find threads, surface specific posts — straight from the chat. Auth with either your X OAuth login or an API key, whichever you have. ([#26763](https://github.com/NousResearch/hermes-agent/pull/26763))
+
+- **Microsoft Teams — end-to-end** — Hermes can now read messages from Teams and post back. The full Microsoft Graph stack lands together: auth + client foundation, a webhook listener that receives Teams events, a pipeline plugin runtime, and outbound delivery. Wire up the bot once, then chat to your agent from any Teams channel, DM, or group. (salvages of #21408–#21411) ([#21922](https://github.com/NousResearch/hermes-agent/pull/21922), [#21969](https://github.com/NousResearch/hermes-agent/pull/21969), [#22007](https://github.com/NousResearch/hermes-agent/pull/22007), [#22024](https://github.com/NousResearch/hermes-agent/pull/22024))
+
+- **Debloating wave — lighter installs, less you don't use** — A clean `pip install hermes-agent` used to pull down everything: every messaging adapter SDK, every image-gen SDK, every voice/TTS provider, whether you used them or not. Now those heavy backends (Slack / Matrix / Feishu / DingTalk adapters, hindsight client, codex app-server, Pixverse / Camofox / image-gen SDKs, voice/TTS providers) install automatically the first time you actually use them. The `[all]` extras drop everything covered by lazy-deps, the installer falls back through tiers when a wheel doesn't fit your platform, and a supply-chain advisory checker scans every install for unsafe versions. Faster installs, smaller disk footprint, fewer transitive vulnerabilities. ([#24220](https://github.com/NousResearch/hermes-agent/pull/24220), [#24515](https://github.com/NousResearch/hermes-agent/pull/24515), [#25014](https://github.com/NousResearch/hermes-agent/pull/25014), [#25038](https://github.com/NousResearch/hermes-agent/pull/25038), [#25766](https://github.com/NousResearch/hermes-agent/pull/25766), [#21818](https://github.com/NousResearch/hermes-agent/pull/21818))
+
+- **`pip install hermes-agent && hermes`** — Hermes Agent is now a real PyPI package. No more cloning the repo or running shell installers — one pip command and you're running. The wheel ships with the Ink TUI bundle and the shell launcher, so the full experience comes out of the box. (salvage of [#26350](https://github.com/NousResearch/hermes-agent/pull/26350)) ([#26593](https://github.com/NousResearch/hermes-agent/pull/26593), [#26148](https://github.com/NousResearch/hermes-agent/pull/26148))
+
+- **Cross-session 1h Claude prompt cache** — When you use Claude through Anthropic, OpenRouter, or Nous Portal, the prompt prefix (system prompt, skills, memory) now caches for an hour across sessions. Start a `/new` session and the first response comes back faster and cheaper because the cache is still warm from your last session. Background memory review hits the cache too, so it's not paying full price every turn. ([#23828](https://github.com/NousResearch/hermes-agent/pull/23828), [#25434](https://github.com/NousResearch/hermes-agent/pull/25434), [#24778](https://github.com/NousResearch/hermes-agent/pull/24778))
+
+- **180x faster `browser_console` evaluations** — When the agent uses the browser tool to inspect a page or run JavaScript, those calls now share one persistent connection to Chrome instead of spinning up a new DevTools session every time. The difference is huge: things that used to take a couple of seconds per call return in milliseconds. Real-world page interactions feel instant. ([#23226](https://github.com/NousResearch/hermes-agent/pull/23226))
+
+- **Cold-start performance wave — ~19 seconds off `hermes` launch** — Running `hermes` used to make you wait through a chunk of import overhead and network calls before you saw a prompt. Now the launch path is mostly deferred: heavy adapters only load when you use them, model catalogs come from disk cache first, doctor checks run in parallel, and `chat -q` skips the welcome banner entirely. The `hermes tools` All-Platforms screen alone dropped from 14 seconds to under 1.5 seconds. ([#22138](https://github.com/NousResearch/hermes-agent/pull/22138), [#22120](https://github.com/NousResearch/hermes-agent/pull/22120), [#22681](https://github.com/NousResearch/hermes-agent/pull/22681), [#22790](https://github.com/NousResearch/hermes-agent/pull/22790), [#22808](https://github.com/NousResearch/hermes-agent/pull/22808), [#22831](https://github.com/NousResearch/hermes-agent/pull/22831), [#22859](https://github.com/NousResearch/hermes-agent/pull/22859), [#22904](https://github.com/NousResearch/hermes-agent/pull/22904), [#22766](https://github.com/NousResearch/hermes-agent/pull/22766), [#25341](https://github.com/NousResearch/hermes-agent/pull/25341))
+
+- **Two new messaging platforms — LINE + SimpleX Chat** — LINE is huge in Japan, Korea, and Taiwan, and now Hermes runs natively on the LINE Messaging API. SimpleX Chat is the privacy-focused decentralized messenger with no user IDs — also wired up as a first-class platform. That brings Hermes to 22 messaging platforms total, so wherever you and your team chat, the agent can be there. ([#23197](https://github.com/NousResearch/hermes-agent/pull/23197), [#26232](https://github.com/NousResearch/hermes-agent/pull/26232))
+
+- **`/handoff` actually transfers the session live** — Switching models or personalities mid-conversation used to mean losing context or starting over. Now `/handoff` moves your active session — every message, every tool call, every piece of context — to the target model, persona, or profile, live, without dropping anything. Mid-debugging hand off from a fast model to a deep-reasoning one, or pass a session between profiles for different parts of a task. ([#23395](https://github.com/NousResearch/hermes-agent/pull/23395))
+
+- **Native button UI for `clarify` on Telegram and Discord** — When the agent uses the `clarify` tool to ask you a multiple-choice question, it now shows real platform-native buttons on Telegram and Discord instead of asking you to type back the option number. Tap the button, the agent gets your answer. Especially nice on mobile. ([#24199](https://github.com/NousResearch/hermes-agent/pull/24199), [#25485](https://github.com/NousResearch/hermes-agent/pull/25485))
+
+- **Discord channel history backfill (default on)** — When Hermes joins a Discord channel or thread for the first time, it now reads the recent message history so it knows what's been said before it responds. No more "what are we talking about?" — the agent has the context that's already on screen for everyone else. ([#25984](https://github.com/NousResearch/hermes-agent/pull/25984))
+
+- **`vision_analyze` returns pixels to vision-capable models** — When you point the agent at an image with `vision_analyze` and the active model can actually see (GPT-5, Claude, Gemini, Grok-vision), Hermes now passes the raw pixels straight to the model instead of converting them to a text description first. You get the model's actual visual reasoning instead of a degraded text-summary round-trip. ([#22955](https://github.com/NousResearch/hermes-agent/pull/22955))
+
+- **Per-turn file-mutation verifier footer** — After every turn that wrote or edited files, the agent now gets a short footer summarizing exactly what changed on disk — the file paths, the line counts, the actual delta. That means the agent catches its own mistakes when a write didn't land or got silently overwritten, instead of confidently telling you "I added the function" when the file wasn't actually saved. ([#24498](https://github.com/NousResearch/hermes-agent/pull/24498))
+
+- **LSP semantic diagnostics on every write** — When the agent uses `write_file` or `patch`, Hermes now runs a real language server against the edited file and surfaces any new errors back to the agent before the next turn. Type errors, undefined symbols, missing imports — caught immediately. Goes way beyond v0.13.0's basic Python/JSON/YAML/TOML linting because it's actual semantic analysis. ([#24168](https://github.com/NousResearch/hermes-agent/pull/24168), [#25978](https://github.com/NousResearch/hermes-agent/pull/25978))
+
+- **Unified `video_generate` with pluggable provider backends** — One tool, any video model. Hermes ships with the obvious backends already, but you can drop in a new video provider as a plugin without touching core. So when a new video model lands next month, it can be a one-file plugin instead of a fork. ([#25126](https://github.com/NousResearch/hermes-agent/pull/25126))
+
+- **`computer_use` cua-driver backend — works with non-Anthropic models now** — Computer-use (the agent controlling your mouse and keyboard to drive GUI apps) used to be locked to Anthropic's SDK. The new cua-driver backend works with non-Anthropic providers too, has proper focus-safe operations, and refreshes itself on `hermes update`. Now any vision-capable model can drive your desktop. (re-salvage of #16936) ([#21967](https://github.com/NousResearch/hermes-agent/pull/21967), [#24063](https://github.com/NousResearch/hermes-agent/pull/24063))
+
+- **Clickable URLs in any terminal** — Links in agent output are now real OSC8 hyperlinks with hover-highlight in any terminal that supports them. Click to open in your browser — no more copy-paste-trim of long URLs from the transcript. Just works in iTerm2, Kitty, Ghostty, modern Windows Terminal, etc. (@OutThisLife) ([#25071](https://github.com/NousResearch/hermes-agent/pull/25071), [#24013](https://github.com/NousResearch/hermes-agent/pull/24013))
+
+- **Zed ACP Registry — `uvx` install in one click** — Hermes is now listed in Zed's Agent Client Protocol registry, so Zed users can install it with one click. The install path uses `uvx` so there's no npm dependency. `hermes acp --setup-browser` bootstraps the browser tools for registry-driven installs. (salvage of [#25908](https://github.com/NousResearch/hermes-agent/pull/25908)) ([#26079](https://github.com/NousResearch/hermes-agent/pull/26079), [#26120](https://github.com/NousResearch/hermes-agent/pull/26120), [#26234](https://github.com/NousResearch/hermes-agent/pull/26234))
+
+- **OpenRouter Pareto Code router with `min_coding_score` knob** — OpenRouter's "Pareto" router automatically picks the cheapest model that meets a minimum quality bar. The new `min_coding_score` config lets you set that bar for coding tasks specifically — Hermes routes to the most affordable model that's at least that good at code. Stop paying for top-tier models when a mid-tier one would do. ([#22838](https://github.com/NousResearch/hermes-agent/pull/22838))
+
+- **NovitaAI as a new model provider** — NovitaAI joins the provider lineup, giving you another option for open-source model hosting (Llama, Qwen, DeepSeek, etc.) with their pricing and rate limits. (salvage #7219) (@kshitijk4poor) ([#25507](https://github.com/NousResearch/hermes-agent/pull/25507))
+
+- **Codex app-server runtime for OpenAI/Codex models** — An optional runtime that drives OpenAI's Codex CLI under the hood when you're using OpenAI or Codex paths. You get session reuse, automatic retirement of wedged sessions, and proper OAuth refresh classification — the kind of plumbing that makes long agentic runs not fall over. ([#24182](https://github.com/NousResearch/hermes-agent/pull/24182), [#25769](https://github.com/NousResearch/hermes-agent/pull/25769))
+
+- **`huggingface/skills` as a trusted default tap** — The community skills index hosted at huggingface.co/skills is now wired into the Skills Hub by default. So when somebody publishes a useful skill there, you can install it from your own `hermes skills` browser without any extra config. (closes #2549) ([#26219](https://github.com/NousResearch/hermes-agent/pull/26219))
+
+- **9 new optional skills** — Hyperliquid (perp + spot trading via the SDK and REST API), Yahoo Finance (live market data, fundamentals, historicals), api-testing (REST + GraphQL debug recipes), unified EVM multi-chain (one skill covers Ethereum + L2s + Base), darwinian-evolver (evolutionary prompt/skill tuning), osint-investigation (OSINT recipes for people / domains / orgs), pinggy-tunnel (expose local services to the public internet), watchers (polls RSS / HTTP JSON / GitHub via cron `no_agent` mode for change detection), and a full Notion overhaul for the May 2026 Developer Platform. ([#23582](https://github.com/NousResearch/hermes-agent/pull/23582), [#23583](https://github.com/NousResearch/hermes-agent/pull/23583), [#23590](https://github.com/NousResearch/hermes-agent/pull/23590), [#25299](https://github.com/NousResearch/hermes-agent/pull/25299), [#26760](https://github.com/NousResearch/hermes-agent/pull/26760), [#26729](https://github.com/NousResearch/hermes-agent/pull/26729), [#26765](https://github.com/NousResearch/hermes-agent/pull/26765), [#21881](https://github.com/NousResearch/hermes-agent/pull/21881), [#26612](https://github.com/NousResearch/hermes-agent/pull/26612))
+
+- **API server exposes run approval events** — If you're driving Hermes programmatically through the HTTP API, long-running runs no longer silently hang when the agent hits an approval-required command. The approval request now surfaces on the API stream so your client can prompt the user and reply — no more silent stalls. (salvage of [#20311](https://github.com/NousResearch/hermes-agent/pull/20311)) ([#21899](https://github.com/NousResearch/hermes-agent/pull/21899))
+
+- **Plugins can run any LLM call via `ctx.llm` + replace built-in tools via `tool_override`** — If you're writing a Hermes plugin, you now get first-class access to make LLM calls through the active provider and credentials — no manual client wiring. The new `tool_override` flag lets a plugin swap out a built-in tool with its own implementation cleanly. Plugin authors get the same model-routing and auth plumbing the core agent uses. (closes #11049) ([#23194](https://github.com/NousResearch/hermes-agent/pull/23194), [#26759](https://github.com/NousResearch/hermes-agent/pull/26759))
+
+- **Brave Search (free tier) + DuckDuckGo (DDGS) as web-search providers** — Two new free web-search backends join Tavily, SearXNG, and Exa. Brave Search has a generous free tier; DDGS is the DuckDuckGo scraper that needs no key at all. Pick whichever fits your budget and rate-limit needs. ([#21337](https://github.com/NousResearch/hermes-agent/pull/21337))
+
+- **Sudo brute-force block + 3 dangerous-command bypasses closed + tool-error sanitization** — The approval gate now blocks `sudo -S` brute-force attempts and classifies stdin-fed or askpass-stripped sudo invocations as DANGEROUS. Three known bypasses of dangerous-command detection are closed (inspired by Claude Code's command-detection work). And tool error strings are now sanitized before being re-injected into the model context, so a malicious file or remote service can't pass instructions to your agent through error output. ([#23736](https://github.com/NousResearch/hermes-agent/pull/23736), [#26829](https://github.com/NousResearch/hermes-agent/pull/26829), [#26823](https://github.com/NousResearch/hermes-agent/pull/26823))
+
+- **`/subgoal` — user-added criteria appended to an active `/goal`** — When you've got a `/goal` running (the persistent Ralph-loop goal where the agent keeps going until criteria are met), you can now use `/subgoal <text>` to layer extra success criteria onto it mid-run. The judge factors your new criteria into the done-or-keep-going decision without restarting the loop. ([#25449](https://github.com/NousResearch/hermes-agent/pull/25449))
+
+- **Provider rename — Alibaba Cloud → Qwen Cloud** — The Alibaba Cloud provider is renamed to Qwen Cloud in the picker and config to match what the rest of the world calls it. Existing config keys still work — no breaking changes — but the UI matches the actual brand now. ([#24835](https://github.com/NousResearch/hermes-agent/pull/24835))
+
+- **Native Windows support (early beta)** — Hermes now runs natively on `cmd.exe` and PowerShell without WSL. A full PowerShell installer handles MinGit auto-install, Microsoft Store python stub detection, and the foreground Ctrl+C dance. There's still rough edges (this is the "early beta" stamp) — ~40 follow-up Windows-only fixes already landed in the window — but the basic loop works end-to-end on a clean Windows box. ([#21561](https://github.com/NousResearch/hermes-agent/pull/21561))
+
+
+---
+
+## 🪟 Windows — Native Support (Early Beta)
+
+### Bootstrap & installer
+- **Native Windows support (early beta)** — first-class native Windows path across CLI / gateway / TUI / tools ([#21561](https://github.com/NousResearch/hermes-agent/pull/21561))
+- **PyPI wheel packaging — `pip install hermes-agent && hermes`** (salvage of #26350) ([#26593](https://github.com/NousResearch/hermes-agent/pull/26593))
+- **Recognise Shift+Enter as a newline key** + Windows docs (salvage #21545) ([#22130](https://github.com/NousResearch/hermes-agent/pull/22130))
+- **Preserve Ctrl+C for Windows foreground runs** (@helix4u) ([#22752](https://github.com/NousResearch/hermes-agent/pull/22752))
+- **Stop spamming cwd-missing + tirith-spawn warnings on every terminal call** ([#26618](https://github.com/NousResearch/hermes-agent/pull/26618))
+- **Use `--extra all` not `--all-extras`; drop lazy-covered extras from `[all]`** ([#24515](https://github.com/NousResearch/hermes-agent/pull/24515))
+
+### Windows-specific fixes (40+ across cli / tools / gateway / curator / TUI)
+A long tail of native-Windows fixes shipped alongside the beta — taskkill-based subprocess management, MinGit auto-install, Microsoft Store python stub detection, npm prefix handling, native PTY paths, signal handling differences, foreground process management, ANSI sequence handling, path normalization, file-locking semantics, and many more. Full list in commit log under `fix(windows)` / `feat(windows)` / `windows`.
+
+---
+
+## 🚀 Performance Wave
+
+### Cold start
+- **Cut ~19s from `hermes` cold start** — skills cache + lazy Feishu + no Nous HTTP at startup ([#22138](https://github.com/NousResearch/hermes-agent/pull/22138))
+- **Skip eager plugin discovery on known built-in subcommands** ([#22120](https://github.com/NousResearch/hermes-agent/pull/22120))
+- **Cache Nous auth + .env loads** — `hermes tools` All Platforms from 14s to <1.5s ([#25341](https://github.com/NousResearch/hermes-agent/pull/25341))
+- **Skip welcome banner on `chat -q` single-query mode** ([#22904](https://github.com/NousResearch/hermes-agent/pull/22904))
+- **Defer heavy google-cloud imports in google_chat to first adapter use** ([#22681](https://github.com/NousResearch/hermes-agent/pull/22681))
+- **Defer QQAdapter and YuanbaoAdapter imports via PEP 562** ([#22790](https://github.com/NousResearch/hermes-agent/pull/22790))
+- **Defer httpx import in teams to first webhook call** ([#22831](https://github.com/NousResearch/hermes-agent/pull/22831))
+- **Defer fal_client import to first generation request** ([#22859](https://github.com/NousResearch/hermes-agent/pull/22859))
+- **models.dev cache-first lookup, skip network when disk cache is fresh** ([#22808](https://github.com/NousResearch/hermes-agent/pull/22808))
+- **Parallelize API connectivity checks in `hermes doctor` and disable IMDS** ([#22766](https://github.com/NousResearch/hermes-agent/pull/22766))
+
+### Runtime
+- **180x faster `browser_console` evaluations** — route through supervisor's persistent CDP WebSocket ([#23226](https://github.com/NousResearch/hermes-agent/pull/23226))
+- **Tune Telegram cadence + adaptive fast-path for short replies** (salvage of #10388) ([#23587](https://github.com/NousResearch/hermes-agent/pull/23587))
+- **Accumulate length-continuation prefix via list+join** ([#26237](https://github.com/NousResearch/hermes-agent/pull/26237))
+
+### Prompt caching
+- **Cross-session 1h prefix cache for Claude on Anthropic / OpenRouter / Nous Portal** ([#23828](https://github.com/NousResearch/hermes-agent/pull/23828))
+- **Hit prefix cache in background review fork** (salvage #17276 + #25427) ([#25434](https://github.com/NousResearch/hermes-agent/pull/25434))
+
+---
+
+## 📦 Installation & Distribution
+
+### PyPI + supply-chain
+- **PyPI wheel packaging — `pip install hermes-agent && hermes`** (salvage of #26350) ([#26593](https://github.com/NousResearch/hermes-agent/pull/26593))
+- **Supply-chain advisory checker + lazy-install framework + tiered install fallback** ([#24220](https://github.com/NousResearch/hermes-agent/pull/24220))
+- **Use `--extra all` not `--all-extras`; drop lazy-covered extras from `[all]`** ([#24515](https://github.com/NousResearch/hermes-agent/pull/24515))
+- **Skip browser download when system chromium exists** (@helix4u) ([#25317](https://github.com/NousResearch/hermes-agent/pull/25317))
+
+### Nix
+- **`extraDependencyGroups` for sealed venv extras** (@alt-glitch) ([#21817](https://github.com/NousResearch/hermes-agent/pull/21817))
+- **Refresh npm lockfile hashes** — keeps Nix flake builds reproducible
+
+### Docker
+- **Bootstrap auth.json from env on first boot** ([#21880](https://github.com/NousResearch/hermes-agent/pull/21880))
+- **Drop manual @hermes/ink build, rely on esbuild bundle** — slimmer image
+
+### ACP / Zed
+- **Zed ACP Registry integration** (salvage of #25908) ([#26079](https://github.com/NousResearch/hermes-agent/pull/26079))
+- **Switch to uvx distribution, drop npm launcher** ([#26120](https://github.com/NousResearch/hermes-agent/pull/26120))
+- **`hermes acp --setup-browser` bootstraps browser tools for registry installs** ([#26234](https://github.com/NousResearch/hermes-agent/pull/26234))
+
+---
+
+## 🏗️ Core Agent & Architecture
+
+### Sessions & handoff
+- **`/handoff` actually transfers the session live** ([#23395](https://github.com/NousResearch/hermes-agent/pull/23395))
+- **Expose `HERMES_SESSION_ID` env var to agent tools** (@alt-glitch) ([#23847](https://github.com/NousResearch/hermes-agent/pull/23847))
+
+### Goals (Ralph loop)

[DIFF TRUNCATED - full diff has  1638 files changed, 226605 insertions(+), 45101 deletions(-) lines]
