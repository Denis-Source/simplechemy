from __future__ import annotations

from logging import getLogger
from uuid import uuid4

from models.base import BaseModel


class Entity(BaseModel):
    NAME = "entity"
    logger = getLogger(NAME)

    def __init__(self, name=None, generate_uuid=True):
        if generate_uuid:
            self.uuid = str(uuid4())
        else:
            self.uuid = None

        if name:
            self.name = name
        else:
            self.name = f"{self.NAME}-{self.uuid}"

    def __eq__(self, other) -> bool:
        return self.uuid == other.uuid

    def __str__(self):
        return f"{self.NAME}-{self.uuid}"

    def __hash__(self):
        return hash(str(self))

    @classmethod
    def from_data(cls, uuid, name, **kwargs) -> Entity:
        cls.logger.debug(f"constructing {cls.NAME} from data")

        instance = cls(name=name, generate_uuid=False)
        instance.uuid = uuid

        return instance

    def change(self, name, **kwargs) -> None:
        if name:
            self.name = name

    def as_dict(self) -> dict:
        return {
            "type": self.NAME,
            "uuid": self.uuid,
            "name": self.name,
        }
