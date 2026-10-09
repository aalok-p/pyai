from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from pyai.config import Config


def resolve_model(config: Config, model_ref: str | None = None):
    if model_ref and ":" in model_ref:
        provider_name, model_name = model_ref.split(":", 1)
        provider_cfg = config.get_provider(provider_name)
        return _build_model(provider_cfg, model_name)

    if model_ref:
        provider_cfg = config.get_provider()
        return _build_model(provider_cfg, model_ref)

    provider_cfg = config.get_provider()
    model_name = provider_cfg.get("default_model")
    if not model_name:
        raise ValueError("No model specified and no default_model in provider config")
    return _build_model(provider_cfg, model_name)


def _build_model(provider_cfg: dict, model_name: str):
    ptype = provider_cfg.get("type", "openai-compatible")
    if ptype == "openai-compatible":
        provider = OpenAIProvider(
            base_url=provider_cfg.get("base_url"),
            api_key=provider_cfg.get("api_key"),
        )
        return OpenAIChatModel(model_name, provider=provider)

    raise ValueError(f"Unsupported provider type: {ptype}")
