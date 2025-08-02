# .craftrc Configuration Format

The `.craftrc` file allows users to extend Craft CLI with custom domain paths and configuration.

## File Locations

Craft CLI searches for configuration files in this order:

1. **Project-level**: `./.craftrc` (current working directory)
2. **User-level**: `~/.config/craft/craftrc` (user's config directory)

Project-level configuration takes precedence over user-level configuration.

## Format

The `.craftrc` file uses YAML format:

```yaml
# Additional domain paths to search
domain_paths:
  - "~/my-craft-domains"        # User's custom domains
  - "./craft/domains"           # Project-specific domains
  - "./src/prompts/tools"       # Use any folder and stack the available agents

# Optional: Override built-in agent paths
include_builtin_domains: true     # Default: true - this allows user to disable the built in agents

# Optional: Global configuration
config:
  default_human_mode: false       # Default: false
  verbose_execution: false        # Default: false
```

## Domain Path Resolution

Craft CLI combines domains from multiple sources:

1. **Built-in domains** (from package installation)
2. **User-configured paths** (from .craftrc files)

Domains with the same name are resolved in this priority order:
1. Project-level custom domains
2. User-level custom domains  
3. Built-in package domains

## Examples

### Basic User Configuration
```yaml
# ~/.config/.craftrc
domain_paths:
  - "~/my-craft-tools"
```

### Project-Specific Configuration
```yaml
# ./.craftrc
domain_paths:
  - "./scripts/craft-domains"
  - "~/shared-team-domains"

config:
  default_human_mode: true
```

### Disable Built-in Domains
```yaml
# Use only custom domains
include_builtin_domains: false
domain_paths:
  - "~/custom-domains"
```

## Domain Directory Structure

Each domain path should contain domain directories:

```
my-craft-domains/
├── mytools/
│   ├── tool1.yaml
│   └── tool2.yaml
└── devops/
    ├── deploy.yaml
    └── monitor.yaml
```

## Configuration Merging

When multiple `.craftrc` files exist:

- `domain_paths` are merged (project paths + user paths)
- `config` settings are merged (project overrides user)
- `include_builtin_domains` uses project value if set, otherwise user value


TODO:

When tools have same name user is shown a startup error but project files take precedence and the other tool isn't available so everything still works


When opening Craft for first time offer to save an example config to the users dir if one isn't found.
