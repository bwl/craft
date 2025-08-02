#!/usr/bin/env python3
"""
Interactive demo of Craft CLI Framework
Shows both AI-optimized and human-friendly interfaces
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str = None) -> None:
    """Run a command and display its output"""
    if description:
        print(f"\n{'=' * 60}")
        print(f"🎯 {description}")
        print(f"{'=' * 60}")
        print(f"Command: {cmd}")
        print()
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"Exit code: {result.returncode}")
    except Exception as e:
        print(f"Error running command: {e}")


def main():
    """Run the interactive demo"""
    print("🎭 CRAFT CLI FRAMEWORK DEMO")
    print("=" * 60)
    print()
    print("This demo shows the difference between:")
    print("• Default: AI-optimized interface (clean, parseable)")
    print("• --noob flag: Human-friendly Rich UI (pretty, visual)")
    print()
    
    # Check if craft is available
    try:
        subprocess.run(["craft", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ERROR: 'craft' command not found!")
        print()
        print("Please install craft-cli first:")
        print("  uv tool install craft-cli")
        print("  # or")
        print("  pip install craft-cli")
        return 1
    
    # Demo commands
    demos = [
        ("craft --help", "Framework Help - AI Optimized"),
        ("craft --help --noob", "Framework Help - Human Friendly"),
        ("craft --domains", "List Domains - AI Optimized"),
        ("craft --domains --noob", "List Domains - Human Friendly"),
        ("craft linting", "List Linting Tools - AI Optimized"),
        ("craft linting --noob", "List Linting Tools - Human Friendly"),
        ("craft linting ruff --help", "Tool-Specific Help - AI Optimized"),
        ("craft linting ruff --help --noob", "Tool-Specific Help - Human Friendly"),
    ]
    
    for cmd, description in demos:
        run_command(cmd, description)
        
        # Pause for user input
        try:
            input("\nPress Enter to continue (Ctrl+C to exit)...")
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted by user")
            return 0
    
    print("\n" + "=" * 60)
    print("🎉 DEMO COMPLETE!")
    print("=" * 60)
    
    print("\nKey Takeaways:")
    print("• Default interface optimized for AI agent consumption")
    print("• --noob flag provides Rich UI for human users")
    print("• Consistent patterns across all domains and tools")
    print("• Perfect for AI-driven workflows with occasional human oversight")
    
    print("\nNext Steps:")
    print("• Try: craft linting ruff check .")
    print("• Try: craft coding test --help")
    print("• Create your own domain following the documentation")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())