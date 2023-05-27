import os.path

import config
from models.fungeble.element import Element
from services.commands.init_commands import LoadElementsInitCommand, LoadElementImagesInitCommand
from services.events.init_events import LoadedElementsInitEvent, LoadedElementInitErroredEvent, \
    LoadedElementImagesInitEvent
from services.message_bus import MessageBus
from services.utils import load_from_txt
from storage.memory import MemoryStorage


class TestInitServices:
    storage = MemoryStorage()
    message_bus = MessageBus(storage=storage)

    def test_loaded_elements_success(self):
        cmd = LoadElementsInitCommand()

        event = self.message_bus.handle(cmd)
        assert type(event) == LoadedElementsInitEvent

    def test_loaded_elements_filename(self):
        cmd = LoadElementsInitCommand(filepath=config.get_element_content_path())

        event = self.message_bus.handle(cmd)
        assert type(event) == LoadedElementsInitEvent

    def test_loaded_elements_wrong_filename(self):
        filepath = "/folder/sub_folder/filepath.txt"
        cmd = LoadElementsInitCommand(filepath=filepath)
        event = self.message_bus.handle(cmd)
        assert type(event) == LoadedElementInitErroredEvent

    def test_loaded_images_success(self):
        load_from_txt()
        event = self.message_bus.handle(
            LoadElementImagesInitCommand(
                convert_to_app_path=False
            )
        )
        assert type(event) == LoadedElementImagesInitEvent

        elements = Element.list()

        for element in elements:
            assert element.image
            assert os.path.exists(element.image)
