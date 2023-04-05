from logging import getLogger

from app.handlers.base_handler import BaseHandler


class PingHandler(BaseHandler):
    NAME = "ping handler"
    logger = getLogger(NAME)

    def get(self):
        self.write("pong")
