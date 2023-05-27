import config
from services.commands.init_commands import LoadElementsInitCommand
from services.events.init_events import LoadedElementsInitEvent, LoadedElementInitErroredEvent
from services.message_bus import MessageBus
from storage.memory import MemoryStorage


class TestInitServices:
    storage = MemoryStorage()
    message_bus = MessageBus(storage=storage)

    def test_loaded_elements(self):
        cmd = LoadElementsInitCommand()

        event = self.message_bus.handle(cmd)
        assert type(event) == LoadedElementsInitEvent

    def test_loaded_elements_filename(self):
        cmd = LoadElementsInitCommand(filename=config.get_element_content_path())

        event = self.message_bus.handle(cmd)
        assert type(event) == LoadedElementsInitEvent

    def test_loaded_elements_wrong_filename(self):
        filename = "/folder/sub_folder/filepath.txt"
        cmd = LoadElementsInitCommand(filename=filename)
        event = self.message_bus.handle(cmd)
        assert type(event) == LoadedElementInitErroredEvent
