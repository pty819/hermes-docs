.. _chapter-model-routing:

####################################
模型路由：多 Provider 的统一接入层
####################################

Hermes Agent 作为一个多模态 AI Agent 框架，其核心设计理念之一是 **Provider 无关性**——用户无需关心底层模型调用究竟发往 OpenRouter、Anthropic、OpenAI Codex 还是本地 Ollama 实例。实现这一抽象的核心模块就是 ``agent/auxiliary_client.py`` ，一个超过 2,400 行的"Provider 路由器"，它为所有辅助任务（上下文压缩、视觉分析、网页提取、会话搜索、记忆刷写等）提供统一的 LLM 调用接口。

本章将从设计动机、架构实现、Provider 注册表、客户端适配器、缓存机制、错误恢复等多个维度，深入剖析 Hermes 的多 Provider 统一接入层。

****************************
1. 为什么需要多 Provider
****************************

单一 Provider 依赖是生产级 Agent 系统的反模式。Hermes 的设计从一开始就假设：**没有哪个 Provider 是永远可用的** 。

成本多样性
============

不同 Provider 的定价模型差异巨大：

- OpenRouter 提供按量付费的聚合接入，同一个模型（如 ``google/gemini-3-flash-preview``）在不同 Provider 的价格可能相差数倍
- Nous Portal 订阅用户享有固定额度的推理调用
- 本地模型（Ollama、vLLM、llama.cpp）边际成本为零
- Anthropic、DeepSeek 等直连 Provider 对特定模型有更优价格

Hermes 的辅助任务（如上下文压缩、会话标题生成）对模型能力要求较低，使用廉价模型即可完成。``_API_KEY_PROVIDER_AUX_MODELS`` 字典为每个 Provider 预设了最优的辅助模型::

    _API_KEY_PROVIDER_AUX_MODELS: Dict[str, str] = {
        "gemini": "gemini-3-flash-preview",
        "zai": "glm-4.5-flash",
        "kimi-coding": "kimi-k2-turbo-preview",
        "minimax": "MiniMax-M2.7",
        "anthropic": "claude-haiku-4-5-20251001",
        ...
    }

可用性保障
============

Provider 中断是常态而非例外：

- OpenRouter 可能在高峰期限流
- Nous Portal OAuth Token 可能过期
- 本地 Ollama 实例可能未运行
- API 余额可能耗尽

Hermes 的自动检测链（auto-detection chain）确保当首选 Provider 不可用时，自动回退到下一个可用的 Provider。这种 **级联回退** 机制是系统可用性的基石。

能力差异
==========

不同 Provider 支持的能力不同：

- 文本任务几乎所有 Provider 都支持
- 视觉/多模态任务需要 Provider 和模型同时支持图像输入
- 工具调用（Tool Calling）并非所有模型都支持
- 长上下文窗口（>128K tokens）只有部分 Provider 提供

Hermes 通过 **任务类型路由** （text vs vision）和 **模型能力查询** （models.dev 注册表）来智能匹配任务与 Provider。

****************************
2. Provider 注册表
****************************

``hermes_cli/auth.py`` 定义了 ``PROVIDER_REGISTRY``——一个全局的 Provider 配置注册表。每个条目是一个 ``ProviderConfig`` 数据类::

    @dataclass
    class ProviderConfig:
        id: str                        # Provider 唯一标识
        name: str                      # 显示名称
        auth_type: str                 # 认证类型
        portal_base_url: str = ""      # Portal URL（OAuth Provider）
        inference_base_url: str = ""   # 推理 API 基础 URL
        client_id: str = ""            # OAuth Client ID
        scope: str = ""                # OAuth Scope
        api_key_env_vars: tuple = ()   # API Key 环境变量（按优先级）
        base_url_env_var: str = ""     # Base URL 覆盖环境变量

认证类型分为三类：

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 认证类型
     - 代表 Provider
     - 认证方式
   * - ``api_key``
     - OpenRouter, Gemini, Z.AI, Kimi, MiniMax, DeepSeek, xAI, Anthropic 等
     - 从环境变量或 .env 文件读取 API Key
   * - ``oauth_device_code``
     - Nous Portal
     - 设备码 OAuth 流程，Token 存储在 auth.json
   * - ``oauth_external``
     - OpenAI Codex, Qwen OAuth, Google Gemini CLI
     - 外部 OAuth 流程（第三方认证页面）

