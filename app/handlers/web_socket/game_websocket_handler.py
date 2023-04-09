from logging import getLogger

from app.handlers.web_socket.base_websocket_handler import BaseWebSocketHandler
from models.nonfungeble.game import Game
from services.commands.model_commands import ModelGetCommand, ModelCreateCommand, ModelListCommand, ModelDeleteCommand


class GameWebSocketHandler(BaseWebSocketHandler):
    NAME = "user wshandler"
    logger = getLogger(NAME)

    def create_game(self, payload: dict):
        cmd = ModelCreateCommand(
            model_cls_name=Game.NAME,
            fields=payload.get("fields", {}) | {"creator_user": self.current_user}
        )
        event = self.application.message_bus.handle(cmd)
        self.broadcast(event.as_dict())

    def get_game(self, payload: dict):
        cmd = ModelGetCommand(
            uuid=payload["uuid"],
            model_cls_name=Game.NAME
        )
        event = self.application.message_bus.handle(cmd)
        self.write_message(event.as_dict())

    def list_game(self, payload: dict):
        cmd = ModelListCommand(
            Game.NAME
        )
        event = self.application.message_bus.handle(cmd)
        self.write_message(event.as_dict())

    def delete_game(self, payload: dict):
        cmd = ModelDeleteCommand(
            instance=payload["uuid"],
            model_cls_name=Game.NAME
        )
        event = self.application.message_bus.handle(cmd)
        self.broadcast(event.as_dict())
