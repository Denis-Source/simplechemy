from logging import getLogger

from jwt import InvalidTokenError, DecodeError
from tornado.web import HTTPError

from app.handlers.auth.jwt_utils import encode_jwt, decode_header, OPTIONS
from app.handlers.base_handler import BaseHandler


class RefreshHandler(BaseHandler):
    NAME = "refresh handler"
    logger = getLogger(NAME)

    def post(self) -> None:
        self.logger.debug("refreshing token")
        options = {**OPTIONS, "verify_exp": False}

        try:
            user_uuid = decode_header(self.request.headers.get("Authorization"), options)

            token = encode_jwt(user_uuid)
            self.write({
                "token": token
            })
        except (DecodeError, InvalidTokenError):
            raise HTTPError(401)
