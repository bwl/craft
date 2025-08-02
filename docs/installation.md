# Installation Guide

## Prerequisites

- Python 3.8 or higher
- UV package manager (recommended) or pip

## Installation Methods

### Method 1: UV Tool Install (Recommended)

UV provides the best experience for CLI tools:

```bash
# Install as a UV tool (isolated environment)
uv tool install craft-cli

# Verify installation
craft --version
```

Benefits:
- Isolated environment prevents dependency conflicts
- Easy to update: `uv tool upgrade craft-cli`
- Easy to remove: `uv tool uninstall craft-cli`

### Method 2: pipx (Alternative)

If you prefer pipx for Python CLI tools:

```bash
# Install with pipx
pipx install craft-cli

# Verify installation
craft --version
```

### Method 3: pip (System-wide)

Standard pip installation:

```bash
# Install system-wide (not recommended for CLI tools)
pip install craft-cli

# Verify installation  
craft --version
```

### Method 4: Development Install

For development or local testing:

```bash
# Clone repository
git clone https://github.com/slate-tui/craft-cli.git
cd craft-cli

# Install in development mode
uv sync --dev
uv run craft --version

# Or with pip
pip install -e .
```

## Post-Installation Setup

### Verify Installation

```bash
# Check version
craft --version

# List available domains
craft --domains

# Test a domain
craft linting
```

### Shell Completion (Optional)

Generate shell completions for better CLI experience:

```bash
# For bash
craft --completion bash >> ~/.bashrc

# For zsh  
craft --completion zsh >> ~/.zshrc

# For fish
craft --completion fish >> ~/.config/fish/completions/craft.fish
```

## Troubleshooting

### Command Not Found

If `craft` command is not found after installation:

1. **Check PATH**: Ensure the installation directory is in your PATH
   ```bash
   echo $PATH
   ```

2. **UV Tool Path**: For UV tool installs, ensure UV tools are in PATH:
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Reinstall**: Try reinstalling with verbose output:
   ```bash
   uv tool install craft-cli --verbose
   ```

### Import Errors

If you see Python import errors:

1. **Check Dependencies**: Verify all dependencies are installed:
   ```bash
   uv tool list
   # Should show craft-cli with its dependencies
   ```

2. **Environment Issues**: Try a fresh installation:
   ```bash
   uv tool uninstall craft-cli
   uv tool install craft-cli
   ```

### Permission Errors

If you encounter permission errors:

1. **Use UV Tool**: Avoid system-wide pip installs:
   ```bash
   uv tool install craft-cli
   ```

2. **User Install**: If using pip, install for current user only:
   ```bash
   pip install --user craft-cli
   ```

## Updating

### UV Tool Update
```bash
uv tool upgrade craft-cli
```

### pip Update
```bash
pip install --upgrade craft-cli
```

## Uninstalling

### UV Tool Uninstall
```bash
uv tool uninstall craft-cli
```

### pip Uninstall
```bash
pip uninstall craft-cli
```

## Next Steps

After installation, see:
- [Quick Start Guide](quickstart.md) - Basic usage patterns
- [Domain Guide](domains.md) - Understanding domains and tools
- [Creating Domains](creating-domains.md) - Build your own tool domains