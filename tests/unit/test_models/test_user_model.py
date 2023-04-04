import pytest

from models.nonfungeble.game import Game
from models.nonfungeble.user import User, UserNotInGameException, UserAlreadyInGameException
from tests.unit.test_models.test_entity_model import TestEntityModel


class TestUserModel(TestEntityModel):
    model_cls = User

    def test_correct_password(self):
        correct_password = "8wQy4py3"
        similar_password = "8wQy4py4"

        instance: User = self.model_cls(
            plain_password=correct_password
        )

        assert instance.verify_password(correct_password)
        assert not instance.verify_password(similar_password)

    @pytest.fixture
    def game_instance(self, model_instance):
        return Game(creator_user=model_instance)

    def test_entered_game(self, game_instance: Game, model_instance: User):
        model_instance.enter_game(game_instance)
        assert model_instance.game_uuid == game_instance.uuid
        assert model_instance in game_instance

    def test_left_game(self, game_instance: Game, model_instance: User):
        assert model_instance not in game_instance
        assert model_instance.game_uuid is None

        model_instance.enter_game(game_instance)
        model_instance.leave_game(game_instance)

        assert model_instance not in game_instance
        assert model_instance.game_uuid is None

    def test_user_not_in_game(self, model_instance: User, game_instance: Game):
        assert model_instance not in game_instance
        with pytest.raises(UserNotInGameException):
            model_instance.leave_game(game_instance)

    def test_user_in_game_but_another_provided(self, model_instance: User, game_instance: Game):
        another_game = Game(
            creator_user=model_instance
        )
        model_instance.enter_game(another_game)

        assert model_instance not in game_instance
        with pytest.raises(UserNotInGameException):
            model_instance.leave_game(game_instance)

    def test_user_already_in_game(self, model_instance: User, game_instance: Game):
        assert model_instance not in game_instance
        model_instance.enter_game(game_instance)
        with pytest.raises(UserAlreadyInGameException):
            model_instance.enter_game(game_instance)

    def test_correct_dict(self, model_instance):
        assert model_instance.to_dict() == {
            "type": model_instance.NAME,
            "name": model_instance.name,
            "uuid": model_instance.uuid,
            "game_uuid": model_instance.game_uuid
        }
