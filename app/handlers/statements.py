from enum import Enum


class Statements(str, Enum):
    GET_USER = "get_user"
    GOT_USER = "got_user"

    NOT_EXIST = "not exist"

    CHANGE_USER = "change_user"
    CHANGED_USER = "changed_user"

    CREATE_GAME = "create_game"
    CREATED_GAME = "created_game"

    GET_GAME = "get_game"
    GOT_GAME = "got_game"

    LIST_GAME = "list_game"
    LISTED_GAME = "listed_game"

    DELETE_GAME = "delete_game"
    DELETED_GAME = "deleted_game"

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
