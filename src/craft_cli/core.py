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

console = Console()


class CraftCLI:
    """Main Craft CLI Framework class"""
    
    def __init__(self, base_path: Optional[Path] = None):
        """Initialize Craft CLI
        
        Args:
            base_path: Base path for finding domains directory
        """
        if base_path is None:
            # Try to find domains directory relative to package location
            package_dir = Path(__file__).parent
            self.base_path = package_dir.parent.parent  # Go up to project root
        else:
            self.base_path = Path(base_path)
        
        self.domains_dir = self.base_path / "domains"
    
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
        if not self.domains_dir.exists():
            print("ERROR: No domains directory found")
            return
        
        domains_data = []
        for domain_dir in self.domains_dir.iterdir():
            if domain_dir.is_dir():
                config_file = domain_dir / "config.yaml"
                tools_dir = domain_dir / "tools"
                
                if config_file.exists():
                    config = yaml.safe_load(config_file.read_text())
                    name = config.get("name", domain_dir.name)
                    desc = config.get("description", "No description")
                else:
                    name = domain_dir.name
                    desc = "No config found"
                
                tool_count = len(list(tools_dir.glob("*.yaml"))) if tools_dir.exists() else 0
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
    
    def list_domain_tools(self, domain: str, human_mode: bool = False) -> None:
        """List tools in a specific domain"""
        domain_dir = self.domains_dir / domain
        tools_dir = domain_dir / "tools"
        
        if not domain_dir.exists():
            print(f"ERROR: Domain '{domain}' not found")
            return
        
        if not tools_dir.exists():
            print(f"ERROR: No tools directory found for domain '{domain}'")
            return
        
        # Load domain config
        config_file = domain_dir / "config.yaml"
        if config_file.exists():
            config = yaml.safe_load(config_file.read_text())
            domain_name = config.get("name", domain)
        else:
            domain_name = domain
        
        tools_data = []
        for tool_file in tools_dir.glob("*.yaml"):
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
    
    def show_tool_help(self, domain: str, tool: str, human_mode: bool = False) -> None:
        """Show help for a specific tool"""
        tool_file = self.domains_dir / domain / "tools" / f"{tool}.yaml"
        
        if not tool_file.exists():
            print(f"ERROR: Tool '{tool}' not found in domain '{domain}'")
            return
        
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
    
    def run_tool(self, domain: str, tool: str, args: List[str]) -> int:
        """Execute a domain tool"""
        domain_dir = self.domains_dir / domain
        tool_file = domain_dir / "tools" / f"{tool}.yaml"
        
        if not domain_dir.exists():
            print(f"ERROR: Domain '{domain}' not found")
            return 1
        
        if not tool_file.exists():
            print(f"ERROR: Tool '{tool}' not found in domain '{domain}'")
            return 1
        
        # Load configurations
        domain_config = {}
        domain_config_file = domain_dir / "config.yaml"
        if domain_config_file.exists():
            domain_config = yaml.safe_load(domain_config_file.read_text())
        
        tool_config = yaml.safe_load(tool_file.read_text())
        
        # Build command
        command_template = tool_config.get("command", "")
        if not command_template:
            print(f"ERROR: No command defined for tool '{tool}'")
            return 1
        
        # Substitute variables
        base_path = domain_config.get("base_path", str(Path.cwd()))
        args_str = " ".join(args)
        
        command = command_template.format(
            base_path=base_path,
            args=args_str,
            domain=domain,
            tool=tool
        )
        
        # Show what we're running (only in verbose mode)
        if "--verbose" in args:
            print(f"Running: {command}")
        
        try:
            result = subprocess.run(command, shell=True, check=False)
            return result.returncode
        except KeyboardInterrupt:
            print("\nInterrupted")
            return 1
        except Exception as e:
            print(f"ERROR: {e}")
            return 1