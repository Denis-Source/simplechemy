import logging
from typing import Union, Type

from models.base import BaseModel, InstanceNotExist
from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.commands.base_commands import ModelCreateCommand, ModelGetCommand, ModelListCommand, ModelDeleteCommand
from services.events.base_events import ModelCreatedEvent, ModelGotEvent, ModelListedEvent, ModelDeletedEvent, \
    InstanceNotExistEvent


class WrongModelClassCommandException(Exception):
    def __init__(self, model_cls_model: Type[BaseModel]):
        self.model_cls_model = model_cls_model

    def __str__(self):
        return f"Command can not have {self.model_cls_model} class"


class ModelHandlerService:
    NAME = "model handler"
    logger = logging.getLogger()

    MODEL_CLS = {
        Game.NAME: Game,
        User.NAME: User
    }

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

    def get_model_cls(self, model_name):
        model_cls = self.MODEL_CLS.get(model_name)
        if not model_cls:
            raise NotImplementedError
        return model_cls

    def create(self, cmd: ModelCreateCommand) -> ModelCreatedEvent:
        self.logger.debug(f"creating {cmd.model_cls_name} with fields: {', '.join(cmd.fields.keys())}")
        model_cls = self.get_model_cls(cmd.model_cls_name)
        instance = model_cls(
            **cmd.fields
        )
        self.storage.put(instance)
        return ModelCreatedEvent(instance)

    def get(self, cmd: ModelGetCommand) -> Union[ModelGotEvent, InstanceNotExistEvent]:
        self.logger.debug(f"getting {cmd.model_cls_name} with {cmd.uuid}")
        try:
            instance = self.get_instance(
                instance_or_uuid=cmd.uuid,
                model_cls=self.get_model_cls(cmd.model_cls_name)
            )
            self.logger.debug(f"got {instance}")
            return ModelGotEvent(
                instance=instance
            )
        except InstanceNotExist:
            self.logger.debug(f"no {cmd.model_cls_name} found")
            return InstanceNotExistEvent(
                uuid=cmd.uuid,
                model_cls_name=cmd.model_cls_name
            )

    def list(self, cmd: ModelListCommand) -> ModelListedEvent:
        self.logger.debug(f"listing {cmd.model_cls_name}")

        instances = self.storage.list(self.get_model_cls(cmd.model_cls_name))

        self.logger.debug(f"listed {cmd.model_cls_name} ({len(instances)})")
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
