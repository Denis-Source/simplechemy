from logging import getLogger
from typing import Optional

from tornado.web import RequestHandler

from models.nonfungeble.user import User


class BaseHandler(RequestHandler):
    NAME = "base handler"
    logger = getLogger(NAME)

    def set_current_user(self, user: Optional[User]):
        self.current_user = user
