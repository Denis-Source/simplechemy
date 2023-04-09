from enum import Enum


class Responses(dict, Enum):
    PONG = {"message": "pong"}

    GENERAL_ERROR = {"message": "unknown error"}
    NOT_FOUND = {"message": "resource not found"}

    WS_OPENED = {"message": "ws opened"}
    BAD_REQUEST = {"message": "bad request"}

    UNAUTHORIZED = {"message": "unauthorized"}
    ALREADY_CONNECTED = {"message": "already connected"}
