from sim.registers import RegisterFile

def test_x0_is_always_zero():
    rf = RegisterFile()
    rf.write(0, 123)
    assert rf.read(0) == 0

def test_write_read():
    rf = RegisterFile()
    rf.write(5, 42)
    assert rf.read(5) == 42

def test_write_masks_32_bits():
    rf = RegisterFile()
    rf.write(1, -1)
    assert rf.read(1) == 0xFFFFFFFF