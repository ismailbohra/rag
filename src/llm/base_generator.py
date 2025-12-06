from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseGenerator(ABC):
    """
    Abstract LLM generator interface.
    Implementations should handle batching, streaming, and error handling.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.0,
        top_p: float = 1.0,
        stop: List[str] | None = None,
        stream_handler = None,
        metadata: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Synchronous generation call.
        Returns a dict containing: { "text": str, "raw": Any, "usage": {...} }
        If stream_handler provided, should call stream_handler.on_data(...) iteratively.
        """
        pass
