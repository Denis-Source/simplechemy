import logging
from typing import Union

from models.nonfungeble.game import Game
from models.nonfungeble.user import UserAlreadyInGameException, UserNotInGameException, User
from services.commands.user_commands import UserEnterGameCommand, UserLeaveGameCommand
from services.events.user_events import UserEnteredGameEvent, UserAlreadyInGameEvent, UserLeftGameEvent, \
    UserNotInGameEvent
from services.handlers.base_handler_service import ModelHandlerService


class UserHandlerService(ModelHandlerService):
    NAME = "user handler"
    logger = logging.getLogger(NAME)

    def enter_game(self, cmd: UserEnterGameCommand) -> Union[UserEnteredGameEvent, UserAlreadyInGameEvent]:
        try:
            instance: User = self.get_instance(cmd.instance, User)
            game: Game = self.get_instance(cmd.game, Game)

            previous_game = None
            if instance.game_uuid:
                previous_game = self.storage.get(Game, instance.game_uuid)

            instance.enter_game(game)
            self.storage.put(instance)
            self.storage.put(game)

            return UserEnteredGameEvent(
                instance=instance,
                game=game
            )
        except UserAlreadyInGameException:
            return UserAlreadyInGameEvent(
                instance=instance,
                game=game
            )

    def leave_game(self, cmd: UserLeaveGameCommand) -> Union[UserLeftGameEvent, UserNotInGameEvent]:
        try:
            instance: User = self.get_instance(cmd.instance, User)
            game: Game = self.get_instance(cmd.game, Game)

            instance.leave_game(game)
            self.storage.put(instance)
            self.storage.put(game)

            return UserLeftGameEvent(
                instance=instance,
                game=game
            )

        except UserNotInGameException:
            return UserNotInGameEvent(
                instance=instance
            )

    @classmethod
    def get_handlers(cls, storage) -> dict:
        handlers = super().get_handlers(storage)
        handler = cls(storage)

        handlers.update({
            UserEnterGameCommand: handler.enter_game,
            UserLeaveGameCommand: handler.leave_game
        })
        return handlers
