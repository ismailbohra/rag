import os
from .pdf_loader import PDFLoader

class LoaderFactory:

    @staticmethod
    def get_loader(file_path: str):
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            return PDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
