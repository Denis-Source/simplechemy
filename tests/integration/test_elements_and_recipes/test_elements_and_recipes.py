from random import shuffle

import pytest

import config
from models.fungeble.element import Element, IncompleteElementContent, IncorrectElementRecipe
from services.utils import load_from_txt


class TestElementsAndRecipes:
    @pytest.fixture
    def element_cls(self):
        yield Element
        Element.reset_all()

    @pytest.fixture
    def mock_recipes(self):
        return "Air\n" \
               "Water\n" \
               "Fire\n" \
               "Soil\n" \
               "Bird = Air + Life\n" \
               "Life = Energy + Water\n" \
               "Energy = Thunderbolt + Thunderbolt\n" \
               "Thunderbolt = Cloud + Cloud\n" \
               "Cloud = Air + Water\n" \
               "Compass = Electricity + Magnet\n" \
               "Electricity = Metal + Thunderbolt\n" \
               "Metal = Fire + Stone\n" \
               "Stone = Soil + Soil\n" \
               "Magnet = Electricity + Metal", 14

    @pytest.fixture
    def mock_txt_file_with_recipes(self, mock_recipes, tmpdir):
        filepath = tmpdir.join("mock_recipes.txt")
        with open(filepath, "w") as f:
            f.write(mock_recipes[0])

        return filepath, mock_recipes[1]

    @pytest.fixture
    def incomplete_mock_recipes(self, mock_recipes):
        return mock_recipes[0] + \
               "Puddle = Road + Water\n", mock_recipes[1] + 2

    @pytest.fixture
    def mock_recipes_with_more_than_one_option(self):
        return "Air\n" \
               "Water\n" \
               "Cloud = Air + Water\n" \
               "Cloud = Air + Air", 3

    @pytest.fixture
    def mock_txt_file_with_recipes_with_more_than_one_option(self, mock_recipes_with_more_than_one_option, tmpdir):
        filepath = tmpdir.join("mock_recipes.txt")
        with open(filepath, "w") as f:
            f.write(mock_recipes_with_more_than_one_option[0])

        return filepath, mock_recipes_with_more_than_one_option[1]

    @pytest.fixture
    def incomplete_mock_txt_file_with_recipes(self, incomplete_mock_recipes, tmpdir):
        filepath = tmpdir.join("mock_recipes.txt")
        with open(filepath, "w") as f:
            f.write(incomplete_mock_recipes[0])

        return filepath

    def test_element_loaded_from_txt(self, element_cls, mock_txt_file_with_recipes):
        filepath, correct_amount = mock_txt_file_with_recipes

        elements = load_from_txt(filepath)
        assert len(elements) == correct_amount
        assert element_cls.get_element_count() == correct_amount

    def test_element_loaded_from_txt_shuffled(self, element_cls, mock_recipes, tmpdir):
        recipe, correct_amount = mock_recipes
        elements_example = None

        for i in range(2):
            filepath = tmpdir.join(f"mock_recipes{i}.txt")
            with open(filepath, "w") as f:
                shuffled_recipe = [line.strip() for line in recipe.split("\n")]
                shuffle(shuffled_recipe)
                f.write(
                    "\n".join(shuffled_recipe)
                )

            elements = load_from_txt(filepath)
            assert len(elements) == correct_amount
            assert element_cls.get_element_count() == correct_amount

            # confirm that every single result is identical to the first one
            if not elements_example:
                elements_example = elements
            else:
                assert set(elements) == set(elements_example)

    def test_incomplete_element_content(self, element_cls, incomplete_mock_txt_file_with_recipes):
        with pytest.raises(IncompleteElementContent):
            load_from_txt(incomplete_mock_txt_file_with_recipes)

    def test_elements_can_have_two_or_more_recipes(self, element_cls,
                                                   mock_txt_file_with_recipes_with_more_than_one_option):
        filepath, correct_amount = mock_txt_file_with_recipes_with_more_than_one_option

        elements = load_from_txt(filepath)
        assert len(elements) == correct_amount
        assert element_cls.get_element_count() == correct_amount

    def test_if_element_content_path_correct(self, element_cls):
        filepath = config.get_element_content_path()
        load_from_txt(filepath)
        assert element_cls.list()

    def test_correct_recipe(self, element_cls, mock_txt_file_with_recipes):
        load_from_txt(mock_txt_file_with_recipes[0])
        recipe_elements = [element_cls.get("Fire"), element_cls.get("Stone")]
        correct_element = element_cls.get("Metal")

        assert element_cls.get_result(recipe_elements) == correct_element

    def test_incorrect_recipe(self, element_cls, mock_txt_file_with_recipes):
        load_from_txt(mock_txt_file_with_recipes[0])
        recipe_elements = [element_cls.get("Fire"), element_cls.get("Bird")]

        with pytest.raises(IncorrectElementRecipe):
            element_cls.get_result(recipe_elements)

    def test_correct_recipe_incorrect_result(self, element_cls, mock_txt_file_with_recipes):
        load_from_txt(mock_txt_file_with_recipes[0])
        recipe_elements = [element_cls.get("Fire"), element_cls.get("Stone")]
        correct_element = element_cls.get("Bird")

        assert element_cls.get_result(recipe_elements) != correct_element
