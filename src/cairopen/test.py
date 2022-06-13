"""Utilities for testing Cairo contracts."""

from starkware.starknet.business_logic.execution.objects import Event
from starkware.starknet.business_logic.state.state import BlockInfo
from starkware.starknet.public.abi import get_selector_from_name
from starkware.starknet.testing.starknet import Starknet
from starkware.starkware_utils.error_handling import StarkException
from starkware.starknet.testing.starknet import StarknetContract

#
# Cache contracts
#


def cached_contract(state, deployed_contract):
    """Returns a cached contract at a certain StarkNet state."""
    contract = StarknetContract(
        state=state,
        abi=deployed_contract.abi,
        contract_address=deployed_contract.contract_address,
        deploy_execution_info=deployed_contract.deploy_execution_info,
    )
    return contract


#
# Assertions
#


async def assert_revert(fun, reverted_with=None):
    """Asserts that a function throws a revert exception."""
    try:
        await fun
        assert False
    except StarkException as err:
        _, error = err.args
        if reverted_with is not None:
            assert reverted_with in error["message"]


def assert_event_emitted(tx_exec_info, from_address, name, data):
    """Asserts that an event was emitted."""
    assert (
        Event(
            from_address=from_address,
            keys=[get_selector_from_name(name)],
            data=data,
        )
        in tx_exec_info.raw_events
    )


#
# Block mocking
#


async def block_mock(starknet: Starknet):
    """Enables mocking of block info."""
    state = starknet.state.copy()

    class Mock:
        def __init__(self, current_block_info):
            self.block_info = current_block_info

        def update(self, block_number, block_timestamp):
            state.state.block_info = BlockInfo(
                block_number,
                block_timestamp,
                self.block_info.gas_price,
                self.block_info.sequencer_address,
            )

        def reset(self):
            state.state.block_info = self.block_info

        def set_block_number(self, block_number):
            state.state.block_info = BlockInfo(
                block_number,
                self.block_info.block_timestamp,
                self.block_info.gas_price,
                self.block_info.sequencer_address,
            )

        def set_block_timestamp(self, block_timestamp):
            state.state.block_info = BlockInfo(
                self.block_info.block_number,
                block_timestamp,
                self.block_info.gas_price,
                self.block_info.sequencer_address,
            )

    return Mock(state.state.block_info), state
