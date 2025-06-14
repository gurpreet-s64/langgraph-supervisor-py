#!/usr/bin/env python3
"""
Fitness AI Main Entry Point

Production-ready entry point for the Fitness AI Orchestration System.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fitness_ai.core import (
    run_interactive_consultation,
    run_demo_scenarios,
    get_system_info,
    create_fitness_ai_system
)

# Export graph for LangGraph Studio
graph = create_fitness_ai_system()


def main():
    """Main entry point with command-line argument parsing."""
    
    print("🤖 FITNESS AI ORCHESTRATION SYSTEM")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "demo":
            print("🎬 Running Demo Scenarios")
            run_demo_scenarios()
            
        elif mode == "info":
            print("📊 System Information")
            info = get_system_info()
            
            for key, value in info.items():
                print(f"\n{key.upper()}:")
                if isinstance(value, dict):
                    for k, v in value.items():
                        print(f"  • {k}: {v}")
                elif isinstance(value, list):
                    for item in value:
                        print(f"  • {item}")
                else:
                    print(f"  {value}")
        else:
            print("🎯 Starting Interactive Consultation Mode")
            run_interactive_consultation()
    else:
        print("🎯 Starting Interactive Consultation Mode")
        run_interactive_consultation()


if __name__ == "__main__":
    main()
