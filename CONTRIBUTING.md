# Contributing to Craft CLI Framework

We welcome contributions! This guide will help you get started.

## Development Setup

### Prerequisites
- Python 3.8+
- UV package manager
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/slate-tui/craft-cli.git
cd craft-cli

# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Run the CLI locally
uv run craft --version
```

## Contributing Guidelines

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write comprehensive docstrings
- Maintain test coverage above 80%

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=craft_cli --cov-report=html

# Run specific test files
uv run pytest tests/test_core.py
```

### Code Formatting
```bash
# Format code
uv run black src/ tests/

# Check formatting
uv run black --check src/ tests/

# Run linting
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

## Adding New Domains

### 1. Create Domain Structure
```bash
mkdir -p domains/your-domain/tools
```

### 2. Domain Configuration
```yaml
# domains/your-domain/config.yaml
name: "Your Domain Name"
description: "Brief description of your domain"
version: "1.0.0"
base_path: "."
author: "Your Name"
```

### 3. Add Tools
```yaml
# domains/your-domain/tools/your-tool.yaml
name: "YOUR-TOOL"
description: "What your tool does"
command: "your-command {args}"
category: "tool_category"
help: |
  Detailed help text with usage examples
  
  Usage: craft your-domain your-tool [options]
  
  Examples:
    craft your-domain your-tool --option=value
```

### 4. Test Your Domain
```bash
# Test locally
uv run craft your-domain
uv run craft your-domain your-tool --help
```

### 5. Add Tests
```python
# tests/test_your_domain.py
def test_your_domain_tools():
    """Test your domain tools work correctly"""
    # Add comprehensive tests
    pass
```

## Pull Request Process

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write code following the guidelines above
- Add/update tests
- Update documentation if needed

### 3. Test Thoroughly
```bash
# Run full test suite
uv run pytest

# Test your changes manually
uv run craft your-domain your-tool
```

### 4. Commit Changes
```bash
git add .
git commit -m "Add: Brief description of changes"
```

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Link to any related issues
- Screenshots if UI changes
- Test results

## Types of Contributions

### 🔧 New Domains
Add tool domains for specific workflows:
- Development tools (testing, building, deployment)
- Content creation (writing, design, media)
- System administration (monitoring, backup, security)
- Data science (analysis, visualization, ML)

### 🐛 Bug Fixes
- Fix existing functionality
- Improve error handling
- Performance improvements

### 📚 Documentation
- Improve README and guides
- Add usage examples
- Create domain-specific documentation

### ✨ Features
- Enhance CLI interface
- Add new framework capabilities
- Improve user experience

## Domain Guidelines

### Good Domain Examples
- **linting**: Python code quality tools (ruff, black, mypy)
- **coding**: Development workflow (test, build, git)
- **deploy**: Deployment tools (docker, kubernetes, terraform)
- **docs**: Documentation tools (sphinx, mkdocs, pandoc)

### Domain Best Practices
1. **Focused scope**: Each domain should have a clear, specific purpose
2. **Consistent naming**: Use clear, descriptive names for tools
3. **Good help text**: Provide comprehensive usage examples
4. **Command compatibility**: Ensure commands work across platforms
5. **Error handling**: Provide clear error messages

### Tool Configuration Best Practices
- Use `{args}` placeholder for tool arguments
- Include comprehensive help text with examples
- Choose appropriate command templates
- Test commands work in isolation

## Release Process

### Version Numbering
We use semantic versioning (semver):
- `1.0.0` - Major version (breaking changes)
- `1.1.0` - Minor version (new features)
- `1.1.1` - Patch version (bug fixes)

### Release Steps
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release tag
4. Publish to PyPI via GitHub Actions

## Getting Help

### Questions
- Create GitHub Discussion for questions
- Tag maintainers in PRs if needed
- Check existing issues and PRs

### Reporting Bugs
- Use GitHub Issues
- Include reproduction steps
- Provide system information
- Include error messages/logs

### Feature Requests
- Create GitHub Issue with "enhancement" label
- Describe the use case
- Explain expected behavior
- Consider creating a draft PR

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers get started
- Maintain professional communication

## Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to Craft CLI Framework! 🎉