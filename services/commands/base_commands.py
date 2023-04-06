from dataclasses import dataclass, field
from typing import Union

from models.base import BaseModel
from services.message import Message


@dataclass
class ModelCommand(Message):
    pass


@dataclass
class ModelCreateCommand(ModelCommand):
    model_cls_name: str
    fields: dict = field(default_factory=dict)


@dataclass
class ModelGetCommand(ModelCommand):
    uuid: str
    model_cls_name: str


@dataclass
class ModelListCommand(ModelCommand):
    model_cls_name: str


@dataclass
class ModelChangeCommand(ModelCommand):
    instance: Union[BaseModel, str]
    fields: dict


@dataclass
class ModelDeleteCommand(ModelCommand):
    instance: Union[BaseModel, str]
