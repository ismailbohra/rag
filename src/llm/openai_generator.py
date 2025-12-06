import openai
from typing import Any, Dict, List
from .base_generator import BaseGenerator

class OpenAIGenerator(BaseGenerator):
    def __init__(self, api_key: str = None, model: str = "gpt-4o", **kwargs):
        if api_key:
            openai.api_key = api_key
        self.model = model
        self.default_kwargs = kwargs

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
        params = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
        }
        if stop:
            params["stop"] = stop

        params.update(self.default_kwargs)

        if stream_handler:
            # streaming mode
            for chunk in openai.Completion.create(stream=True, **params):
                # chunk handling depends on provider. This is a simplified example.
                stream_handler.on_data(chunk)
            return {"text": stream_handler.get_result(), "raw": None, "usage": {}}

        # non-stream
        resp = openai.Completion.create(**params)
        text = resp.choices[0].text
        return {"text": text, "raw": resp, "usage": getattr(resp, "usage", {})}
