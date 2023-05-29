import asyncio
from enum import Enum
from logging import getLogger

from tornado.web import Application, StaticFileHandler

import config
from app.handlers.auth.login_handler import LoginHandler
from app.handlers.auth.refresh_handler import RefreshHandler
from app.handlers.auth.register_handler import RegisterHandler
from app.handlers.not_found_handler import NotFoundHandler
from app.handlers.ping_handler import PingHandler
from app.handlers.web_socket.web_socket_handler import WebSocketHandler
from services.commands.init_commands import LoadElementsInitCommand, LoadElementImagesInitCommand
from services.message_bus import MessageBus


class Routes(str, Enum):
    user_http = r"/user"
    register = r"/register",
    login = r"/login",
    refresh = r"/refresh"

    ping = r"/ping",
    room = r"/room",
    ws = r"/"


class App(Application):
    NAME = "chat app"
    logger = getLogger(NAME)

    def __init__(
            self,
            storage=config.get_storage()
    ) -> None:
        settings = {
            "login_url": "/login",
        }
        self._handlers = [
            (Routes.register, RegisterHandler),
            (Routes.ping, PingHandler),
            (Routes.login, LoginHandler),
            (Routes.refresh, RefreshHandler),

            (Routes.ws, WebSocketHandler),
            (f"/{config.get_media_sub_url()}/(.*)", StaticFileHandler, {"path": config.get_media_path()})
        ]

        super().__init__(
            self._handlers,
            None,
            None,
            default_handler_class=NotFoundHandler,
            **settings
        )
        self.storage = config.get_storage()
        self.message_bus = MessageBus(self.storage)

    def initialize(self):
        self.logger.info("initializing")
        self.message_bus.handle(
            LoadElementsInitCommand()
        )
        self.message_bus.handle(
            LoadElementImagesInitCommand()
        )

    async def _main(self):
        self.initialize()
        self.logger.info(f"running on {config.get_api_url()}")
        self.listen(config.get_api_port())

        shutdown_event = asyncio.Event()
        await shutdown_event.wait()

    def main(self):
        asyncio.run(self._main())
