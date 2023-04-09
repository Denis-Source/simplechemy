import os
from datetime import timedelta
from logging import INFO

from dotenv import load_dotenv

from storage.base import BaseStorage
from storage.memory import MemoryStorage

LOGGING_FORMAT = "%(asctime)s\t%(levelname)-7s\t%(name)-20s\t%(message)s"
JWT_ALGORITHM = "HS256"
TOKEN_LIFETIME = timedelta(days=60)


def get_logging_file():
    return os.getenv("LOGGING_FILE", None)


def get_logging_level():
    return int(os.getenv("LOGGING_LEVEL", INFO))


def get_api_port():
    return os.getenv("API_PORT", 8888)


def get_api_url(http=True):
    host = os.getenv("API_HOST", "localhost")
    if http:
        return f"http://{host}:{get_api_port()}"
    else:
        return f"ws://{host}:{get_api_port()}"


def get_storage() -> BaseStorage:
    return MemoryStorage()


def get_element_content_path():
    return os.getenv("ELEMENT_CONTENT_PATH", "recipes.txt")


def get_secret():
    return os.getenv("SECRET", "very secret secret")


load_dotenv()
