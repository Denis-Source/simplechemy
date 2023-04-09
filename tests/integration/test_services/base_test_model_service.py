import pytest

from services.commands.model_commands import ModelCreateCommand, ModelListCommand, ModelGetCommand, ModelDeleteCommand, \
    ModelChangeCommand
from services.events.base_events import InstanceNotExistEvent, ModelGotEvent, ModelListedEvent, ModelDeletedEvent, \
    ModelChangedEvent
from services.message_bus import MessageBus
from storage.memory import MemoryStorage


class BaseTestModelServices:
    model_cls = None
    handler_cls = None
    storage = MemoryStorage()
    message_bus = MessageBus(storage=storage)

    @pytest.fixture
    def reset_storage(self):
        yield
        self.storage.reset()

    @pytest.fixture
    def saved_instance(self):
        instance = self.model_cls()
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    def test_created(self, reset_storage):
        cmd = ModelCreateCommand(
            self.model_cls,
        )

        event = self.message_bus.handle(cmd)

        saved_instance = self.storage.get(
            model_cls=self.model_cls,
            uuid=event.instance.uuid
        )

        assert event.instance == saved_instance

    def test_got(self, reset_storage, saved_instance):
        cmd = ModelGetCommand(
            saved_instance.uuid,
            self.model_cls.NAME
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, ModelGotEvent)
        assert event.instance == saved_instance

    def test_got_but_not_exist(self, saved_instance):
        self.storage.delete(saved_instance)

        cmd = ModelGetCommand(
            saved_instance.uuid,
            self.model_cls.NAME
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, InstanceNotExistEvent)

    def test_changed_success(self, saved_instance, reset_storage):
        new_name = "new name"
        fields = {"name": new_name}
        cmd = ModelChangeCommand(
            saved_instance,
            fields
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, ModelChangedEvent)
        assert event.instance.name == new_name

    def test_changed_extra_fields(self, saved_instance, reset_storage):
        new_name = "new name"

        fields = {
            "name": new_name,
            "extra1": "extra",
            "extra2": {"hello": "world"},
            "extra3": [1, 2, 3],
        }
        cmd = ModelChangeCommand(
            saved_instance,
            fields
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, ModelChangedEvent)
        assert event.instance.name == new_name

    def test_listed(self, saved_instance, reset_storage):
        cmd = ModelListCommand(
            model_cls_name=self.model_cls.NAME
        )
        event = self.message_bus.handle(cmd)

        assert isinstance(event, ModelListedEvent)
        assert set(self.storage.list(self.model_cls)) == set(event.instances)

    def test_deleted_not_success(self, saved_instance):
        cmd = ModelDeleteCommand(
            saved_instance.uuid,
            saved_instance.NAME
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, ModelDeletedEvent)
        assert self.storage.get(self.model_cls, saved_instance.uuid) is None

    def test_deleted_not_exist(self, saved_instance):
        self.storage.delete(saved_instance)

        cmd = ModelDeleteCommand(
            saved_instance.uuid,
            saved_instance.NAME
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, InstanceNotExistEvent)
