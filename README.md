<div align="center">

<h1>⚡ XBasic</h1>
<p>A compiled XBasic language targeting a custom 8-bit CPU — powered by C++, Verilog, and Python.</p>

<h4>
<a href="SYNTAX.md">Syntax Guide</a>
<span> · </span>
<a href="docs/comparison.md">v1 vs v2 Comparison</a>
<span> · </span>
<a href="docs/architecture.md">Architecture</a>
<span> · </span>
<a href="docs/migration.md">Migration Guide</a>
</h4>

</div>

---

## What is XBasic?

XBasic is a BASIC-inspired programming language that compiles to real 8-bit machine code. Unlike the original Python interpreter, this version uses:

- **C++20** for the compiler (lexer, parser, codegen)
- **Verilog** for the 8-bit CPU (ALU, registers, stack, RAM)
- **Python** for the toolchain CLI (assembler, simulation orchestration)

Your XBasic code becomes assembly → machine code → runs on a cycle-accurate CPU simulation.

## 🚀 Quick Start

### Install

```bash
git clone https://github.com/alwaysvivek/xbasic.git
cd xbasic
pip install .
```

### Run

```bash
xb-modern examples/hello.sl
```

Debug mode (shows full CPU trace):
```bash
xb-modern examples/hello.sl --debug
```

> [!NOTE]
> On macOS, you may need to add the Python bin directory to your PATH.
> Dependencies: `g++`, `make`, `iverilog`, `vvp`, Python 3.x

## 📦 What's Included

```text
.
├── xbasic_modern/
│   ├── compiler/       # C++ compiler (Lexer, Parser, AST, Codegen)
│   ├── simulator/      # 8-bit CPU (Verilog RTL + Python assembler)
│   └── tests/          # Example programs
├── docs/
│   ├── comparison.md   # Feature comparison: v1 vs v2
│   ├── migration.md    # How to migrate from v1
│   ├── architecture.md # System architecture overview
│   └── ISA.md          # Instruction set reference
├── SYNTAX.md           # Complete language syntax guide
├── setup.py            # pip packaging
└── Makefile            # C++ build system
```

## ✨ Language Features

| Feature | Support |
|---------|---------|
| Integer variables (`num`) | ✅ 8-bit (0–255) |
| String literals (`text`) | ⚠️ Experimental |
| `IF` / `ELIF` / `ELSE` | ✅ Full branching |
| `FOR` loops | ✅ |
| `WHILE` loops | ✅ |
| Functions (`FN` / `RETURN`) | ✅ |
| Comparison operators | ✅ `==` `!=` `>` `<` `>=` `<=` |
| Arithmetic | ✅ `+` `-` (hardware), ⚠️ `*` `/` |
| Comments | ✅ `#` |
| Lists | ⚠️ Parse-only |

## 📝 Example

```xbasic
FN double(n)
    RETURN n + n
END

num val = 10
num res = double(val)
PRINT res

num x = 5
IF x > 10 THEN
    PRINT 0
ELIF x < 3 THEN
    PRINT 1
ELSE
    PRINT 2
END
```

**Output:**
```
> 20
> 2
```

## 🏗️ How It Works

```
XBasic Source (.sl)
       │
       ▼
┌─────────────────┐
│  C++ Compiler   │  Lexer → Parser → AST → Codegen
└────────┬────────┘
         │  output.asm
         ▼
┌─────────────────┐
│  Python Assembler│  Labels → Machine code bytes
└────────┬────────┘
         │  memory.list
         ▼
┌─────────────────┐
│  Verilog 8-bit  │  Fetch → Decode → Execute
│  CPU Simulator  │  ALU, Registers, Stack, RAM
└─────────────────┘
```

## ⚡ Performance vs v1

| Metric | v1 (Python) | v2 (Compiled) |
|--------|------------|---------------|
| Execution | ~1000 ops/sec | 1 op/cycle |
| Memory | ~30MB (Python VM) | 256 bytes |
| Startup | ~200ms | ~5ms |
| Determinism | GC pauses | Cycle-accurate |

> See [docs/comparison.md](docs/comparison.md) for the full feature comparison.

## 📋 Register Map

| Register | Purpose |
|----------|---------|
| A | Accumulator / ALU result |
| B | Secondary operand |
| C–G | General purpose / temporaries |
| T | Memory address buffer |

## 📄 Documentation

- **[SYNTAX.md](SYNTAX.md)** — Complete language reference
- **[docs/comparison.md](docs/comparison.md)** — What changed from v1 to v2
- **[docs/migration.md](docs/migration.md)** — How to port your v1 programs
- **[docs/architecture.md](docs/architecture.md)** — System internals
- **[docs/ISA.md](docs/ISA.md)** — CPU instruction set

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.