注册表中包含 20+ 个 Provider，覆盖了从全球到中国的主流 LLM 服务：

- **聚合器** ：OpenRouter, Nous Portal, AI Gateway (Vercel), OpenCode, Kilo Code, Hugging Face
- **直连国际** ：Anthropic, OpenAI Codex, Google Gemini, xAI, NVIDIA NIM, DeepSeek
- **直连中国** ：Z.AI (智谱/GLM), Kimi (月之暗面), MiniMax, Alibaba (通义千问), Xiaomi (小米 MiMo)
- **本地部署** ：Custom (Ollama, llama.cpp, vLLM, LM Studio)
- **企业级** ：AWS Bedrock, GitHub Copilot

.. mermaid:: ../diagrams/provider-resolution-flow.mmd

****************************
3. 辅助客户端路由
****************************

``resolve_provider_client()`` 是 Provider 路由的核心工厂函数，接受一个 Provider 标识符和可选的模型名称，返回一个配置好的客户端实例::

    def resolve_provider_client(
        provider: str,
        model: str = None,
        async_mode: bool = False,
        raw_codex: bool = False,
        explicit_base_url: str = None,
        explicit_api_key: str = None,
        api_mode: str = None,
        main_runtime: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Optional[Any], Optional[str]]:

该函数的解析逻辑如下：

1.  **规范化 Provider 名称** ：通过 ``_normalize_aux_provider()`` 处理别名（如 ``google`` -> ``gemini`` 、``claude`` -> ``anthropic`` 、``codex`` -> ``openai-codex``）
2.  **分派到特定 Provider 分支** ：根据规范化后的 Provider 名称，进入对应的解析分支
3.  **认证查找** ：从环境变量、auth.json、凭证池中查找认证信息
4.  **客户端构建** ：创建 OpenAI SDK 客户端（或适配器包装的客户端）
5.  **异步模式转换** ：如果 ``async_mode=True`` ，将同步客户端转换为异步客户端

Provider 名称别名系统 ``_PROVIDER_ALIASES`` 支持 20+ 个常见别名映射，降低用户的记忆负担::

    _PROVIDER_ALIASES = {
        "google": "gemini",
        "x-ai": "xai",
        "grok": "xai",
        "glm": "zai",
        "kimi": "kimi-coding",
        "moonshot": "kimi-coding",
        "claude": "anthropic",
        "claude-code": "anthropic",
        ...
    }

****************************
4. 文本/视觉任务的优先级链
****************************

Hermes 对文本任务和视觉任务采用不同的自动检测链。

文本任务优先级链
==================

``_resolve_auto()`` 函数实现了文本任务的自动检测链::

    # Step 1: 用户的主 Provider + 主模型
    # Step 2: 聚合器/回退链
    #   OpenRouter -> Nous Portal -> Custom -> Codex -> API-key Providers

**Step 1** 是首要路径：使用用户在 ``config.yaml`` 中配置的主 Provider 和主模型。这意味着如果用户选择了 ``deepseek/deepseek-chat`` ，辅助任务也会使用 DeepSeek，保持行为一致性。

**Step 2** 是回退链：当主 Provider 不可用时，按以下顺序尝试：

1.  **OpenRouter** — 最广泛的模型聚合器
2.  **Nous Portal** — OAuth 认证的推理平台
3.  **Custom** — 本地或自定义端点
4.  **Codex** — OpenAI Codex OAuth（通过 Responses API）
5.  **API-key Providers** — 遍历所有配置了 API Key 的 Provider

视觉任务优先级链
==================

``resolve_vision_provider_client()`` 实现了视觉任务的自动检测链，与文本任务有关键差异：

1.  **用户的主 Provider（如果支持视觉）** — 使用 ``_PROVIDER_VISION_MODELS`` 映射特定 Provider 的视觉模型::

        _PROVIDER_VISION_MODELS: Dict[str, str] = {
            "xiaomi": "mimo-v2-omni",
            "zai": "glm-5v-turbo",
        }

2.  **OpenRouter** — 使用 ``google/gemini-3-flash-preview``
3.  **Nous Portal** — 免费用户使用 ``xiaomi/mimo-v2-omni`` ，付费用户使用 ``google/gemini-3-flash-preview``
4.  **停止** — 视觉任务不像文本任务那样尝试所有 Provider

.. mermaid:: ../diagrams/auto-detection-chain.mmd

****************************
5. 客户端适配器模式
****************************

