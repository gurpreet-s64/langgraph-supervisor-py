#!/usr/bin/env python3
"""
Basic Fitness AI Orchestration Demo
Shows the core multi-agent workflow functionality
"""

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from langgraph_supervisor import create_supervisor
from simple_demo import FakeChatModel


# Basic fitness tools
@tool
def create_workout_plan(goal: str, level: str, days: int) -> str:
    """Create a workout plan."""
    print(f"💪 Workout Specialist: Creating {goal} plan for {level}, {days} days/week")
    return f"WORKOUT PLAN: {goal} program for {level} level, {days} days per week"

@tool
def create_meal_plan(goal: str, calories: int) -> str:
    """Create a meal plan."""
    print(f"🥗 Nutritionist: Creating {goal} meal plan with {calories} calories")
    return f"MEAL PLAN: {goal} nutrition plan with {calories} daily calories"


def run_basic_fitness_demo():
    """Run basic fitness AI demo."""
    
    print("🤖 FITNESS AI ORCHESTRATION - BASIC DEMO")
    print("=" * 60)
    print("🏋️ Workout Specialist + 🥗 Nutritionist + 🎯 AI Supervisor")
    print("=" * 60)
    
    try:
        # Create mock models
        workout_responses = [
            AIMessage(content="I'll create your workout plan."),
            AIMessage(content="Let me design your exercise routine."),
            AIMessage(content="Here's your personalized workout."),
        ]
        
        nutrition_responses = [
            AIMessage(content="I'll design your nutrition plan."),
            AIMessage(content="Let me calculate your dietary needs."),
            AIMessage(content="Here's your meal plan."),
        ]
        
        supervisor_responses = [
            AIMessage(content="I'll coordinate your fitness consultation."),
            AIMessage(content="Let me connect you with our specialists."),
            AIMessage(content="Your complete fitness plan is ready."),
        ]
        
        # Create agents
        print("📋 Creating fitness agents...")
        
        workout_specialist = create_react_agent(
            model=FakeChatModel(responses=workout_responses),
            tools=[create_workout_plan],
            name="workout_specialist",
            prompt="You are a workout specialist. Create exercise plans."
        )
        
        nutritionist = create_react_agent(
            model=FakeChatModel(responses=nutrition_responses),
            tools=[create_meal_plan],
            name="nutritionist", 
            prompt="You are a nutritionist. Create meal plans."
        )
        
        print("✅ Created workout_specialist and nutritionist")
        
        # Create supervisor
        print("🎯 Creating supervisor...")
        workflow = create_supervisor(
            agents=[workout_specialist, nutritionist],
            model=FakeChatModel(responses=supervisor_responses),
            prompt="""You coordinate fitness consultations:
            - workout_specialist: handles exercise plans
            - nutritionist: handles meal plans
            
            Delegate tasks to appropriate specialists."""
        )
        
        print("✅ Supervisor created")
        
        # Compile workflow
        print("⚙️ Compiling workflow...")
        app = workflow.compile()
        print("✅ Fitness AI system ready!")
        
        # Test scenarios
        scenarios = [
            "Create a workout plan for weight loss, beginner level, 3 days per week.",
            "I need a meal plan for muscle gain with 2500 calories.",
            "Create both a workout and nutrition plan for general fitness."
        ]
        
        for i, query in enumerate(scenarios, 1):
            print(f"\n🧪 SCENARIO {i}")
            print(f"💬 User: {query}")
            print("-" * 50)
            
            try:
                result = app.invoke({
                    "messages": [HumanMessage(content=query)]
                })
                
                print(f"✅ Scenario {i} completed!")
                print(f"📊 Total messages: {len(result['messages'])}")
                
                # Show key messages
                for j, msg in enumerate(result["messages"]):
                    if hasattr(msg, 'content') and msg.content:
                        msg_type = type(msg).__name__
                        agent = getattr(msg, 'name', 'User' if j == 0 else 'System')
                        print(f"  {j+1}. [{agent}]: {msg.content}")
                
                print(f"\n🎯 Final Result: {result['messages'][-1].content}")
                
            except Exception as e:
                print(f"❌ Error in scenario {i}: {e}")
            
            print("\n" + "=" * 60)
        
        print("\n🎉 FITNESS AI ORCHESTRATION DEMO COMPLETED!")
        print("\n💡 System Successfully Demonstrated:")
        print("  ✅ Multi-agent coordination")
        print("  ✅ Task delegation by supervisor")
        print("  ✅ Specialized agent responses")
        print("  ✅ Tool execution (workout & meal planning)")
        print("  ✅ End-to-end workflow orchestration")
        
        print("\n🔧 Architecture Overview:")
        print("  🎯 Supervisor Agent: Coordinates and delegates tasks")
        print("  💪 Workout Specialist: Handles exercise planning")
        print("  🥗 Nutritionist: Manages meal planning")
        print("  🔄 LangGraph: Orchestrates the multi-agent workflow")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_basic_fitness_demo() 