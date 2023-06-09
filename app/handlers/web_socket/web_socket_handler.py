from app.handlers.allowed_commands import AllowedCommands
from app.handlers.web_socket.game_websocket_handler import GameWebSocketHandler
from app.handlers.web_socket.user_websocket_handler import UserWebSocketHandler


class WebSocketHandler(UserWebSocketHandler, GameWebSocketHandler):
    def get_methods(self):
        return {
            AllowedCommands.CREATE_GAME: self.create_game,
            AllowedCommands.GET_GAME: self.get_game,
            AllowedCommands.LIST_GAME: self.list_game,
            AllowedCommands.DELETE_GAME: self.delete_game,

            AllowedCommands.GET_USER: self.get_user,
            AllowedCommands.CHANGE_USER: self.change_user,
            AllowedCommands.ENTER_GAME: self.enter_game,
            AllowedCommands.LEAVE_GAME: self.leave_game,

            AllowedCommands.ADD_ELEMENT_P: self.add_element_p,
            AllowedCommands.REMOVE_ELEMENT_P: self.remove_element_p,
            AllowedCommands.MOVE_ELEMENT_P: self.move_element_p,
            AllowedCommands.CLEAR_ELEMENTS_P: self.clear_elements_p
        }
