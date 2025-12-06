from typing import List, Dict, Any
from langchain_core.documents import Document
class ResponseFormatter:
    @staticmethod
    def format_answer(text: str, retrieved: List[tuple]) -> Dict[str, Any]:
        """
        Attach retrieved doc ids as citations and return structured JSON.
        retrieved: List[(Document, score)]
        """
        citations = []
        for doc, score in retrieved:
            cid = doc.metadata.get("id", doc.metadata.get("source"))
            citations.append({"id": cid, "score": float(score), "meta": doc.metadata})

        return {
            "answer": text.strip(),
            "citations": citations
        }
