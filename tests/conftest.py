"""
Test configuration and fixtures for Craft CLI Framework
"""
import pytest
import tempfile
import yaml
from pathlib import Path


@pytest.fixture
def mock_domains_project():
    """Create a complete mock project with multiple domains for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create domains directory
        domains_dir = temp_path / "domains"
        domains_dir.mkdir()
        
        # Create multiple test domains
        domains = {
            "linting": {
                "config": {
                    "name": "Python Code Quality Tools",
                    "description": "Linting and formatting tools",
                    "base_path": str(temp_path)
                },
                "tools": {
                    "ruff": {
                        "name": "RUFF",
                        "description": "Fast Python linter",
                        "command": "ruff {args}",
                        "help": "Usage: craft linting ruff [options]"
                    },
                    "black": {
                        "name": "BLACK", 
                        "description": "Python code formatter",
                        "command": "black {args}",
                        "help": "Usage: craft linting black [files]"
                    }
                }
            },
            "coding": {
                "config": {
                    "name": "Development Tools",
                    "description": "Development workflow tools",
                    "base_path": str(temp_path)
                },
                "tools": {
                    "test": {
                        "name": "TEST",
                        "description": "Run test suites",
                        "command": "pytest {args}",
                        "help": "Usage: craft coding test [options]"
                    }
                }
            }
        }
        
        # Create domain structures
        for domain_name, domain_data in domains.items():
            domain_dir = domains_dir / domain_name
            domain_dir.mkdir()
            
            # Create config file
            config_file = domain_dir / "config.yaml"
            config_file.write_text(yaml.dump(domain_data["config"]))
            
            # Create tools directory and tool files
            tools_dir = domain_dir / "tools"
            tools_dir.mkdir()
            
            for tool_name, tool_data in domain_data["tools"].items():
                tool_file = tools_dir / f"{tool_name}.yaml"
                tool_file.write_text(yaml.dump(tool_data))
        
        yield temp_path


@pytest.fixture
def empty_project():
    """Create an empty project directory for testing error conditions"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def broken_project():
    """Create a project with broken/invalid configurations for error testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create domains directory
        domains_dir = temp_path / "domains"
        domains_dir.mkdir()
        
        # Create domain with invalid YAML
        broken_domain = domains_dir / "broken"
        broken_domain.mkdir()
        (broken_domain / "config.yaml").write_text("invalid: yaml: content: [")
        
        # Create domain with missing tools directory
        no_tools_domain = domains_dir / "notools"
        no_tools_domain.mkdir()
        (no_tools_domain / "config.yaml").write_text(yaml.dump({
            "name": "No Tools Domain",
            "description": "Domain without tools directory"
        }))
        
        # Create domain with broken tool config
        broken_tools_domain = domains_dir / "brokentools"
        broken_tools_domain.mkdir()
        (broken_tools_domain / "config.yaml").write_text(yaml.dump({
            "name": "Broken Tools Domain", 
            "description": "Domain with broken tool configs"
        }))
        
        tools_dir = broken_tools_domain / "tools"
        tools_dir.mkdir()
        (tools_dir / "broken.yaml").write_text("invalid: yaml: [[[")
        
        yield temp_path


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Custom assertions
def assert_output_contains(capsys, expected_strings):
    """Assert that captured output contains all expected strings"""
    captured = capsys.readouterr()
    output = captured.out + captured.err
    
    for expected in expected_strings:
        assert expected in output, f"Expected '{expected}' not found in output: {output}"


def assert_exit_code(result, expected_code):
    """Assert that the result matches expected exit code"""
    assert result == expected_code, f"Expected exit code {expected_code}, got {result}"