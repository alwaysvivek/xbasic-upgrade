# XBasic: Migration Guide — v1 → v2

This document explains how to migrate your existing XBasic programs from the Python interpreter (v1) to the compiled C++/Verilog version (v2).

---

## File Format

| | v1 | v2 |
|---|---|---|
| Extension | `.bsx` | `.sl` |
| Encoding | UTF-8 | ASCII |

Rename your files from `.bsx` to `.sl` and ensure all text is ASCII-compatible.

---

## Syntax Changes

### FOR Loops

v1 used both `THEN` and `END` or `NEXT` as loop terminators, with optional `STEP`:

```xbasic
# v1 syntax (with STEP)
FOR i = 1 TO 10 STEP 2 THEN
    print(i)
END
```

v2 supports both `THEN` and no-`THEN`, and terminates with `END` or `NEXT`:

```xbasic
# v2 syntax (no STEP support)
FOR i = 1 TO 10 THEN
    PRINT i
END
```

> [!WARNING]
> `STEP` is not supported in v2. All FOR loops increment by 1.

### PRINT Statement

v1 used `print()` as a function call. v2 uses `PRINT` as a keyword with optional parentheses:

```xbasic
# v1
print("hello")

# v2 — both work
PRINT 42
PRINT(42)
```

### Variable Declarations

v1 performed runtime type-checking via the interpreter. v2 performs no type validation — everything is an 8-bit unsigned integer internally:

```xbasic
# v1 — type checked at runtime
text name = "John"    # ✅ Works
num name = "John"     # ❌ Runtime error

# v2 — text is experimental, num is 0-255
num x = 300           # Wraps to 44 (300 % 256)
```

---

## Feature Removal Workarounds

### No `STEP` → Manual Increment

```xbasic
# v1
FOR i = 0 TO 10 STEP 2 THEN
    print(i)
END

# v2 workaround
num i = 0
WHILE i < 10
    PRINT i
    i = i + 2
END
```

### No `BREAK`/`CONTINUE` → Restructure Logic

```xbasic
# v1
FOR i = 1 TO 100 THEN
    IF i == 50 THEN BREAK
    print(i)
END

# v2 workaround — use a flag variable
num i = 0
num done = 0
FOR i = 1 TO 100 THEN
    IF done == 0 THEN
        PRINT i
    END
    IF i == 50 THEN
        num done = 1
    END
END
```

### No `AND`/`OR` → Nested IFs

```xbasic
# v1
IF x > 5 AND x < 10 THEN
    print("in range")
END

# v2 workaround
IF x > 5 THEN
    IF x < 10 THEN
        PRINT 1
    END
END
```

---

## Size Constraints

v2 runs on an 8-bit CPU with 256 bytes of total memory:

| Resource | Limit |
|----------|-------|
| Code size | ~128 bytes |
| Data (variables) | ~128 bytes (starting at `0x80`) |
| Stack depth | ~16 levels |
| Value range | 0–255 (unsigned) |

> [!CAUTION]
> Programs that exceed these limits will silently produce incorrect results or fail to assemble. Keep programs small and focused.

---

## CLI Migration

| Action | v1 | v2 |
|--------|----|----|
| Install | `pip install xbasic` | `pip install .` |
| Run file | `xbasic file -f prog.bsx` | `xbasic prog.sl` |
| Interactive | `xbasic shell` | Not available |
| Debug | N/A | `xbasic prog.sl --debug` |
