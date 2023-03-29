from __future__ import annotations

from logging import getLogger


class Recipe:
    NAME = "recipe model"
    logger = getLogger(NAME)

    def __init__(self, result, schema):
        self.schema = schema
        self.result = result

    def __str__(self):
        return f"{self.result.name} = {' + '.join(element.name for element in self.schema)}"

    def __eq__(self, other):
        return self.schema == other.schema

    def __hash__(self):
        return hash(str(self))
