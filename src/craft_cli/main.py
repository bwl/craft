"""
Main entry point for Craft CLI Framework
"""
import sys
from pathlib import Path
from .core import CraftCLI


def find_domains_dir() -> Path:
    """Find domains directory, checking multiple locations"""
    # First check if we're in a project that has a domains/ directory
    current = Path.cwd()
    while current != current.parent:
        domains_dir = current / "domains"
        if domains_dir.exists():
            return current
        current = current.parent
    
    # Fall back to package location
    package_dir = Path(__file__).parent
    return package_dir.parent.parent


def main() -> int:
    """Main CLI entry point"""
    # Find the base path for domains
    base_path = find_domains_dir()
    cli = CraftCLI(base_path)
    
    # Check for version flag
    if len(sys.argv) > 1 and sys.argv[1] in ["--version", "-v"]:
        cli.show_version()
        return 0
    
    # Check for --noob flag anywhere in args
    human_mode = "--noob" in sys.argv
    if human_mode:
        sys.argv = [arg for arg in sys.argv if arg != "--noob"]
    
    if len(sys.argv) == 1 or sys.argv[1] == "--help":
        cli.show_help(human_mode)
        return 0
    
    if sys.argv[1] == "--domains":
        cli.list_domains(human_mode)
        return 0
    
    if len(sys.argv) == 2:
        # craft <domain> - list domain tools
        success = cli.list_domain_tools(sys.argv[1], human_mode)
        return 0 if success else 1
    
    if len(sys.argv) >= 3:
        domain = sys.argv[1]
        tool = sys.argv[2]
        
        # Check for help flag
        if len(sys.argv) > 3 and sys.argv[3] in ["--help", "-h"]:
            cli.show_tool_help(domain, tool, human_mode)
            return 0  # Help should always return success, even for non-existent tools
        
        # Run the tool
        args = sys.argv[3:] if len(sys.argv) > 3 else []
        return cli.run_tool(domain, tool, args)
    
    cli.show_help(human_mode)
    return 0


if __name__ == "__main__":
    sys.exit(main())