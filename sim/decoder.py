'''
Projeto Final - Organização de Computadores | Professor: Walter Oliveira
                                            | Aluno: Felipe Gomes Vieira Pais — 1234078
'''

def bits(word: int, hi: int, lo: int) -> int:
    n = hi - lo + 1
    return (word >> lo) & ((1 << n) - 1)

def decode_fields(word: int) -> dict[str, int]:
    return {
        'opcode': bits(word, 6, 0),
        'rd': bits(word, 11, 7),
        'funct3': bits(word, 14, 12),
        'rs1': bits(word, 19, 15),
        'rs2': bits(word, 24, 20),
        'funct7': bits(word, 31, 25)
    }

def sign_extend(value: int, nbits: int) -> int: # se o bit (nbits - 1) de value for 1, devolva value - 2**nbits, caso contrário devolva value
    if value & (1 << (nbits - 1)):
        return value - (1 << nbits)
    else:
        return value

def imm_i(word: int) -> int:
    imm = bits(word, 31, 20)
    return sign_extend(imm, 12)

def imm_s(word: int) -> int: # devolve os 12 bits de imediato do tipo S, que são compostos pelos 7 bits mais 
                             # significativos (31 a 25) e pelos 5 bits menos significativos (11 a 7)
    alta = bits(word, 31, 25)
    baixa = bits(word, 11, 7)
    imm = (alta << 5) | baixa
    return sign_extend(imm, 12)

def imm_b(word: int) -> int:
    imm = bits(word, 31, 31) << 12
    imm |= bits(word, 7, 7) << 11
    imm |= bits(word, 30, 25) << 5
    imm |= bits(word, 11, 8) << 1
    return sign_extend(imm, 13)

def imm_u(word: int) -> int: # só devolve os 20 bits mais significativos de word,
                             # deslocados para a esquerda 12 bits
    return word & 0xFFFFF000

def imm_j(word: int) -> int:
    imm = bits(word, 31, 31) << 20
    imm |= bits(word, 19, 12) << 12
    imm |= bits(word, 20, 20) << 11
    imm |= bits(word, 30, 21) << 1
    return sign_extend(imm, 21)