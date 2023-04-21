from logging import getLogger

from app.handlers.web_socket.base_websocket_handler import BaseWebSocketHandler
from models.nonfungeble.game import Game
from services.commands.game_commands import GameAddElementPCommand, GameRemoveElementPCommand, GameMoveElementPCommand, \
    GameClearElementsPCommand
from services.commands.model_commands import ModelGetCommand, ModelCreateCommand, ModelListCommand, ModelDeleteCommand
from services.events.game_events import GameAddedElementPEvent, GameRemovedElementPEvent, GameMovedElementPEvent, \
    GameNewElementPCraftedEvent
from services.events.user_events import UserNotInGameEvent


class GameWebSocketHandler(BaseWebSocketHandler):
    NAME = "user wshandler"
    logger = getLogger(NAME)

    def create_game(self, payload: dict):
        cmd = ModelCreateCommand(
            model_cls_name=Game.NAME,
            fields=payload.get("fields", {}) | {"creator_user": self.current_user}
        )
        event = self.application.message_bus.handle(cmd)
        self.broadcast(event.as_dict())

    def get_game(self, payload: dict):
        cmd = ModelGetCommand(
            uuid=payload["uuid"],
            model_cls_name=Game.NAME
        )
        event = self.application.message_bus.handle(cmd)
        self.write_message(event.as_dict())

    def list_game(self, payload: dict):
        cmd = ModelListCommand(
            Game.NAME
        )
        event = self.application.message_bus.handle(cmd)
        self.write_message(event.as_dict())

    def delete_game(self, payload: dict):
        cmd = ModelDeleteCommand(
            instance=payload["uuid"],
            model_cls_name=Game.NAME
        )
        event = self.application.message_bus.handle(cmd)
        self.broadcast(event.as_dict())

    def add_element_p(self, payload: dict):
        if self.current_user.game_uuid:
            game = self.application.message_bus.handle(
                ModelGetCommand(
                    uuid=self.current_user.game_uuid,
                    model_cls_name=Game.NAME
                )).instance

            cmd = GameAddElementPCommand(
                instance=self.current_user.game_uuid,
                element=payload["element"],
                x=payload.get("x", 0),
                y=payload.get("y", 0)
            )
            event = self.application.message_bus.handle(cmd)

            if isinstance(event, GameAddedElementPEvent):
                self.broadcast(event.as_dict(), game.users)
            else:
                self.write_message(event.as_dict())
        else:
            self.write_message(UserNotInGameEvent(self.current_user).as_dict())

    def remove_element_p(self, payload: dict):
        if self.current_user.game_uuid:
            game = self.application.message_bus.handle(
                ModelGetCommand(
                    uuid=self.current_user.game_uuid,
                    model_cls_name=Game.NAME
                )).instance

            cmd = GameRemoveElementPCommand(
                instance=self.current_user.game_uuid,
                element_p=payload["element_p"]
            )
            event = self.application.message_bus.handle(cmd)

            if isinstance(event, GameRemovedElementPEvent):
                self.broadcast(event.as_dict(), game.users)
            else:
                self.write_message(event.as_dict())
        else:
            self.write_message(UserNotInGameEvent(self.current_user).as_dict())

    def move_element_p(self, payload: dict):
        if self.current_user.game_uuid:
            game = self.application.message_bus.handle(
                ModelGetCommand(
                    uuid=self.current_user.game_uuid,
                    model_cls_name=Game.NAME
                )).instance

            cmd = GameMoveElementPCommand(
                instance=self.current_user.game_uuid,
                element_p=payload["element_p"],
                x=payload["x"],
                y=payload["y"],
                user=self.current_user,
                is_done=payload["is_done"]
            )
            event = self.application.message_bus.handle(cmd)

            if type(event) in [GameMovedElementPEvent, GameNewElementPCraftedEvent]:
                self.broadcast(event.as_dict(), game.users)
            else:
                self.write_message(event.as_dict())
        else:
            self.write_message(UserNotInGameEvent(self.current_user).as_dict())

    def clear_elements_p(self, payload: dict):
        if self.current_user.game_uuid:
            game = self.application.message_bus.handle(
                ModelGetCommand(
                    uuid=self.current_user.game_uuid,
                    model_cls_name=Game.NAME
                )).instance

            cmd = GameClearElementsPCommand(
                instance=self.current_user.game_uuid
            )
            event = self.application.message_bus.handle(cmd)

            if isinstance(event, GameMovedElementPEvent):
                self.broadcast(event.as_dict(), game.users)
            else:
                self.write_message(event.as_dict())
        else:
            self.write_message(UserNotInGameEvent(self.current_user).as_dict())
