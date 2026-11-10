'''
Dois conceitos:

Endereço é em bytes, palavra tem 4 bytes. bytearray guarda um byte por posição, então uma palavra ocupa addr até addr+3.
Little-endian: o byte menos significativo fica no menor endereço. A palavra 0x12345678 em addr vira os bytes 78 56 34 12.

Dica: int.from_bytes(self.data[addr:addr+4], "little") e value.to_bytes(4, "little") fazem o trabalho. Lembre de mascarar value com & 0xFFFFFFFF na escrita.
'''

#23 testes passando e o código está correto. from_bytes e to_bytes em little-endian fazem exatamente o que o enunciado de memória pede, e o value &= 0xFFFFFFFF garante 32 bits (o -1 vira 0xFFFFFFFF).

#Hoje a Memory aceita endereços que não deveria, e isso vai importar na defesa e no bloco da RAM (2 pontos):
#Leitura além do fim: read_word(0x7FFFE) pega só 2 bytes (o slice é cortado) e devolve um valor errado sem avisar.
#Escrita além do fim: write_word(0x7FFFE, ...) com um slice maior que o espaço aumenta o bytearray silenciosamente, quebrando o tamanho da RAM.

# O enunciado fala em “o endereço correto”, então o comportamento fora da faixa precisa ser uma decisão sua, documentada. Sugestão: levantar IndexError se addr < 0 ou addr + 4 > len(self.data). Tarefa pequena: adicione essa checagem nos dois métodos e escreva um teste com pytest.raises(IndexError)

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