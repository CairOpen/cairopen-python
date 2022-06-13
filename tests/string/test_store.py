import pytest

from src.cairopen.utils import str_to_felt_arr, felt_arr_to_str


@pytest.mark.asyncio
async def test_read(string_factory):
    string = string_factory
    execution_info = await string.send_hello().call()
    assert len(execution_info.result.str) == 5
    assert felt_arr_to_str(execution_info.result.str) == "Hello"


LONG_STRING = (
    "This is a long string way longer than 31 characters that also includes numerals."
)


@pytest.mark.asyncio
async def test_read_write_string(string_factory):
    string = string_factory
    await string.write(str_to_felt_arr(LONG_STRING)).invoke()
    execution_info = await string.read().call()
    assert len(execution_info.result.str) == len(LONG_STRING)
    assert felt_arr_to_str(execution_info.result.str) == LONG_STRING
