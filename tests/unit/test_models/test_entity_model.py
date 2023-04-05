from models.nonfungeble.entity import Entity
from tests.unit.test_models.base_test_model import BaseTestModel


class TestEntityModel(BaseTestModel):
    model_cls = Entity

    def test_correct_dict(self, model_instance):
        assert model_instance.as_dict() == {
            "type": model_instance.NAME,
            "name": model_instance.name,
            "uuid": model_instance.uuid
        }
