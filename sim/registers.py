class RegisterFile:
    def __init__(self) -> None:
        self.regs: list[int] = [0] * 32

    def read(self, n: int) -> int:  # devolva regs[n]
        return self.regs[n]

    def write(self, n: int, value: int) -> None: # ignore se n == 0; senão guarde value & 0xFFFFFFFF
        if n != 0:
            self.regs[n] = value & 0xFFFFFFFF