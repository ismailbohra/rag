import google.generativeai as genai
from typing import Any, Dict, List
from .base_generator import BaseGenerator


class GeminiGenerator(BaseGenerator):
    """
    Safe, crash-proof Gemini text generator.
    Handles safety blocks, empty responses, and streaming.
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
        self._model = genai.GenerativeModel(model_name=self.model)

    def _extract_text(self, response) -> str:
        """
        Safely extract text from the Gemini response.
        Avoids crashes when response.text is invalid due to safety blocks.
        """
        try:
            # Normal case — response.text usually works
            return response.text
        except Exception:
            pass

        # Fallback: manually extract text from candidates/parts
        if not getattr(response, "candidates", None):
            return ""

        candidate = response.candidates[0]
        if not getattr(candidate, "content", None):
            return ""

        parts = getattr(candidate.content, "parts", [])
        texts = [
            p.text for p in parts
            if hasattr(p, "text") and isinstance(p.text, str)
        ]

        return " ".join(texts).strip()

    def generate(
        self,
        prompt: str,
        max_tokens: int = 5000,
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
                try:
                    if chunk.text:
                        stream_handler.on_data(chunk.text)
                except Exception:
                    # Ignore chunks that fail due to safety
                    pass

            return {
                "text": stream_handler.get_result(),
                "raw": None,
                "usage": {}
            }

        # -------------------------------
        # NON-STREAMING MODE
        # -------------------------------
        response = self._model.generate_content(
            prompt,
            generation_config=params,
            safety_settings=None,
        )

        # Safe text extraction
        text_output = self._extract_text(response)

        # Check safety block
        if not text_output:
            finish_reason = getattr(
                response.candidates[0], "finish_reason", None
            )
            if finish_reason == 2:  # SAFETY
                text_output = (
                    "The model could not provide an answer due to safety rules."
                )

        # Usage (if available)
        usage = {}
        if hasattr(response, "usage_metadata"):
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count,
                "completion_tokens": response.usage_metadata.candidates_token_count,
                "total_tokens": response.usage_metadata.total_token_count,
            }
        print(prompt)
        print(response)
        return {
            "text": text_output,
            "raw": response,
            "usage": usage,
        }
