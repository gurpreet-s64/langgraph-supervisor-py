#!/usr/bin/env python3
"""
Demo script for LangGraph Multi-Agent Supervisor
This demo uses mock models to demonstrate the supervisor functionality without requiring API keys.
"""

from typing import Any, Optional, Sequence, Callable
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel, LanguageModelInput
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool, tool
from langgraph.prebuilt import create_react_agent

from langgraph_supervisor import create_supervisor


class MockChatModel(BaseChatModel):
    """Mock chat model for demonstration purposes."""
    
    responses: list[str] = []
    current_index: int = 0
    
    def __init__(self, responses: list[str], **kwargs):
        super().__init__(responses=responses, current_index=0, **kwargs)
    
    @property
    def _llm_type(self) -> str:
        return "mock-chat-model"
    
    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Simple logic: return next response in sequence
        if self.current_index < len(self.responses):
            response = self.responses[self.current_index]
            self.current_index += 1
        else:
            response = "I don't have more responses configured."
        
        message = AIMessage(content=response)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])
    
    def bind_tools(
        self, tools: Sequence[dict[str, Any] | type | Callable | BaseTool], **kwargs: Any
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        """Bind tools to the model (mock implementation)."""
        # For demo purposes, just return self
        return self


def create_demo_agents():
    """Create demo agents with mock functionality."""
    
    # Define tools for the math agent
    @tool
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        print(f"🧮 Math Agent: Adding {a} + {b} = {result}")
        return result
    
    @tool
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        result = a * b
        print(f"🧮 Math Agent: Multiplying {a} × {b} = {result}")
        return result
    
    # Define tools for the research agent
    @tool
    def web_search(query: str) -> str:
        """Search the web for information (mock implementation)."""
        print(f"🔍 Research Agent: Searching for '{query}'")
        # Mock search results
        mock_results = {
            "FAANG": "FAANG companies headcount 2024: Meta (67,317), Apple (164,000), Amazon (1,551,000), Netflix (14,000), Google (181,269)",
            "weather": "Today's weather is sunny with a temperature of 72°F",
            "news": "Latest tech news: AI developments continue to accelerate across industries"
        }
        
        for key in mock_results:
            if key.lower() in query.lower():
                return mock_results[key]
        
        return f"Mock search results for: {query}"
    
    # Create mock models with predefined responses
    math_responses = [
        "I'll help you with the math calculation.",
        "Let me add these numbers for you.",
        "The calculation is complete."
    ]
    
    research_responses = [
        "I'll search for that information.",
        "Let me find the latest data on that topic.",
        "Here's what I found from my search."
    ]
    
    supervisor_responses = [
        "I'll delegate this task to the appropriate expert.",
        "Let me route this to the right agent.",
        "Task completed successfully."
    ]
    
    # Create agents
    math_agent = create_react_agent(
        model=MockChatModel(math_responses),
        tools=[add, multiply],
        name="math_expert",
        prompt="You are a math expert. Use the available tools to perform calculations."
    )
    
    research_agent = create_react_agent(
        model=MockChatModel(research_responses),
        tools=[web_search],
        name="research_expert", 
        prompt="You are a research expert. Use web search to find information."
    )
    
    return math_agent, research_agent, MockChatModel(supervisor_responses)


def run_demo():
    """Run the supervisor demo."""
    print("🤖 LangGraph Multi-Agent Supervisor Demo")
    print("=" * 50)
    
    # Create demo agents
    math_agent, research_agent, supervisor_model = create_demo_agents()
    
    # Create supervisor workflow
    print("\n📋 Creating supervisor workflow...")
    workflow = create_supervisor(
        agents=[research_agent, math_agent],
        model=supervisor_model,
        prompt=(
            "You are a team supervisor managing a research expert and a math expert. "
            "For research questions, delegate to research_expert. "
            "For math problems, delegate to math_expert."
        )
    )
    
    # Compile the workflow
    print("⚙️  Compiling workflow...")
    app = workflow.compile()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Math Problem",
            "message": "What is 15 + 27?",
            "description": "Testing math delegation"
        },
        {
            "name": "Research Query", 
            "message": "What are the FAANG company headcounts?",
            "description": "Testing research delegation"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 Test {i}: {scenario['name']}")
        print(f"📝 Description: {scenario['description']}")
        print(f"💬 User Message: {scenario['message']}")
        print("-" * 30)
        
        try:
            # Run the workflow
            result = app.invoke({
                "messages": [HumanMessage(content=scenario["message"])]
            })
            
            print("✅ Workflow completed successfully!")
            print(f"📊 Total messages in conversation: {len(result['messages'])}")
            
            # Display the conversation flow
            print("\n📜 Conversation Flow:")
            for j, msg in enumerate(result["messages"]):
                msg_type = type(msg).__name__
                content = str(msg.content)[:100] + "..." if len(str(msg.content)) > 100 else str(msg.content)
                agent_name = getattr(msg, 'name', 'Unknown')
                print(f"  {j+1}. [{msg_type}] {agent_name}: {content}")
                
        except Exception as e:
            print(f"❌ Error running scenario: {e}")
        
        print("\n" + "="*50)
    
    print("\n🎉 Demo completed!")
    print("\n💡 Key Features Demonstrated:")
    print("  • Supervisor agent coordination")
    print("  • Agent specialization (math vs research)")
    print("  • Tool-based handoff mechanism")
    print("  • Message history management")


if __name__ == "__main__":
    run_demo() 