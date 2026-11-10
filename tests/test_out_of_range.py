import pytest
from sim.memory import Memory

def test_out_of_range_read():
    m = Memory()
    with pytest.raises(IndexError):
        m.read_word(0x7FFFE)

def test_out_of_range_write():
    m = Memory()
    with pytest.raises(IndexError):
        m.write_word(0x7FFFE, 1)

def test_last_valid_word():
    m = Memory()
    m.write_word(0x7FFFC, 0xAABBCCDD)
    assert m.read_word(0x7FFFC) == 0xAABBCCDD