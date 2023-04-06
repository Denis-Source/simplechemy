import logging
from typing import Union, Type

from models.base import BaseModel, InstanceNotExist
from services.commands.base_commands import ModelCreateCommand, ModelGetCommand, ModelListCommand, ModelDeleteCommand
from services.events.base_events import ModelCreatedEvent, ModelGotEvent, ModelListedEvent, ModelDeletedEvent, \
    InstanceNotExistEvent


class WrongModelClassCommandException(Exception):
    def __init__(self, model_cls: Type[BaseModel]):
        self.model_cls = model_cls

    def __str__(self):
        return f"Command can not have {self.model_cls} class"


class ModelHandlerService:
    NAME = "model handler"
    logger = logging.getLogger()

    def __init__(self, storage):
        self.storage = storage

    def get_instance(self, instance_or_uuid: Union[BaseModel, str], model_cls) -> BaseModel:
        if isinstance(instance_or_uuid, model_cls):
            return instance_or_uuid
        elif isinstance(instance_or_uuid, str):
            instance = self.storage.get(
                model_cls=model_cls,
                uuid=instance_or_uuid
            )
            if not instance:
                raise InstanceNotExist(instance_or_uuid, model_cls)
            return instance
        else:
            raise WrongModelClassCommandException(instance_or_uuid)

    def create(self, cmd: ModelCreateCommand) -> ModelCreatedEvent:
        self.logger.debug(f"creating {cmd.model_cls.NAME} with fields: {', '.join(cmd.fields.keys())}")
        instance = cmd.model_cls(
            **cmd.fields
        )
        self.storage.put(instance)
        return ModelCreatedEvent(instance)

    def get(self, cmd: ModelGetCommand) -> Union[ModelGotEvent, InstanceNotExistEvent]:
        self.logger.debug(f"getting {cmd.model_cls} with {cmd.uuid}")
        try:
            instance = self.get_instance(
                instance_or_uuid=cmd.uuid,
                model_cls=cmd.model_cls
            )
            self.logger.debug(f"got {instance}")
            return ModelGotEvent(
                instance=instance
            )
        except InstanceNotExist:
            self.logger.debug(f"no {cmd.model_cls} found")
            return InstanceNotExistEvent(
                uuid=cmd.uuid,
                model_cls=cmd.model_cls
            )

    def list(self, cmd: ModelListCommand) -> ModelListedEvent:
        self.logger.debug(f"listing {cmd.model_cls}")

        instances = self.storage.list(cmd.model_cls)

        self.logger.debug(f"listed {cmd.model_cls} ({len(instances)})")
        return ModelListedEvent(
            instances=instances
        )

    def delete(self, cmd: ModelDeleteCommand) -> ModelDeletedEvent:
        self.logger.debug(f"deleting {cmd.instance}")

        instance = self.get_instance(cmd.instance, cmd.instance.__class__)
        self.storage.delete(instance)
        return ModelDeletedEvent(
            instance=instance
        )

    @classmethod
    def get_handlers(cls, storage) -> dict:
        handler = cls(storage)

        return {
            ModelCreateCommand: handler.create,
            ModelGetCommand: handler.get,
            ModelListCommand: handler.list,
            ModelDeleteCommand: handler.delete,
        }
