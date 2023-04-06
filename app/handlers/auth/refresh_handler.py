from logging import getLogger

from app.handlers.auth.jwt_utils import jwt_authenticated, encode_jwt
from app.handlers.base_handler import BaseHandler


class RefreshHandler(BaseHandler):
    NAME = "refresh handler"
    logger = getLogger(NAME)

    @jwt_authenticated
    def post(self) -> None:
        self.logger.debug("refreshing token")

        token = encode_jwt(self.current_user.uuid)
        self.write({
            "token": token
        })
