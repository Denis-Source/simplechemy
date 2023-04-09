from logging import getLogger

from app.handlers.web_socket.base_websocket_handler import BaseWebSocketHandler
from models.nonfungeble.user import User
from services.commands.model_commands import ModelGetCommand, ModelChangeCommand
from services.commands.user_commands import UserEnterGameCommand, UserLeaveGameCommand
from services.events.user_events import UserEnteredGameEvent


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

    def enter_game(self, payload: dict):
        cmd = UserEnterGameCommand(
            instance=self.current_user,
            game=payload["game_uuid"]
        )
        event = self.application.message_bus.handle(cmd)
        if isinstance(event, UserEnteredGameEvent):
            self.broadcast(event.as_dict())
        else:
            self.write_message(event.as_dict())

    def leave_game(self, payload: dict):
        cmd = UserLeaveGameCommand(
            instance=self.current_user,
            game=self.current_user.game_uuid
        )
        event = self.application.message_bus.handle(cmd)
        self.broadcast(event.as_dict())
