from langchain_core.documents import Document
from typing import List
import os

class MetadataExtractor:

    @staticmethod
    def attach(file_path: str, docs: List[Document]):
        base_name = os.path.basename(file_path)
        # Convert to relative path for portability
        rel_path = os.path.relpath(file_path)
        for doc in docs:
            doc.metadata["source"] = base_name
            doc.metadata["file_path"] = rel_path
            doc.metadata["file_name"] = base_name
            # Store original absolute path as well for serving
            doc.metadata["file_path_absolute"] = os.path.abspath(file_path)