Hermes 的辅助客户端使用 OpenAI SDK 的 ``chat.completions.create()`` 接口作为统一抽象。然而并非所有 Provider 都原生支持这一接口。适配器模式通过 **接口转换** 解决这一不一致性。

CodexAuxiliaryClient（Responses -> ChatCompletions）
======================================================

OpenAI Codex 端点（``chatgpt.com/backend-api/codex``）使用 **Responses API** 而非 Chat Completions API。``CodexAuxiliaryClient`` 将 Chat Completions 风格的调用转换为 Responses API 调用::

    class CodexAuxiliaryClient:
        """OpenAI-client-compatible wrapper that routes through Codex Responses API."""

        def __init__(self, real_client: OpenAI, model: str):
            self._real_client = real_client
            adapter = _CodexCompletionsAdapter(real_client, model)
            self.chat = _CodexChatShim(adapter)
            self.api_key = real_client.api_key
            self.base_url = real_client.base_url

适配的核心转换逻辑在 ``_CodexCompletionsAdapter.create()`` 中：

1.  **消息格式转换** ：``text`` -> ``input_text`` ，``image_url`` -> ``input_image``
2.  **系统消息提取** ：将 ``system`` 角色消息提取为 ``instructions`` 参数
3.  **流式响应收集** ：使用 ``responses.stream()`` 收集所有文本增量和工具调用
4.  **响应格式归一化** ：将 Responses API 的输出转换为 ``choices[0].message.content`` 格式

AnthropicAuxiliaryClient
==========================

Anthropic 的 Messages API 使用与 OpenAI 不同的请求/响应格式。``AnthropicAuxiliaryClient`` 封装了原生 Anthropic 客户端，对外暴露统一的 ``chat.completions.create()`` 接口::

    class AnthropicAuxiliaryClient:
        def __init__(self, real_client, model, api_key, base_url, is_oauth=False):
            adapter = _AnthropicCompletionsAdapter(real_client, model, is_oauth)
            self.chat = _AnthropicChatShim(adapter)

适配器内部调用 ``build_anthropic_kwargs()`` 和 ``normalize_anthropic_response()`` 进行参数构建和响应归一化，并处理温度参数的特殊限制（Opus 4.7+ 拒绝任何非默认采样参数）。

异步适配器
============

每个同步适配器都有对应的异步版本（``AsyncCodexAuxiliaryClient`` 、``AsyncAnthropicAuxiliaryClient``），通过 ``asyncio.to_thread()`` 将同步调用包装为异步调用。这保证了所有消费者——无论是同步还是异步——都能使用相同的接口::

    class _AsyncCodexCompletionsAdapter:
        async def create(self, **kwargs) -> Any:
            import asyncio
            return await asyncio.to_thread(self._sync.create, **kwargs)

****************************
6. 客户端缓存架构
****************************

``_get_cached_client()`` 实现了一个线程安全的客户端缓存，避免每次 LLM 调用都重新创建客户端。

缓存设计要点
==============

- **缓存键** ：``(provider, async_mode, base_url, api_key, api_mode, runtime_key)``
- **最大容量** ：64 条（``_CLIENT_CACHE_MAX_SIZE``）
- **驱逐策略** ：FIFO（当缓存超过最大容量时，驱逐最早的条目）
- **线程安全** ：通过 ``_client_cache_lock`` （``threading.Lock``）保护

异步客户端的事件循环验证
==========================

异步客户端（``AsyncOpenAI``）内部使用 httpx，绑定到创建时的事件循环。在错误的事件循环上使用异步客户端会导致死锁或 ``RuntimeError`` 。缓存通过以下机制防止跨循环问题：

1.  **缓存键不包含循环标识**——循环身份在命中时检查而非在键中编码
2.  **每次异步命中验证** ：检查缓存的循环是否是当前且开放的循环
3.  **就地替换** ：当检测到过时循环时，强制关闭旧客户端并替换为新客户端

::

    if async_mode:
        loop_ok = (
            cached_loop is not None
            and cached_loop is current_loop
            and not cached_loop.is_closed()
        )
        if loop_ok:
            return cached_client, effective
        # Stale — evict and fall through to create a new client.
        _force_close_async_httpx(cached_client)
        del _client_cache[cache_key]

这种设计将缓存大小限制为 **每个唯一 Provider 配置一个条目** ，而不是 **每个（配置 x 事件循环）一个条目**——后者曾在长运行的 Gateway 进程中导致无限的文件描述符累积。

