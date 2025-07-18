from abc import ABC, abstractmethod
from functools import reduce

from pydantic import BaseModel


class AbstractHandler(ABC):

    @abstractmethod
    def processing(self, x: str, y: BaseModel):
        raise NotImplementedError()

    def convertor_func(self, entities: list) -> str:
        return reduce(self.processing, entities, "")
