import pytest

from models.element import Element
from models.recipe import Recipe


class TestRecipeModel:
    @pytest.fixture
    def element_one(self):
        return Element(
            "Air",
            starting=True,
        )

    @pytest.fixture
    def element_two(self):
        return Element(
            "Water",
            starting=True
        )

    def test_equal_recipes(self, element_one, element_two):
        result_element = Element("Cloud")
        recipe_one = Recipe(
            result=result_element,
            schema=[element_one, element_two]
        )

        recipe_two = Recipe(
            result=result_element,
            schema=[element_one, element_two]
        )

        assert recipe_one == recipe_two
        assert recipe_one.schema == recipe_two.schema

    def test_different_recipes(self, element_one, element_two):
        result_element = Element("Cloud")

        recipe_one = Recipe(
            result=result_element,
            schema=[element_one, element_two]
        )

        recipe_two = Recipe(
            result=result_element,
            schema=[element_two, element_two]
        )

        assert recipe_one != recipe_two
        assert recipe_one.result == recipe_two.result
        assert recipe_one.schema != recipe_two.schema
