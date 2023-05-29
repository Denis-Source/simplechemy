from enum import Enum


class Responses(dict, Enum):
    PONG = {"message": "pong"}
    AUTHENTICATED = {"message": "successfully authenticated"}

    GENERAL_ERROR = {"message": "unknown error"}
    NOT_FOUND = {"message": "resource not found"}

    WS_OPENED = {"message": "ws opened"}
    BAD_REQUEST = {"message": "bad request"}

    UNAUTHENTICATED = {"message": "unauthenticated"}
    ALREADY_CONNECTED = {"message": "already connected"}
