import logging
from typing import Union

from models.base import InstanceNotExist
from models.fungeble.element import Element, NotUnlockedElementException, ElementNotExistException
from models.nonfungeble.element_position import ElementPosition, ElementPositionOutOfBounds
from models.nonfungeble.game import Game, ElementPNotInGameException
from models.nonfungeble.user import User
from services.commands.game_commands import GameAddElementPCommand, GameRemoveElementPCommand, GameMoveElementPCommand, \
    GameClearElementsPCommand
from services.events.game_events import GameAddedElementPEvent, GameElementNotExistEvent, \
    GameRemovedElementPEvent, GameElementPNotInGameEvent, GameMovedElementPEvent, GameClearedElementsPEvent, \
    GameElementPOutOfBoundsEvent, GameNewElementPCraftedEvent
from services.handlers.model_handler_service import ModelHandlerService


class GameHandlerService(ModelHandlerService):
    NAME = "game handler"
    logger = logging.getLogger(NAME)

    @staticmethod
    def get_element(element_or_name: Union[Element, str]):
        if isinstance(element_or_name, Element):
            return element_or_name
        elif isinstance(element_or_name, str):
            element = Element.get(element_or_name)
            if not element:
                raise InstanceNotExist(element_or_name, Element)
            return element

    def add_element_p(self, cmd: GameAddElementPCommand) -> \
            Union[
                GameAddedElementPEvent, GameElementNotExistEvent]:
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

        except (ElementNotExistException, NotUnlockedElementException):
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

    def move_element_p(self, cmd: GameMoveElementPCommand) -> \
            Union[
                GameMovedElementPEvent, GameNewElementPCraftedEvent,
                GameElementPNotInGameEvent, GameElementPOutOfBoundsEvent]:
        instance: Game = self.get_instance(
            instance_or_uuid=cmd.instance,
            model_cls=Game
        )
        user: User = self.get_instance(
            instance_or_uuid=cmd.user,
            model_cls=User
        )
        element_p: ElementPosition = self.get_instance(
            instance_or_uuid=cmd.element_p,
            model_cls=ElementPosition
        )

        try:
            result, used_elements_p = instance.move_element_p(
                element_p=element_p,
                x=cmd.x,
                y=cmd.y,
                user=user,
                is_done=cmd.is_done
            )

            if not result:
                self.storage.put(element_p)
                self.storage.put(instance)

                return GameMovedElementPEvent(
                    instance=instance,
                    element_p=element_p
                )
            else:
                self.storage.put(result)
                for u_ps in used_elements_p:
                    self.storage.delete(u_ps)
                self.storage.put(instance)
                return GameNewElementPCraftedEvent(
                    instance=instance,
                    element_p=result,
                    used_elements_p=used_elements_p
                )

        except ElementPNotInGameException:
            return GameElementPNotInGameEvent(
                instance=instance,
                element_p=element_p
            )
        except ElementPositionOutOfBounds:
            return GameElementPOutOfBoundsEvent(
                instance=instance,
                element_p=element_p,
                x=cmd.x,
                y=cmd.y,
                bounds=ElementPosition.BOUNDS
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
