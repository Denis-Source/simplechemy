import pytest

from models.fungeble.element import Element
from models.nonfungeble.element_position import ElementPosition
from storage.memory import MemoryStorage
from tests.integration.test_model_in_storage.test_entity_in_storage import TestEntityInMemoryStorage


class TestElementPositionInMemoryStorage(TestEntityInMemoryStorage):
    storage = MemoryStorage()
    model_cls = ElementPosition

    @pytest.fixture(scope="module")
    def element_cls(self):
        yield Element
        Element.reset_all()

    @pytest.fixture
    def saved_instance(self, element_cls):
        instance = self.model_cls(
            x=0,
            y=0,
            element=element_cls("Air")
        )
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    @pytest.fixture
    def not_saved_instance(self, element_cls):
        instance = self.model_cls(
            x=0,
            y=0,
            element=element_cls("Air"),
        )

        yield instance

    def test_model_change(self, saved_instance):
        new_cords = 0.3, 0.4
        saved_instance.move_to(
            new_cords[0], new_cords[1],
            user=None,
            is_done=True
        )
        assert self.storage.get(self.model_cls, saved_instance.uuid).x == new_cords[0]
        assert self.storage.get(self.model_cls, saved_instance.uuid).y == new_cords[1]
