from logging import getLogger
from typing import List

from tornado.web import HTTPError
from tornado.websocket import WebSocketHandler

from app.handlers.auth.jwt_utils import jwt_authenticated_ws
from app.handlers.base_handler import BaseHandler
from app.handlers.responses import Responses
from models.base import BaseModel
from models.nonfungeble.user import User
from services.commands.base_commands import ModelGetCommand
from services.events.base_events import BaseEvent


class BaseWebSocketHandler(WebSocketHandler, BaseHandler):
    NAME = "base ws handler"
    logger = getLogger(NAME)

    _connections = {}

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.methods = {}

    def _add_connection(self, user: User) -> None:
        self._connections[user.uuid] = self

    def _remove_connection(self, user: User) -> None:
        self._connections.pop(user.uuid)

    @jwt_authenticated_ws
    def open(self) -> None:
        self.logger.debug(f"opened {self.NAME} connection ({id(self)})")
        self._add_connection(self.current_user)
        self.write_message(Responses.WS_OPENED)

    def on_close(self) -> None:
        self.logger.debug(f"closed {self.NAME} connection ({id(self)})")
        self._remove_connection(self.current_user)

    def broadcast(self, event: BaseEvent, user_list: List[User]) -> None:
        for user in user_list:
            connection = self._connections.get(user.uuid)
            if connection:
                connection.write(event.as_dict())

    def get_instance(self, payload) -> BaseModel:
        try:
            cmd = ModelGetCommand(
                model_cls_name=payload["model"],
                uuid=payload["uuid"]
            )
            event = self.application.message_bus.handle(cmd)
            return event.as_dict()
        except KeyError:
            raise HTTPError(403)
        except NotImplementedError:
            raise HTTPError(404)
