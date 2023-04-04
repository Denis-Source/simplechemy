from __future__ import annotations
from logging import getLogger

import config
from models.base import ModelException
from models.nonfungeble.entity import Entity
from models.nonfungeble.game import Game


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
        super().__init__(name=name, **kwargs)

        if plain_password:
            self.password = self.hash_password(plain_password)
        else:
            self.password = None

        self.game_uuid = None

    def change(self, name, plain_password=None, to_save=True, **kwargs) -> None:
        if plain_password:
            self.password = self.hash_password(plain_password)

        super().change(name, to_save=to_save, **kwargs)

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

        if self.game_uuid:
            raise UserAlreadyInGameException(self)

        game.add_user(self)
        self.game_uuid = game.uuid

    def leave_game(self, game):
        self.logger.debug(f"{self.NAME} {self} leaving {Game.NAME}")

        if self.game_uuid != game.uuid:
            raise UserNotInGameException(self)

        game.remove_user(self)
        self.game_uuid = None

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_.update({
            "game_uuid": self.game_uuid
        })
        return dict_
