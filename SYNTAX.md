# XBasic Syntax Guide

Complete reference for the XBasic language (v2.0 — Compiled Edition).

---

## Table of Contents

1. [Comments](#comments)
2. [Variables & Data Types](#variables--data-types)
3. [Operators](#operators)
4. [Control Flow](#control-flow)
5. [Functions](#functions)
6. [Output](#output)
7. [Grammar (BNF)](#formal-grammar)

---

## Comments

Single-line comments start with `#`:

```xbasic
# This is a comment
num x = 10  # Inline comment
```

---

## Variables & Data Types

### Declaration

Variables are declared with a type keyword and optional initializer:

```xbasic
num x = 42
num counter = 0
text greeting = "hello"
```

### Supported Types

| Type | Description | Value Range |
|------|-------------|-------------|
| `num` | 8-bit unsigned integer | 0–255 (wraps on overflow) |
| `text` | String literal | Experimental, parse-only |
| `list` | List of values | Experimental, parse-only |

### Assignment

Variables can be reassigned after declaration:

```xbasic
num x = 10
x = x + 5
```

---

## Operators

### Arithmetic

| Operator | Description | Example | Hardware Support |
|----------|-------------|---------|-----------------|
| `+` | Addition | `x + 5` | ✅ ALU ADD |
| `-` | Subtraction | `x - 3` | ✅ ALU SUB |
| `*` | Multiplication | `x * 2` | ⚠️ No hardware mul |
| `/` | Division | `x / 4` | ⚠️ No hardware div |

### Comparison

All comparisons use the CPU's `cmp` instruction and flag-based conditional jumps:

| Operator | Description | CPU Flags Used |
|----------|-------------|----------------|
| `==` | Equal | Zero flag |
| `!=` | Not equal | Zero flag (inverted) |
| `>` | Greater than | Zero + Carry flags |
| `<` | Less than | Carry flag |
| `>=` | Greater or equal | Carry flag (inverted) |
| `<=` | Less or equal | Zero + Carry flags |

Example:
```xbasic
num x = 5
num y = 10
IF x < y THEN
    PRINT 1
END
```

---

## Control Flow

### IF / ELIF / ELSE

```xbasic
IF condition THEN
    # executed if condition is true
ELIF condition THEN
    # executed if first condition was false, this one true
ELSE
    # executed if all conditions were false
END
```

Full example:
```xbasic
num score = 85

IF score >= 90 THEN
    PRINT 1
ELIF score >= 80 THEN
    PRINT 2
ELIF score >= 70 THEN
    PRINT 3
ELSE
    PRINT 0
END
```

### FOR Loops

```xbasic
FOR variable = start TO end THEN
    # loop body
END
```

The loop variable increments by 1 each iteration, from `start` up to (but not including) `end`.

```xbasic
num sum = 0
FOR i = 1 TO 6 THEN
    sum = sum + i
END
PRINT sum
# Output: 15 (1+2+3+4+5)
```

Alternative syntax with `NEXT`:
```xbasic
FOR i = 1 TO 5
    PRINT i
NEXT
```

### WHILE Loops

```xbasic
WHILE condition
    # loop body
END
```

Example:
```xbasic
num x = 1
WHILE x < 10
    PRINT x
    x = x + 1
END
```

---

## Functions

### Definition

Functions are declared with `FN`, accept parameters, and can return values:

```xbasic
FN functionName(param1, param2)
    # function body
    RETURN result
END
```

### Calling Functions

```xbasic
num result = myFunction(arg1, arg2)
```

### Complete Example

```xbasic
FN double(n)
    RETURN n + n
END

num val = 10
num res = double(val)
PRINT res
# Output: 20
```

### Function with Conditional Logic

```xbasic
FN classify(score)
    IF score >= 90 THEN
        RETURN 1
    ELIF score >= 70 THEN
        RETURN 2
    ELSE
        RETURN 0
    END
END

PRINT classify(85)
# Output: 2
```

### Limitations

| Constraint | Detail |
|-----------|--------|
| Max parameters | 2 (passed via registers A and B) |
| Scope | Global only (no local variables) |
| Recursion | Not supported (global variable conflicts) |

---

## Output

The `PRINT` statement outputs a value to the CPU's I/O port:

```xbasic
PRINT 42
PRINT(x + 5)
```

Both syntaxes are valid. Output appears as decimal values in the simulator.

---

## Formal Grammar

```text
program        → (declaration | function | statement)* EOF

declaration    → ("num" | "text" | "list") IDENTIFIER ["=" expression]

function       → "FN" IDENTIFIER "(" [params] ")" body "END"
params         → IDENTIFIER ("," IDENTIFIER)*
body           → statement*

statement      → if_stmt | for_stmt | while_stmt | print_stmt
               | return_stmt | assignment

if_stmt        → "IF" expression "THEN" body
                 ("ELIF" expression "THEN" body)*
                 ["ELSE" body]
                 "END"

for_stmt       → "FOR" IDENTIFIER "=" expression "TO" expression ["THEN"]
                 body ("END" | "NEXT")

while_stmt     → "WHILE" expression body "END"

print_stmt     → "PRINT" ["("] expression [")"]

return_stmt    → "RETURN" expression

assignment     → IDENTIFIER "=" expression

expression     → term (("+"|"-"|"=="|"!="|">"|"<"|">="|"<=") term)*

term           → factor (("*"|"/") factor)*

factor         → NUMBER | STRING | IDENTIFIER ["(" [args] ")"]
               | "(" expression ")" | "[" [list_items] "]"

args           → expression ("," expression)*
list_items     → expression ("," expression)*
```
