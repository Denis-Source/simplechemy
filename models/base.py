from __future__ import annotations

from abc import ABC, abstractmethod
from logging import getLogger
from typing import List


class ModelException(Exception):
    def __init__(self, instance: BaseModel, message: str):
        self.user = instance
        self.message = message

    def __str__(self):
        return self.message


class InstanceDoesNotExist(Exception):
    def __init__(self, uuid, model_cls):
        self.model_uuid = uuid
        self.model_cls = model_cls

    def __str__(self):
        return f"model {self.model_cls.NAME} with {self.model_uuid} uuid does not exist"


class BaseModel(ABC):
    NAME = "base storage"
    logger = getLogger(NAME)

    @classmethod
    @abstractmethod
    def from_data(cls, **kwargs) -> BaseModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def list(cls, **kwargs) -> List[BaseModel]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get(cls, **kwargs) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def delete(self, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def change(self, to_save=True, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError
