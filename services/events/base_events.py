from dataclasses import dataclass
from typing import List, Type

from models.base import BaseModel
from services.message import Message


@dataclass
class BaseEvent(Message):
    pass


@dataclass
class ModelCreatedEvent(BaseEvent):
    instance: BaseModel


@dataclass
class ModelGotEvent(BaseEvent):
    instance: BaseModel


@dataclass
class ModelListedEvent(BaseEvent):
    instances: List[BaseModel]


@dataclass
class ModelChangedEvent(BaseEvent):
    instance: BaseModel
    fields: dict


@dataclass
class ModelDeletedEvent(BaseEvent):
    instance: BaseModel


@dataclass
class ModelNotExistEvent(BaseEvent):
    uuid: str
    model_cls: Type[BaseModel]
