import pytest

from models.element import Element
from models.element_position import ElementPosition
from storage.memory import MemoryStorage
from tests.integration.test_model_in_storage.test_entity_in_storage import TestEntityInMemoryStorage


class TestElementPositionInMemoryStorage(TestEntityInMemoryStorage):
    storage = MemoryStorage()
    model_cls = ElementPosition

    element_cls = Element

    @pytest.fixture
    def saved_instance(self):
        instance = self.model_cls(
            storage=self.storage,
            x=0,
            y=0,
            element=self.element_cls("Air")
        )

        yield instance
        instance.delete()
        self.element_cls.reset_all()

    @pytest.fixture
    def not_saved_instance(self):
        instance = self.model_cls(
            storage=self.storage,
            x=0,
            y=0,
            element=self.element_cls("Air"),
            to_save=False
        )

        yield instance
        instance.delete()
        self.element_cls.reset_all()

    def test_model_change(self, saved_instance):
        new_cords = 0.3, 0.4
        saved_instance.move_to(
            new_cords[0], new_cords[1],
            user=None,
            is_done=True
        )
        assert self.storage.get(self.model_cls, saved_instance.uuid).x == new_cords[0]
        assert self.storage.get(self.model_cls, saved_instance.uuid).y == new_cords[1]