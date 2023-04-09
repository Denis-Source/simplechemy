from dataclasses import dataclass
from typing import Union

from models.fungeble.element import Element
from models.nonfungeble.element_position import ElementPosition
from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.commands.model_commands import ModelCommand


@dataclass
class GameCommand(ModelCommand):
    pass


@dataclass
class GameAddElementPCommand(GameCommand):
    NAME = "game_add_element_p_cmd"

    instance: Union[Game, str]
    element: Union[Element, str]
    x: int = 0
    y: int = 0


@dataclass
class GameRemoveElementPCommand(GameCommand):
    NAME = "game_remove_element_p_cmd"

    instance: Union[Game, str]
    element_p: Union[ElementPosition, str]


@dataclass
class GameMoveElementPCommand(GameCommand):
    NAME = "game_move_element_p_cmd"

    instance: Union[Game, str]
    element_p: Union[ElementPosition, str]
    x: int
    y: int
    user: Union[User, str]
    is_done: bool


@dataclass
class GameClearElementsPCommand(GameCommand):
    NAME = "game_clear_elements_p_command"

    instance: Union[Game, str]
