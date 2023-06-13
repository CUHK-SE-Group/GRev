from abc import ABC, abstractmethod
from typing import List

class GdbFactory(ABC):
    @abstractmethod
    def run(self, query: str) -> any:
        pass

    @abstractmethod
    def batch_run(self, query: List[str]) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
