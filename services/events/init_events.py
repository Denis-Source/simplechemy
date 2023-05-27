from dataclasses import dataclass

from services.events.base_event import BaseEvent


@dataclass
class LoadedElementsInitEvent(BaseEvent):
    NAME = "loaded_elements_init_event"


@dataclass
class LoadedElementInitErroredEvent(BaseEvent):
    NAME = "loaded_elements_errored_init_event"
