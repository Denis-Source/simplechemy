import sys
from logging import getLogger
from typing import Optional, Union, Awaitable

from tornado.web import RequestHandler

from app.handlers.responses import Responses
from models.nonfungeble.user import User


class BaseHandler(RequestHandler):
    NAME = "base handler"

    def set_current_user(self, user: Optional[User]):
        self.current_user = user

    logger = getLogger(NAME)

    def set_default_headers(self):
        # TODO provide specific domains
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type")

    def options(self):
        self.set_status(200)
        self.finish()

    def write_error(self, status_code: int, **kwargs) -> None:
        _, error, _ = sys.exc_info()
        if hasattr(error, "log_message"):
            if error.log_message:
                error = error.log_message

        message = {"message": str(error)}

        if not str(error):
            message = Responses.GENERAL_ERROR

        self.write(
            message
        )
        self.finish()

    def write(self, chunk: Union[str, bytes, dict]) -> None:
        if isinstance(chunk, str):
            chunk = {"message": chunk}
        return super().write(chunk)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass
