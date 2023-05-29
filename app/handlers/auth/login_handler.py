from logging import getLogger

from tornado.web import HTTPError

from app.handlers.auth.jwt_utils import encode_jwt
from app.handlers.base_handler import BaseHandler
from services.commands.user_commands import UserVerifyPasswordCommand
from services.events.model_events import InstanceNotExistEvent


class LoginHandler(BaseHandler):
    NAME = "login handler"
    logger = getLogger(NAME)

    def post(self) -> None:
        self.logger.info("logging user")

        user_uuid = self.get_argument("user_uuid")
        password = self.get_argument("password")

        self.logger.debug("verifying user password")
        cmd = UserVerifyPasswordCommand(
            instance=user_uuid,
            plain_password=password
        )
        event = self.application.message_bus.handle(cmd)
        if isinstance(event, InstanceNotExistEvent):
            self.logger.info("user not found")
            raise HTTPError(404)

        if event.is_correct:
            self.logger.info(f"{event.instance} is verified")
            token = encode_jwt(event.instance.uuid)
            self.write(
                event.as_dict() |
                {"token": token}
            )
        else:
            self.logger.info(f"{event.instance} is not verified")
            raise HTTPError(401)
