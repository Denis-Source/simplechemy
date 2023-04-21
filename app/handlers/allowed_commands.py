from enum import Enum


class AllowedCommands(str, Enum):
    GET_USER = "get_user"
    CHANGE_USER = "change_user"

    CREATE_GAME = "create_game"
    GET_GAME = "get_game"
    LIST_GAME = "list_game"
    DELETE_GAME = "delete_game"

    ENTER_GAME = "enter_game"
    LEAVE_GAME = "leave_game"

    ADD_ELEMENT_P = "add_element_p"
    REMOVE_ELEMENT_P = "remove_element_p"
    MOVE_ELEMENT_P = "move_element_p"
    CLEAR_ELEMENTS_P = "clear_elements_p"

    # GOT = "got_user"
    #
    # CHANGE = "change_user"
    # CHANGED = "user_changed"
    #
    # ENTER = "user_enter_room"
    # ENTERED = "user_entered_room"
    #
    # LEAVE = "user_leave_room"
    # LEFT = "user_left_room"
    #
    # NOT_IN_ROOM = "user_not_in_room"
    # ALREADY_IN_ROOM = "user_already_in_room"
