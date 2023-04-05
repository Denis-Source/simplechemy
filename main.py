import asyncio
import logging
from threading import Thread
from time import sleep

import config
from app.app import App


if __name__ == '__main__':
    logging.basicConfig(
        level=config.get_logging_level(),
        format=config.LOGGING_FORMAT,
        filename=config.get_logging_file()
    )

    App().main()