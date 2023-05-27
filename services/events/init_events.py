from dataclasses import dataclass

from services.events.base_event import BaseEvent


@dataclass
class InitEvent(BaseEvent):
    pass


@dataclass
class LoadedElementsInitEvent(InitEvent):
    NAME = "loaded_elements_init_event"


@dataclass
class LoadedElementInitErroredEvent(InitEvent):
    NAME = "loaded_elements_errored_init_event"


@dataclass
class LoadedElementImagesInitEvent(InitEvent):
    NAME = "loaded_elements_images_event"
