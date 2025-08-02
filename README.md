# 🚀 Craft CLI Framework

*Trick Gemini into being actually useful*

> ⚠️ **Friendly Disclaimer**: Most of the features promised below exist but some um... we will get back to you soon, dw 😅

## Fire Up Specialized Agents for Any Task

[![PyPI version](https://badge.fury.io/py/craft-cli.svg)](https://badge.fury.io/py/craft-cli)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Transform any specialized workflow into intelligent, agent-ready commands.**

Stop context-switching between tools. Stop explaining your domain knowledge over and over. **Craft CLI lets you deploy domain experts instantly** - whether that's a coding specialist, a linting expert, or a creative writing assistant.

Every `craft` command is really saying: *"Hey, someone smart who understands this domain - handle this for me."*

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

### 🎯 Linting - Deploy a Code Quality Expert
```bash
craft linting ruff check --fix        # "Fix all the issues you find"
craft linting black .                 # "Format this code properly"
craft linting mypy src/               # "Check types thoroughly"
```

### 🛠️ Coding - Fire Up a Development Specialist  
```bash
craft coding test --coverage          # "Run comprehensive tests"
craft coding build sync --dev         # "Handle my dependencies"
craft coding git status               # "Show me what's changed"
```

### ✍️ SLATE - Summon a Creative Writing Assistant
```bash
craft slate namer character --type=protagonist    # "Generate perfect character names"
craft slate embark "New Series" --genre=fantasy   # "Set up my novel project"
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

### 🤖 For AI Agents - Deploy Domain Experts Instantly
- **Clean, parseable output** - No fluff, just actionable results
- **Domain expertise on-demand** - Every command taps specialized knowledge
- **Natural integration** - Works with existing agent workflows seamlessly  
- **Zero context-switching** - The tool understands your domain

### 👤 For Humans - Access Specialists Without the Overhead
- **Rich UI option** - Beautiful tables and panels when you need them
- **Instant expertise** - No need to remember complex tool syntax
- **Self-documenting** - Help and examples built into every command
- **Consistent patterns** - Learn once, use everywhere

### 🏢 For Teams - Standardize Your Specialist Tools
- **Unified interface** - All domain tools follow the same patterns
- **Easy onboarding** - New team members get productive immediately  
- **Extensible architecture** - Add new domains without changing the framework
- **Built-in documentation** - Every tool comes with usage examples

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