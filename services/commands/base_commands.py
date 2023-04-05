from dataclasses import dataclass, field
from typing import Union, Type

from models.base import BaseModel


@dataclass
class ModelCommand:
    pass


@dataclass
class ModelCreateCommand(ModelCommand):
    model_cls: Type[BaseModel]
    fields: dict = field(default_factory=dict)


@dataclass
class ModelGetCommand(ModelCommand):
    uuid: str
    model_cls: Type[BaseModel]


@dataclass
class ModelListCommand(ModelCommand):
    model_cls: Type[BaseModel]


@dataclass
class ModelChangeCommand(ModelCommand):
    instance: Union[BaseModel, str]
    fields: dict


@dataclass
class ModelDeleteCommand(ModelCommand):
    instance: Union[BaseModel, str]
