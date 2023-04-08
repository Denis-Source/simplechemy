import json
from json import JSONDecodeError
from logging import getLogger
from typing import List

from tornado.websocket import WebSocketHandler

from app.handlers.auth.jwt_utils import jwt_authenticated_ws
from app.handlers.base_handler import BaseHandler
from app.handlers.responses import Responses
from app.handlers.statements import Statements
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
        self.methods = {
            Statements.GET_INSTANCE: self.get_instance
        }

    def _add_connection(self, user: User) -> None:
        if user:
            self._connections[user.uuid] = self

    def _remove_connection(self, user: User = None) -> None:
        if user:
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

    def get_instance(self, payload: dict) -> BaseModel:
        try:
            cmd = ModelGetCommand(
                model_cls_name=payload["model"],
                uuid=payload["uuid"]
            )
            event = self.application.message_bus.handle(cmd)
            return event.as_dict()
        except (KeyError, NotImplementedError):
            self.write_message(Responses.BAD_STATEMENT)

    def on_message(self, message: str) -> None:
        try:
            self.logger.debug(f"handling websocket {self.model_cls.NAME} message")
            message = json.loads(message)

            method = self.methods[message["statement"]]
            method(message["payload"])
        except (JSONDecodeError, KeyError):
            self.logger.info(f"bad statement from {self.current_user}")
            self.write_message()
