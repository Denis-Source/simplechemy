import pytest

from models.game import Game
from models.user import User
from storage.memory import MemoryStorage
from tests.integration.test_model_in_storage.test_entity_in_storage import TestEntityInMemoryStorage


class TestUserInMemoryStorage(TestEntityInMemoryStorage):
    storage = MemoryStorage()
    model_cls = User

    def test_model_change(self, saved_instance: User):
        ordinary_name = "Fine Name"

        saved_instance.change(name=ordinary_name)

        assert self.storage.get(self.model_cls, saved_instance.uuid).name == ordinary_name

    @pytest.fixture
    def game_instance(self, saved_instance: User):
        instance = Game(
            creator_user=saved_instance,
            storage=self.storage
        )
        yield instance
        instance.delete()

    def test_user_entered_game(self, saved_instance: User, game_instance: Game):
        saved_instance.enter_game(game_instance)

        assert User.get(saved_instance.uuid).game_uuid == game_instance.uuid
        assert saved_instance in Game.get(game_instance.uuid)
        assert saved_instance in Game.get(game_instance.uuid).users
