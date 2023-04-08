from enum import Enum


class Responses(dict, Enum):
    PONG = {"message": "pong"}

    GENERAL = {"message": "unknown error"}
    NOT_FOUND = {"message": "resource not found"}

    WS_OPENED = {"message": "ws opened"}
    BAD_STATEMENT = {"message": "bad statement"}

    UNAUTHORIZED = {"message": "unauthorized"}