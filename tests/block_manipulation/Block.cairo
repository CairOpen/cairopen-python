%lang starknet

from starkware.starknet.common.syscalls import get_block_number, get_block_timestamp

@view
func block_and_time{syscall_ptr : felt*, range_check_ptr}() -> (time : felt, block : felt):
    let (current_timestamp) = get_block_timestamp()
    let (current_block) = get_block_number()

    return (current_timestamp, current_block)
end
