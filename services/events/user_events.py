from dataclasses import dataclass

from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.events.model_events import ModelEvent


@dataclass
class UserEvent(ModelEvent):
    NAME = "user_event"


@dataclass
class UserEnteredGameEvent(UserEvent):
    NAME = "user_entered_game_event"

    instance: User
    game: Game


@dataclass
class UserAlreadyInGameEvent(UserEvent):
    NAME = "user_already_in_game_event"

    instance: User
    game: Game


@dataclass
class UserLeftGameEvent(UserEvent):
    NAME = "user_left_game_event"

    instance: User
    game: Game


@dataclass
class UserNotInGameEvent(UserEvent):
    NAME = "user_not_in_game_event"

    instance: User


@dataclass
class UserVerifiedPasswordEvent(UserEvent):
    NAME = "user_verified_password_event"

    instance: User
    is_correct: bool
