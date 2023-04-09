from dataclasses import dataclass
from typing import Union

from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.commands.model_commands import ModelCommand


@dataclass
class UserCommand(ModelCommand):
    NAME = "user_cmd"


@dataclass
class UserEnterGameCommand(UserCommand):
    NAME = "user_enter_game_cmd"

    instance: Union[User, str]
    game: Union[Game, str]


@dataclass
class UserLeaveGameCommand(UserCommand):
    NAME = "user_leave_game_command"

    instance: Union[User, str]
    game: Union[Game, str]


@dataclass
class UserVerifyPasswordCommand(UserCommand):
    NAME = "user_verified_password_cmd"

    instance: Union[User, str]
    plain_password: str
