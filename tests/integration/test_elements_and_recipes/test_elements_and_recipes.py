from random import shuffle

import pytest

from models.element import Element


class TestElementsAndRecipes:
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
               "Magnet = Electricity + Metal"

    @pytest.fixture
    def mock_txt_file_with_recipes(self, mock_recipes, tmpdir):
        filepath = tmpdir.join("mock_recipes.txt")
        with open(filepath, "w") as f:
            f.write(mock_recipes)

        return filepath

    def test_element_loaded_from_txt(self, mock_recipes, mock_txt_file_with_recipes):
        correct_elements_amount = len(mock_recipes.split("\n"))

        elements = Element.load_from_txt(mock_txt_file_with_recipes)
        assert len(elements) == correct_elements_amount
        assert Element.get_element_count() == correct_elements_amount

    def test_element_loaded_from_txt_shuffled(self, mock_recipes, tmpdir):
        correct_elements_amount = len(mock_recipes.split("\n"))
        elements_example = None

        for i in range(1000):
            filepath = tmpdir.join(f"mock_recipes{i}.txt")
            with open(filepath, "w") as f:
                shuffled_recipe = [line.strip() for line in mock_recipes.split("\n")]
                shuffle(shuffled_recipe)
                f.write(
                    "\n".join(shuffled_recipe)
                )

            elements = Element.load_from_txt(filepath)
            assert len(elements) == correct_elements_amount
            assert Element.get_element_count() == correct_elements_amount

            # confirm that every single result is identical to the first one
            if not elements_example:
                elements_example = elements
            else:
                assert elements == elements_example




