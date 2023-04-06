from tornado.web import HTTPError

from app.handlers.base_handler import BaseHandler
from app.handlers.responses import Responses


class NotFoundHandler(BaseHandler):
    def prepare(self):
        raise HTTPError(
            404,
            Responses.NOT_FOUND["message"]
        )
