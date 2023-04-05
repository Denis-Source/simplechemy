from __future__ import annotations

from logging import getLogger
from typing import Type

from storage.base import BaseStorage


class MemoryStorage(BaseStorage):
    _dict = {}
    NAME = "memory repo"
    logger = getLogger(NAME)

    def get(self, model_cls: Type[BaseStorage], uuid: str):
        self.logger.debug(f"getting {model_cls.NAME} from {self}")
        return self._dict.get(uuid)

    def list(self, model_cls, **kwargs):
        self.logger.debug(f"listing {model_cls.NAME}s from {self}")
        return list(filter(lambda i: isinstance(i, model_cls), self._dict.values()))

    def put(self, instance) -> None:
        self.logger.debug(f"putting {instance} in {self}")
        self._dict[instance.uuid] = instance

    def delete(self, instance) -> None:
        self.logger.debug(f"deleting {instance} from {self}")
        try:
            self._dict.pop(instance.uuid)
        except KeyError:
            return

    def reset(self) -> None:
        self._dict = {}
