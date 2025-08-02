# Craft CLI Usage

This document provides a comprehensive overview of the Craft CLI framework, demonstrating its core functionalities and showcasing both the AI-optimized and human-friendly interfaces.

## Table of Contents

- [Framework Help](#framework-help)
- [List Domains](#list-domains)
- [List Tools in a Domain](#list-tools-in-a-domain)
- [Tool-Specific Help](#tool-specific-help)

---

## Framework Help

The `--help` flag displays general help information for the Craft CLI framework.

### AI-Optimized Output

This output is clean, simple, and easily parsable, making it ideal for scripting and AI agent consumption.

```text
CRAFT CLI FRAMEWORK
Usage: craft <domain> <tool> [args]
       craft <domain>  (list domain tools)
       craft --help [--noob]  (show help)

Examples:
  craft linting ruff check --fix
  craft coding test --coverage
  craft slate namer character --type=protagonist

Add --noob flag for human-friendly Rich UI interface
```

### Human-Friendly Output

The `--noob` flag provides a visually appealing, human-readable output using the Rich library.

```text
╭──────────────────────────────── 🔨 Craft CLI ────────────────────────────────╮
│ Craft CLI Framework                                                          │
│                                                                              │
│ Domain-specific tool orchestration                                           │
│                                                                              │
│ Usage:                                                                       │
│   craft <domain> <tool>      Run a tool                                      │
│   craft <domain>                   List domain tools                         │
│   craft --help                     Show this help                            │
│   craft --help --noob              Show pretty human interface               │
│                                                                              │
│ Examples:                                                                    │
│   craft linting ruff check --fix                                             │
│   craft coding test --coverage                                               │
│   craft slate namer character --type=protagonist                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

## List Domains

The `--domains` flag lists all available domains.

### AI-Optimized Output

```text
AVAILABLE DOMAINS:
  linting: 3 tools - Linting, formatting, and code quality tools for Python development
  slate: 2 tools - Specialized tools for fiction writers and TUI development
  coding: 3 tools - Essential development tools for testing, building, and project management

Use: craft <domain> to list domain tools
Add --noob flag for Rich UI tables
```

### Human-Friendly Output

```text
                                Available Domains                                
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Domain  ┃ Description                                                ┃ Tools ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ linting │ Linting, formatting, and code quality tools for Python     │     3 │
│         │ development                                                │       │
│ slate   │ Specialized tools for fiction writers and TUI development  │     2 │
│ coding  │ Essential development tools for testing, building, and     │     3 │
│         │ project management                                         │       │
└─────────┴────────────────────────────────────────────────────────────┴───────┘
```

---

## List Tools in a Domain

To list the tools available within a specific domain, use the command `craft <domain>`.

### AI-Optimized Output (`craft linting`)

```text
PYTHON CODE QUALITY TOOLS TOOLS:
  RUFF: Fast Python linter and code formatter, written in Rust
    Usage: craft linting ruff check .
  BLACK: The uncompromising Python code formatter
    Usage: craft linting black .
  MYPY: Static type checker for Python
    Usage: craft linting mypy src/

Use: craft linting <tool> --help for tool-specific help
Add --noob flag for Rich UI tables
```

### Human-Friendly Output (`craft linting --noob`)

```text
                         Python Code Quality Tools Tools                         
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Tool  ┃ Description                             ┃ Usage                      ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ruff  │ Fast Python linter and code formatter,  │ craft linting ruff check . │
│       │ written in Rust                         │                            │
│ black │ The uncompromising Python code          │ craft linting black .      │
│       │ formatter                               │                            │
│ mypy  │ Static type checker for Python          │ craft linting mypy src/    │
└───────┴─────────────────────────────────────────┴────────────────────────────┘
```

---

## Tool-Specific Help

To get help for a specific tool, use the command `craft <domain> <tool> --help`.

### AI-Optimized Output (`craft linting ruff --help`)

```text
RUFF
Description: Fast Python linter and code formatter, written in Rust

Ultra-fast Python linter and formatter for code quality enforcement.

Usage: craft linting ruff <action> [options]

Actions:
  check           Run linting checks on Python files
  format          Format Python code according to style rules
  --fix           Automatically fix auto-fixable lint violations
  --watch         Run in watch mode for continuous checking
  
Options:
  --select=RULES  Select specific rule codes to check
  --ignore=RULES  Ignore specific rule codes  
  --config=FILE   Use specific configuration file
  --verbose       Show verbose output
  --quiet         Minimize output
  
Examples:
  craft linting ruff check .
  craft linting ruff check --fix src/
  craft linting ruff format --diff
  craft linting ruff check --select=E,W --ignore=E203

Add --noob flag for Rich UI panel
```

### Human-Friendly Output (`craft linting ruff --help --noob`)

```text
╭────────────────────────────────── 🔧 ruff ───────────────────────────────────╮
│ RUFF                                                                         │
│ Fast Python linter and code formatter, written in Rust                       │
│                                                                              │
│ Ultra-fast Python linter and formatter for code quality enforcement.         │
│                                                                              │
│ Usage: craft linting ruff <action>                                           │
│                                                                              │
│ Actions:                                                                     │
│   check           Run linting checks on Python files                         │
│   format          Format Python code according to style rules                │
│   --fix           Automatically fix auto-fixable lint violations             │
│   --watch         Run in watch mode for continuous checking                  │
│                                                                              │
│ Options:                                                                     │
│   --select=RULES  Select specific rule codes to check                        │
│   --ignore=RULES  Ignore specific rule codes                                 │
│   --config=FILE   Use specific configuration file                            │
│   --verbose       Show verbose output                                        │
│   --quiet         Minimize output                                            │
│                                                                              │
│ Examples:                                                                    │
│   craft linting ruff check .                                                 │
│   craft linting ruff check --fix src/                                        │
│   craft linting ruff format --diff                                           │
│   craft linting ruff check --select=E,W --ignore=E203                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```