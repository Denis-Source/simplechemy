from dataclasses import dataclass

from services.message import Message


@dataclass
class BaseEvent(Message):
    pass
