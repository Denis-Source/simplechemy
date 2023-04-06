from dataclasses import dataclass
from typing import Union

from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.commands.base_commands import ModelCommand


@dataclass
class UserCommand(ModelCommand):
    pass


@dataclass
class UserEnterGameCommand(UserCommand):
    instance: Union[User, str]
    game: Union[Game, str]


@dataclass
class UserLeaveGameCommand(UserCommand):
    instance: Union[User, str]
    game: Union[Game, str]


@dataclass
class UserVerifyPasswordCommand(UserCommand):
    instance: Union[User, str]
    plain_password: str
