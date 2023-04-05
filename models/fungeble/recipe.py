from __future__ import annotations

from logging import getLogger

from models.base import BaseModel


class Recipe(BaseModel):
    NAME = "recipe model"
    logger = getLogger(NAME)

    @classmethod
    def from_data(cls, **kwargs) -> Recipe:
        pass

    def __init__(self, result, schema):
        self.schema = schema
        self.result = result

    def __str__(self):
        return f"{self.result.name} = {' + '.join(element.name for element in self.schema)}"

    def __eq__(self, other):
        return self.schema == other.schema

    def __hash__(self):
        return hash(str(self))

    def as_dict(self) -> dict:
        return {
            "result": self.result.as_dict(),
            "schema": [e.as_dict() for e in self.schema]
        }