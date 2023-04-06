import logging
import os
import signal
import time
from multiprocessing import Process

import pytest
import requests
from requests import ConnectTimeout

import config
from app.app import App, Routes
from storage.memory import MemoryStorage


def run_app():
    logging.basicConfig(
        level=logging.CRITICAL,
    )

    app = App(storage=MemoryStorage())
    app.main()


@pytest.fixture(scope="session")
def app():
    try:
        response = requests.get(f"{config.get_api_url()}{Routes.ping}", timeout=0.5)
        assert response.status_code == 200
        yield
    except ConnectTimeout:
        process = Process(target=run_app)
        process.start()
        time.sleep(1)
        yield

        os.kill(process.pid, signal.SIGINT)
