from sim.memory import Memory

def test_write_read_word():
    m = Memory()
    m.write_word(0x100, 0x12345678)
    assert m.read_word(0x100) == 0x12345678

def test_little_endian():
    m = Memory()
    m.write_word(0, 0x12345678)
    assert m.data[0] == 0x78
    assert m.data[3] == 0x12

def test_write_masks_32_bits():
    m = Memory()
    m.write_word(0, -1)
    assert m.read_word(0) == 0xFFFFFFFF