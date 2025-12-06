from abc import ABC, abstractmethod

class BaseStreamHandler(ABC):
    @abstractmethod
    def on_data(self, chunk):
        pass

    @abstractmethod
    def get_result(self):
        pass
