# Craft CLI Framework

**Domain-specific tool orchestration made simple**

[![PyPI version](https://badge.fury.io/py/craft-cli.svg)](https://badge.fury.io/py/craft-cli)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Craft CLI transforms specialized tools into system-tool-like experiences that feel natural and get consistently used. Perfect for AI agent workflows where domain-specific tools need to integrate seamlessly with command-line operations.

## The Problem

Domain-specific tools often have great functionality but poor adoption because they:
- Feel like "extra steps" outside normal workflow  
- Are easy to forget when focused on other tasks
- Lack integration with existing command-line habits
- Don't provide immediate feedback and guidance

## The Solution

Craft CLI makes domain tools feel like system commands (`git`, `npm`, `docker`) by providing:

- **Natural CLI integration** - `craft linting ruff check --fix`
- **Rich feedback** - Beautiful tables and panels using Rich library
- **Contextual help** - `craft linting ruff --help` shows tool-specific guidance
- **Tool discovery** - `craft linting` lists all available tools in domain
- **AI-optimized output** - Clean, parseable default output for agents
- **Human-friendly mode** - `--noob` flag for Rich UI when humans need it

## Quick Start

### Installation

```bash
# Install from PyPI
uv tool install craft-cli

# Or with pip
pip install craft-cli
```

### Basic Usage

```bash
# Show help
craft --help

# List available domains  
craft --domains

# List tools in a domain
craft linting

# Run a tool
craft linting ruff check --fix

# Get tool-specific help
craft linting ruff --help

# Use human-friendly Rich UI
craft linting --noob
```

## Built-in Domains

### 🎯 Linting - Python Code Quality
```bash
craft linting ruff check --fix        # Fast Rust-based linter
craft linting black .                 # Code formatting
craft linting mypy src/               # Type checking
```

### 🛠️ Coding - Development Workflow  
```bash
craft coding test --coverage          # Run tests with coverage
craft coding build sync --dev         # UV package management
craft coding git status               # Git workflow shortcuts
```

### ✍️ SLATE - Novel Writing (Example)
```bash
craft slate namer character --type=protagonist
craft slate embark "New Series" --genre=fantasy
```

## Key Features

### 🤖 AI-Optimized by Default
```bash
$ craft linting
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

### 👤 Human-Friendly Rich UI (--noob flag)
Beautiful tables, panels, and colors when humans need visual interface:

```bash
craft linting --noob
```

## Creating Custom Domains

### 1. Create Domain Structure
```bash
mkdir -p domains/mytools/tools
```

### 2. Domain Configuration
```yaml
# domains/mytools/config.yaml
name: "My Custom Tools"
description: "Tools for my specific workflow"
base_path: "/path/to/my/scripts"
```

### 3. Add Tools
```yaml
# domains/mytools/tools/mytool.yaml
name: "MYTOOL"
description: "What my tool does"
command: "python {base_path}/mytool.py {args}"
help: |
  Usage: craft mytools mytool [options]
  Examples:
    craft mytools mytool --option=value
```

### 4. Use Your Domain
```bash
craft mytools                    # List your tools
craft mytools mytool --help      # Tool help
craft mytools mytool --verbose   # Run your tool
```

## Architecture

### Simple File Structure
```
domains/
├── linting/
│   ├── config.yaml
│   └── tools/
│       ├── ruff.yaml
│       ├── black.yaml
│       └── mypy.yaml
├── coding/
│   ├── config.yaml
│   └── tools/
│       ├── test.yaml
│       ├── build.yaml
│       └── git.yaml
└── mytools/
    ├── config.yaml
    └── tools/
        └── mytool.yaml
```

### Tool Definition Format
```yaml
name: "TOOL-NAME"
description: "Brief description"
command: "actual-command {args}"
category: "tool_category"
help: |
  Detailed help text with usage examples
```

## Advanced Usage

### Environment Integration
Craft CLI automatically finds domain directories in:
1. Current working directory
2. Parent directories (walks up the tree)
3. Package installation location

### Command Patterns
```bash
craft <domain>                    # List domain tools
craft <domain> <tool> [args]      # Run tool with arguments
craft <domain> <tool> --help      # Tool-specific help
craft --domains                   # List all domains
craft --help [--noob]            # Framework help
craft --version                   # Show version
```

### Flags
- `--noob` - Enable Rich UI (tables, panels, colors)
- `--verbose` - Show command being executed
- `--help` - Context-sensitive help

## Why Craft CLI?

### For AI Agents
- **Clean, parseable output** by default
- **Consistent interface** across all domain tools
- **Natural command patterns** that integrate with existing workflows
- **Immediate feedback** that can't be ignored or forgotten

### For Humans  
- **Rich UI option** with beautiful tables and panels
- **Tool discovery** through natural exploration
- **Contextual help** exactly when and where needed
- **Consistent patterns** across different tool domains

### For Teams
- **Standardized tooling** across projects and developers
- **Easy onboarding** - one pattern to learn, all tools accessible
- **Extensible architecture** - add new domains without changing framework
- **Documentation built-in** - help and usage examples embedded in tool definitions

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Adding New Domains
1. Create domain directory structure
2. Add domain config and tool definitions  
3. Test with `craft your-domain`
4. Submit pull request with documentation

### Reporting Issues
- [GitHub Issues](https://github.com/slate-tui/craft-cli/issues) for bugs and feature requests
- Include domain, tool, and command that caused the issue
- Provide expected vs actual behavior

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- **Documentation**: https://craft-cli.readthedocs.io
- **PyPI Package**: https://pypi.org/project/craft-cli/
- **Source Code**: https://github.com/slate-tui/craft-cli
- **Issue Tracker**: https://github.com/slate-tui/craft-cli/issues

---

*Built with ❤️ for AI agents and human developers who want their specialized tools to feel like system commands.*