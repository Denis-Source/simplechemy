from app.handlers.statements import Statements
from app.handlers.web_socket.game_websocket_handler import GameWebSocketHandler
from app.handlers.web_socket.user_websocket_handler import UserWebSocketHandler


class WebSocketHandler(UserWebSocketHandler, GameWebSocketHandler):
    def get_methods(self):
        return {
            Statements.CREATE_GAME: self.create_game,
            Statements.GET_GAME: self.get_game,
            Statements.LIST_GAME: self.list_game,
            Statements.DELETE_GAME: self.delete_game,

            Statements.GET_USER: self.get_user,
            Statements.CHANGE_USER: self.change_user
        }
