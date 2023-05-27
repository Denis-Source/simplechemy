import logging
import os
from os import path
from typing import Union

import config
from models.fungeble.element import Element
from services.commands.init_commands import LoadElementsInitCommand, LoadElementImagesInitCommand
from services.events.init_events import LoadedElementsInitEvent, LoadedElementInitErroredEvent, \
    LoadedElementImagesInitEvent
from services.handlers.base_handler_service import BaseHandlerService
from services.utils import load_from_txt, create_element_image, convert_image_path


class InitHandlerService(BaseHandlerService):
    NAME = "init handler"
    logger = logging.getLogger(NAME)
    IMAGE_FORMAT = "png"

    def load_elements(self, cmd: LoadElementsInitCommand) -> \
            Union[LoadedElementsInitEvent, LoadedElementInitErroredEvent]:
        if cmd.filepath:
            filepath = cmd.filepath
        else:
            filepath = config.get_element_content_path()

        try:
            load_from_txt(filepath=filepath)
        except IOError:
            return LoadedElementInitErroredEvent()
        return LoadedElementsInitEvent()

    def load_element_images(self, cmd: LoadElementImagesInitCommand):
        if cmd.media_path:
            folder = cmd.media_path
        else:
            folder = config.get_media_path()

        if not path.exists(folder):
            os.makedirs(folder)

        for element in Element.list():
            image_path = path.join(folder, f"{element.name}.{self.IMAGE_FORMAT}")
            if not path.exists(image_path):
                create_element_image(element, image_path)

            if cmd.convert_to_app_path:
                image_path = convert_image_path(image_path)
            element.add_image(image_path)

        return LoadedElementImagesInitEvent()

    @classmethod
    def get_handlers(cls, **kwargs) -> dict:
        handler = cls()

        return {
            LoadElementsInitCommand: handler.load_elements,
            LoadElementImagesInitCommand: handler.load_element_images
        }
