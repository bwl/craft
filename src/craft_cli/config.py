"""
Configuration management for Craft CLI
"""
import os
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class CraftConfig:
    """Craft CLI configuration"""
    domain_paths: List[str] = field(default_factory=list)
    include_builtin_domains: bool = True
    default_human_mode: bool = False
    verbose_execution: bool = False
    show_startup_checklist: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CraftConfig':
        """Create config from dictionary"""
        config_data = data.get('config', {})
        return cls(
            domain_paths=data.get('domain_paths', []),
            include_builtin_domains=data.get('include_builtin_domains', True),
            default_human_mode=config_data.get('default_human_mode', False),
            verbose_execution=config_data.get('verbose_execution', False),
            show_startup_checklist=config_data.get('show_startup_checklist', True)
        )
    
    def merge_with(self, other: 'CraftConfig') -> 'CraftConfig':
        """Merge this config with another, other takes precedence"""
        return CraftConfig(
            domain_paths=self.domain_paths + other.domain_paths,
            include_builtin_domains=other.include_builtin_domains,
            default_human_mode=other.default_human_mode,
            verbose_execution=other.verbose_execution,
            show_startup_checklist=other.show_startup_checklist
        )


class ConfigManager:
    """Manages Craft CLI configuration discovery and loading"""
    
    def __init__(self):
        self.project_config_path = Path.cwd() / ".craftrc"
        self.user_config_path = Path.home() / ".config" / "craft" / "craftrc"
        self._config_cache: Optional[CraftConfig] = None
    
    def get_config(self) -> CraftConfig:
        """Get merged configuration from all sources"""
        if self._config_cache is None:
            self._config_cache = self._load_merged_config()
        return self._config_cache
    
    def _load_merged_config(self) -> CraftConfig:
        """Load and merge configuration from all sources"""
        # Start with defaults
        base_config = CraftConfig()
        
        # Load user-level config
        user_config = self._load_config_file(self.user_config_path)
        if user_config:
            base_config = base_config.merge_with(user_config)
        
        # Load project-level config (takes precedence)
        project_config = self._load_config_file(self.project_config_path)
        if project_config:
            base_config = base_config.merge_with(project_config)
        
        return base_config
    
    def _load_config_file(self, config_path: Path) -> Optional[CraftConfig]:
        """Load config from a specific file"""
        if not config_path.exists():
            return None
        
        try:
            with open(config_path, 'r') as f:
                data = yaml.safe_load(f)
                if data is None:
                    return None
                return CraftConfig.from_dict(data)
        except (yaml.YAMLError, IOError) as e:
            print(f"Warning: Failed to load config from {config_path}: {e}")
            return None
    
    def get_domain_paths(self) -> List[Path]:
        """Get all domain paths including built-in and user-configured"""
        config = self.get_config()
        paths = []
        
        # Add built-in domains if enabled
        if config.include_builtin_domains:
            builtin_path = Path(__file__).parent / "domains"
            if builtin_path.exists():
                paths.append(builtin_path)
        
        # Add user-configured paths
        for path_str in config.domain_paths:
            expanded_path = Path(path_str).expanduser().resolve()
            if expanded_path.exists():
                paths.append(expanded_path)
            else:
                print(f"Warning: Domain path does not exist: {path_str}")
        
        return paths
    
    def check_for_conflicts(self) -> List[Tuple[str, List[Path]]]:
        """Check for domain name conflicts across paths"""
        conflicts = []
        domain_sources = {}
        
        for domain_path in self.get_domain_paths():
            for domain_dir in domain_path.iterdir():
                if domain_dir.is_dir():
                    domain_name = domain_dir.name
                    if domain_name not in domain_sources:
                        domain_sources[domain_name] = []
                    domain_sources[domain_name].append(domain_dir)
        
        # Find conflicts
        for domain_name, sources in domain_sources.items():
            if len(sources) > 1:
                conflicts.append((domain_name, sources))
        
        return conflicts
    
    def should_offer_example_config(self) -> bool:
        """Check if we should offer to create an example config"""
        return not self.user_config_path.exists() and not self.project_config_path.exists()
    
    def create_example_user_config(self) -> bool:
        """Create an example user config file"""
        try:
            # Ensure directory exists
            self.user_config_path.parent.mkdir(parents=True, exist_ok=True)
            
            example_config = {
                'domain_paths': [
                    '~/my-craft-domains'
                ],
                'include_builtin_domains': True,
                'config': {
                    'default_human_mode': False,
                    'verbose_execution': False,
                    'show_startup_checklist': True
                }
            }
            
            with open(self.user_config_path, 'w') as f:
                yaml.dump(example_config, f, default_flow_style=False, sort_keys=False)
            
            return True
        except (IOError, OSError) as e:
            print(f"Error creating example config: {e}")
            return False