.. mermaid:: ../diagrams/client-cache-lifecycle.mmd

启动和关闭
============

- **启动时** ：``neuter_async_httpx_del()`` 猴子补丁 ``AsyncHttpxClientWrapper.__del__`` 为空操作，防止垃圾回收时在死循环上调度 ``aclose()``
- **关闭时** ：``shutdown_cached_clients()`` 关闭所有缓存客户端（同步客户端调用 ``close()`` ，异步客户端标记 httpx 状态为 ``CLOSED``）
- **每轮清理** ：``cleanup_stale_async_clients()`` 在每个 Agent 轮次后清理事件循环已关闭的异步客户端

****************************
7. 支付错误自动回退
****************************

当用户的 Provider 余额耗尽或支付失败时，Hermes 会自动尝试其他可用的 Provider，而不是直接向用户报告错误。

支付错误检测
==============

``_is_payment_error()`` 检测以下类型的错误：

1.  **HTTP 402** （Payment Required）
2.  **HTTP 429 或其他状态码** ，但错误消息包含支付相关关键词（``credits`` 、``insufficient funds`` 、``can only afford`` 、``billing`` 、``payment required``）
3.  **连接错误** （DNS 失败、连接拒绝、超时）——这类错误表明 Provider 端点完全不可达

::

    def _is_payment_error(exc: Exception) -> bool:
        status = getattr(exc, "status_code", None)
        if status == 402:
            return True
        err_lower = str(exc).lower()
        if status in (402, 429, None):
            if any(kw in err_lower for kw in ("credits", "insufficient funds",
                                               "can only afford", "billing",
                                               "payment required")):
                return True
        return False

回退链
========

``_try_payment_fallback()`` 在支付/连接错误后尝试替代 Provider：

1.  跳过已失败的 Provider
2.  遍历标准自动检测链
3.  对每个可用 Provider 构建新的请求参数并重试

关键设计决策：**只有 "auto" 模式（用户未明确指定 Provider）才触发回退** 。如果用户明确配置了某个 Provider 并遇到支付错误，系统会直接报错而不是静默切换——避免用户误以为仍在使用付费 Provider 而实际上切换到了免费但质量较低的 Provider。

****************************
8. 模型特定策略
****************************

不同模型有不同的行为契约，Hermes 通过一系列模型特定策略来适配这些差异。

固定温度
==========

Kimi 的 ``kimi-for-coding`` 端点对温度参数有严格限制：

- 非思考模式（``kimi-k2.5`` 、``kimi-k2-turbo-preview`` 等）：固定 0.6
- 思考模式（``kimi-k2-thinking`` 等）：固定 1.0
- 任何其他值都会导致 API 错误

::

    def _fixed_temperature_for_model(model: Optional[str]) -> Optional[float]:
        normalized = (model or "").strip().lower()
        fixed = _FIXED_TEMPERATURE_MODELS.get(normalized)
        if fixed is not None:
            return fixed
        bare = normalized.rsplit("/", 1)[-1]
        if bare in _KIMI_THINKING_MODELS:
            return 1.0
        if bare in _KIMI_INSTANT_MODELS:
            return 0.6
        return None

Developer 角色处理
====================

GPT-5/Codex 系列模型使用 ``developer`` 角色（通过 Responses API）而非 ``system`` 角色。``_CodexCompletionsAdapter.create()`` 自动将系统消息提取为 ``instructions`` 参数。

Anthropic 兼容 Provider
=========================

MiniMax 和 MiniMax-CN 等 Provider 暴露 Anthropic 兼容的 Messages API 端点（``/anthropic``）。``_to_openai_base_url()`` 将这些 URL 重写为 OpenAI 兼容的 ``/v1`` 端点。同时 ``_is_anthropic_compat_endpoint()`` 检测是否需要将 OpenAI 格式的图像块转换为 Anthropic 格式。

Opus 4.7+ 采样参数限制
========================

Opus 4.7+ 拒绝任何非默认的 ``temperature`` 、``top_p`` 、``top_k`` 参数。``_build_call_kwargs()`` 在构建请求参数时检查这一限制并静默移除采样参数。

*******************************
9. 上下文长度解析 10 级优先级
*******************************

``agent/model_metadata.py`` 中的 ``get_model_context_length()`` 实现了一个 10 级优先级的上下文长度解析链，确保在任何环境下都能获取尽可能准确的上下文窗口大小。

