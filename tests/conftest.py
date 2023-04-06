import logging
import os
import signal
import time
from multiprocessing import Process

import pytest

from app.app import App
from storage.memory import MemoryStorage


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
