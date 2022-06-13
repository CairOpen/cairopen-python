import os
import pytest_asyncio
from starkware.starknet.testing.starknet import Starknet


@pytest_asyncio.fixture
async def string_factory(tests_path, cairo_path):
    starknet = await Starknet.empty()
    string = await starknet.deploy(
        os.path.join(tests_path, "string/String.cairo"), cairo_path=cairo_path
    )

    return string
