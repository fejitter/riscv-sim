'''
Esse arquivo contém testes unitários para a função decode_fields e outras funções auxiliares do módulo 'sim.decoder'.
'''

from sim.decoder import decode_fields, sign_extend, imm_i, imm_s, imm_b, imm_u, imm_j

def test_add():
    f = decode_fields(0x002081B3)  # add x3, x1, x2

    assert f["opcode"] == 0b0110011
    assert f["rd"] == 3
    assert f["funct3"] == 0
    assert f["rs1"] == 1
    assert f["rs2"] == 2
    assert f["funct7"] == 0

def test_sub(): 
    f = decode_fields(0x402081B3)  # sub x3, x1, x2

    assert f["opcode"] == 0b0110011
    assert f["rd"] == 3
    assert f["funct3"] == 0
    assert f["rs1"] == 1
    assert f["rs2"] == 2
    assert f["funct7"] == 0b0100000

def test_addi():
    f = decode_fields(0x00500093) # addi x1, x0, 5

    assert f["opcode"] == 0b0010011
    assert f["rd"] == 1
    assert f["funct3"] == 0
    assert f["rs1"] == 0
    assert f["rs2"] == 5
    assert f["funct7"] == 0

def test_sign_extend():
    assert sign_extend(0b0111, 4) == 7
    assert sign_extend(0b1111, 4) == -1
    assert sign_extend(0b1000, 4) == -8

def test_imm_i():
    assert imm_i(0x00500093) == 5      # addi x1, x0, 5
    assert imm_i(0xFFF00093) == -1     # addi x1, x0, -1

def test_imm_s():
    assert imm_s(0x00112423) == 8
    assert imm_s(0xFE112E23) == -4

def test_imm_b():
    assert imm_b(0x00208463) == 8
    assert imm_b(0xFE208EE3) == -4

def test_imm_u():
    assert imm_u(0x123450B7) == 0x12345000

def test_imm_j():
    assert imm_j(0x008000EF) == 8
    assert imm_j(0xFFDFF0EF) == -4