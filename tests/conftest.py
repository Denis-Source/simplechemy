import pytest

import config
from models.fungeble.element import Element


@pytest.fixture
def element_cls(self):
    filepath = config.get_element_content_path()
    Element.load_from_txt(filepath)

    yield Element
    Element.reset_all()
