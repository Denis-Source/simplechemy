from dataclasses import dataclass
from typing import Optional

from services.commands.base_command import BaseCommand


@dataclass
class InitCommand(BaseCommand):
    pass


@dataclass
class LoadElementsInitCommand(InitCommand):
    NAME = "load_elements_init_event"

    filename: Optional[str] = None
