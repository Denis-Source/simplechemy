import pytest

from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.handlers.game_handler_service import GameHandlerService
from services.handlers.user_handler_service import UserHandlerService
from services.message_bus import MessageBus
from storage.memory import MemoryStorage


class BaseTestHandler:
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

        instance_by_uuid = self.handler_cls(self.storage).get_instance(saved_instance.uuid, self.model_cls)
        instance_by_self = self.handler_cls(self.storage).get_instance(saved_instance, self.model_cls)

        assert instance_by_self == instance_by_uuid


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
