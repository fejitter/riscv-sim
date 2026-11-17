from sim.asm import encode_r, encode_i, encode_s, encode_b, encode_j, encode_u

OP_R, OP_I, OP_LOAD, OP_S, OP_B = 0b0110011, 0b0010011, 0b0000011, 0b0100011, 0b1100011
OP_LUI, OP_JAL, OP_CUSTOM0 = 0b0110111, 0b1101111, 0b0001011

PROGRAMA = [
    encode_i(0x41, 0, 0b000, 1, OP_I),
    encode_i(0x42, 0, 0b000, 2, OP_I),
    encode_r(0, 2, 1, 0b000, 0, OP_CUSTOM0),
    encode_i(8, 2, 0b001, 2, OP_I),
    encode_r(0, 2, 1, 0b110, 3, OP_R),
    encode_i(0, 0, 0b000, 4, OP_I),
    encode_i(3, 0, 0b000, 5, OP_I),               
    encode_r(0, 5, 4, 0b000, 4, OP_R),           
    encode_i(-1, 5, 0b000, 5, OP_I),
    encode_b(-8, 0, 5, 0b001, OP_B),
    encode_u(0x1000, 6, OP_LUI),
    encode_s(0, 4, 6, 0b010, OP_S), 
    encode_i(0, 6, 0b010, 7, OP_LOAD),
    encode_i(0x30, 7, 0b000, 7, OP_I),
    encode_i(16, 7, 0b001, 7, OP_I),
    encode_r(0, 7, 3, 0b110, 3, OP_R),
    encode_u(0x80000, 8, OP_LUI),
    encode_s(0, 3, 8, 0b010, OP_S),
    encode_j(0, 0, OP_JAL),
]

if __name__ == "__main__":
    from sim.machine import Machine
    m = Machine(n=5)
    m.load(PROGRAMA)
    m.run(30)