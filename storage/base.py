from abc import ABC, abstractmethod
from logging import getLogger
from typing import Type, List

from models.base import BaseModel


class BaseStorage(ABC):
    NAME = "base storage"
    logger = getLogger(NAME)

    def __str__(self):
        return f"{self.NAME} ({id(self)})"

    @abstractmethod
    def get(self, model_cls: Type[BaseModel], uuid: str) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def list(self, model_cls: Type[BaseModel], **kwargs) -> List[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    def put(self, model_cls: Type[BaseModel]) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, instance) -> None:
        raise NotImplementedError
