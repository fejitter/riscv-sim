# Simulador RISC-V (RV32I) em Python

Projeto final de Organização de Computadores, Universidade Católica de Santos.
Simulador de um computador com CPU RV32I, barramento, RAM, VRAM e saída ASCII no terminal.

## Estado atual

CPU RV32I de ciclo único = Implementada: R (10), I aritmético (9), LW, SW, 6 branches, LUI, AUIPC, JAL, JALR
Instrução especial (Grupo 14) = SWAP implementada e testada
Barramento = Roteia leitura e escrita de 32 bits por faixa de endereço
Memória RAM = 0x00000 a 0x7FFFF, com validação de limites
VRAM e E/S programada = 0x80000 a 0x8FFFF, exibida no terminal a cada n instruções
Programa de teste = Implementado (`sim/programa.py`)
Mini montador = `sim/asm.py`, inverso do decodificador

## Ainda não implementado

- Interrupções (CPU e barramento)
- Periféricos em 0x9FC00 a 0x9FFFF e faixa reservada 0x90000 a 0x9FBFF
- Sinais de controle explícitos e log de acessos no barramento
- LB, LH, SB, SH
- Cache, pipeline e interface gráfica (pontuação extra)

## Instrução especial: SWAP (Grupo 14)

Troca o conteúdo de dois registradores sem registrador temporário: `rs1, rs2 = rs2, rs1`.

- Formato: Tipo R, opcode `0001011` (custom-0), `rd` ignorado
- Codificação de `swap x1, x2`: `0x0020800B`
- Os dois valores são lidos antes de qualquer escrita
- `swap x0, x5` não altera x0, pois a escrita em x0 é ignorada: x5 recebe 0

## Decisões de projeto

- Palavras de 32 bits sem sinal nos registradores (máscara `0xFFFFFFFF`)
- Memória em little-endian
- Acesso a endereço sem dispositivo no barramento levanta `IndexError`
- VRAM: cada byte é um caractere ASCII; bytes fora de 32 a 126 aparecem como espaço
- Valor de n (impressão da VRAM): definido em `Machine(n=...)`; o padrão é 100

## Como executar

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python -m pytest

Demonstração (programa de teste, imprime a VRAM a cada 5 instruções):

    python -m sim.programa

O programa usa SWAP, laço com desvio, `sw`/`lw` na RAM, `lui` e escrita na VRAM. A tela final mostra `BA6`.

## Estrutura

    sim/decoder.py     campos da instrução e imediatos
    sim/registers.py   32 registradores (x0 fixo em zero)
    sim/ula.py         operações da ULA
    sim/memory.py      RAM com validação de limites
    sim/bus.py         barramento com roteamento por faixa
    sim/vram.py        VRAM com render ASCII
    sim/cpu.py         execução das instruções e ciclo de busca
    sim/machine.py     junta CPU, barramento, RAM e VRAM
    sim/asm.py         codificador de instruções
    sim/programa.py    programa de teste
    tests/             testes automatizados

## Versão do Python

Testado com Python 3.14 e no 3.12.
