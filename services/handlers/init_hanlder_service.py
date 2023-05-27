import logging
from typing import Union

import config
from services.commands.init_commands import LoadElementsInitCommand
from services.events.init_events import LoadedElementsInitEvent, LoadedElementInitErroredEvent
from services.handlers.base_handler_service import BaseHandlerService
from services.utils import load_from_txt


class InitHandlerService(BaseHandlerService):
    NAME = "init handler"
    logger = logging.getLogger(NAME)

    def load_elements(self, cmd: LoadElementsInitCommand) -> Union[
            LoadedElementsInitEvent, LoadedElementInitErroredEvent]:
        if cmd.filename:
            filepath = cmd.filename
        else:
            filepath = config.get_element_content_path()

        try:
            load_from_txt(filepath=filepath)
        except IOError:
            return LoadedElementInitErroredEvent()
        return LoadedElementsInitEvent()

    @classmethod
    def get_handlers(cls, **kwargs) -> dict:
        handler = cls()

        return {
            LoadElementsInitCommand: handler.load_elements
        }
