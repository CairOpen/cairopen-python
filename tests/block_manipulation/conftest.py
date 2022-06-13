import os
import pytest
import pytest_asyncio
from starkware.starknet.testing.starknet import Starknet

from src.cairopen.test import block_mock, cached_contract


@pytest_asyncio.fixture
async def starknet():
    starknet = await Starknet.empty()
    return starknet


@pytest_asyncio.fixture
async def time_init(tests_path, cairo_path, starknet):
    time = await starknet.deploy(
        os.path.join(tests_path, "block_manipulation/Block.cairo"),
        cairo_path=cairo_path,
    )

    return time


@pytest_asyncio.fixture
async def block_info_mock_builder(starknet):
    block_info_mock, state = await block_mock(starknet)
    return block_info_mock, state


@pytest.fixture
def time_factory(time_init, block_info_mock_builder):
    time = time_init
    block_info_mock, state = block_info_mock_builder
    time = cached_contract(state, time)

    return time, block_info_mock
