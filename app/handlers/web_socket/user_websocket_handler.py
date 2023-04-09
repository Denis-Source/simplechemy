from logging import getLogger

from app.handlers.allowed_commands import AllowedCommands
from app.handlers.web_socket.base_websocket_handler import BaseWebSocketHandler
from models.nonfungeble.user import User
from services.commands.model_commands import ModelGetCommand, ModelChangeCommand


class UserWebSocketHandler(BaseWebSocketHandler):
    NAME = "user wshandler"
    logger = getLogger(NAME)

    def get_user(self, payload: dict):
        cmd = ModelGetCommand(
            uuid=self.current_user.uuid,
            model_cls_name=User.NAME
        )
        event = self.application.message_bus.handle(cmd)
        self.current_user = event.instance
        self.write_message(event.as_dict())

    def change_user(self, payload: dict):
        cmd = ModelChangeCommand(
            instance=self.current_user,
            fields=payload["fields"]
        )
        event = self.application.message_bus.handle(cmd)
        self.write_message(event.as_dict())
