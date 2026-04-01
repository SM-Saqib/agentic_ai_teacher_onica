"""OpenRouter Models Configuration - Available models from OpenRouter"""

# OpenRouter API models - Add more models as needed
# Full list: https://openrouter.ai/api/v1/models
OPENROUTER_MODELS = {
    # OpenAI Models
    "openai/gpt-4": {
        "name": "OpenAI: GPT-4",
        "description": "Most capable model, best for complex tasks",
        "pricing": {
            "prompt": 0.03,  # per 1K tokens
            "completion": 0.06,
        },
    },
    "openai/gpt-4-turbo": {
        "name": "OpenAI: GPT-4 Turbo",
        "description": "Fast GPT-4 with 128K context",
        "pricing": {
            "prompt": 0.01,
            "completion": 0.03,
        },
    },
    "openai/gpt-3.5-turbo": {
        "name": "OpenAI: GPT-3.5 Turbo",
        "description": "Fast and cost-effective",
        "pricing": {
            "prompt": 0.0005,
            "completion": 0.0015,
        },
    },
    # Anthropic Models
    "anthropic/claude-3-opus": {
        "name": "Anthropic: Claude 3 Opus",
        "description": "Most capable Claude model",
        "pricing": {
            "prompt": 0.015,
            "completion": 0.075,
        },
    },
    "anthropic/claude-3-sonnet": {
        "name": "Anthropic: Claude 3 Sonnet",
        "description": "Balanced Claude model",
        "pricing": {
            "prompt": 0.003,
            "completion": 0.015,
        },
    },
    "anthropic/claude-3-haiku": {
        "name": "Anthropic: Claude 3 Haiku",
        "description": "Fastest Claude model",
        "pricing": {
            "prompt": 0.00025,
            "completion": 0.00125,
        },
    },
    # Google Models
    "google/gemini-pro": {
        "name": "Google: Gemini Pro",
        "description": "Fast general-purpose model",
        "pricing": {
            "prompt": 0.000125,
            "completion": 0.000375,
        },
    },
    # Meta Llama
    "meta-llama/llama-2-70b-chat": {
        "name": "Meta: Llama 2 70B Chat",
        "description": "Open-source large model",
        "pricing": {
            "prompt": 0.0007,
            "completion": 0.0009,
        },
    },
    "meta-llama/llama-2-13b-chat": {
        "name": "Meta: Llama 2 13B Chat",
        "description": "Open-source medium model",
        "pricing": {
            "prompt": 0.0001,
            "completion": 0.0001,
        },
    },
    # Mistral
    "mistralai/mistral-7b-instruct": {
        "name": "Mistral: 7B Instruct",
        "description": "Efficient open-source model",
        "pricing": {
            "prompt": 0.00014,
            "completion": 0.00014,
        },
    },
    "mistralai/mistral-large": {
        "name": "Mistral: Large",
        "description": "Powerful instruction-tuned model",
        "pricing": {
            "prompt": 0.008,
            "completion": 0.024,
        },
    },
    # NousResearch
    "nousresearch/nous-hermes-2-mistral-7b-dpo": {
        "name": "NousResearch: Hermes 2 7B",
        "description": "Quality open-source model",
        "pricing": {
            "prompt": 0.00018,
            "completion": 0.00018,
        },
    },
}


def get_model_id(model_key: str) -> str:
    """Get the full model ID from the key"""
    if model_key in OPENROUTER_MODELS:
        return model_key
    return None


def get_all_model_ids() -> list:
    """Get list of all available model IDs"""
    return list(OPENROUTER_MODELS.keys())


def get_model_info(model_key: str) -> dict:
    """Get information about a specific model"""
    return OPENROUTER_MODELS.get(model_key, {})


def is_valid_model(model_key: str) -> bool:
    """Check if a model ID is valid"""
    return model_key in OPENROUTER_MODELS
