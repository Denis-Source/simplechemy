from models.entity import Entity
from storage.memory import MemoryStorage
from tests.integration.test_model_in_storage.base_test_model_in_storage import BaseTestModelInStorage


class TestEntityInMemoryStorage(BaseTestModelInStorage):
    storage = MemoryStorage()
    model_cls = Entity

    def test_model_to_dict_conversion(self, saved_instance: Entity):
        assert saved_instance.to_dict() == {
            "type": self.model_cls.NAME,
            "uuid": saved_instance.uuid,
            "name": saved_instance.name
        }
