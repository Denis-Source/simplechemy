from models.nonfungeble.user import User
from storage.memory import MemoryStorage
from tests.integration.test_model_in_storage.test_entity_in_storage import TestEntityInMemoryStorage


class TestUserInMemoryStorage(TestEntityInMemoryStorage):
    storage = MemoryStorage()
    model_cls = User

    def test_model_change(self, saved_instance: User):
        ordinary_name = "Fine Name"

        saved_instance.change(name=ordinary_name)

        assert self.storage.get(self.model_cls, saved_instance.uuid).name == ordinary_name
