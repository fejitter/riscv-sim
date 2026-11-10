from sim.ula import ula

def test_add():
    assert ula("ADD", 2, 3) == 5

def test_add_overflow():
    assert ula("ADD", 0xFFFFFFFF, 1) == 0

def test_sub_negative():
    assert ula("SUB", 3, 5) == 0xFFFFFFFE   # -2 em 32 bits

def test_and_or():
    assert ula("AND", 0b1100, 0b1010) == 0b1000
    assert ula("OR", 0b1100, 0b1010) == 0b1110

def test_srl_vs_sra():
    assert ula("SRL", 0xFFFFFFF0, 4) == 0x0FFFFFFF
    assert ula("SRA", 0xFFFFFFF0, 4) == 0xFFFFFFFF

def test_slt_vs_sltu():
    assert ula("SLT", 0xFFFFFFFF, 1) == 1    # -1 < 1 com sinal
    assert ula("SLTU", 0xFFFFFFFF, 1) == 0   # 4294967295 < 1 é falso

def test_sll_xor():
    assert ula("SLL", 1, 4) == 16
    assert ula("XOR", 0b1100, 0b1010) == 0b0110