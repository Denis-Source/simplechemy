from dataclasses import dataclass
from typing import List, Type

from models.base import BaseModel


@dataclass
class ModelEvent:
    pass


@dataclass
class ModelCreatedEvent(ModelEvent):
    instance: BaseModel


@dataclass
class ModelGotEvent(ModelEvent):
    instance: BaseModel


@dataclass
class ModelListedEvent(ModelEvent):
    instances: List[BaseModel]


@dataclass
class ModelChangedEvent(ModelEvent):
    instance: BaseModel
    fields: dict


@dataclass
class ModelDeletedEvent(ModelEvent):
    instance: BaseModel


@dataclass
class ModelNotExistEvent(ModelEvent):
    uuid: str
    model_cls: Type[BaseModel]
