"""
Core Craft CLI Framework functionality
"""
import sys
import yaml
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .config import ConfigManager

console = Console()


class CraftCLI:
    """Main Craft CLI Framework class"""
    
    def __init__(self, base_path: Optional[Path] = None):
        """Initialize Craft CLI
        
        Args:
            base_path: Base path for finding domains directory (legacy, ignored with config system)
        """
        self.config_manager = ConfigManager()
        
        # Check for first-time setup (skip in test environments)
        if (self.config_manager.should_offer_example_config() and 
            not self._is_test_environment()):
            self._offer_example_config()
        
        # Check for domain conflicts and warn user
        conflicts = self.config_manager.check_for_conflicts()
        if conflicts:
            self._show_conflict_warnings(conflicts)
    
    def _is_test_environment(self) -> bool:
        """Check if running in a test environment"""
        import os
        return (
            'pytest' in sys.modules or
            'PYTEST_CURRENT_TEST' in os.environ or
            'TESTING' in os.environ
        )
    
    def _offer_example_config(self) -> None:
        """Offer to create example config for first-time users"""
        print("🚀 Welcome to Craft CLI!")
        print("No configuration found. Would you like to create an example config?")
        print("This will create ~/.config/craft/craftrc with sensible defaults.")
        
        try:
            response = input("Create example config? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                if self.config_manager.create_example_user_config():
                    print(f"✅ Example config created at {self.config_manager.user_config_path}")
                    print("You can edit this file to add your own domain paths.")
                else:
                    print("❌ Failed to create example config")
        except (KeyboardInterrupt, EOFError):
            print("\nSkipping config creation.")
    
    def _show_conflict_warnings(self, conflicts) -> None:
        """Show warnings about domain name conflicts"""
        print("⚠️  Domain name conflicts detected:")
        for domain_name, sources in conflicts:
            print(f"  Domain '{domain_name}' found in multiple locations:")
            for i, source in enumerate(sources):
                precedence = "✓ ACTIVE" if i == 0 else "  (shadowed)"
                print(f"    {precedence}: {source}")
        print("Project-level domains take precedence over user-level and built-in domains.")
        print()
    
    def _get_domain_paths(self) -> List[Path]:
        """Get all domain paths from config manager"""
        return self.config_manager.get_domain_paths()
    
    def _find_domain_by_name(self, domain_name: str) -> Optional[Path]:
        """Find the active domain directory by name (respects precedence)"""
        for domain_path in self._get_domain_paths():
            domain_dir = domain_path / domain_name
            if domain_dir.is_dir():
                return domain_dir
        return None
    
    def show_help(self, human_mode: bool = False) -> None:
        """Display main help information"""
        if human_mode:
            panel = Panel(
                Text.from_markup(
                    "[bold blue]Craft CLI Framework[/bold blue]\n\n"
                    "[dim]Domain-specific tool orchestration[/dim]\n\n"
                    "[bold]Usage:[/bold]\n"
                    "  craft <domain> <tool> [args]     Run a tool\n"
                    "  craft <domain>                   List domain tools\n"
                    "  craft --help                     Show this help\n"
                    "  craft --help --noob              Show pretty human interface\n\n"
                    "[bold]Examples:[/bold]\n"
                    "  craft linting ruff check --fix\n"
                    "  craft coding test --coverage\n"
                    "  craft slate namer character --type=protagonist"
                ),
                title="🔨 Craft CLI",
                border_style="blue"
            )
            console.print(panel)
        else:
            # AI-optimized output
            print("CRAFT CLI FRAMEWORK")
            print("Usage: craft <domain> <tool> [args]")
            print("       craft <domain>  (list domain tools)")
            print("       craft --help [--noob]  (show help)")
            print("")
            print("Examples:")
            print("  craft linting ruff check --fix")
            print("  craft coding test --coverage")
            print("  craft slate namer character --type=protagonist")
            print("")
            print("Add --noob flag for human-friendly Rich UI interface")
    
    def show_version(self) -> None:
        """Show version information"""
        from . import __version__
        print(f"Craft CLI Framework v{__version__}")
        print("Domain-specific tool orchestration")
        print("Built for AI agent workflows")
    
    def list_domains(self, human_mode: bool = False) -> None:
        """List available domains"""
        domain_paths = self._get_domain_paths()
        if not domain_paths:
            print("ERROR: No domain paths configured")
            return
        
        # Collect unique domains (respects precedence)
        seen_domains = set()
        domains_data = []
        
        for domain_path in domain_paths:
            if not domain_path.exists():
                continue
                
            for domain_dir in domain_path.iterdir():
                if domain_dir.is_dir() and domain_dir.name not in seen_domains:
                    seen_domains.add(domain_dir.name)
                    
                    # Domain name is just the directory name
                    name = domain_dir.name.title()
                    desc = f"Tools for {domain_dir.name}"
                    
                    # Count YAML files directly in domain directory
                    tool_count = len(list(domain_dir.glob("*.yaml")))
                    domains_data.append((domain_dir.name, name, desc, tool_count))
        
        if human_mode:
            table = Table(title="Available Domains")
            table.add_column("Domain", style="cyan")
            table.add_column("Description", style="dim")
            table.add_column("Tools", justify="right", style="green")
            
            for domain_id, name, desc, tool_count in domains_data:
                table.add_row(domain_id, desc, str(tool_count))
            
            console.print(table)
        else:
            # AI-optimized output
            print("AVAILABLE DOMAINS:")
            for domain_id, name, desc, tool_count in domains_data:
                print(f"  {domain_id}: {tool_count} tools - {desc}")
            print("")
            print("Use: craft <domain> to list domain tools")
            print("Add --noob flag for Rich UI tables")
    
    def list_domain_tools(self, domain: str, human_mode: bool = False) -> bool:
        """List tools in a specific domain. Returns True on success, False on error."""
        domain_dir = self._find_domain_by_name(domain)
        
        if not domain_dir:
            print(f"ERROR: Domain '{domain}' not found")
            return False
        
        # Domain name is just the directory name
        domain_name = domain.title()
        
        tools_data = []
        for tool_file in domain_dir.glob("*.yaml"):
            tool_config = yaml.safe_load(tool_file.read_text())
            name = tool_config.get("name", tool_file.stem)
            desc = tool_config.get("description", "No description")
            
            # Extract first usage example from help
            help_text = tool_config.get("help", "")
            usage = "No usage info"
            if "craft" in help_text:
                lines = help_text.split("\n")
                for line in lines:
                    if "craft" in line and "Examples:" not in line and "Usage:" not in line:
                        usage = line.strip()
                        break
            
            tools_data.append((tool_file.stem, name, desc, usage))
        
        if human_mode:
            table = Table(title=f"{domain_name} Tools")
            table.add_column("Tool", style="cyan")
            table.add_column("Description", style="dim")
            table.add_column("Usage", style="yellow")
            
            for tool_id, name, desc, usage in tools_data:
                table.add_row(tool_id, desc, usage)
            
            console.print(table)
        else:
            # AI-optimized output
            print(f"{domain_name.upper()} TOOLS:")
            for tool_id, name, desc, usage in tools_data:
                print(f"  {name.upper()}: {desc}")
                if usage != "No usage info":
                    print(f"    Usage: {usage}")
            print("")
            print(f"Use: craft {domain} <tool> --help for tool-specific help")
            print("Add --noob flag for Rich UI tables")
        
        return True
    
    def show_tool_help(self, domain: str, tool: str, human_mode: bool = False) -> bool:
        """Show help for a specific tool. Returns True on success, False on error."""
        domain_dir = self._find_domain_by_name(domain)
        
        if not domain_dir:
            print(f"ERROR: Domain '{domain}' not found")
            return False
            
        tool_file = domain_dir / f"{tool}.yaml"
        
        if not tool_file.exists():
            print(f"ERROR: Tool '{tool}' not found in domain '{domain}'")
            return False
        
        config = yaml.safe_load(tool_file.read_text())
        name = config.get("name", tool)
        desc = config.get("description", "No description")
        help_text = config.get("help", "No help available")
        
        if human_mode:
            panel = Panel(
                Text.from_markup(f"[bold]{name}[/bold]\n{desc}\n\n{help_text}"),
                title=f"🔧 {tool}",
                border_style="green"
            )
            console.print(panel)
        else:
            # AI-optimized output
            print(f"{name.upper()}")
            print(f"Description: {desc}")
            print("")
            print(help_text)
            print("")
            print("Add --noob flag for Rich UI panel")
        
        return True
    
    def run_tool(self, domain: str, tool: str, args: List[str], human_mode: bool = False) -> int:
        """Execute a domain tool"""
        domain_dir = self._find_domain_by_name(domain)
        
        if not domain_dir:
            print(f"ERROR: Domain '{domain}' not found")
            return 1
            
        tool_file = domain_dir / f"{tool}.yaml"
        
        if not tool_file.exists():
            print(f"ERROR: Tool '{tool}' not found in domain '{domain}'")
            return 1
        
        # Load tool configuration
        tool_config = yaml.safe_load(tool_file.read_text())
        
        # Build command
        command_template = tool_config.get("command", "")
        if not command_template:
            print(f"ERROR: No command defined for tool '{tool}'")
            return 1
        
        # Substitute variables
        base_path = str(Path.cwd())  # Always use current working directory
        args_str = " ".join(args)
        
        command = command_template.format(
            base_path=base_path,
            args=args_str,
            domain=domain,
            tool=tool,
            tool_config=tool_config
        )

        # Display execution context
        return self._display_execution_context(
            domain, tool, args, tool_config, command, base_path, human_mode
        )
    
    def _display_execution_context(self, domain: str, tool: str, args: List[str], 
                                 tool_config: dict, command: str, base_path: str, 
                                 human_mode: bool = False) -> int:
        """Display execution context in appropriate format"""
        
        # Prepare context data
        context = {
            "execution": {
                "domain": domain,
                "tool": tool,
                "args": args,
                "command": command,
                "base_path": base_path
            },
            "tool_config": tool_config,
            "resolved_command": command,
            "variables": {
                "base_path": base_path,
                "args": " ".join(args),
                "domain": domain,
                "tool": tool
            }
        }
        
        if human_mode:
            # Rich table display for humans
            from rich.table import Table
            from rich.panel import Panel
            from rich.console import Console
            from rich.text import Text
            from rich.syntax import Syntax
            
            console = Console()
            
            # Main execution panel
            exec_panel = Panel(
                Text.from_markup(
                    f"[bold]Domain:[/bold] {domain}\n"
                    f"[bold]Tool:[/bold] {tool}\n"
                    f"[bold]Arguments:[/bold] {' '.join(args) if args else 'None'}\n"
                    f"[bold]Base Path:[/bold] {base_path}\n"
                    f"[bold]Resolved Command:[/bold] {command}"
                ),
                title="🔧 Execution Context",
                border_style="cyan"
            )
            console.print(exec_panel)
            
            # Tool configuration
            if tool_config:
                config_text = f"Name: {tool_config.get('name', 'Unknown')}\n"
                config_text += f"Description: {tool_config.get('description', 'No description')}\n"
                config_text += f"Category: {tool_config.get('category', 'uncategorized')}\n"
                config_text += f"Command Template: {tool_config.get('command', 'None')}"
                
                config_panel = Panel(
                    Text(config_text),
                    title="📋 Tool Configuration",
                    border_style="green"
                )
                console.print(config_panel)
            
            # Full help text if available
            help_text = tool_config.get('help', '')
            if help_text:
                help_panel = Panel(
                    Text(help_text),
                    title="📖 Tool Help",
                    border_style="yellow"
                )
                console.print(help_panel)
        else:
            # JSON format for AI agents
            import json
            print("EXECUTION_CONTEXT:")
            print(json.dumps(context, indent=2, default=str))
        
        return 0  # Success - context displayed
