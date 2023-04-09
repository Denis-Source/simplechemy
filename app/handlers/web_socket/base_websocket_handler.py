import json
from json import JSONDecodeError
from logging import getLogger
from typing import List

from tornado.websocket import WebSocketHandler

from app.handlers.auth.jwt_utils import jwt_authenticated_ws
from app.handlers.base_handler import BaseHandler
from app.handlers.responses import Responses
from models.nonfungeble.user import User
from services.events.model_events import ModelEvent


class BaseWebSocketHandler(WebSocketHandler, BaseHandler):
    NAME = "base ws handler"
    logger = getLogger(NAME)

    _connections = {}

    def get_methods(self):
        raise NotImplementedError

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

    def broadcast(self, event: ModelEvent, user_list: List[User]) -> None:
        for user in user_list:
            connection = self._connections.get(user.uuid)
            if connection:
                connection.write(event.as_dict())

    def on_message(self, request: str) -> None:
        try:
            self.logger.debug(f"handling websocket message for {self.current_user}")
            request = json.loads(request)

            method = self.get_methods()[request["message"]]
            payload = request.get("payload", {})
            method(
                payload=payload
            )
        except (JSONDecodeError, KeyError, NotImplementedError):
            self.logger.info(f"bad statement from {self.current_user}")
            self.write_message(Responses.BAD_REQUEST)
