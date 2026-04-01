"""OpenRouter LLM Provider - Integration with OpenRouter API"""
import logging
from typing import List, AsyncGenerator, Dict
import httpx

from app.llm.providers.base import LLMProvider
from app.llm.providers.openrouter_models import get_all_model_ids
from app.config.settings import settings
from app.core.exceptions import LLMError

logger = logging.getLogger(__name__)


class OpenRouterClient(LLMProvider):
    """Client for OpenRouter LLM service"""

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.model = model or settings.OPENROUTER_MODEL
        self.base_url = "https://openrouter.ai/api/v1"
        self.timeout = 300  # 5 minutes for LLM responses

        if not self.api_key:
            logger.warning("OpenRouter API key not configured. Set OPENROUTER_API_KEY environment variable.")

    async def health_check(self) -> bool:
        """Check if OpenRouter service is available"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                headers = self._get_headers()
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=headers,
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"OpenRouter health check failed: {e}")
            return False

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",  # Required by OpenRouter
            "X-Title": "AI Teacher",
        }

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
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=self._get_headers(),
                )

                if response.status_code != 200:
                    error_msg = f"OpenRouter API error: {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('error', {}).get('message', '')}"
                    except:
                        pass
                    raise LLMError(error_msg)

                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"].strip()
                return ""

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
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                }

                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=self._get_headers(),
                ) as response:
                    if response.status_code != 200:
                        error_msg = f"OpenRouter API error: {response.status_code}"
                        try:
                            error_data = await response.json()
                            error_msg += f" - {error_data.get('error', {}).get('message', '')}"
                        except:
                            pass
                        raise LLMError(error_msg)

                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]  # Remove "data: " prefix
                            if data_str.strip() == "[DONE]":
                                break

                            try:
                                import json
                                data = json.loads(data_str)
                                if "choices" in data and len(data["choices"]) > 0:
                                    choice = data["choices"][0]
                                    if "delta" in choice and "content" in choice["delta"]:
                                        yield choice["delta"]["content"]
                            except Exception as e:
                                logger.error(f"Error parsing stream: {e}")

        except httpx.TimeoutException:
            raise LLMError("LLM request timeout")
        except Exception as e:
            logger.error(f"LLM streaming error: {e}")
            raise LLMError(str(e))

    async def get_available_models(self) -> List[str]:
        """Get list of available models from OpenRouter"""
        try:
            # Return configured models (OpenRouter has many models, return our curated list)
            return get_all_model_ids()
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            return []
