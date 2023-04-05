from logging import getLogger

from app.handlers.base_handler import BaseHandler
from models.nonfungeble.user import User
from services.commands.base_commands import ModelCreateCommand


class RegisterHandler(BaseHandler):
    NAME = "register handler"
    logger = getLogger(NAME)

    def post(self) -> None:
        self.logger.debug("registering new user")
        password = self.get_argument("password")

        cmd = ModelCreateCommand(
            User,
            fields={
                "plain_password": password})
        event = self.application.message_bus.handle(cmd)

        self.set_current_user(event.instance)
        self.write(
            event.as_dict()
        )
        self.logger.debug(f"{event.instance} registered")
