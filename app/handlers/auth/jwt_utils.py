import functools
from datetime import datetime
from logging import getLogger
from typing import Union

import jwt
from jwt.exceptions import DecodeError, InvalidTokenError
from tornado.web import HTTPError
from tornado.web import RequestHandler

import config
from models.nonfungeble.user import User
from services.commands.model_commands import ModelGetCommand
from services.events.model_events import ModelGotEvent

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
        except (DecodeError, InvalidTokenError):
            raise HTTPError(401)

    return wrapper


def jwt_authenticated_ws(method):
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
        except (DecodeError, InvalidTokenError):
            logger.debug(f"request is not authorized ({id(self)})")
            self.close(3000)

    return wrapper


def decode_header(header, options=OPTIONS):
    if not header or len(header.split()) != 2:
        raise DecodeError

    name, token = header.split()
    decoded = decode_jwt(token, options=options)
    if name.lower() != "bearer" or not isinstance(decoded, dict):
        raise DecodeError
    try:
        user_uuid = decoded["sub"]
    except KeyError:
        raise DecodeError

    return user_uuid


def encode_jwt(instance_uuid: str, secret=config.get_secret(), dt=None) -> str:
    ts = datetime.utcnow()
    if not dt:
        dt = config.TOKEN_LIFETIME

    return jwt.encode(
        {
            "alg": config.JWT_ALGORITHM,
            "iss": config.get_api_url(),
            "iat": ts,
            "exp": ts + dt,
            "sub": instance_uuid
        },
        secret,
        algorithm=config.JWT_ALGORITHM
    )


def decode_jwt(token: Union[str, bytes], options=OPTIONS) -> Union[str, dict]:
    return jwt.decode(
        token,
        config.get_secret(),
        options=options,
        algorithms=[config.JWT_ALGORITHM]
    )
