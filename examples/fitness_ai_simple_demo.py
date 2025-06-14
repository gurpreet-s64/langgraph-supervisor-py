#!/usr/bin/env python3
"""
Simple Fitness AI Orchestration Demo
Demonstrates the multi-agent workflow with clear output
"""

import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from langgraph_supervisor import create_supervisor
from simple_demo import FakeChatModel


# Simplified tools for demo
@tool
def create_workout_plan(goal: str, level: str, days: int) -> str:
    """Create a workout plan."""
    print(f"💪 Workout Specialist: Creating {goal} plan for {level} level, {days} days/week")
    return f"🏋️ WORKOUT PLAN: {goal} program for {level} level, {days} days per week"

@tool
def create_meal_plan(goal: str, calories: int) -> str:
    """Create a meal plan."""
    print(f"🥗 Nutritionist: Creating {goal} meal plan with {calories} calories")
    return f"🍽️ MEAL PLAN: {goal} nutrition plan with {calories} daily calories"

@tool
def calculate_metrics(weight: float, height: float, age: int) -> str:
    """Calculate fitness metrics."""
    print(f"📊 Calculating metrics for {age}yr old, {weight}kg, {height}cm")
    bmi = weight / ((height/100) ** 2)
    return f"📊 METRICS: BMI {bmi:.1f}, Target heart rate: {220-age} bpm"


def create_simple_fitness_ai():
    """Create a simple fitness AI system for demo."""
    
    print("🤖 SIMPLE FITNESS AI ORCHESTRATION")
    print("=" * 50)
    
    # Create mock models with more responses
    workout_responses = [
        AIMessage(content="I'll create your workout plan."),
        AIMessage(content="Let me design your exercise routine."),
        AIMessage(content="Here's your personalized workout."),
        AIMessage(content="I'll modify exercises for your needs."),
        AIMessage(content="Your training plan is ready."),
    ]
    
    nutrition_responses = [
        AIMessage(content="I'll design your nutrition plan."),
        AIMessage(content="Let me calculate your dietary needs."),
        AIMessage(content="Here's your meal plan."),
        AIMessage(content="I'll optimize your nutrition timing."),
        AIMessage(content="Your diet plan is complete."),
    ]
    
    supervisor_responses = [
        AIMessage(content="I'll coordinate your fitness consultation."),
        AIMessage(content="Let me connect you with our specialists."),
        AIMessage(content="I'll ensure you get comprehensive guidance."),
        AIMessage(content="Your complete fitness plan is ready."),
        AIMessage(content="I've coordinated both workout and nutrition plans."),
    ]
    
    # Create agents
    workout_model = FakeChatModel(responses=workout_responses)
    nutrition_model = FakeChatModel(responses=nutrition_responses)
    supervisor_model = FakeChatModel(responses=supervisor_responses)
    
    print("📋 Creating fitness agents...")
    
    # Workout Specialist
    workout_specialist = create_react_agent(
        model=workout_model,
        tools=[create_workout_plan, calculate_metrics],
        name="workout_specialist",
        prompt="You are a workout specialist. Create exercise plans and calculate fitness metrics."
    )
    
    # Nutritionist
    nutritionist = create_react_agent(
        model=nutrition_model,
        tools=[create_meal_plan],
        name="nutritionist", 
        prompt="You are a nutritionist. Create meal plans and dietary recommendations."
    )
    
    print("✅ Created workout_specialist and nutritionist")
    
    # Supervisor
    print("🎯 Creating supervisor...")
    workflow = create_supervisor(
        agents=[workout_specialist, nutritionist],
        model=supervisor_model,
        prompt="""You coordinate fitness consultations:
        - workout_specialist: handles exercise plans and metrics
        - nutritionist: handles meal plans and nutrition
        
        Delegate tasks to appropriate specialists based on user needs."""
    )
    
    print("✅ Supervisor created")
    
    # Compile workflow
    print("⚙️ Compiling workflow...")
    app = workflow.compile()
    print("✅ Fitness AI system ready!")
    
    return app


def run_simple_demo():
    """Run simple fitness AI demo."""
    
    try:
        # Create system
        fitness_ai = create_simple_fitness_ai()
        
        # Test scenarios
        scenarios = [
            "I want to lose weight. Create a workout plan for a beginner, 3 days per week.",
            "I need a meal plan for muscle gain with 2500 calories per day.",
            "I'm 25 years old, 70kg, 175cm tall. Calculate my fitness metrics and create both a workout and nutrition plan."
        ]
        
        for i, query in enumerate(scenarios, 1):
            print(f"\n🧪 TEST {i}")
            print(f"💬 Query: {query}")
            print("-" * 50)
            
            try:
                result = fitness_ai.invoke({
                    "messages": [HumanMessage(content=query)]
                })
                
                print(f"✅ Test {i} completed!")
                print(f"📊 Messages generated: {len(result['messages'])}")
                
                # Show conversation flow
                print("\n📜 Conversation Flow:")
                for j, msg in enumerate(result["messages"], 1):
                    msg_type = type(msg).__name__
                    agent_name = getattr(msg, 'name', 'User' if j == 1 else 'System')
                    content = str(msg.content)[:100] + "..." if len(str(msg.content)) > 100 else str(msg.content)
                    print(f"  {j}. [{msg_type:12}] {agent_name:15}: {content}")
                
                # Show tool calls
                tool_calls = []
                for msg in result["messages"]:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tc in msg.tool_calls:
                            tool_calls.append(tc.get('name', 'unknown'))
                
                if tool_calls:
                    print(f"\n🔧 Tools Used: {', '.join(set(tool_calls))}")
                
                # Show final response
                final_msg = result["messages"][-1]
                print(f"\n🎯 Final Response: {final_msg.content}")
                
            except Exception as e:
                print(f"❌ Error in test {i}: {e}")
            
            print("\n" + "=" * 50)
        
        print("\n🎉 SIMPLE FITNESS AI DEMO COMPLETED!")
        print("\n💡 Demonstrated Capabilities:")
        print("  🏋️ Workout plan creation")
        print("  🥗 Meal plan generation") 
        print("  📊 Fitness metrics calculation")
        print("  🎯 Intelligent task delegation")
        print("  🤝 Multi-agent coordination")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_simple_demo() 