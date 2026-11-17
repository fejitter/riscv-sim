def encode_r(funct7, rs2, rs1, funct3, rd, opcode):
    return (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode

def encode_i(imm, rs1, funct3, rd, opcode):
    imm &= 0xFFF
    return (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode

def encode_s(imm, rs2, rs1, funct3, opcode):
    imm &= 0xFFF
    alto = imm >> 5          
    baixo = imm & 0x1F       
    return (alto << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (baixo << 7) | opcode

def encode_b(imm, rs2, rs1, funct3, opcode):
    imm &= 0x1FFF
    bit12 = (imm >> 12) & 0x1
    bit11 = (imm >> 11) & 0x1
    bits10_5 = (imm >> 5) & 0x3F
    bits4_1 = (imm >> 1) & 0xF
    return (bit12 << 31) | (bits10_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (bits4_1 << 8) | (bit11 << 7) | opcode

def encode_j(imm, rd, opcode):
    imm &= 0x1FFFFF
    bit20 = (imm >> 20) & 0x1
    bits19_12 = (imm >> 12) & 0xFF
    bit11 = (imm >> 11) & 0x1
    bits10_1 = (imm >> 1) & 0x3FF
    return (bit20 << 31) | (bits19_12 << 12) | (bit11 << 20) | (bits10_1 << 21) | (rd << 7) | opcode

def encode_u(imm, rd, opcode):
    imm &= 0xFFFFF000
    return (imm) | (rd << 7) | opcode