import os

from dotenv import load_dotenv

from storage.memory import MemoryStorage

load_dotenv()


def get_storage():
    return MemoryStorage()


def get_element_content_path():
    return os.getenv("ELEMENT_CONTENT_PATH", "recipes.txt")
