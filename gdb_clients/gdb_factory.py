from abc import ABC, abstractmethod


class GdbFactory(ABC):
    @abstractmethod
    def run(self, query):
        pass

    @abstractmethod
    def batch_run(self, query):
        pass
