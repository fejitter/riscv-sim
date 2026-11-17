from sim.asm import encode_r, encode_i, encode_s, encode_b, encode_j, encode_u
from sim.decoder import imm_b, imm_j, imm_s

def test_encode_add():
    assert encode_r(0, 2, 1, 0, 3, 0b0110011) == 0x002081B3   # add x3, x1, x2

def test_encode_addi():
    assert encode_i(5, 0, 0, 1, 0b0010011) == 0x00500093      # addi x1, x0, 5

def test_encode_addi_negative():
    assert encode_i(-1, 1, 0, 1, 0b0010011) == 0xFFF08093     # addi x1, x1, -1

def test_encode_sw():
    assert encode_s(8, 1, 2, 0b010, 0b0100011) == 0x00112423      # sw x1, 8(x2)

def test_encode_sw_negative():
    assert encode_s(-4, 1, 2, 0b010, 0b0100011) == 0xFE112E23     # sw x1, -4(x2)

def test_encode_beq():
    assert encode_b(8, 2, 1, 0b000, 0b1100011) == 0x00208463      # beq x1, x2, +8

def test_encode_beq_negative():
    assert encode_b(-4, 2, 1, 0b000, 0b1100011) == 0xFE208EE3     # beq x1, x2, -4

def test_encode_jal():
    assert encode_j(8, 1, 0b1101111) == 0x008000EF                # jal x1, +8

def test_encode_jal_negative():
    assert encode_j(-4, 1, 0b1101111) == 0xFFDFF0EF               # jal x1, -4

def test_encode_lui():
    assert encode_u(0x12345000, 1, 0b0110111) == 0x123450B7       # lui x1, 0x12345

def test_roundtrip_imm():
    for v in (-2048, -100, -4, 0, 8, 100, 2047):
        assert imm_s(encode_s(v, 2, 1, 0b010, 0b0100011)) == v
    for v in (-4096, -100, -4, 0, 8, 100, 4094):
        assert imm_b(encode_b(v, 2, 1, 0b000, 0b1100011)) == v
    for v in (-1048576, -100, -4, 0, 8, 100, 1048574):
        assert imm_j(encode_j(v, 1, 0b1101111)) == v