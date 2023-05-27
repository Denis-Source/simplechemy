from dataclasses import dataclass
from typing import Tuple, List

from models.nonfungeble.element_position import ElementPosition
from models.nonfungeble.game import Game
from services.events.model_events import ModelEvent


@dataclass
class GameEvent(ModelEvent):
    pass

@dataclass
class GameAddedElementPEvent(GameEvent):
    NAME = "game_added_element_p_event"
    instance: Game
    element_p: ElementPosition


@dataclass
class GameElementNotExistEvent(GameEvent):
    NAME = "game_element_not_exist_event"
    instance: Game
    name: str


@dataclass
class GameRemovedElementPEvent(GameEvent):
    NAME = "game_removed_element_p_event"
    instance: Game
    element_p: ElementPosition


@dataclass
class GameMovedElementPEvent(GameEvent):
    NAME = "game_moved_element_p_event"
    instance: Game
    element_p: ElementPosition


@dataclass
class GameElementPNotInGameEvent(GameEvent):
    NAME = "game_element_p_not_in_game_event"
    instance: Game
    element_p: ElementPosition


@dataclass
class GameElementPOutOfBoundsEvent(GameEvent):
    NAME = "game_element_p_put_of_bounds_event"
    instance: Game
    element_p: ElementPosition
    x: int
    y: int
    bounds: Tuple[int, int]


@dataclass
class GameNewElementPCraftedEvent(GameEvent):
    NAME = "game_new_element_p_crafred_event"
    instance: Game
    element_p: ElementPosition
    used_elements_p: List[ElementPosition]


@dataclass
class GameClearedElementsPEvent(GameEvent):
    NAME = "game_cleared_elements_p_event"
    instance: Game
