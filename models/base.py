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


class InstanceNotExist(Exception):
    def __init__(self, uuid, model_cls):
        self.model_uuid = uuid
        self.model_cls = model_cls

    def __str__(self):
        return f"{self.model_cls.NAME} with {self.model_uuid} uuid does not exist"


class BaseModel(ABC):
    NAME = "base model"
    logger = getLogger(NAME)

    @classmethod
    @abstractmethod
    def from_data(cls, **kwargs) -> BaseModel:
        raise NotImplementedError
