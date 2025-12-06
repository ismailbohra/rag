from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from typing import List
from ..base_loader import BaseLoader

class PDFLoader(BaseLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:
        loader = PyPDFLoader(self.file_path)
        return loader.load()
