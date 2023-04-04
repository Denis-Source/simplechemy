import os

from dotenv import load_dotenv

from storage.base import BaseStorage
from storage.memory import MemoryStorage

load_dotenv()


def get_storage() -> BaseStorage:
    return MemoryStorage()


def get_element_content_path():
    return os.getenv("ELEMENT_CONTENT_PATH", "recipes.txt")
