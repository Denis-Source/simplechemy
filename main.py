import logging

from models.element import Element, ElementAlreadyHasInvolvedRecipeException, ElementAlreadyHasRecipeException
from models.recipe import Recipe

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )

    Element.load_from_txt("recepies.txt")

    for i in Element.list():
        print(i)
