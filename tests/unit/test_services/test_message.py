from dataclasses import dataclass

import pytest

from models.base import BaseModel
from services.message import Message


class TestMessage:
    @pytest.fixture
    def complex_instance(self):
        class TestModelOne(BaseModel):
            def __init__(self, field1: str, field2: str):
                self.field1 = field1
                self.field2 = field2

            @classmethod
            def from_data(cls, **kwargs) -> BaseModel:
                pass

            def as_dict(self) -> dict:
                return {
                    "field1": self.field1,
                    "field2": self.field2
                }

        class TestModelTwo(TestModelOne):
            def __init__(self, field1: int, field2: str, field3: TestModelOne):
                self.field1 = field1
                self.field2 = field2
                self.field3 = field3

            @classmethod
            def from_data(cls, **kwargs) -> BaseModel:
                pass

            def as_dict(self) -> dict:
                return {
                    "field1": self.field1,
                    "field2": self.field2,
                    "field3": self.field3.as_dict()
                }

        @dataclass
        class TestMessageClass(Message):
            field1: int
            field2: str
            field3: TestModelTwo

        instance = TestMessageClass(
            0,
            "0",
            TestModelTwo(0, "0", TestModelOne(0, "0"))
        )
        return instance

    def test_as_dict_conversion(self, complex_instance):
        a = complex_instance.as_dict()

        assert complex_instance.as_dict() == {
            "field1": 0,
            "field2": "0",
            "field3": {
                "field1": 0,
                "field2": "0",
                "field3": {
                    "field1": 0,
                    "field2": "0"
                }
            }
        }
