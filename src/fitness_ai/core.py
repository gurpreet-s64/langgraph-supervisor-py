"""
Fitness AI Core Module

Main entry point for creating and running the fitness AI system.
Integrates all components: configuration, agents, tools, and workflows.
"""

import os
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from .config import config
from .agents import create_fitness_agents, FitnessSupervisor
from .tools import all_fitness_tools


def create_fitness_ai_system(custom_config: Optional[Dict[str, Any]] = None) -> Optional[Any]:
    """
    Create the complete fitness AI system with all agents and workflows.
    
    Args:
        custom_config: Optional custom configuration overrides
    
    Returns:
        Compiled LangGraph workflow ready for execution
    """
    print("🤖 INITIALIZING FITNESS AI SYSTEM")
    print("=" * 50)
    
    try:
        # Validate configuration
        config.validate()
        print(f"✅ Configuration validated: {config}")
        
        # Apply custom config if provided
        if custom_config:
            for key, value in custom_config.items():
                if hasattr(config, key):
                    setattr(config, key, value)
                    print(f"🔧 Config override: {key} = {value}")
        
        # Create OpenAI model
        model = ChatOpenAI(
            model=config.openai_model,
            temperature=config.openai_temperature,
            max_tokens=config.openai_max_tokens,
            api_key=config.openai_api_key
        )
        print(f"🔑 OpenAI model initialized: {config.openai_model}")
        
        # Create fitness agents
        workout_specialist, nutritionist, supervisor = create_fitness_agents(model)
        print("🏋️ Workout Specialist created")
        print("🥗 Nutritionist created")
        print("🎯 Supervisor created")
        
        # Compile the supervisor workflow
        fitness_ai = supervisor.compile()
        print("⚡ Fitness AI system compiled successfully")
        
        # System summary
        print("\n📊 SYSTEM SUMMARY:")
        print(f"   • Model: {config.openai_model}")
        print(f"   • Temperature: {config.openai_temperature}")
        print(f"   • Tracing: {'Enabled' if config.langchain_tracing_v2 else 'Disabled'}")
        print(f"   • Project: {config.langchain_project}")
        print(f"   • Tools: {len(all_fitness_tools)} specialized fitness tools")
        print(f"   • Agents: 3 (Supervisor + 2 Specialists)")
        
        return fitness_ai
        
    except Exception as e:
        print(f"❌ Error creating fitness AI system: {e}")
        print("💡 Check your .env file and ensure all required variables are set")
        return None


def run_fitness_consultation(fitness_ai: Any, query: str) -> None:
    """
    Run a single fitness consultation query.
    
    Args:
        fitness_ai: Compiled fitness AI system
        query: User's fitness question or request
    """
    if not fitness_ai:
        print("❌ Fitness AI system not available")
        return
    
    print(f"\n🗣️ USER QUERY: {query}")
    print("-" * 50)
    
    try:
        # Stream the response
        for chunk in fitness_ai.stream(
            {"messages": [HumanMessage(content=query)]},
            {"configurable": {"thread_id": "fitness_consultation"}}
        ):
            if "__end__" not in chunk:
                for node, messages in chunk.items():
                    if messages and hasattr(messages, 'get'):
                        last_message = messages.get('messages', [])
                        if last_message and hasattr(last_message[-1], 'content'):
                            print(f"\n🤖 {node.upper()}: {last_message[-1].content}")
    
    except Exception as e:
        print(f"❌ Error during consultation: {e}")


def run_interactive_consultation() -> None:
    """
    Run an interactive fitness consultation session.
    """
    print("🎯 INTERACTIVE FITNESS CONSULTATION")
    print("=" * 50)
    print("Ask me anything about fitness, workouts, or nutrition!")
    print("Type 'quit', 'exit', or 'bye' to end the session.\n")
    
    # Create fitness AI system
    fitness_ai = create_fitness_ai_system()
    if not fitness_ai:
        return
    
    print("\n🚀 System ready! How can I help you with your fitness journey?")
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Thanks for using Fitness AI! Stay healthy!")
                break
            
            if not user_input:
                print("Please enter a question or type 'quit' to exit.")
                continue
            
            run_fitness_consultation(fitness_ai, user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Session ended. Stay healthy!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def run_demo_scenarios() -> None:
    """
    Run predefined demo scenarios to showcase the fitness AI system.
    """
    print("🎬 FITNESS AI DEMO SCENARIOS")
    print("=" * 50)
    
    # Create fitness AI system
    fitness_ai = create_fitness_ai_system()
    if not fitness_ai:
        return
    
    # Demo scenarios
    scenarios = [
        {
            "title": "Weight Loss Consultation",
            "query": "I'm 30 years old, 180cm tall, weigh 85kg, and want to lose 10kg. Can you create a workout and meal plan for me? I'm a beginner and can work out 4 days a week."
        },
        {
            "title": "Muscle Building Plan",
            "query": "I'm 25, male, 175cm, 70kg, intermediate level. I want to build muscle and can train 5 days a week with full gym access. What's my nutrition and workout plan?"
        },
        {
            "title": "Fitness Metrics Calculation",
            "query": "Calculate my BMI, BMR, and daily calorie needs. I'm a 28-year-old female, 165cm, 60kg, moderately active, looking to maintain my current weight."
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎯 SCENARIO {i}: {scenario['title']}")
        print("=" * 60)
        run_fitness_consultation(fitness_ai, scenario['query'])
        
        if i < len(scenarios):
            input("\n⏸️ Press Enter to continue to next scenario...")
    
    print("\n✅ All demo scenarios completed!")


def get_system_info() -> Dict[str, Any]:
    """
    Get comprehensive information about the fitness AI system.
    
    Returns:
        Dictionary containing system information
    """
    return {
        "version": "1.0.0",
        "config": config.to_dict(),
        "agents": {
            "supervisor": "Coordinates fitness consultations",
            "workout_specialist": "Creates workout plans and calculates fitness metrics",
            "nutritionist": "Provides meal plans and nutrition calculations"
        },
        "tools": {
            "workout_tools": [tool.name for tool in all_fitness_tools[:2]],
            "nutrition_tools": [tool.name for tool in all_fitness_tools[2:]]
        },
        "features": [
            "Real OpenAI integration",
            "LangSmith tracing and monitoring", 
            "LangGraph Studio visual debugging",
            "Multi-agent coordination",
            "Specialized fitness tools",
            "Interactive consultations",
            "Demo scenarios"
        ]
    }


# Main execution functions for different use cases
def main_interactive():
    """Main function for interactive mode."""
    run_interactive_consultation()


def main_demo():
    """Main function for demo mode."""
    run_demo_scenarios()


def main_info():
    """Main function to display system information."""
    info = get_system_info()
    print("🤖 FITNESS AI SYSTEM INFORMATION")
    print("=" * 50)
    
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


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "demo":
            main_demo()
        elif mode == "info":
            main_info()
        else:
            main_interactive()
    else:
        main_interactive() 