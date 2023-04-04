import pytest

from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from tests.unit.test_models.test_entity_model import TestEntityModel


class TestGameModel(TestEntityModel):
    model_cls = Game

    @pytest.fixture
    def user_instance(self):
        return User()

    @pytest.fixture
    def model_instance(self, user_instance):
        return self.model_cls(
            creator_user=user_instance
        )

    @pytest.fixture
    def another_model_instance(self, user_instance):
        return self.model_cls(
            creator_user=user_instance
        )

    def test_creator_user(self, model_instance, user_instance):
        user_instance.enter_game(model_instance)

        assert model_instance.creator_uuid == user_instance.uuid

    def test_correct_dict(self, model_instance):
        assert model_instance.to_dict() == {
            "type": model_instance.NAME,
            "name": model_instance.name,
            "uuid": model_instance.uuid,
            "creator_uuid": model_instance.creator_uuid,
            "users": model_instance.users,
            "element_positions": [element_p.to_dict() for element_p in model_instance.element_positions],
            "unlocked_elements": [element.name for element in model_instance.unlocked_elements]
        }
