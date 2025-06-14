#!/usr/bin/env python3
"""
Real-world example of LangGraph Multi-Agent Supervisor
This example can work with actual OpenAI API when OPENAI_API_KEY is set.
"""

import os
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from langgraph_supervisor import create_supervisor


def create_real_world_demo():
    """Create a real-world demo with actual or mock OpenAI."""
    
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        print("🔑 OpenAI API key found - using real OpenAI models")
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    else:
        print("⚠️  No OpenAI API key found - using mock model for demo")
        print("   Set OPENAI_API_KEY environment variable to use real OpenAI")
        
        # Use our mock model from the simple demo
        from simple_demo import FakeChatModel
        from langchain_core.messages import AIMessage
        
        # Simple responses for demo
        model = FakeChatModel(responses=[
            AIMessage(content="I'll help you with that task."),
            AIMessage(content="Let me delegate this to the appropriate expert."),
            AIMessage(content="Task completed successfully.")
        ])
    
    # Define tools for different agents
    @tool
    def calculate_sum(numbers: list[float]) -> float:
        """Calculate the sum of a list of numbers."""
        result = sum(numbers)
        print(f"🧮 Math Agent: Calculating sum of {numbers} = {result}")
        return result
    
    @tool
    def calculate_average(numbers: list[float]) -> float:
        """Calculate the average of a list of numbers."""
        if not numbers:
            return 0
        result = sum(numbers) / len(numbers)
        print(f"🧮 Math Agent: Calculating average of {numbers} = {result}")
        return result
    
    @tool
    def search_information(query: str) -> str:
        """Search for information (mock implementation)."""
        print(f"🔍 Research Agent: Searching for '{query}'")
        
        # Mock responses based on query keywords
        if "weather" in query.lower():
            return "Current weather: Sunny, 75°F with light winds"
        elif "stock" in query.lower() or "price" in query.lower():
            return "AAPL: $150.25 (+2.1%), GOOGL: $2,800.50 (+1.8%), MSFT: $380.75 (+0.9%)"
        elif "news" in query.lower():
            return "Latest tech news: AI developments continue, new breakthrough in quantum computing announced"
        else:
            return f"Search results for '{query}': Found relevant information about the topic"
    
    @tool
    def analyze_data(data: str) -> str:
        """Analyze provided data and give insights."""
        print(f"📊 Analysis Agent: Analyzing data: {data[:50]}...")
        return f"Analysis complete: The data shows positive trends with key insights about {data[:30]}..."
    
    # Create specialized agents
    print("\n📋 Creating specialized agents...")
    
    math_agent = create_react_agent(
        model=model,
        tools=[calculate_sum, calculate_average],
        name="math_expert",
        prompt="You are a math expert. Use your tools to perform calculations accurately."
    )
    
    research_agent = create_react_agent(
        model=model,
        tools=[search_information],
        name="research_expert",
        prompt="You are a research expert. Use search to find current information."
    )
    
    analysis_agent = create_react_agent(
        model=model,
        tools=[analyze_data],
        name="analysis_expert", 
        prompt="You are a data analysis expert. Analyze data and provide insights."
    )
    
    print("✅ Created math_expert, research_expert, and analysis_expert")
    
    # Create supervisor workflow
    print("\n🎯 Creating supervisor workflow...")
    workflow = create_supervisor(
        agents=[math_agent, research_agent, analysis_agent],
        model=model,
        prompt=(
            "You are a team supervisor managing three experts: "
            "math_expert (for calculations), research_expert (for information gathering), "
            "and analysis_expert (for data analysis). "
            "Delegate tasks to the most appropriate expert based on the user's request."
        )
    )
    
    print("✅ Supervisor workflow created")
    
    # Compile the workflow
    print("\n⚙️  Compiling workflow...")
    app = workflow.compile()
    print("✅ Workflow compiled successfully")
    
    return app


def run_real_world_demo():
    """Run the real-world demo with multiple scenarios."""
    print("🤖 LangGraph Multi-Agent Supervisor - Real World Example")
    print("=" * 60)
    
    try:
        app = create_real_world_demo()
        
        # Test scenarios
        scenarios = [
            {
                "name": "Math Calculation",
                "query": "Calculate the sum and average of these numbers: 10, 20, 30, 40, 50",
                "description": "Testing math delegation with multiple operations"
            },
            {
                "name": "Information Research", 
                "query": "What's the current weather and latest tech news?",
                "description": "Testing research capabilities"
            },
            {
                "name": "Data Analysis",
                "query": "Analyze this sales data: Q1: $100k, Q2: $150k, Q3: $200k, Q4: $180k",
                "description": "Testing data analysis delegation"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🧪 Test Scenario {i}: {scenario['name']}")
            print(f"📝 Description: {scenario['description']}")
            print(f"💬 User Query: {scenario['query']}")
            print("-" * 60)
            
            try:
                result = app.invoke({
                    "messages": [HumanMessage(content=scenario["query"])]
                })
                
                print(f"✅ Scenario {i} completed successfully!")
                print(f"📊 Messages generated: {len(result['messages'])}")
                
                # Show final response
                final_message = result["messages"][-1]
                print(f"🎯 Final Response: {final_message.content}")
                
            except Exception as e:
                print(f"❌ Error in scenario {i}: {e}")
            
            print("\n" + "=" * 60)
        
        print("\n🎉 Real-world demo completed!")
        print("\n💡 Features Demonstrated:")
        print("  • Multi-agent coordination with 3 specialized experts")
        print("  • Dynamic task delegation based on query content")
        print("  • Tool-based agent communication")
        print("  • Scalable supervisor architecture")
        print("  • Compatible with both real and mock LLM models")
        
        if not os.getenv("OPENAI_API_KEY"):
            print("\n🔧 To use with real OpenAI:")
            print("   export OPENAI_API_KEY=your_api_key_here")
            print("   python real_world_example.py")
            
    except Exception as e:
        print(f"❌ Error setting up demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_real_world_demo() 