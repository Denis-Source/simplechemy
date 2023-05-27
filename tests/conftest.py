import logging
import os
import signal
import time
from multiprocessing import Process

import pytest
import requests
from requests import ConnectTimeout
from requests.exceptions import ConnectionError

import config
from app.app import App, Routes
from storage.memory import MemoryStorage

TIMEOUT = 5


def run_app():
    logging.basicConfig(
        level=logging.CRITICAL,
    )

    app = App(storage=MemoryStorage())
    app.main()


@pytest.fixture(scope="session")
def app():
    try:
        response = requests.get(f"{config.get_api_url()}{Routes.ping}", timeout=1)
        assert response.status_code == 200
        yield
    except (ConnectTimeout, ConnectionError):
        process = Process(target=run_app)
        process.start()
        time.sleep(10)
        yield

        os.kill(process.pid, signal.SIGINT)
