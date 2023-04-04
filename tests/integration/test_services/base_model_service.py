import pytest

from services.commands.base_commands import ModelCreateCommand, ModelListCommand, ModelGetCommand, ModelDeleteCommand
from services.events.base_events import ModelNotExistEvent, ModelGotEvent, ModelListedEvent, ModelDeletedEvent
from services.message_bus import MessageBus
from storage.memory import MemoryStorage


class BaseTestModelServices:
    model_cls = None
    handler_cls = None
    storage = MemoryStorage()
    message_bus = MessageBus(storage=storage)

    @pytest.fixture
    def set_storage(self):
        yield
        self.storage.reset()

    def test_instance_got(self, set_storage):
        saved_instance = self.model_cls()
        self.storage.put(saved_instance)

        # TODO move in unittest
        instance_by_uuid = self.handler_cls(self.storage).get_instance(saved_instance.uuid, self.model_cls)
        instance_by_self = self.handler_cls(self.storage).get_instance(saved_instance, self.model_cls)

        assert instance_by_self == instance_by_uuid

    @pytest.fixture
    def saved_instance(self):
        instance = self.model_cls()
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    def test_created(self, set_storage):
        cmd = ModelCreateCommand(
            self.model_cls,
        )

        event = self.message_bus.handle(cmd)

        saved_instance = self.storage.get(
            model_cls=self.model_cls,
            uuid=event.instance.uuid
        )

        assert event.instance == saved_instance

    def test_got(self, set_storage, saved_instance):
        cmd = ModelGetCommand(
            saved_instance.uuid, self.model_cls
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, ModelGotEvent)
        assert event.instance == saved_instance

    def test_got_but_not_exist(self, saved_instance):
        self.storage.delete(saved_instance)

        cmd = ModelGetCommand(
            saved_instance.uuid,
            self.model_cls
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, ModelNotExistEvent)

    def test_listed(self, saved_instance, set_storage):
        cmd = ModelListCommand(
            model_cls=self.model_cls
        )
        event = self.message_bus.handle(cmd)

        assert isinstance(event, ModelListedEvent)
        assert set(self.storage.list(self.model_cls)) == set(event.instances)

    def test_deleted(self, saved_instance):
        self.storage.delete(saved_instance)

        cmd = ModelDeleteCommand(
            saved_instance
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, ModelDeletedEvent)
        assert self.storage.get(self.model_cls, saved_instance.uuid) is None