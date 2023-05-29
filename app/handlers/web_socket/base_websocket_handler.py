import json
from json import JSONDecodeError
from logging import getLogger
from typing import List

from jwt import DecodeError
from tornado.httputil import HTTPServerRequest
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from app.handlers.auth.jwt_utils import decode_jwt
from app.handlers.base_handler import BaseHandler
from app.handlers.responses import Responses
from models.nonfungeble.user import User
from services.commands.model_commands import ModelGetCommand
from services.commands.user_commands import UserLeaveGameCommand
from services.events.model_events import ModelGotEvent


class UserAlreadyConnectedException(Exception):
    def __init__(self, user: User):
        self.user = user

    def __str__(self):
        return f"{self.user} already has ws connection"


class Connection:
    def __init__(self, user: User, handler):
        self.user = user
        self.handler = handler
        self.count = 0
        self.is_authenticated = False

    def authenticate(self, token):
        if decode_jwt(token).get("sub") == self.user.uuid:
            self.is_authenticated = True

    def increment_count(self):
        self.count += 1


class BaseWebSocketHandler(WebSocketHandler, BaseHandler):
    NAME = "base ws handler"
    logger = getLogger(NAME)

    _connections = {}

    def __init__(
            self,
            application: Application,
            request: HTTPServerRequest,
            **kwargs
    ) -> None:
        super().__init__(application, request, **kwargs)
        self.authenticated = False

    def check_origin(self, origin):
        # TODO add origin check
        return True

    def get_methods(self):
        raise NotImplementedError

    def _add_connection(self, user: User) -> None:
        if user:
            if user.uuid not in self._connections:
                self._connections[user.uuid] = Connection(user, self)
            else:
                raise UserAlreadyConnectedException(user)

    def _remove_connection(self, user: User = None) -> None:
        if user:
            if user.uuid in self._connections:
                self._connections.pop(user.uuid)

    def open(self) -> None:
        self.logger.info(f"opened {self.NAME} connection ({id(self)})")
        try:
            self.write_message(Responses.WS_OPENED)
        except UserAlreadyConnectedException as e:
            self.logger.info(e)
            self.close()

    def on_close(self) -> None:
        self.logger.info(f"closed {self.NAME} connection ({id(self)})")
        self._remove_connection(self.current_user)
        if self.current_user:
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
                connection.handler.write_message(message)

    def authenticate(self, payload):
        token = payload.get("token")
        if not token:
            raise DecodeError
        user_uuid = decode_jwt(token).get("sub")
        if not user_uuid:
            raise DecodeError

        cmd = ModelGetCommand(user_uuid, User.NAME)
        event = self.application.message_bus.handle(cmd)

        if isinstance(event, ModelGotEvent):
            self.current_user = event.instance
            self.authenticated = True

            if self.current_user.uuid in self._connections:
                self.logger.warning("multiple connections from one user")
                self.close(3000)
            else:
                self.write_message(Responses.AUTHENTICATED)
                self._connections[self.current_user.uuid] = Connection(self.current_user, self)

        else:
            raise DecodeError

    def on_message(self, request: str) -> None:
        try:
            self.logger.debug(f"handling websocket message for {self.current_user}")
            request = json.loads(request)

            if not self.authenticated:
                self.authenticate(request["payload"])
            else:
                connection = self._connections[self.current_user.uuid]
                connection.increment_count()

                method = self.get_methods()[request["message"]]
                payload = request.get("payload", {})
                method(
                    payload=payload
                )

        except DecodeError:
            self.logger.debug(f"request is not authenticated ({id(self)})")
            self.close(3000)

        except (JSONDecodeError, KeyError, NotImplementedError):
            self.logger.info(f"bad statement from {self.current_user}")
            self.close(1006)
