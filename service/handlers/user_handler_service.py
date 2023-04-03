import logging
from typing import Union

from models.game import Game
from models.user import UserAlreadyInGameException, UserNotInGameException, User
from service.commands.user_commands import UserEnterGameCommand, UserLeaveGameCommand
from service.events.user_events import UserEnteredGameEvent, UserAlreadyInGameEvent, UserLeftGameEvent, \
    UserNotInGameEvent
from service.handlers.base_handler_service import ModelHandlerService


class UserHandlerService(ModelHandlerService):
    NAME = "user handler"
    logger = logging.getLogger(NAME)

    @classmethod
    def enter_game(cls, cmd: UserEnterGameCommand) -> Union[UserEnteredGameEvent, UserAlreadyInGameEvent]:
        try:
            instance: User = cls.get_instance(cmd.instance)
            game: Game = cls.get_instance(cmd.game, Game)

            instance.enter_game(game)

            return UserEnteredGameEvent(
                instance=instance,
                game=game
            )
        except UserAlreadyInGameException:
            return UserAlreadyInGameEvent(
                instance=instance,
                game=game
            )

    @classmethod
    def leave_game(cls, cmd: UserLeaveGameCommand) -> Union[UserLeftGameEvent, UserNotInGameEvent]:
        try:
            instance: User = cls.get_instance(cmd.instance)
            game: Game = cls.get_instance(cmd.game, Game)

            instance.leave_game(Game)

            return UserLeftGameEvent(
                instance=instance,
                game=game
            )

        except UserNotInGameException:
            return UserNotInGameEvent(
                instance=instance
            )
