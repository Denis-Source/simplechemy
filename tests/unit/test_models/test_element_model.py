import pytest

from models.fungeble.element import Element


class TestElementModel:
    def test_equal_elements(self, element_cls):
        element_one = element_cls("Air")
        element_two = element_cls("Air")

        assert element_one == element_two

    @pytest.fixture
    def element_cls(self):
        yield Element
        Element.reset_all()

    @pytest.fixture
    def element_names(self):
        yield ["Air", "Soil", "Water", "Fire"]

    def test_correct_amount_of_elements_created(self, element_names, element_cls):
        for element_name in element_names:
            for _ in range(10):
                element_cls(element_name)

        assert element_cls.get_element_count() == len(element_name)
