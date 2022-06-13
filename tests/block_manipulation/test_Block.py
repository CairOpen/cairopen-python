import pytest


@pytest.mark.asyncio
async def test_factory_update(time_factory):

    time, block_info_mock = time_factory

    execution_info = await time.block_and_time().call()
    initial_time = execution_info.result.time
    initial_block = execution_info.result.block

    #
    # Set custom block number
    #
    block_info_mock.set_block_number(123)
    block_info = await time.block_and_time().call()
    assert block_info.result.block != initial_block
    assert block_info.result.block == 123

    #
    # Set custom block timestamp
    #
    block_info_mock.set_block_timestamp(1653412708)
    block_info = await time.block_and_time().call()
    assert block_info.result.time != initial_time
    assert block_info.result.time == 1653412708
