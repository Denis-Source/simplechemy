import pytest

from models.game import Game
from models.user import User
from tests.unit.test_model.test_entity_model import TestEntityModel


class TestGameModel(TestEntityModel):
    model_cls = Game

    @pytest.fixture
    def user_instance(self):
        return User(storage=self.storage)

    @pytest.fixture
    def model_instance(self, user_instance):
        return self.model_cls(
            creator_user=user_instance,
            storage=self.storage
        )

    @pytest.fixture
    def another_model_instance(self, user_instance):
        return self.model_cls(
            creator_user=user_instance,
            storage=self.storage
        )

    def test_creator_user(self, model_instance, user_instance):
        user_instance.enter_game(model_instance)

        assert model_instance.creator_uuid == user_instance.uuid
