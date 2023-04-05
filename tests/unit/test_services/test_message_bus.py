from dataclasses import dataclass

import pytest

from services.commands.base_commands import ModelCommand
from services.message_bus import MessageBus, NoHandlerAvailableException
from storage.memory import MemoryStorage


class TestMessageBus:
    storage = MemoryStorage

    @pytest.fixture
    def message_bus(self):
        return MessageBus(self.storage)

    def test_no_handler_available_exception(self, message_bus):
        @dataclass
        class NotSupportedCommand(ModelCommand):
            pass

        cmd = NotSupportedCommand()

        with pytest.raises(NoHandlerAvailableException):
            message_bus.handle(cmd)
