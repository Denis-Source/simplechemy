import logging
import os
import signal
import time
from multiprocessing import Process
from subprocess import Popen

import pytest

import config
from app.app import App
from models.fungeble.element import Element
from storage.memory import MemoryStorage


@pytest.fixture
def element_cls(self):
    filepath = config.get_element_content_path()
    Element.load_from_txt(filepath)

    yield Element
    Element.reset_all()


def run_app():
    logging.basicConfig(
        level=logging.CRITICAL,
    )

    app = App(storage=MemoryStorage())
    app.main()


@pytest.fixture(scope="session")
def app():
    process = Process(target=run_app)
    process.start()
    time.sleep(1)
    yield process

    os.kill(process.pid, signal.SIGINT)
