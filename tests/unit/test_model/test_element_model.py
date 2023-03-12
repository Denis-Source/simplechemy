import pytest

from models.element import Element


class TestElementModel:
    def test_equal_elements(self):
        element_one = Element("Air")
        element_two = Element("Air")

        assert element_one == element_two

    @pytest.fixture
    def element_names(self):
        return ["Air", "Soil", "Water", "Fire"]

    def test_correct_amount_of_elements_created(self, element_names):
        for element_name in element_names:
            for _ in range(10):
                e = Element(element_name)

        assert Element.get_element_count() == len(element_name)
