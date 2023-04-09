import pytest

from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.commands.model_commands import ModelCreateCommand, ModelChangeCommand
from services.commands.user_commands import UserEnterGameCommand, UserLeaveGameCommand, UserVerifyPasswordCommand
from services.events.model_events import InstanceNotExistEvent, ModelChangedEvent
from services.events.user_events import UserEnteredGameEvent, UserAlreadyInGameEvent, UserLeftGameEvent, \
    UserVerifiedPasswordEvent
from services.handlers.user_handler_service import UserHandlerService
from tests.integration.test_services.base_test_model_service import BaseTestModelServices


class TestUserServices(BaseTestModelServices):
    model_cls = User
    handler_cls = UserHandlerService

    @pytest.fixture
    def saved_instance(self):
        instance = self.model_cls(
            name="test name",
            plain_password="plain_password"
        )
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    @pytest.fixture
    def saved_game(self, saved_instance):
        instance = Game(
            creator_user=saved_instance
        )
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    @pytest.fixture
    def another_saved_game(self, saved_instance):
        instance = Game(
            creator_user=saved_instance
        )
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    def test_created(self, reset_storage):
        cmd = ModelCreateCommand(
            model_cls_name=self.model_cls.NAME,
            fields={
                "name": "test name",
                "plain_password": "plain_password"
            }
        )

        event = self.message_bus.handle(cmd)

        saved_instance = self.storage.get(
            model_cls=self.model_cls,
            uuid=event.instance.uuid
        )

        assert event.instance == self.storage.get(User, saved_instance.uuid)
        assert event.instance.name == cmd.fields.get("name")
        assert event.instance.verify_password(cmd.fields.get("plain_password"))

    def test_changed_password_success(self, saved_instance, reset_storage):
        new_password = "new password"
        fields = {
            "plain_password": new_password
        }
        cmd = ModelChangeCommand(
            saved_instance,
            fields
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, ModelChangedEvent)

        cmd = UserVerifyPasswordCommand(
            saved_instance,
            new_password
        )

        event = self.message_bus.handle(cmd)
        assert isinstance(event, UserVerifiedPasswordEvent)
        assert event.is_correct

    def test_password_verified_success(self, saved_instance):
        cmd = UserVerifyPasswordCommand(
            instance=saved_instance,
            plain_password="plain_password"
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, UserVerifiedPasswordEvent)
        assert event.is_correct

    def test_password_verified_not_exist(self, saved_instance):
        self.storage.delete(saved_instance)
        cmd = UserVerifyPasswordCommand(
            instance=saved_instance.uuid,
            plain_password="plain_password"
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, InstanceNotExistEvent)

    def test_password_verified_wrong(self, saved_instance):
        cmd = UserVerifyPasswordCommand(
            instance=saved_instance,
            plain_password="plain_passord"
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, UserVerifiedPasswordEvent)
        assert not event.is_correct

    def test_enter_game(self, saved_instance, saved_game, reset_storage):
        assert saved_instance.game_uuid is None

        cmd = UserEnterGameCommand(
            saved_instance,
            saved_game,
        )
        event = self.message_bus.handle(cmd)

        assert isinstance(event, UserEnteredGameEvent)
        assert event.instance == saved_instance
        assert event.game == saved_game

        assert self.storage.get(User, saved_instance.uuid).game_uuid == saved_game.uuid
        assert self.storage.get(User, saved_instance.uuid) in self.storage.get(Game, saved_game.uuid)

    def test_enter_game_left_not_left_previous(self, saved_game, another_saved_game, saved_instance, reset_storage):
        cmd = UserEnterGameCommand(
            saved_instance,
            saved_game,
        )
        self.message_bus.handle(cmd)

        assert saved_instance in saved_game
        assert saved_instance not in another_saved_game

        cmd = UserEnterGameCommand(
            saved_instance,
            another_saved_game
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, UserAlreadyInGameEvent)

    def test_enter_already_enter_game(self, saved_game, saved_instance, reset_storage):
        cmd = UserEnterGameCommand(
            saved_instance,
            saved_game,
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, UserEnteredGameEvent)

        event = self.message_bus.handle(cmd)
        assert isinstance(event, UserAlreadyInGameEvent)

    def test_user_left_game(self, saved_game, saved_instance, reset_storage):
        cmd = UserEnterGameCommand(
            saved_instance,
            saved_game,
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, UserEnteredGameEvent)
        assert self.storage.get(User, saved_instance.uuid) in self.storage.get(Game, saved_game.uuid)

        cmd = UserLeaveGameCommand(
            saved_instance,
            saved_game
        )

        event = self.message_bus.handle(cmd)
        assert isinstance(event, UserLeftGameEvent)
        assert self.storage.get(User, saved_instance.uuid) not in self.storage.get(Game, saved_game.uuid)
