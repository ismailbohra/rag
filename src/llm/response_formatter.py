from typing import List, Dict, Any
from langchain_core.documents import Document
class ResponseFormatter:
    @staticmethod
    def format_answer(text: str, retrieved: List[tuple]) -> Dict[str, Any]:
        """
        Attach retrieved doc ids as citations with PDF file links and return structured JSON.
        retrieved: List[(Document, score)]
        """
        citations = []
        for doc, score in retrieved:
            cid = doc.metadata.get("id", doc.metadata.get("source"))
            file_path = doc.metadata.get("file_path")
            file_name = doc.metadata.get("file_name")
            
            citation = {
                "id": cid, 
                "score": float(score), 
                "meta": doc.metadata
            }
            
            # Add PDF link information if available
            if file_name and file_path:
                citation["pdf_file"] = file_name
                citation["pdf_path"] = file_path
                citation["pdf_link"] = f"/api/files/{file_name}"
            
            citations.append(citation)

        return {
            "answer": text.strip(),
            "citations": citations
        }
