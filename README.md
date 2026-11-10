# Simulador RISC-V (RV32I) em Python

Projeto Final de Organização de Computadores, Universidade Católica de Santos.

## Estado atual
- Decodificador de instruções e imediatos (I, S, B, U, J);
- Banco de registradores (x0 fixo em zero);
- ULA (ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU);
- Memória RAM principal com validação de limites;
- CPU com ciclo de busca e execução (RV32I: R, I, LW, SW, branches, LUI, AUIPC, JAL, JALR).

## Ainda não implementado
- Instrução especial do grupo;
- Barramento, VRAM, periféricos e terminal;
- Programa de teste.

## Como executar os testes
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python -m pytest

Testado com Python 3.14 (a verificar no 3.12).