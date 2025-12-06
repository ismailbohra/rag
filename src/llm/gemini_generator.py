import google.generativeai as genai
from typing import Any, Dict, List
from .base_generator import BaseGenerator


class GeminiGenerator(BaseGenerator):
    """
    Google Gemini text generator.
    This matches the same interface as OpenAIGenerator and supports streaming.
    """

    def __init__(
        self,
        api_key: str = None,
        model: str = "gemini-2.5-flash",
        **kwargs
    ):
        if api_key:
            genai.configure(api_key=api_key)

        self.model = model
        self.default_kwargs = kwargs

        # Create model instance
        self._model = genai.GenerativeModel(model_name=self.model)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.0,
        top_p: float = 1.0,
        stop: List[str] | None = None,
        stream_handler=None,
        metadata: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:

        params = {
            "temperature": temperature,
            "top_p": top_p,
            "max_output_tokens": max_tokens,
        }
        params.update(self.default_kwargs)

        # -------------------------------
        # STREAMING MODE
        # -------------------------------
        if stream_handler:
            response = self._model.generate_content(
                prompt,
                generation_config=params,
                stream=True,
                safety_settings=None,
            )

            for chunk in response:
                if chunk.text:
                    stream_handler.on_data(chunk.text)

            return {
                "text": stream_handler.get_result(),
                "raw": None,
                "usage": {}   # Gemini doesn't return usage for streaming
            }

        # -------------------------------
        # NON-STREAMING MODE
        # -------------------------------
        response = self._model.generate_content(
            prompt,
            generation_config=params,
            safety_settings=None,
        )

        text_output = response.text if hasattr(response, "text") else ""

        usage = {}
        if hasattr(response, "usage_metadata"):
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count,
                "completion_tokens": response.usage_metadata.candidates_token_count,
                "total_tokens": response.usage_metadata.total_token_count,
            }

        return {
            "text": text_output,
            "raw": response,
            "usage": usage,
        }
