from service.commands.base_commands import ModelCreateCommand, ModelGetCommand, ModelDeleteCommand, ModelListCommand
from service.handlers.base_handler_service import ModelHandlerService
from service.handlers.user_handler_service import UserHandlerService


class NoHandlerAvailableException(Exception):
    def __init__(self, cmd):
        self.cmd = cmd

    def __str__(self):
        return f"No handler exists for {self.cmd.__class__} command"


class MessageBus:
    _handlers = {
        ModelCreateCommand: ModelHandlerService.create,
        ModelGetCommand: ModelHandlerService.get,
        ModelListCommand: ModelHandlerService.list,
        ModelDeleteCommand: ModelHandlerService.delete,
    }

    def handle(self, cmd):
        handler = self._handlers.get(cmd.__class__)
        if handler:
            return handler(cmd)
        else:
            raise NoHandlerAvailableException(cmd)
