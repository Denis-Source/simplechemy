import pytest

from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.commands.base_commands import ModelCreateCommand
from services.handlers.game_handler_service import GameHandlerService
from tests.integration.test_services.base_model_service import BaseTestModelServices


class TestGameServices(BaseTestModelServices):
    model_cls = Game
    handler_cls = GameHandlerService

    @pytest.fixture
    def saved_user(self, set_storage):
        instance = User()
        yield instance
        instance.delete()

    @pytest.fixture
    def saved_instance(self, saved_user):
        instance = self.model_cls(
            creator_user=saved_user
        )
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    def test_instance_got(self, set_storage):
        # TODO move in unit tests
        pass

    def test_created(self, set_storage, saved_user):
        cmd = ModelCreateCommand(
            model_cls=self.model_cls,
            fields={
                "name": "test name",
                "creator_user": saved_user
            }
        )

        event = self.message_bus.handle(cmd)

        saved_instance = self.storage.get(
            model_cls=self.model_cls,
            uuid=event.instance.uuid
        )

        assert event.instance == saved_instance
        assert event.instance.name == cmd.fields.get("name")
        assert self.storage.get(Game, event.instance.uuid).creator_uuid == saved_user.uuid



