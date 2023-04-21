import pytest

from models.fungeble.element import Element
from models.nonfungeble.element_position import ElementPosition, ElementPositionOutOfBounds
from models.nonfungeble.user import User
from tests.unit.test_models.test_entity_model import TestEntityModel


class TestElementPositionModel(TestEntityModel):
    model_cls = ElementPosition

    @pytest.fixture
    def element_cls(self):
        yield Element
        Element.reset_all()

    @pytest.fixture
    def element_instance(self, element_cls):
        yield element_cls("Air")
        element_cls.reset_all()

    @pytest.fixture
    def another_element_instance(self, element_cls):
        yield element_cls("Water")
        element_cls.reset_all()

    @pytest.fixture
    def user_instance(self):
        return User()

    @pytest.fixture
    def model_instance(self, element_instance):
        return self.model_cls(
            element=element_instance,
            x=0,
            y=0
        )

    @pytest.fixture
    def another_model_instance(self, another_element_instance):
        return self.model_cls(
            element=another_element_instance,
            x=0,
            y=0
        )

    def test_move_element(self, model_instance: ElementPosition, user_instance: User):
        new_coords = 0.3, 0.3

        model_instance.move_to(
            x=new_coords[0],
            y=new_coords[1],
            user=user_instance,
            is_done=False
        )

        assert model_instance.x == new_coords[0]
        assert model_instance.y == new_coords[1]

        assert model_instance.carried_by is not None

        new_coords = 0.7, 0.7

        model_instance.move_to(
            x=new_coords[0],
            y=new_coords[1],
            user=user_instance,
            is_done=True
        )

        assert model_instance.x == new_coords[0]
        assert model_instance.y == new_coords[1]

        assert model_instance.carried_by is None

    def test_move_element_out_of_bounds(self, model_instance: ElementPosition, user_instance: User):
        wrong_coords = [
            (0, 1.1),
            (1.1, 0),
            (-2, 0),
            (1, 1),
            (0, -2)
        ]

        for c in wrong_coords:
            with pytest.raises(ElementPositionOutOfBounds):
                model_instance.move_to(
                    x=c[0],
                    y=c[1],
                    user=user_instance,
                    is_done=False
                )

    def test_correct_dict(self, model_instance):
        assert model_instance.as_dict() == {
            "type": model_instance.NAME,
            "name": model_instance.name,
            "uuid": model_instance.uuid,
            "carried_by": model_instance.carried_by,
            "x": model_instance.x,
            "y": model_instance.y,
            "element": model_instance.element.as_dict()
        }
