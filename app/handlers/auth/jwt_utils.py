import functools
from datetime import datetime, timedelta
from logging import getLogger
from typing import Union

import jwt
from jwt.exceptions import DecodeError
from tornado.web import HTTPError
from tornado.web import RequestHandler

import config
from models.nonfungeble.user import User
from services.commands.base_commands import ModelGetCommand
from services.events.base_events import ModelGotEvent

OPTIONS = {
    "verify_signature": True,
    "verify_exp": True,
    "verify_nbf": False,
    "verify_iat": True,
    "verify_aud": False
}

logger = getLogger("jwt_auth")


def jwt_authenticated(method):
    @functools.wraps(method)
    def wrapper(self: RequestHandler, *args, **kwargs):
        try:
            logger.debug(f"authorizing request ({id(self)})")
            header = self.request.headers.get("Authorization")

            user_uuid = decode_header(header)
            cmd = ModelGetCommand(user_uuid, User.NAME)
            event = self.application.message_bus.handle(cmd)

            if isinstance(event, ModelGotEvent):
                self.current_user = event.instance
                logger.debug(f"request is authorized ({id(self)})")
                return method(self, *args, **kwargs)
            else:
                raise DecodeError
        except DecodeError:
            raise HTTPError(401)

    return wrapper


def jwt_authenticated_ws(method):
    @functools.wraps(method)
    def wrapper(self: RequestHandler, *args, **kwargs):
        try:
            logger.debug(f"authorizing request ({id(self)})")
            header = self.request.headers.get("Authorization")

            user_uuid = decode_header(header)
            cmd = ModelGetCommand(user_uuid, User)
            event = self.application.message_bus.handle(cmd)

            if isinstance(event, ModelGotEvent):
                self.current_user = event.instance
                logger.debug(f"request is authorized ({id(self)})")
                return method(self, *args, **kwargs)
            else:
                raise DecodeError
        except DecodeError:
            logger.debug(f"request is not authorized ({id(self)})")
            self.close(3000)

    return wrapper


def decode_header(header):
    if not header or len(header.split()) != 2:
        raise DecodeError

    name, token = header.split()
    decoded = decode_jwt(token)
    if name.lower() != "bearer" or not isinstance(decoded, dict):
        raise DecodeError
    try:
        user_uuid = decoded["sub"]
    except KeyError:
        raise DecodeError

    return user_uuid


def encode_jwt(instance_uuid: str, secret=config.get_secret(), dt=timedelta(60)) -> str:
    ts = datetime.utcnow()

    return jwt.encode(
        {
            "alg": config.JWT_ALGORITHM,
            "iss": config.get_api_url(),
            "iat": ts,
            "exp": ts + config.TOKEN_LIFETIME,
            "sub": instance_uuid
        },
        secret,
        algorithm=config.JWT_ALGORITHM
    )


def decode_jwt(token: Union[str, bytes]) -> Union[str, dict]:
    return jwt.decode(
        token,
        config.get_secret(),
        options=OPTIONS,
        algorithms=[config.JWT_ALGORITHM]
    )
