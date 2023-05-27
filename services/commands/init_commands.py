from dataclasses import dataclass
from typing import Optional

from services.commands.base_command import BaseCommand


@dataclass
class InitCommand(BaseCommand):
    pass


@dataclass
class LoadElementsInitCommand(InitCommand):
    NAME = "load_elements_init_event"

    filepath: Optional[str] = None


@dataclass
class LoadElementImagesInitCommand(InitCommand):
    NAME = "load_element_images_init_event"

    convert_to_app_path: Optional[bool] = True
    media_path: Optional[str] = None
