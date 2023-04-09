from dataclasses import dataclass
from typing import List

from models.base import BaseModel
from services.message import Message


@dataclass
class ModelEvent(Message):
    NAME = "model event"


@dataclass
class ModelCreatedEvent(ModelEvent):
    NAME = "model_created_event"

    instance: BaseModel


@dataclass
class ModelGotEvent(ModelEvent):
    NAME = "model_got_event"

    instance: BaseModel


@dataclass
class ModelListedEvent(ModelEvent):
    NAME = "model_listed_event"

    instances: List[BaseModel]


@dataclass
class ModelChangedEvent(ModelEvent):
    NAME = "model_changed_event"

    instance: BaseModel


@dataclass
class ModelDeletedEvent(ModelEvent):
    NAME = "model_deleted_event"

    instance: BaseModel


@dataclass
class InstanceNotExistEvent(ModelEvent):
    NAME = "instance_not_exist_event"

    uuid: str
    model_cls_name: str
