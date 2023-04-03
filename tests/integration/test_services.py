import pytest

import config
from models.game import Game
from models.user import User
from service.commands.base_commands import ModelCreateCommand
from service.events.base_events import ModelCreatedEvent
from service.handlers.game_handler_service import GameHandlerService
from service.handlers.user_handler_service import UserHandlerService
from service.message_bus import MessageBus
from storage.memory import MemoryStorage


class BaseTestModelServices:
    model_cls = None
    handler_cls = None
    message_bus = MessageBus()
    storage = MemoryStorage()

    @pytest.fixture
    def set_storage(self):
        self.handler_cls.set_storage(self.storage)
        yield
        self.handler_cls.set_storage(config.get_storage())

    @pytest.fixture
    def saved_instance(self, set_storage):
        instance = self.model_cls()
        yield instance
        instance.delete()

    def test_instance_got(self, set_storage, saved_instance):
        instance_by_uuid = self.handler_cls.get_instance(saved_instance.uuid, self.model_cls)
        instance_by_self = self.handler_cls.get_instance(saved_instance, self.model_cls)

        assert instance_by_self == instance_by_uuid

    @pytest.fixture
    def cmd_fields(self):
        return {}

    def test_create(self, set_storage, cmd_fields):
        cmd = ModelCreateCommand(self.model_cls, fields=cmd_fields)
        event = self.message_bus.handle(cmd)
        assert isinstance(event, ModelCreatedEvent)
        assert isinstance(event.instance, self.model_cls)

        storage_instance: User = self.storage.list(self.model_cls)[0]
        assert event.instance == storage_instance

class TestUserServices(BaseTestModelServices):
    model_cls = User
    handler_cls = UserHandlerService

    @pytest.fixture
    def cmd_fields(self):
        return {"name": "test", "plain_password": "123"}


class TestGameServices(BaseTestModelServices):
    model_cls = Game
    handler_cls = GameHandlerService

    @pytest.fixture
    def saved_user(self, set_storage):
        instance = User()
        yield instance
        instance.delete()

    @pytest.fixture
    def saved_instance(self, set_storage, saved_user):
        instance = self.model_cls(creator_user=saved_user)
        yield instance
        instance.delete()

    @pytest.fixture
    def cmd_fields(self, saved_user):
        return {"creator_user": saved_user}