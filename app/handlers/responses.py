from enum import Enum


class Responses(dict, Enum):
    PONG = {"message": "pong"}

    GENERAL = {"message": "unknown error"}
    NOT_FOUND = {"message": "resource not found"}

    WS_OPENED = {"ws_connection": "opened"}
