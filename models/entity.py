from __future__ import annotations

from logging import getLogger
from typing import List
from uuid import uuid4

import config
from models.base import BaseModel, InstanceDoesNotExist


class Entity(BaseModel):
    NAME = "entity model"
    logger = getLogger(NAME)

    def __init__(self, name=None, generate_uuid=True, storage=None, save=True):
        if not storage:
            self.storage = config.get_storage()
        else:
            self.storage = storage

        if generate_uuid:
            self.uuid = str(uuid4())
        else:
            self.uuid = None

        if name:
            self.name = name
        else:
            self.name = f"{self.NAME}-{self.uuid}"

        if save:
            self.save()

    def save(self) -> None:
        self.logger.debug(f"saving instance ({self})")
        self.storage.put(self)

    def __eq__(self, other) -> bool:
        return self.uuid == other.uuid

    def __str__(self):
        return f"{self.NAME}-{self.uuid}"

    @classmethod
    def from_data(cls, uuid, name, storage=config.get_storage(), **kwargs) -> Entity:
        cls.logger.debug(f"constructing {cls.NAME} from data")

        instance = cls(name=name, generate_uuid=False, storage=storage, save=False)
        instance.uuid = uuid
        instance.save()

        return instance

    def change(self, name, to_save=True, **kwargs) -> None:
        if name:
            self.name = name

        if to_save:
            self.save()

    @classmethod
    def list(cls, storage=config.get_storage(), **kwargs) -> List[BaseModel]:
        cls.logger.debug(f"listing {cls.NAME} instances")
        return storage.list(cls)

    @classmethod
    def get(cls, uuid, storage=config.get_storage(), **kwargs) -> BaseModel:
        instance = storage.get(cls, uuid)

        cls.logger.debug(f"getting instance ({uuid})")
        if not instance:
            cls.logger.debug(f"instance ({uuid}) not found")
            raise InstanceDoesNotExist(uuid, cls)
        return instance

    def delete(self, storage=config.get_storage(), **kwargs) -> None:
        self.logger.debug(f"deleting instance ({self})")
        self.delete(self)

    def to_dict(self) -> dict:
        return {
            "type": self.NAME,
            "uuid": self.uuid,
            "name": self.name,
        }
