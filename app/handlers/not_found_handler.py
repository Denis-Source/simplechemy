from tornado.web import HTTPError

from app.handlers.base_handler import BaseHandler


class NotFoundHandler(BaseHandler):
    def prepare(self):
        raise HTTPError(
            404
        )

