from dataclasses import dataclass

from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.events.base_events import ModelEvent


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


@dataclass
class UserVerifiedPassword(UserEvent):
    instance: User
    plain_password: str
    is_correct: bool
