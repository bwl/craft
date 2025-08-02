"""
Craft CLI Framework

Domain-specific tool orchestration made simple.
Makes specialized tools feel like system commands.
"""

__version__ = "1.0.0"
__author__ = "SLATE Team"
__license__ = "MIT"

from .main import main
from .core import CraftCLI

__all__ = ["main", "CraftCLI", "__version__"]