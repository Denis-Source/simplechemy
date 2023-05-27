from dataclasses import dataclass, field
from typing import Union

from models.base import BaseModel
from services.commands.base_command import BaseCommand


@dataclass
class ModelCommand(BaseCommand):
    NAME = "model_cmd"


@dataclass
class ModelCreateCommand(ModelCommand):
    NAME = "model_create_cmd"

    model_cls_name: str
    fields: dict = field(default_factory=dict)


@dataclass
class ModelGetCommand(ModelCommand):
    NAME = "model_get_cmd"

    uuid: str
    model_cls_name: str


@dataclass
class ModelListCommand(ModelCommand):
    NAME = "model_list_cmd"

    model_cls_name: str


@dataclass
class ModelChangeCommand(ModelCommand):
    NAME = "model_change_cmd"

    instance: BaseModel
    fields: dict


@dataclass
class ModelDeleteCommand(ModelCommand):
    NAME = "model_delete_cmd"

    instance: Union[BaseModel, str]
    model_cls_name: str
