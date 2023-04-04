from dataclasses import dataclass
from typing import Union

from models.fungeble.element import Element
from models.nonfungeble.element_position import ElementPosition
from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.commands.base_commands import ModelCommand


@dataclass
class GameCommand(ModelCommand):
    pass


@dataclass
class GameAddElementPCommand(GameCommand):
    instance: Union[Game, str]
    element: Element
    x: int = 0
    y: int = 0


@dataclass
class GameRemoveElementPCommand(GameCommand):
    instance: Union[Game, str]
    element_p: Union[ElementPosition, str]


@dataclass
class GameMoveElementPCommand(GameCommand):
    instance: Union[Game, str]
    element_p: Union[ElementPosition, str]
    x: int
    y: int
    user: Union[User, str]
    is_done: bool


@dataclass
class GameClearElementsPCommand(GameCommand):
    instance: Union[Game, str]
