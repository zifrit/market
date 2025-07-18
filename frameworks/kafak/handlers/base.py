from abc import ABC, abstractmethod
from functools import reduce
from typing import List


class AbstractHandler(ABC):

    @abstractmethod
    def processing(self, x: str, y: dict):
        raise NotImplementedError()

    def convertor_func(self, entities: list) -> str:
        return reduce(self.processing, entities, "")
