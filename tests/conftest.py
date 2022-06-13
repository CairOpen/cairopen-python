import os
import pytest


@pytest.fixture
def cairo_path():
    cairo_path = [os.path.join(os.path.dirname(__file__))]
    return cairo_path


@pytest.fixture
def tests_path():
    return os.path.dirname(__file__)
