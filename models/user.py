from __future__ import annotations
from logging import getLogger

import config
from models.base import ModelException
from models.entity import Entity
from models.game import Game


class UserException(ModelException):
    pass


class UserAlreadyInGameException(UserException):
    def __init__(self, instance: User):
        super().__init__(instance, f"{instance} is already in {Game.NAME} {instance.uuid}")


class UserNotInGameException(UserException):
    def __init__(self, user):
        super().__init__(user, f"{user} is not in {Game.NAME} to leave")


class User(Entity):
    NAME = "user model"
    logger = getLogger(NAME)

    def __init__(self, name: str = None, plain_password: str = None, to_save=True, storage=config.get_storage(),
                 **kwargs):
        super().__init__(name=name, to_save=False, **kwargs)

        if plain_password:
            self.password = self.hash_password(plain_password)
        else:
            self.password = None

        self.game_uuid = None

        if to_save:
            self.save()

    @staticmethod
    def hash_password(plain_password: str) -> bytes:
        # TODO
        return plain_password.encode()

    def verify_password(self, plain_password: str) -> bool:
        self.logger.debug(f"verifying password ({id(plain_password)}) of {self.NAME} {self}")
        verified = self.hash_password(plain_password) == self.password
        self.logger.debug(f"password ({id(plain_password)}) of {self.NAME} {self} is correct: {verified}")
        return verified

    def enter_game(self, game: Game) -> None:
        self.logger.debug(f"{self.NAME} {self} entering {Game.NAME} {game}")

        if self.game_uuid == game.uuid:
            raise UserAlreadyInGameException(self)

        if self.game_uuid:
            self.leave_game()

        game.add_user(self)
        self.game_uuid = game.uuid
        self.save()

    def leave_game(self, game):
        self.logger.debug(f"{self.NAME} {self} leaving {Game.NAME}")

        if self.game_uuid != game.uuid:
            raise UserNotInGameException(self)

        game.remove_user(self)
        self.game_uuid = None
        self.save()

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_.update({
            "game_uuid": self.game_uuid
        })
        return dict_
