import logging
from abc import ABC, abstractmethod


class BaseHandlerService(ABC):
    NAME = "base handler"
    logger = logging.getLogger()

    @classmethod
    @abstractmethod
    def get_handlers(cls, **kwargs) -> dict:
        raise NotImplementedError
