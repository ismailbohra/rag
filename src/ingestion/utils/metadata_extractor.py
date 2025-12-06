from langchain_core.documents import Document
from typing import List
import os

class MetadataExtractor:

    @staticmethod
    def attach(file_path: str, docs: List[Document]):
        base_name = os.path.basename(file_path)
        for doc in docs:
            doc.metadata["source"] = base_name
            doc.metadata["file_path"] = file_path