.. list-table::
   :header-rows: 1
   :widths: 10 40 50

   * - 优先级
     - 来源
     - 说明
   * - 0
     - 显式配置覆盖
     - ``config.yaml`` 中的 ``model.context_length``
   * - 1
     - 持久缓存
     - ``~/.hermes/context_length_cache.yaml`` 中之前探测到的值
   * - 2
     - 端点元数据
     - 自定义端点的 ``/models`` API 返回值
   * - 3
     - 本地服务器查询
     - Ollama ``/api/show`` 、LM Studio ``/api/v1/models`` 、vLLM ``/models``
   * - 4
     - Anthropic API
     - Anthropic ``/v1/models`` 端点（仅 API Key，不支持 OAuth）
   * - 5
     - Provider 感知查询
     - Nous 后缀匹配、models.dev Provider 映射
   * - 6
     - OpenRouter 元数据
     - OpenRouter ``/models`` API 缓存
   * - 7
     - Hardcoded 默认值
     - ``DEFAULT_CONTEXT_LENGTHS`` 中的模型家族模式匹配
   * - 8
     - 本地服务器探测
     - 作为最后手段再次查询本地服务器
   * - 9
     - 128K 回退
     - 默认上下文长度 ``DEFAULT_FALLBACK_CONTEXT``

本地服务器类型检测
====================

``detect_local_server_type()`` 通过探测已知端点来识别本地服务器类型：

- **Ollama** ：``/api/tags`` 返回 ``{"models": [...]}``
- **LM Studio** ：``/api/v1/models`` 返回 200
- **llama.cpp** ：``/v1/props`` 包含 ``default_generation_settings``
- **vLLM** ：``/version`` 返回 ``{"version": "..."}``

URL 到 Provider 推断
======================

``_infer_provider_from_url()`` 从 base URL 推断 Provider 名称，使得即使没有显式配置 Provider，也能通过 models.dev 查询上下文长度::

    _URL_TO_PROVIDER: Dict[str, str] = {
        "api.openai.com": "openai",
        "api.anthropic.com": "anthropic",
        "dashscope.aliyuncs.com": "alibaba",
        "api.deepseek.com": "deepseek",
        ...
    }

.. mermaid:: ../diagrams/context-length-resolution.mmd

****************************
10. Token 估算
****************************

Hermes 在多个环节需要进行 Token 估算，例如上下文压缩触发检查、预飞行（pre-flight）上下文窗口检查等。

estimate_tokens_rough
=======================

::

    def estimate_tokens_rough(text: str) -> int:
        """Rough token estimate (~4 chars/token) for pre-flight checks."""
        if not text:
            return 0
        return (len(text) + 3) // 4

使用 **4 字符/token** 的粗略估算比例。这是一个保守估计——实际分词器（如 tiktoken）的 token/字符比通常在 3-4 之间，取决于文本语言和内容。使用 4 字符/token 意味着估算值偏低，确保不会误报上下文溢出。

向上取整（``+3 // 4``）保证短文本（1-3 字符）不会估算为 0 个 token——这在处理大量短工具结果时尤其重要。

estimate_request_tokens_rough
===============================

