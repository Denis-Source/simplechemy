from logging import getLogger

from app.handlers.web_socket.base_websocket_handler import BaseWebSocketHandler
from models.nonfungeble.user import User


class UserHandler(BaseWebSocketHandler):
    NAME = "user wshandler"
    logger = getLogger(NAME)

    model_cls = User

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.methods = {
            self.statements.GET: self.get_instance,
            # self.statements.CHANGE: self.change,
            # self.statements.ENTER: self.enter,
            # self.statements.LEAVE: self.leave
        }
