class Memory:
    def __init__(self, size: int = 0x80000) -> None:
            self.data = bytearray(size)

    def read_word(self, addr: int) -> int:  # junte os 4 bytes a partir de addr em little-endian
        if addr < 0 or addr + 4 > len(self.data):
            raise IndexError("Endereço fora dos limites")
        return int.from_bytes(self.data[addr:addr+4], byteorder='little')

    def write_word(self, addr: int, value: int) -> None:  # grave os 4 bytes de value em little-endian
        if addr < 0 or addr + 4 > len(self.data):
            raise IndexError("Endereço fora dos limites")
        value &= 0xFFFFFFFF  # Mascarar para garantir que seja um valor de 32 bits
        self.data[addr:addr+4] = value.to_bytes(4, byteorder='little')