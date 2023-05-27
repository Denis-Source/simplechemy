import config
from services.events.model_events import ModelEvent
from services.handlers.game_handler_service import GameHandlerService
from services.handlers.init_hanlder_service import InitHandlerService
from services.handlers.user_handler_service import UserHandlerService


class NoHandlerAvailableException(Exception):
    def __init__(self, cmd):
        self.cmd = cmd

    def __str__(self):
        return f"No handler exists for {self.cmd.__class__} command"


class MessageBus:
    def __init__(self, storage=config.get_storage()):
        self.storage = storage
        self._handlers = \
            InitHandlerService.get_handlers() | \
            UserHandlerService.get_handlers(self.storage) | \
            GameHandlerService.get_handlers(self.storage)

    def handle(self, cmd) -> ModelEvent:
        handler = self._handlers.get(cmd.__class__)
        if handler:
            return handler(cmd)
        else:
            raise NoHandlerAvailableException(cmd)
