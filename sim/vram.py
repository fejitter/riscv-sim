from sim.memory import Memory

class Vram(Memory):
    def __init__(self) -> None:
        super().__init__(0x10000)

    def render(self, cols: int = 10, rows: int = 5) -> str:
        result = []
        for r in range(rows):
            line = []
            for c in range(cols):
                addr = r * cols + c
                if addr < len(self.data):
                    byte = self.data[addr]
                    line.append(chr(byte) if 32 <= byte <= 126 else ' ')
                else:
                    line.append(' ')
            result.append(''.join(line))
        return '\n'.join(result)