::

    def estimate_request_tokens_rough(
        messages: List[Dict[str, Any]],
        *,
        system_prompt: str = "",
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> int:

这个函数估算完整的 Chat Completions 请求的 token 数，包括三个主要部分：

1.  **System Prompt** ：系统提示文本
2.  **消息列表** ：对话历史
3.  **工具 Schema** ：工具定义 JSON

工具 Schema 是一个容易被忽视但影响显著的 token 消耗源——当启用 50+ 工具时，仅 Schema 就可能消耗 20-30K tokens。

上下文探测阶梯
================

当模型的上下文长度未知时，Hermes 使用 ``CONTEXT_PROBE_TIERS`` 阶梯式探测::

    CONTEXT_PROBE_TIERS = [128_000, 64_000, 32_000, 16_000, 8_000]

从 128K 开始，如果请求超出上下文限制，逐步降低到下一个阶梯，直到找到可用的长度。这种方式避免了过度压缩或浪费上下文空间。

****************************
11. models.dev 注册表
****************************

``agent/models_dev.py`` 集成了 `models.dev <https://models.dev>`_ ——一个社区维护的 LLM 模型数据库，覆盖 4000+ 模型和 109+ Provider。

数据解析链
============

::

    1. Bundled snapshot (离线优先)
    2. Disk cache (~/.hermes/models_dev_cache.json)
    3. Network fetch (https://models.dev/api.json)
    4. Background refresh every 60 minutes

Hermes 采用 **离线优先** 策略：优先使用打包的快照，然后是磁盘缓存，最后才尝试网络获取。即使网络不可用，系统也能正常工作。

Provider ID 映射
==================

Hermes 的 Provider 命名与 models.dev 不完全一致。``PROVIDER_TO_MODELS_DEV`` 字典建立了映射关系::

    PROVIDER_TO_MODELS_DEV: Dict[str, str] = {
        "openrouter": "openrouter",
        "anthropic": "anthropic",
        "openai-codex": "openai",
        "kimi-coding": "kimi-for-coding",
        "copilot": "github-copilot",
        "ai-gateway": "vercel",
        ...
    }

模型查找使用 **精确匹配 + 大小写不敏感回退** 的策略::

    def _find_model_entry(models, model):
        entry = models.get(model)          # 精确匹配
        if entry:
            return entry
        model_lower = model.lower()
        for mid, mdata in models.items():   # 大小写不敏感
            if mid.lower() == model_lower:
                return mdata
        return None

隐藏模型过滤
==============

某些模型不适合在 Provider 目录中展示。``_should_hide_from_provider_catalog()`` 过滤以下模型：

- Google 的低 TPM Gemma 模型（在 Agent 流量下容易触发配额限制）
- 已废弃的 Google 模型（仍通过 models.dev 出现但在当前端点 404）

Agent 模型过滤
================

``list_agentic_models()`` 返回适合 Agent 使用的模型，过滤条件：

1.  ``tool_call=True`` —— 必须支持工具调用
2.  排除噪音模型（TTS、Embedding、预览快照、流式模型、纯图像模型）

::

    _NOISE_PATTERNS = re.compile(
        r"-tts\b|embedding|live-|-(preview|exp)-\d{2,4}[-_]|"
        r"-image\b|-image-preview\b|-customtools\b",
        re.IGNORECASE,
    )

****************************
12. 错误消息解析
****************************

当 API 调用因上下文限制失败时，Hermes 能从错误消息中提取关键信息，用于动态调整上下文窗口。

上下文限制提取
================

``parse_context_limit_from_error()`` 使用多个正则表达式模式从错误消息中提取上下文限制::

    patterns = [
        r'(?:max(?:imum)?|limit)\s*(?:context\s*)?(?:length|size|window)?\s*(?:is|of|:)?\s*(\d{4,})',
        r'context\s*(?:length|size|window)\s*(?:is|of|:)?\s*(\d{4,})',
        r'(\d{4,})\s*(?:token)?\s*(?:context|limit)',
        r'>\s*(\d{4,})\s*(?:max|limit|token)',
        r'(\d{4,})\s*(?:max(?:imum)?)\b',
    ]

支持的错误消息格式包括：

- ``"maximum context length is 32768 tokens"``
- ``"context_length_exceeded: 131072"``
- ``"Maximum context size 32768 exceeded"``
- ``"model's max context length is 65536"``

可用输出 Token 提取
=====================

``parse_available_output_tokens_from_error()`` 区分两类上下文错误：

1.  **Prompt 过长** ：输入本身超出上下文窗口——需要压缩历史
2.  **max_tokens 过大** ：输入没问题，但 ``input + max_tokens > window``——只需降低输出上限

Anthropic 的错误消息格式为::

    "max_tokens: 32768 > context_window: 200000 - input_tokens: 190000 = available_tokens: 10000"

该函数提取 ``available_tokens`` 值，使得 Hermes 可以在不改变 ``context_length`` 的前提下，仅调整 ``max_tokens`` 参数重试请求。

****************************
总结
****************************

Hermes 的多 Provider 统一接入层是一个精心设计的系统，其核心原则是：

1.  **Provider 无关性** ：所有辅助任务通过统一接口调用，无需关心底层 Provider
2.  **级联回退** ：当首选 Provider 不可用时，自动尝试下一个
3.  **适配器模式** ：通过适配器桥接不同 API 格式（Chat Completions、Responses、Anthropic Messages）
4.  **智能缓存** ：线程安全的客户端缓存，带有事件循环验证和过时驱逐
5.  **优雅降级** ：从精确配置到启发式估算，多层次的上下文长度解析

这些设计使得 Hermes 能够在 20+ 个 Provider 之间无缝切换，为用户提供始终可用的 Agent 体验。
