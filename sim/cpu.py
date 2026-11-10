from sim.decoder import decode_fields, imm_i, imm_s, imm_b, imm_u, imm_j, sign_extend
from sim.registers import RegisterFile
from sim.memory import Memory
from sim.ula import ula

R_OPS = {
    (0x0, 0x00): "ADD",
    (0x0, 0x20): "SUB",
    (0x1, 0x00): "SLL",
    (0x2, 0x00): "SLT",
    (0x3, 0x00): "SLTU",
    (0x4, 0x00): "XOR",
    (0x5, 0x00): "SRL",
    (0x5, 0x20): "SRA",
    (0x6, 0x00): "OR",
    (0x7, 0x00): "AND",
}

def execute_r(rf: RegisterFile, word: int) -> None:
    f = decode_fields(word)
    key = (f["funct3"], f["funct7"])
    if key not in R_OPS:
        raise ValueError(f"instrução R inválida: {key}")
    a = rf.read(f["rs1"])
    b = rf.read(f["rs2"])
    rf.write(f["rd"], ula(R_OPS[key], a, b))

I_OPS = {
    0x0: "ADD",    # ADDI
    0x2: "SLT",    # SLTI
    0x3: "SLTU",   # SLTIU
    0x4: "XOR",    # XORI
    0x6: "OR",     # ORI
    0x7: "AND",    # ANDI
}

def execute_i(rf: RegisterFile, word: int) -> None:
    f = decode_fields(word)
    a = rf.read(f["rs1"])
    f3 = f["funct3"]
    if f3 == 0x1:
        op, b = "SLL", f["rs2"]                 # SLLI: shamt = bits [24:20]
    elif f3 == 0x5:
        op = "SRA" if f["funct7"] == 0x20 else "SRL"
        b = f["rs2"]                            # shamt
    else:
        op = I_OPS[f3]
        b = imm_i(word) & 0xFFFFFFFF            # imediato com sinal, em 32 bits
    rf.write(f["rd"], ula(op, a, b))

def execute_u(rf: RegisterFile, pc: int, word: int) -> None:
    f = decode_fields(word)
    if f["opcode"] == 0b0110111:      # LUI
        rf.write(f["rd"], imm_u(word))
    elif f["opcode"] == 0b0010111: # AUIPC | rd = (pc + imm_u) & 0xFFFFFFFF
        rf.write(f["rd"], (pc + imm_u(word)) & 0xFFFFFFFF)

def execute_jal(rf: RegisterFile, pc: int, word: int) -> int:
    f = decode_fields(word)
    rf.write(f["rd"], pc + 4)
    return (pc + imm_j(word)) & 0xFFFFFFFF

def execute_jalr(rf: RegisterFile, pc: int, word: int) -> int:
    f = decode_fields(word)
    target = (rf.read(f["rs1"]) + imm_i(word)) & 0xFFFFFFFE
    rf.write(f["rd"], pc + 4)
    return target

# Ligue no step: opcode 0000011 chama execute_load, e 0100011 chama execute_s.
def execute_load(rf: RegisterFile, mem: Memory, word: int) -> None:
    f = decode_fields(word)
    addr = (rf.read(f["rs1"]) + imm_i(word)) & 0xFFFFFFFF
    rf.write(f["rd"], mem.read_word(addr))

def execute_s(rf: RegisterFile, mem: Memory, word: int) -> None:
    f = decode_fields(word)
    addr = (rf.read(f["rs1"]) + imm_s(word)) & 0xFFFFFFFF
    mem.write_word(addr, rf.read(f["rs2"]))

def execute_b(rf: RegisterFile, pc: int, word: int) -> int:
    f = decode_fields(word)
    a = rf.read(f["rs1"])
    b = rf.read(f["rs2"])
    f3 = f["funct3"]
    if f3 == 0x0:        # BEQ
        taken = a == b
    elif f3 == 0x1:      # BNE
        taken = a != b
    elif f3 == 0x4:      # BLT (com sinal)
        taken = sign_extend(a, 32) < sign_extend(b, 32)
    elif f3 == 0x5:      # BGE (com sinal)
        taken = sign_extend(a, 32) >= sign_extend(b, 32)
    elif f3 == 0x6:
        taken = (a & 0xFFFFFFFF) < (b & 0xFFFFFFFF)
    elif f3 == 0x7:
        taken = (a & 0xFFFFFFFF) >= (b & 0xFFFFFFFF)
    else:
        raise ValueError(f"funct3 de branch inválido: {f3}")
    if taken:
        return (pc + imm_b(word)) & 0xFFFFFFFF
    return pc + 4

class CPU:
    def __init__(self, mem: Memory) -> None:
        self.rf = RegisterFile()
        self.mem = mem
        self.pc = 0

    def step(self) -> None:
        word = self.mem.read_word(self.pc)   # 1. busca
        opcode = word & 0x7F                 # 2. decodifica o formato
        next_pc = self.pc + 4
        if opcode == 0b0110011:
            execute_r(self.rf, word)
        elif opcode == 0b0010011:
            execute_i(self.rf, word)
        elif opcode == 0b0000011:
            execute_load(self.rf, self.mem, word)
        elif opcode == 0b0100011:
            execute_s(self.rf, self.mem, word)
        elif opcode == 0b1100011:
            next_pc = execute_b(self.rf, self.pc, word)
        elif opcode in (0b0110111, 0b0010111):
            execute_u(self.rf, self.pc, word)
        elif opcode == 0b1101111:
            next_pc = execute_jal(self.rf, self.pc, word)
        elif opcode == 0b1100111:
            next_pc = execute_jalr(self.rf, self.pc, word)
        else:
            raise ValueError(f"opcode não suportado: {opcode:#09b}")
        self.pc = next_pc & 0xFFFFFFFF       # 3. atualiza o PC