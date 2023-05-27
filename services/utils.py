import logging
from typing import List

from PIL import Image, ImageFont, ImageDraw

import config
from models.fungeble.element import Element, ElementNotExistException, ElementAlreadyHasRecipeException, \
    ElementAlreadyHasInvolvedRecipeException, IncompleteElementContent
from models.fungeble.recipe import Recipe

logger = logging.getLogger("utils")


def _load_starting_elements(lines: List[str], element_cls=Element):
    for line in lines:
        if line.count("=") == 0:
            element = element_cls(
                name=line.strip(),
                starting=True,
                recipes=[],
                recipe=None
            )
            if element not in element_cls.list(starting=True):
                element_cls.add_element(element, starting=True)


def _load_non_starting_elements(lines: List[str], total_elements: List[Element], element_cls=Element,
                                filepath=config.get_element_content_path()):
    not_found_recipes = set()
    found_flag = True
    while element_cls.get_element_count() != total_elements:
        previous_count = element_cls.get_element_count()
        for line in lines:
            if not line.count("="):
                continue

            result_name = line.split("=")[0].strip()
            if found_flag:
                not_found_recipes.add(result_name)

            recipe_names = [recipe_name.strip() for recipe_name in line.split("=")[1].strip().split("+")]
            try:
                all_there = all([Element.get(element_name) for element_name in recipe_names])
            except ElementNotExistException:
                all_there = False

            if all_there:
                new_element = element_cls(result_name, recipe=None)
                recipe = Recipe(result=new_element,
                                schema=[element_cls.get(element_name) for element_name in recipe_names])
                if result_name in not_found_recipes:
                    not_found_recipes.remove(result_name)
                try:
                    new_element.add_recipe(recipe)
                except ElementAlreadyHasRecipeException:
                    pass
                for involved_element in recipe.schema:
                    try:
                        involved_element.add_involved_recipe(recipe)
                    except ElementAlreadyHasInvolvedRecipeException:
                        pass
        if previous_count == element_cls.get_element_count():
            raise IncompleteElementContent(filepath, not_found_recipes)
        found_flag = False


def load_from_txt(filepath: str = config.get_element_content_path(), element_cls=Element):
    element_cls.reset_all()
    logger.info(f"loading {element_cls.NAME} from {filepath}")

    with open(filepath, "r") as f:
        lines = f.readlines()

    # starting elements
    total_elements = len(set([line.split("=")[0].strip() for line in lines]))
    _load_starting_elements(lines, element_cls=element_cls)
    logger.debug(f"loaded ({Element.get_element_count()}) starting elements")
    logger.debug("loading secondary elements")

    # locked elements
    _load_non_starting_elements(lines, total_elements, element_cls, filepath)
    logger.debug(f"loaded total: ({Element.get_element_count()}) elements")
    return Element.list()


def create_element_image(element: Element, image_path: str, size=512, padding=10):
    image = Image.new(mode="RGBA", size=(size, size), color=(0, 0, 0, 0))

    font_size = round((size - padding * 2) / len(element.name) * 2)

    font = ImageFont.truetype(config.get_font_path(), font_size)

    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(element.name, font=font)

    draw.text(((size - text_width) / 2, (size - text_height) / 2), element.name, font=font)
    image.save(image_path)


def convert_image_path(path: str) -> str:
    return path.replace(config.get_media_path(), config.get_media_url()).replace("\\", "/")
