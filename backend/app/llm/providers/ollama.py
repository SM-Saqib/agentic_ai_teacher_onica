"""Ollama LLM Provider - Integration with Ollama local LLM service"""
import logging
from typing import List, AsyncGenerator
import httpx

from app.llm.providers.base import LLMProvider
from app.config.settings import settings
from app.core.exceptions import LLMError

logger = logging.getLogger(__name__)


class OllamaClient(LLMProvider):
    """Client for Ollama LLM service"""

    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL
        self.client = None
        self.timeout = 300  # 5 minutes for LLM responses

    async def health_check(self) -> bool:
        """Check if Ollama service is running"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """Generate text from LLM"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False,
                    "num_predict": max_tokens,
                }

                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                )

                if response.status_code != 200:
                    raise LLMError(f"Ollama API error: {response.status_code}")

                result = response.json()
                return result.get("response", "").strip()

        except httpx.TimeoutException:
            raise LLMError("LLM request timeout")
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            raise LLMError(str(e))

    async def stream_generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> AsyncGenerator[str, None]:
        """Stream text generation from LLM"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": True,
                    "num_predict": max_tokens,
                }

                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json=payload,
                ) as response:
                    if response.status_code != 200:
                        raise LLMError(f"Ollama API error: {response.status_code}")

                    async for line in response.aiter_lines():
                        if line:
                            try:
                                import json
                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                            except Exception as e:
                                logger.error(f"Error parsing stream: {e}")

        except httpx.TimeoutException:
            raise LLMError("LLM request timeout")
        except Exception as e:
            logger.error(f"LLM streaming error: {e}")
            raise LLMError(str(e))

    async def get_available_models(self) -> List[str]:
        """Get list of available models in Ollama"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    models = data.get("models", [])
                    return [model.get("name", "") for model in models]
                return []
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            return []
