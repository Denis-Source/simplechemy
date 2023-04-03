from dataclasses import dataclass

from models.game import Game
from models.user import User
from service.events.base_events import ModelEvent


@dataclass
class UserEvent(ModelEvent):
    pass


@dataclass
class UserEnteredGameEvent(UserEvent):
    instance: User
    game: Game


@dataclass
class UserAlreadyInGameEvent(UserEvent):
    instance: User
    game: Game


@dataclass
class UserLeftGameEvent(UserEvent):
    instance: User
    game: Game


@dataclass
class UserNotInGameEvent(UserEvent):
    instance: User

# 
# class UserChangePasswordCommand(UserCommand):
#     # TODO
#     user: User
