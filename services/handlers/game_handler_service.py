import logging
from typing import Union

from models.fungeble.element import Element, NotUnlockedElementException, ElementNotExistException
from models.nonfungeble.element_position import ElementPosition
from models.nonfungeble.game import Game, ElementPNotInGameException
from models.nonfungeble.user import User
from services.commands.game_commands import GameAddElementPCommand, GameRemoveElementPCommand, GameMoveElementPCommand, \
    GameClearElementsPCommand
from services.events.game_events import GameAddedElementPEvent, GameNotUnlockedElementEvent, GameElementNotExistEvent, \
    GameRemovedElementPEvent, GameElementPNotInGameEvent, GameMovedElementPEvent, GameClearedElementsPEvent
from services.handlers.base_handler_service import ModelHandlerService


class GameHandlerService(ModelHandlerService):
    NAME = "game handler"
    logger = logging.getLogger(NAME)

    @staticmethod
    def get_element(element_or_name: Union[Element, str]):
        if isinstance(element_or_name, Element):
            return element_or_name
        elif isinstance(element_or_name, str):
            return Element.get(element_or_name)

    def add_element_p(self, cmd: GameAddElementPCommand) -> \
            Union[
                GameAddedElementPEvent, GameNotUnlockedElementEvent, GameElementNotExistEvent]:
        instance: Game = self.get_instance(
            instance_or_uuid=cmd.instance,
            model_cls=Game
        )

        try:
            element: Element = self.get_element(cmd.element)
            element_p: ElementPosition = instance.add_element_p(
                element=element,
                x=cmd.x,
                y=cmd.y
            )
            self.storage.put(element_p)
            self.storage.put(instance)

            return GameAddedElementPEvent(
                instance=instance,
                element_p=element_p
            )

        except NotUnlockedElementException:
            return GameNotUnlockedElementEvent(
                instance=instance,
                element=element
            )

        except ElementNotExistException:
            return GameElementNotExistEvent(
                instance=instance,
                name=cmd.element,
            )

    def remove_element_p(self, cmd: GameRemoveElementPCommand) -> \
            Union[
                GameRemovedElementPEvent, GameElementPNotInGameEvent]:
        instance: Game = self.get_instance(
            instance_or_uuid=cmd.instance,
            model_cls=Game
        )
        element_p: ElementPosition = self.get_instance(
            instance_or_uuid=cmd.element_p,
            model_cls=ElementPosition
        )

        try:
            instance.remove_element_p(
                element_p=element_p
            )
            self.storage.delete(element_p)
            self.storage.put(instance)

            return GameRemovedElementPEvent(
                instance=instance,
                element_p=element_p
            )
        except ElementPNotInGameException:
            return GameElementPNotInGameEvent(
                instance=instance,
                element_p=element_p
            )

    @classmethod
    def move_element_p(cls, cmd: GameMoveElementPCommand) -> \
            Union[
                GameMovedElementPEvent, GameElementPNotInGameEvent]:
        # TODO out of bounds event

        instance: Game = cls.get_instance(
            instance_or_uuid=cmd.instance,
            model_cls=Game
        )
        user: User = cls.get_instance(
            instance_or_uuid=cmd.instance,
            model_cls=User
        )
        element_p: ElementPosition = cls.get_instance(
            instance_or_uuid=cmd.element_p,
            model_cls=ElementPosition
        )

        try:
            instance.move_element_p(
                element_p=element_p,
                x=cmd.x,
                y=cmd.y,
                user=user,
                is_done=cmd.is_done
            )
            return GameMovedElementPEvent(
                instance=instance,
                element_p=element_p
            )
        except ElementPNotInGameException:
            return GameElementPNotInGameEvent(
                instance=instance,
                element_p=element_p
            )

    @classmethod
    def clear_elements_p(cls, cmd: GameClearElementsPCommand) -> GameClearedElementsPEvent:
        instance: Game = cls.get_instance(
            instance_or_uuid=cmd.instance,
            model_cls=Game
        )

        instance.clear_elements_p()

        return GameClearedElementsPEvent(
            instance=instance
        )

    @classmethod
    def get_handlers(cls, storage) -> dict:
        handlers = super().get_handlers(storage)
        handler = cls(storage)

        handlers.update({
            GameAddElementPCommand: handler.add_element_p,
            GameRemoveElementPCommand: handler.remove_element_p,
            GameMoveElementPCommand: handler.move_element_p,
            GameClearElementsPCommand: handler.clear_elements_p,
        })
        return handlers
