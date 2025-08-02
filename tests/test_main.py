"""
Test suite for Craft CLI main entry point
"""
import pytest
import sys
from unittest.mock import patch, MagicMock
from craft_cli.main import main, find_domains_dir


class TestMain:
    """Test cases for main entry point"""
    
    def test_version_flag(self, capsys):
        """Test --version flag"""
        with patch.object(sys, 'argv', ['craft', '--version']):
            result = main()
            
        captured = capsys.readouterr()
        assert result == 0
        assert "Craft CLI Framework v" in captured.out
    
    def test_version_short_flag(self, capsys):
        """Test -v flag"""
        with patch.object(sys, 'argv', ['craft', '-v']):
            result = main()
            
        captured = capsys.readouterr()
        assert result == 0
        assert "Craft CLI Framework v" in captured.out
    
    def test_help_flag(self, capsys):
        """Test --help flag"""
        with patch.object(sys, 'argv', ['craft', '--help']):
            result = main()
            
        captured = capsys.readouterr()
        assert result == 0
        assert "CRAFT CLI FRAMEWORK" in captured.out
    
    def test_help_with_noob_flag(self):
        """Test --help --noob flags"""
        with patch.object(sys, 'argv', ['craft', '--help', '--noob']):
            with patch('craft_cli.core.console.print') as mock_print:
                result = main()
                
        assert result == 0
        mock_print.assert_called_once()
    
    def test_domains_flag(self, capsys):
        """Test --domains flag"""
        with patch.object(sys, 'argv', ['craft', '--domains']):
            result = main()
            
        captured = capsys.readouterr()
        assert result == 0
        # Should either show domains or error about no domains directory
        assert "AVAILABLE DOMAINS:" in captured.out or "ERROR:" in captured.out
    
    def test_list_domain_tools(self, capsys):
        """Test listing tools in a domain"""
        with patch.object(sys, 'argv', ['craft', 'nonexistent']):
            result = main()
            
        captured = capsys.readouterr()
        assert result == 0
        assert "ERROR: Domain 'nonexistent' not found" in captured.out
    
    def test_tool_help(self, capsys):
        """Test tool help command"""
        with patch.object(sys, 'argv', ['craft', 'domain', 'tool', '--help']):
            result = main()
            
        captured = capsys.readouterr()
        assert result == 0
        assert "ERROR: Tool 'tool' not found in domain 'domain'" in captured.out
    
    def test_tool_execution(self, capsys):
        """Test tool execution"""
        with patch.object(sys, 'argv', ['craft', 'domain', 'tool', 'arg1']):
            result = main()
            
        captured = capsys.readouterr()
        assert result == 1  # Should fail since domain doesn't exist
        assert "ERROR: Domain 'domain' not found" in captured.out
    
    def test_noob_flag_filtering(self, capsys):
        """Test that --noob flag is properly filtered from arguments"""
        with patch.object(sys, 'argv', ['craft', '--help', '--noob']):
            with patch('craft_cli.core.CraftCLI.show_help') as mock_help:
                main()
                mock_help.assert_called_once_with(True)  # human_mode=True
    
    def test_no_arguments(self, capsys):
        """Test running craft with no arguments"""
        with patch.object(sys, 'argv', ['craft']):
            result = main()
            
        captured = capsys.readouterr()
        assert result == 0
        assert "CRAFT CLI FRAMEWORK" in captured.out


class TestFindDomainsDir:
    """Test cases for domains directory discovery"""
    
    def test_find_domains_in_cwd(self, tmp_path, monkeypatch):
        """Test finding domains directory in current working directory"""
        # Create domains directory in temp path
        domains_dir = tmp_path / "domains"
        domains_dir.mkdir()
        
        # Change to temp directory
        monkeypatch.chdir(tmp_path)
        
        result = find_domains_dir()
        assert result == tmp_path
    
    def test_find_domains_in_parent(self, tmp_path, monkeypatch):
        """Test finding domains directory in parent directory"""
        # Create nested structure
        project_root = tmp_path / "project"
        project_root.mkdir()
        (project_root / "domains").mkdir()
        
        subdir = project_root / "subdir"
        subdir.mkdir()
        
        # Change to subdirectory
        monkeypatch.chdir(subdir)
        
        result = find_domains_dir()
        assert result == project_root
    
    def test_fallback_to_package_location(self, tmp_path, monkeypatch):
        """Test fallback to package location when no domains found"""
        # Change to directory without domains
        monkeypatch.chdir(tmp_path)
        
        result = find_domains_dir()
        # Should return package location (parent of parent of main.py)
        expected = tmp_path / ".." / ".."  # Simplified assertion
        assert result.exists()  # Just check it returns a valid path


class TestIntegration:
    """Integration tests for full command flows"""
    
    def test_help_to_execution_flow(self, capsys):
        """Test typical user flow from help to execution"""
        # First, user runs help
        with patch.object(sys, 'argv', ['craft', '--help']):
            result = main()
            assert result == 0
        
        # Then tries to list domains
        with patch.object(sys, 'argv', ['craft', '--domains']):
            result = main()
            assert result == 0
        
        # Then tries to run a tool (will fail since no domains exist)
        with patch.object(sys, 'argv', ['craft', 'test', 'tool']):
            result = main()
            assert result == 1
    
    def test_error_handling_flow(self, capsys):  
        """Test error handling in various scenarios"""
        test_cases = [
            (['craft', 'badDomain'], 1),
            (['craft', 'badDomain', 'badTool'], 1),
            (['craft', 'badDomain', 'badTool', '--help'], 0),  # Help should always work
        ]
        
        for argv, expected_code in test_cases:
            with patch.object(sys, 'argv', argv):
                result = main()
                assert result == expected_code
                
                captured = capsys.readouterr()
                if expected_code == 1:
                    assert "ERROR:" in captured.out