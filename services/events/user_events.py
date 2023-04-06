from dataclasses import dataclass

from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.events.base_events import BaseEvent


@dataclass
class UserEvent(BaseEvent):
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
class UserVerifiedPasswordEvent(UserEvent):
    instance: User
    is_correct: bool
