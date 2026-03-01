# XBasic Architecture Guide

## System Overview

XBasic v2 uses a three-stage pipeline to transform high-level code into hardware execution:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  XBasic Code │───▶│ C++ Compiler │───▶│   Assembler  │───▶│  8-bit CPU   │
│   (.sl)      │    │  (Lexer →    │    │  (Python,    │    │  (Verilog    │
│              │    │   Parser →   │    │   asm.py)    │    │   RTL sim)   │
│              │    │   Codegen)   │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

## Compiler (C++20)

| Component | File | Purpose |
|-----------|------|---------|
| Lexer | `Lexer.cpp` / `Lexer.h` | Tokenizes source into keywords, identifiers, operators, literals |
| Token | `Token.h` | Defines all token types (30+ tokens) |
| Parser | `Parser.cpp` / `Parser.h` | Recursive descent parser → builds AST |
| AST | `AST.h` | Node types: Program, Declaration, Assignment, If, For, While, Print, Function, Return, Call, List, BinaryOp, Number, String, Identifier |
| Codegen | `Codegen.h` | Translates AST → 8-bit assembly |
| Symbols | `SymbolTable.h` | Tracks variable names → memory addresses (starting at `0x80`) |

## Assembler (Python)

`asm.py` converts human-readable assembly into machine code bytes. Supports:
- Labels and forward references
- `.text` and `.data` sections
- All CPU instructions (30+ opcodes)

## 8-bit CPU (Verilog)

| Module | Description |
|--------|-------------|
| `cpu.v` | Main CPU with fetch-decode-execute cycle |
| `alu.v` | 8-bit ALU: ADD, SUB, ADC, INC, DEC, AND, OR, XOR |
| `cpu_registers.v` | 7 general-purpose registers (A–G) + Temp |
| `machine.v` | Top-level: CPU + RAM + I/O |
| `ram.v` | 256-byte RAM |
| `register.v` | Single 8-bit register |
| `counter.v` | Program counter / stack pointer |

### CPU Features
- 7 general-purpose registers (A, B, C, D, E, F, G)
- Hardware stack with push/pop
- Conditional jumps: JZ, JNZ, JC, JNC (zero/carry flags)
- CALL/RET for subroutine support
- Memory-mapped I/O at address `0x00`

### Memory Map
```
0x00 – 0x7F : Program code (128 bytes)
0x80 – 0xFE : Variable storage (127 bytes)
0xFF        : Stack pointer init
```
