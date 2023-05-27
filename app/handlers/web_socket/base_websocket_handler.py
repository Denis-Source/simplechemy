import json
from json import JSONDecodeError
from logging import getLogger
from typing import List

from tornado.websocket import WebSocketHandler

from app.handlers.auth.jwt_utils import jwt_authenticated_ws
from app.handlers.base_handler import BaseHandler
from app.handlers.responses import Responses
from models.nonfungeble.user import User
from services.commands.user_commands import UserLeaveGameCommand


class UserAlreadyConnectedException(Exception):
    def __init__(self, user: User):
        self.user = user

    def __str__(self):
        return f"{self.user} already has ws connection"


class BaseWebSocketHandler(WebSocketHandler, BaseHandler):
    NAME = "base ws handler"
    logger = getLogger(NAME)

    _connections = {}

    def get_methods(self):
        raise NotImplementedError

    def _add_connection(self, user: User) -> None:
        if user:
            if user.uuid not in self._connections:
                self._connections[user.uuid] = self
            else:
                raise UserAlreadyConnectedException(user)

    def _remove_connection(self, user: User = None) -> None:
        if user:
            if user.uuid in self._connections:
                self._connections.pop(user.uuid)

    @jwt_authenticated_ws
    def open(self) -> None:
        self.logger.info(f"opened {self.NAME} connection ({id(self)})")
        try:
            self._add_connection(self.current_user)
            self.write_message(Responses.WS_OPENED)
        except UserAlreadyConnectedException as e:
            self.logger.info(e)
            self.close()

    def on_close(self) -> None:
        self.logger.info(f"closed {self.NAME} connection ({id(self)})")
        self._remove_connection(self.current_user)
        if self.current_user.game_uuid:
            cmd = UserLeaveGameCommand(
                instance=self.current_user,
                game=self.current_user.game_uuid
            )
            self.application.message_bus.handle(cmd)

    def broadcast(self, message: dict, user_list: List[User] = None) -> None:
        if user_list is None:
            connection_uuids = self._connections.keys()
        else:
            connection_uuids = [user.uuid for user in user_list]

        for cu in connection_uuids:
            connection = self._connections.get(cu)
            if connection:
                connection.write_message(message)

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
