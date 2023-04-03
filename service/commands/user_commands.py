from dataclasses import dataclass
from typing import Optional, Union

from models.game import Game
from models.user import User
from service.commands.base_commands import ModelCreateCommand, ModelCommand


@dataclass
class UserCommand(ModelCommand):
    pass


@dataclass
class UserCreateCommand(UserCommand, ModelCreateCommand):
    name: Optional[str]
    plain_password: str


@dataclass
class UserEnterGameCommand(UserCommand):
    instance: Union[User, str]
    game: Union[Game, str]


@dataclass
class UserLeaveGameCommand(UserCommand):
    instance: Union[User, str]
    game: Union[Game, str]

#
# class UserChangePasswordCommand(UserCommand):
#     # TODO
#     user: User
