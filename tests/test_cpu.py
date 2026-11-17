from sim.cpu import CPU, execute_r, execute_i
from sim.registers import RegisterFile
from sim.memory import Memory
from sim.bus import Bus

def test_add_executes():
    rf = RegisterFile()
    rf.write(1, 10)
    rf.write(2, 32)
    execute_r(rf, 0x002081B3)    # add x3, x1, x2
    assert rf.read(3) == 42

def test_sub_executes():
    rf = RegisterFile()
    rf.write(1, 10)
    rf.write(2, 32)
    execute_r(rf, 0x402081B3)    # sub x3, x1, x2
    assert rf.read(3) == 0xFFFFFFEA   # 10 - 32 = -22

def test_addi_positive():
    rf = RegisterFile()
    execute_i(rf, 0x00500093)    # addi x1, x0, 5
    assert rf.read(1) == 5

def test_addi_negative():
    rf = RegisterFile()
    rf.write(1, 10)
    execute_i(rf, 0xFFF08093)    # addi x1, x1, -1
    assert rf.read(1) == 9

def test_step_runs_program():
    m = Memory()
    m.write_word(0, 0x00500093)   # addi x1, x0, 5
    m.write_word(4, 0x00A08113)   # addi x2, x1, 10
    cpu = CPU(m)
    cpu.step()
    cpu.step()
    assert cpu.rf.read(1) == 5
    assert cpu.rf.read(2) == 15
    assert cpu.pc == 8

def test_slt_executes():
    rf = RegisterFile()
    rf.write(1, 0xFFFFFFFF)       # -1
    rf.write(2, 1)
    execute_r(rf, 0x0020A1B3)     # slt x3, x1, x2
    assert rf.read(3) == 1

def test_srai_executes():
    rf = RegisterFile()
    rf.write(1, 0xFFFFFFF0)
    execute_i(rf, 0x4040D113)     # srai x2, x1, 4
    assert rf.read(2) == 0xFFFFFFFF

def test_andi_executes():
    rf = RegisterFile()
    rf.write(1, 0b1111)
    execute_i(rf, 0x0060F113)     # andi x2, x1, 6
    assert rf.read(2) == 0b0110

def test_sw_lw():
    m = Memory()
    cpu = CPU(m)
    cpu.rf.write(1, 0x100)       # endereço base
    cpu.rf.write(2, 0xABCD)      # valor
    m.write_word(0, 0x0020A023)  # sw x2, 0(x1)
    m.write_word(4, 0x0000A183)  # lw x3, 0(x1)
    cpu.step()
    cpu.step()
    assert cpu.rf.read(3) == 0xABCD

def test_beq_taken():
    m = Memory()
    cpu = CPU(m)
    cpu.rf.write(1, 5)
    cpu.rf.write(2, 5)
    m.write_word(0, 0x00208463)   # beq x1, x2, +8
    cpu.step()
    assert cpu.pc == 8

def test_beq_not_taken():
    m = Memory()
    cpu = CPU(m)
    cpu.rf.write(1, 5)
    cpu.rf.write(2, 6)
    m.write_word(0, 0x00208463)   # beq x1, x2, +8
    cpu.step()
    assert cpu.pc == 4

def test_blt_signed():
    m = Memory()
    cpu = CPU(m)
    cpu.rf.write(1, 0xFFFFFFFF)   # -1
    cpu.rf.write(2, 1)
    m.write_word(0, 0x0020C463)   # blt x1, x2, +8
    cpu.step()
    assert cpu.pc == 8

def test_bltu_unsigned():
    m = Memory()
    cpu = CPU(m)
    cpu.rf.write(1, 0xFFFFFFFF)   # grande, sem sinal
    cpu.rf.write(2, 1)
    m.write_word(0, 0x0020E463)   # bltu x1, x2, +8
    cpu.step()
    assert cpu.pc == 4            # não salta: 4294967295 < 1 é falso

def test_lui():
    m = Memory(); cpu = CPU(m)
    m.write_word(0, 0x123450B7)   # lui x1, 0x12345
    cpu.step()
    assert cpu.rf.read(1) == 0x12345000

def test_jal():
    m = Memory(); cpu = CPU(m)
    m.write_word(0, 0x008000EF)   # jal x1, +8
    cpu.step()
    assert cpu.pc == 8
    assert cpu.rf.read(1) == 4

def test_jalr_rd_equals_rs1():
    m = Memory(); cpu = CPU(m)
    cpu.rf.write(1, 0x20)
    m.write_word(0, 0x000080E7)   # jalr x1, 0(x1)
    cpu.step()
    assert cpu.pc == 0x20
    assert cpu.rf.read(1) == 4

def test_swap_basic():
    m = Memory(); cpu = CPU(m)
    cpu.rf.write(1, 10)
    cpu.rf.write(2, 20)
    m.write_word(0, 0x0020800B)   # swap x1, x2
    cpu.step()
    assert cpu.rf.read(1) == 20
    assert cpu.rf.read(2) == 10
    assert cpu.pc == 4

def test_swap_same_register():
    m = Memory(); cpu = CPU(m)
    cpu.rf.write(1, 7)
    m.write_word(0, 0x0010800B)   # swap x1, x1
    cpu.step()
    assert cpu.rf.read(1) == 7

def test_swap_with_x0():
    m = Memory(); cpu = CPU(m)
    cpu.rf.write(5, 99)
    m.write_word(0, 0x0050000B)   # swap x0, x5
    cpu.step()
    assert cpu.rf.read(0) == 0    # x0 continua zero
    assert cpu.rf.read(5) == 0

def test_cpu_through_bus():
    bus = Bus()
    bus.attach(0x00000, 0x7FFFF, Memory(0x80000))
    bus.write_word(0, 0x00500093)   # addi x1, x0, 5
    cpu = CPU(bus)
    cpu.step()
    assert cpu.rf.read(1) == 5