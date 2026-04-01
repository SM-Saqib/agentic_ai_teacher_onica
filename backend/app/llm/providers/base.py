"""Base LLM Provider - Abstract interface for all LLM providers"""
from abc import ABC, abstractmethod
from typing import List, Dict, AsyncGenerator, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the LLM service is available"""
        pass

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """Generate text from a prompt (non-streaming)"""
        pass

    @abstractmethod
    async def stream_generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> AsyncGenerator[str, None]:
        """Stream text generation from a prompt"""
        pass

    @abstractmethod
    async def get_available_models(self) -> List[str]:
        """Get list of available models"""
        pass
