"""LLM Module - Multi-Provider LLM Integration

This module provides a flexible, provider-agnostic interface for integrating Large Language Models.
Currently supported providers:
- Ollama (local inference)
- OpenRouter (cloud API with access to multiple models)

Easy to extend for additional providers (Claude, Gemini, custom APIs, etc.)
"""

# USAGE EXAMPLES

# 1. CONFIGURE IN ENVIRONMENT VARIABLES
# ======================================

# For Ollama (default):
# LLM_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=mistral

# For OpenRouter:
# LLM_PROVIDER=openrouter
# OPENROUTER_API_KEY=sk-or-xxxxxxxx  # Get from https://openrouter.ai
# OPENROUTER_MODEL=openai/gpt-3.5-turbo


# 2. USE IN YOUR CODE
# ===================

# In any module, import the configured LLM client:
# from app.llm.client import llm_client

# Generate a response:
# response = await llm_client.generate(
#     prompt="What is machine learning?",
#     temperature=0.7,
#     max_tokens=512,
# )

# Stream a response (for real-time updates):
# async for chunk in llm_client.stream_generate(
#     prompt="Explain neural networks",
#     temperature=0.7,
#     max_tokens=1024,
# ):
#     print(chunk, end="", flush=True)

# Check service health:
# is_healthy = await llm_client.health_check()

# Get available models:
# models = await llm_client.get_available_models()


# 3. ADDING A NEW PROVIDER
# =========================

# Step 1: Create a new file in app/llm/providers/ (e.g., anthropic.py)

# from app.llm.providers.base import LLMProvider
# from typing import List, AsyncGenerator

# class AnthropicClient(LLMProvider):
#     async def health_check(self) -> bool:
#         # Implement
#         pass
#     
#     async def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
#         # Implement
#         pass
#
#     async def stream_generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> AsyncGenerator[str, None]:
#         # Implement
#         pass
#
#     async def get_available_models(self) -> List[str]:
#         # Implement
#         pass

# Step 2: Update settings (app/config/settings.py)
# ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
# ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-opus")

# Step 3: Update factory in app/llm/client.py
# elif provider == "anthropic":
#     return AnthropicClient(
#         api_key=settings.ANTHROPIC_API_KEY,
#         model=settings.ANTHROPIC_MODEL,
#     )

# Step 4: Update providers/__init__.py to export your new client

# Step 5: Update docker-compose.yml and .env files with new variables


# 4. AVAILABLE MODELS (OpenRouter)
# ================================

# See openrouter_models.py for the complete list with pricing info
# 
# Popular options:
# - openai/gpt-4              (Most capable, highest cost)
# - openai/gpt-3.5-turbo      (Fast, affordable, great balance)
# - anthropic/claude-3-opus   (Great at reasoning)
# - meta-llama/llama-2-70b    (Open source, free tier available)
# - mistralai/mistral-7b      (Small, efficient)


# 5. MIGRATION FROM OLLAMA_CLIENT TO LLM_CLIENT
# ==============================================

# Old code:
# from app.llm.client import ollama_client
# await ollama_client.generate(prompt)

# New code (works now, backward compatible):
# from app.llm.client import llm_client
# await llm_client.generate(prompt)

# Note: ollama_client still works as it's aliased to llm_client for backward compatibility
