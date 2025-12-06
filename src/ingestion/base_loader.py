from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document

class BaseLoader(ABC):
    """Abstract base class for all file loaders.
    Each loader must return LangChain Document objects.
    """

    @abstractmethod
    def load(self) -> List[Document]:
        pass
