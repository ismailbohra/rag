from typing import List
from langchain_core.documents import Document
from .loaders.loader_factory import LoaderFactory
from .utils.metadata_extractor import MetadataExtractor
from .utils.file_validator import FileValidator

class IngestionPipeline:

    def __init__(self, enable_metadata: bool = True):
        self.enable_metadata = enable_metadata

    def load(self, file_path: str) -> List[Document]:
        # Step 1: Validate
        FileValidator.validate(file_path)

        # Step 2: Auto-select loader
        loader = LoaderFactory.get_loader(file_path)

        # Step 3: Extract documents
        documents = loader.load()

        # Step 4: Enhance metadata
        if self.enable_metadata:
            MetadataExtractor.attach(file_path, documents)

        return documents
