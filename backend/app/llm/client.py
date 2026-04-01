"""LLM Client Factory - Get the configured LLM provider"""
import logging
from app.config.settings import settings
from app.llm.providers.base import LLMProvider
from app.llm.providers.ollama import OllamaClient
from app.llm.providers.openrouter import OpenRouterClient

logger = logging.getLogger(__name__)


def get_llm_client() -> LLMProvider:
    """Factory function to get the configured LLM provider"""
    provider = settings.LLM_PROVIDER.lower()

    if provider == "ollama":
        logger.info(f"Using Ollama provider with model: {settings.OLLAMA_MODEL}")
        return OllamaClient(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
        )
    elif provider == "openrouter":
        if not settings.OPENROUTER_API_KEY:
            logger.warning("OpenRouter API key not configured. Set OPENROUTER_API_KEY environment variable.")
        logger.info(f"Using OpenRouter provider with model: {settings.OPENROUTER_MODEL}")
        return OpenRouterClient(
            api_key=settings.OPENROUTER_API_KEY,
            model=settings.OPENROUTER_MODEL,
        )
    else:
        logger.warning(f"Unknown LLM provider: {provider}. Defaulting to Ollama.")
        return OllamaClient(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
        )


# Global LLM client instance
llm_client = get_llm_client()

# Legacy export for backward compatibility
ollama_client = llm_client
