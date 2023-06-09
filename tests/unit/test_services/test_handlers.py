import pytest

from models.fungeble.element import Element
from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.handlers.base_handler_service import BaseHandlerService
from services.handlers.game_handler_service import GameHandlerService
from services.handlers.user_handler_service import UserHandlerService
from services.message_bus import MessageBus
from storage.memory import MemoryStorage


class BaseTestHandler(BaseHandlerService):
    model_cls = None
    handler_cls = None
    storage = MemoryStorage()
    message_bus = MessageBus(storage=storage)

    @pytest.fixture
    def saved_instance(self):
        instance = self.model_cls()
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    def test_instance_got(self, saved_instance):
        self.storage.put(saved_instance)

        instance_by_uuid = self.handler_cls(self.storage).\
            get_instance(saved_instance.uuid, self.model_cls)
        instance_by_self = self.handler_cls(self.storage).\
            get_instance(saved_instance, self.model_cls)

        assert instance_by_self == instance_by_uuid

    def get_handlers(cls, **kwargs) -> dict:
        {}


class TestUserHandler(BaseTestHandler):
    model_cls = User
    handler_cls = UserHandlerService


class TestGameHandler(BaseTestHandler):
    model_cls = Game
    handler_cls = GameHandlerService

    @pytest.fixture
    def saved_user(self):
        instance = User()
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    @pytest.fixture
    def saved_instance(self, saved_user):
        instance = self.model_cls(creator_user=saved_user)
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    @pytest.fixture
    def element_cls(self):
        Element(
            "Air",
            starting=True,
        )
        yield Element
        Element.reset_all()

    def test_element_got(self, element_cls):
        element = Element.list()[0]
        element_by_name = self.handler_cls(self.storage).\
            get_element(element.name)
        element_by_self = self.handler_cls(self.storage).\
            get_element(element)

        assert element_by_name == element_by_self
