%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.alloc import alloc

@storage_var
func chars(index : felt) -> (char : felt):
end

@storage_var
func string_len() -> (len : felt):
end

# Send raw string
@view
func send_hello{syscall_ptr : felt*}() -> (str_len : felt, str : felt*):
    let str_len = 5
    let (str) = alloc()
    assert str[0] = 'H'
    assert str[1] = 'e'
    assert str[2] = 'l'
    assert str[3] = 'l'
    assert str[4] = 'o'

    return (str_len, str)
end

# Store string
@external
func write{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    str_len : felt, str : felt*
):
    string_len.write(str_len)
    _loop_write(str_len, str)

    return ()
end

func _loop_write{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    str_len : felt, str : felt*
):
    chars.write(str_len - 1, str[str_len - 1])

    if str_len == 1:
        return ()
    end

    return _loop_write(str_len - 1, str)
end

# Read string
@view
func read{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}() -> (
    str_len : felt, str : felt*
):
    alloc_locals
    let (str_len) = string_len.read()
    let (str) = alloc()
    _loop_read(str_len, str)

    return (str_len, str)
end

func _loop_read{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    str_len : felt, str : felt*
):
    let (char) = chars.read(str_len - 1)
    assert str[str_len - 1] = char

    if str_len == 1:
        return ()
    end

    return _loop_read(str_len - 1, str)
end
