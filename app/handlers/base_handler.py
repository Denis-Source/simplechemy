import sys
from logging import getLogger
from typing import Optional

from tornado.web import RequestHandler

from app.handlers.responses import Responses
from models.nonfungeble.user import User


class BaseHandler(RequestHandler):
    NAME = "base handler"
    logger = getLogger(NAME)

    def set_current_user(self, user: Optional[User]):
        self.current_user = user

    def write_error(self, status_code: int, **kwargs) -> None:
        _, error, _ = sys.exc_info()
        if hasattr(error, "log_message"):
            error = error.log_message

        message = {"message": str(error)}

        if not str(error):
            message = Responses.GENERAL

        self.write(
            message
        )
        self.finish()
