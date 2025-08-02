"""
Test suite for Craft CLI Framework core functionality
"""
import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock
from craft_cli.core import CraftCLI


@pytest.fixture
def temp_project():
    """Create a temporary project structure for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create domains directory
        domains_dir = temp_path / "domains"
        domains_dir.mkdir()
        
        # Create test domain
        test_domain = domains_dir / "test"
        test_domain.mkdir()
        
        # Create domain config
        domain_config = {
            "name": "Test Domain",
            "description": "Test domain for unit tests",
            "base_path": str(temp_path)
        }
        (test_domain / "config.yaml").write_text(yaml.dump(domain_config))
        
        # Create tools directory and test tool
        tools_dir = test_domain / "tools"
        tools_dir.mkdir()
        
        tool_config = {
            "name": "TEST-TOOL",
            "description": "A test tool",
            "command": "echo {args}",
            "help": "Usage: craft test testtool [args]"
        }
        (tools_dir / "testtool.yaml").write_text(yaml.dump(tool_config))
        
        yield temp_path


class TestCraftCLI:
    """Test cases for CraftCLI class"""
    
    def test_initialization(self, temp_project):
        """Test CraftCLI initialization"""
        cli = CraftCLI(temp_project)
        assert cli.base_path == temp_project
        assert cli.domains_dir == temp_project / "domains"
    
    def test_show_version(self, capsys):
        """Test version display"""
        cli = CraftCLI()
        cli.show_version()
        
        captured = capsys.readouterr()
        assert "Craft CLI Framework v" in captured.out
        assert "Domain-specific tool orchestration" in captured.out
    
    def test_show_help_ai_mode(self, capsys):
        """Test help display in AI mode (default)"""
        cli = CraftCLI()
        cli.show_help(human_mode=False)
        
        captured = capsys.readouterr()
        assert "CRAFT CLI FRAMEWORK" in captured.out
        assert "Usage: craft <domain> <tool> [args]" in captured.out
        assert "--noob flag" in captured.out
    
    def test_show_help_human_mode(self, temp_project):
        """Test help display in human mode"""
        cli = CraftCLI(temp_project)
        
        # Mock console.print to capture Rich output
        with patch('craft_cli.core.console.print') as mock_print:
            cli.show_help(human_mode=True)
            mock_print.assert_called_once()
            # Verify it's a Panel object
            panel_arg = mock_print.call_args[0][0]
            assert hasattr(panel_arg, 'title')
    
    def test_list_domains_ai_mode(self, temp_project, capsys):
        """Test domain listing in AI mode"""
        cli = CraftCLI(temp_project)
        cli.list_domains(human_mode=False)
        
        captured = capsys.readouterr()
        assert "AVAILABLE DOMAINS:" in captured.out
        assert "test: 1 tools - Test domain for unit tests" in captured.out
    
    def test_list_domains_human_mode(self, temp_project):
        """Test domain listing in human mode"""
        cli = CraftCLI(temp_project)
        
        with patch('craft_cli.core.console.print') as mock_print:
            cli.list_domains(human_mode=True)
            mock_print.assert_called_once()
            # Verify it's a Table object
            table_arg = mock_print.call_args[0][0]
            assert hasattr(table_arg, 'title')
    
    def test_list_domain_tools_ai_mode(self, temp_project, capsys):
        """Test tool listing in AI mode"""
        cli = CraftCLI(temp_project)
        cli.list_domain_tools("test", human_mode=False)
        
        captured = capsys.readouterr()
        assert "TEST DOMAIN TOOLS:" in captured.out
        assert "TEST-TOOL: A test tool" in captured.out
    
    def test_list_domain_tools_human_mode(self, temp_project):
        """Test tool listing in human mode"""
        cli = CraftCLI(temp_project)
        
        with patch('craft_cli.core.console.print') as mock_print:
            cli.list_domain_tools("test", human_mode=True)
            mock_print.assert_called_once()
    
    def test_show_tool_help_ai_mode(self, temp_project, capsys):
        """Test tool help in AI mode"""
        cli = CraftCLI(temp_project)
        cli.show_tool_help("test", "testtool", human_mode=False)
        
        captured = capsys.readouterr()
        assert "TEST-TOOL" in captured.out
        assert "A test tool" in captured.out
        assert "Usage: craft test testtool [args]" in captured.out
    
    def test_show_tool_help_human_mode(self, temp_project):
        """Test tool help in human mode"""
        cli = CraftCLI(temp_project)
        
        with patch('craft_cli.core.console.print') as mock_print:
            cli.show_tool_help("test", "testtool", human_mode=True)
            mock_print.assert_called_once()
    
    def test_run_tool_success(self, temp_project):
        """Test successful tool execution"""
        cli = CraftCLI(temp_project)
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            result = cli.run_tool("test", "testtool", ["arg1", "arg2"])
            
            assert result == 0
            mock_run.assert_called_once()
            # Verify command was properly formatted
            call_args = mock_run.call_args
            assert "echo arg1 arg2" in call_args[0][0]
    
    def test_run_tool_failure(self, temp_project):
        """Test tool execution failure"""
        cli = CraftCLI(temp_project)
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            result = cli.run_tool("test", "testtool", [])
            
            assert result == 1
    
    def test_run_nonexistent_domain(self, temp_project, capsys):
        """Test running tool in nonexistent domain"""
        cli = CraftCLI(temp_project)
        result = cli.run_tool("nonexistent", "tool", [])
        
        captured = capsys.readouterr()
        assert result == 1
        assert "ERROR: Domain 'nonexistent' not found" in captured.out
    
    def test_run_nonexistent_tool(self, temp_project, capsys):
        """Test running nonexistent tool in valid domain"""
        cli = CraftCLI(temp_project)
        result = cli.run_tool("test", "nonexistent", [])
        
        captured = capsys.readouterr()
        assert result == 1
        assert "ERROR: Tool 'nonexistent' not found in domain 'test'" in captured.out
    
    def test_keyboard_interrupt_handling(self, temp_project, capsys):
        """Test handling of keyboard interrupt during tool execution"""
        cli = CraftCLI(temp_project)
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = KeyboardInterrupt()
            result = cli.run_tool("test", "testtool", [])
            
            captured = capsys.readouterr()
            assert result == 1
            assert "Interrupted" in captured.out
    
    def test_exception_handling(self, temp_project, capsys):
        """Test handling of general exceptions during tool execution"""
        cli = CraftCLI(temp_project)
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Test error")
            result = cli.run_tool("test", "testtool", [])
            
            captured = capsys.readouterr()
            assert result == 1
            assert "ERROR: Test error" in captured.out


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_no_domains_directory(self, capsys):
        """Test behavior when domains directory doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cli = CraftCLI(Path(temp_dir))
            cli.list_domains()
            
            captured = capsys.readouterr()
            assert "ERROR: No domains directory found" in captured.out
    
    def test_domain_without_config(self, temp_project, capsys):
        """Test domain listing with missing config file"""
        # Create domain without config file
        (temp_project / "domains" / "noconfig").mkdir()
        (temp_project / "domains" / "noconfig" / "tools").mkdir()
        
        cli = CraftCLI(temp_project)
        cli.list_domains(human_mode=False)
        
        captured = capsys.readouterr()
        assert "noconfig:" in captured.out
        assert "No config found" in captured.out
    
    def test_tool_without_command(self, temp_project, capsys):
        """Test tool execution when command is missing"""
        # Create tool config without command
        tools_dir = temp_project / "domains" / "test" / "tools"
        broken_tool = {
            "name": "BROKEN",
            "description": "Tool without command"
        }
        (tools_dir / "broken.yaml").write_text(yaml.dump(broken_tool))
        
        cli = CraftCLI(temp_project)
        result = cli.run_tool("test", "broken", [])
        
        captured = capsys.readouterr()
        assert result == 1
        assert "ERROR: No command defined for tool 'broken'" in captured.out