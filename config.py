import os
from datetime import timedelta
from logging import INFO

from dotenv import load_dotenv

from storage.base import BaseStorage
from storage.memory import MemoryStorage

LOGGING_FORMAT = "%(asctime)s\t%(levelname)-7s\t%(name)-20s\t%(message)s"
JWT_ALGORITHM = "HS256"
TOKEN_LIFETIME = timedelta(days=60)
IMAGE_FORMAT = "png"


def get_base_dir():
    return os.path.dirname(__file__)


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


def get_font_path() -> str:
    return os.getenv("FONT_PATH", f"{get_base_dir()}/fonts/default.ttf")


def get_storage() -> BaseStorage:
    return MemoryStorage()


def get_media_path() -> str:
    return os.getenv("MEDIA_PATH", f"{get_base_dir()}/media")


def get_media_sub_url():
    return os.getenv('MEDIA_URL', 'media')


def get_media_url() -> str:
    return f"{get_api_url()}/{get_media_sub_url()}"


def get_element_content_path():
    return os.getenv("ELEMENT_CONTENT_PATH", f"{get_base_dir()}/recipes.txt")


def get_secret():
    return os.getenv("SECRET", "very secret secret")


load_dotenv()
