from dataclasses import dataclass
from typing import Tuple, List

from models.fungeble.element import Element
from models.nonfungeble.element_position import ElementPosition
from models.nonfungeble.game import Game
from services.events.base_events import ModelEvent


@dataclass
class GameEvent(ModelEvent):
    pass


@dataclass
class GameAddedElementPEvent(GameEvent):
    instance: Game
    element_p: ElementPosition


@dataclass
class GameNotUnlockedElementEvent(GameEvent):
    instance: Game
    element: Element


@dataclass
class GameElementNotExistEvent(GameEvent):
    instance: Game
    name: str


@dataclass
class GameRemovedElementPEvent(GameEvent):
    instance: Game
    element_p: ElementPosition


@dataclass
class GameMovedElementPEvent(GameEvent):
    instance: Game
    element_p: ElementPosition


@dataclass
class GameElementPNotInGameEvent(GameEvent):
    instance: Game
    element_p: ElementPosition


@dataclass
class GameElementPOutOfBoundsEvent(GameEvent):
    instance: Game
    element_p: ElementPosition
    x: int
    y: int
    bounds: Tuple[int, int]


@dataclass
class GameNewElementCraftedEvent(GameEvent):
    instance: Game
    element_p: ElementPosition
    used_elements_p: List[ElementPosition]


@dataclass
class GameClearedElementsPEvent(GameEvent):
    instance: Game
