from sim.decoder import sign_extend

MASK = 0xFFFFFFFF

def ula(op: str, a: int, b: int) -> int:
    if op == "XOR":
        return a ^ b
    
    if op == "SLL":
        return (a << (b & 0x1F)) & MASK
    
    if op == "SRL":
        return (a >> (b & 0x1F)) & MASK
    
    if op == "SRA":
        a_signed = sign_extend(a, 32)
        return (a_signed >> (b & 0x1F)) & MASK
    
    if op == "SLT":
        a_signed = sign_extend(a, 32)
        b_signed = sign_extend(b, 32)
        return 1 if a_signed < b_signed else 0

    if op == "SLTU":
        return 1 if a < b else 0
    
    if op == "ADD":
        return (a + b) & MASK
    
    if op == "SUB":
        return (a - b) & MASK
    
    if op == "AND":
        return a & b
    
    if op == "OR":
        return a | b
    raise ValueError(f"operação desconhecida: {op}")