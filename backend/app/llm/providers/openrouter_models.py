"""OpenRouter Models Configuration - Available models from OpenRouter

Free models are available on OpenRouter with no cost (rate-limited).
Full list: https://openrouter.ai/api/v1/models
"""

# Free models available on OpenRouter (no cost, rate-limited)
FREE_MODELS = [
    # 🔁 Router (recommended fallback)
    "openrouter/free",

    # 🧠 General / reasoning
    "openai/gpt-oss-120b:free",
    "z-ai/glm-4.5-air:free",

    # ⚡ Fast / cheap inference
    "stepfun/step-3.5-flash:free",

    # 🧠 NVIDIA Nemotron family
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "nvidia/nemotron-3-super:free",

    # 🧪 Arcee models
    "arcee-ai/trinity-mini:free",
    "arcee-ai/trinity-large-preview:free",

    # 💻 Coding / heavy models
    "qwen/qwen3-coder-480b-a35b-instruct:free",

    # 🧠 Meta (Llama family - free variants rotate but commonly available)
    "meta-llama/llama-3.3-70b-instruct:free",

    # 🧪 Other commonly routed free models (availability may vary)
    "deepseek/deepseek-r1:free",
]


def get_model_id(model_key: str) -> str:
    """Get the full model ID if it exists in FREE_MODELS"""
    if model_key in FREE_MODELS:
        return model_key
    return None


def get_all_model_ids() -> list:
    """Get list of all available free model IDs"""
    return FREE_MODELS.copy()


def get_model_info(model_key: str) -> dict:
    """Get information about a specific model"""
    if model_key in FREE_MODELS:
        return {
            "id": model_key,
            "name": model_key,
            "description": "Free OpenRouter model",
            "pricing": "FREE",
        }
    return {}


def is_valid_model(model_key: str) -> bool:
    """Check if a model ID is a valid free model"""
    return model_key in FREE_MODELS
