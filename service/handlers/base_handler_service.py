import logging
from typing import Union, Type

import config
from models.base import BaseModel, InstanceDoesNotExist
from service.commands.base_commands import ModelCreateCommand, ModelGetCommand, ModelListCommand, ModelDeleteCommand
from service.events.base_events import ModelCreatedEvent, ModelGotEvent, ModelListedEvent, ModelDeletedEvent, \
    ModelNotExistEvent


class WrongModelClassCommandException(Exception):
    def __init__(self, model_cls: Type[BaseModel]):
        self.model_cls = model_cls

    def __str__(self):
        return f"Command can not have {self.model_cls} class"


class ModelHandlerService:
    NAME = "model handler"
    storage = config.get_storage()
    logger = logging.getLogger()

    @classmethod
    def set_storage(cls, storage):
        cls.storage = storage

    @classmethod
    def get_instance(cls, instance_or_uuid: Union[BaseModel, str], model_cls) -> BaseModel:
        if isinstance(instance_or_uuid, model_cls):
            return instance_or_uuid
        elif isinstance(instance_or_uuid, str):
            return model_cls.get(instance_or_uuid)
        else:
            raise WrongModelClassCommandException(instance_or_uuid)

    @classmethod
    def create(cls, cmd: ModelCreateCommand) -> ModelCreatedEvent:
        instance = cmd.model_cls(
            storage=cls.storage,
            **cmd.fields
        )

        return ModelCreatedEvent(
            instance=instance
        )

    @classmethod
    def get(cls, cmd: ModelGetCommand) -> Union[ModelGotEvent, ModelNotExistEvent]:
        try:
            instance = cmd.model_cls.get(
                uuid=cmd.uuid,
                storage=cls.storage
            )
            return ModelGotEvent(
                instance=instance
            )
        except InstanceDoesNotExist:
            return ModelNotExistEvent(
                uuid=cmd.uuid,
                model_cls=cmd.model_cls
            )

    @classmethod
    def list(cls, cmd: ModelListCommand) -> ModelListedEvent:
        instances = cls.default_model_cls.list(storage=cls.storage)
        return ModelListedEvent(
            instances=instances
        )

    @classmethod
    def delete(cls, cmd: ModelDeleteCommand) -> ModelDeletedEvent:
        cmd.instance.delete()
        return ModelDeletedEvent()
