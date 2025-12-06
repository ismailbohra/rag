from typing import List
from langchain_core.documents import Document
import textwrap

DEFAULT_SYSTEM_PROMPT = """
You are an assistant that answers user questions using the provided context. 
Be concise, cite sources in square brackets like [source-id], and don't hallucinate facts.
If the answer is not present in the context, say "I don't know".
"""

class PromptManager:
    def __init__(self, system_prompt: str | None = None, user_template: str | None = None):
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        # user_template expects {context} and {question}
        self.user_template = user_template or (
            "Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
        )

    def build_context(self, docs: List[Document], max_chars: int = 4000) -> str:
        """
        Joins retrieved documents into a single string while keeping track of sources.
        Truncates to max_chars (simple heuristic).
        """
        pieces = []
        total = 0
        for i, d in enumerate(docs):
            snippet = d.page_content.strip()
            # include small snippet and a citation tag
            piece = f"[{d.metadata.get('id', d.metadata.get('source', f'doc{i}'))}] {snippet}"
            if total + len(piece) > max_chars:
                # truncate piece if needed
                remaining = max_chars - total - 20
                if remaining <= 0:
                    break
                piece = piece[:remaining] + "..."
                pieces.append(piece)
                break
            pieces.append(piece)
            total += len(piece)
        return "\n\n".join(pieces)

    def build_prompt(self, docs: List[Document], question: str, max_context_chars: int = 4000) -> str:
        context = self.build_context(docs, max_chars=max_context_chars)
        user_part = self.user_template.format(context=context, question=question)
        # Combine system + user as single prompt (for providers that accept single prompt)
        full_prompt = textwrap.dedent(self.system_prompt).strip() + "\n\n" + user_part
        return full_prompt
