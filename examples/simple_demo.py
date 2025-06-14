#!/usr/bin/env python3
"""
Simple Demo for LangGraph Multi-Agent Supervisor
Based on the working test patterns from the project.
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


class FakeChatModel(BaseChatModel):
    """Fake chat model based on the test implementation."""
    idx: int = 0
    responses: Sequence[BaseMessage]

    @property
    def _llm_type(self) -> str:
        return "fake-tool-call-model"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: dict[str, Any],
    ) -> ChatResult:
        generation = ChatGeneration(message=self.responses[self.idx])
        self.idx += 1
        return ChatResult(generations=[generation])

    def bind_tools(
        self, tools: Sequence[dict[str, Any] | type | Callable | BaseTool], **kwargs: Any
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        tool_dicts = [
            {
                "name": tool.name if isinstance(tool, BaseTool) else str(tool),
            }
            for tool in tools
        ]
        return self.bind(tools=tool_dicts)


def run_simple_demo():
    """Run a simple supervisor demo."""
    print("🤖 LangGraph Multi-Agent Supervisor - Simple Demo")
    print("=" * 55)
    
    # Define tools
    @tool
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        print(f"🧮 Math Agent: {a} + {b} = {result}")
        return result

    @tool
    def web_search(query: str) -> str:
        """Search the web for information."""
        print(f"🔍 Research Agent: Searching for '{query}'")
        return (
            "Here are the headcounts for each of the FAANG companies in 2024:\n"
            "1. **Facebook (Meta)**: 67,317 employees.\n"
            "2. **Apple**: 164,000 employees.\n"
            "3. **Amazon**: 1,551,000 employees.\n"
            "4. **Netflix**: 14,000 employees.\n"
            "5. **Google (Alphabet)**: 181,269 employees."
        )

    # Predefined responses (from the test file)
    supervisor_messages = [
        AIMessage(
            content="I'll delegate this to the research expert to find the information.",
            tool_calls=[
                {
                    "name": "transfer_to_research_expert",
                    "args": {},
                    "id": "call_research_001",
                    "type": "tool_call",
                }
            ],
        ),
        AIMessage(
            content="Now I'll have the math expert calculate the total.",
            tool_calls=[
                {
                    "name": "transfer_to_math_expert",
                    "args": {},
                    "id": "call_math_001",
                    "type": "tool_call",
                }
            ],
        ),
        AIMessage(
            content="The combined headcount of the FAANG companies in 2024 is 1,977,586 employees.",
        ),
    ]

    research_agent_messages = [
        AIMessage(
            content="I'll search for the FAANG company headcounts.",
            tool_calls=[
                {
                    "name": "web_search",
                    "args": {"query": "FAANG headcount 2024"},
                    "id": "call_search_001",
                    "type": "tool_call",
                },
            ],
        ),
        AIMessage(
            content="I found the headcount data for all FAANG companies. The numbers are: Meta (67,317), Apple (164,000), Amazon (1,551,000), Netflix (14,000), and Google (181,269) employees.",
        ),
    ]

    math_agent_messages = [
        AIMessage(
            content="I'll calculate the total headcount step by step.",
            tool_calls=[
                {
                    "name": "add",
                    "args": {"a": 67317, "b": 1551000},
                    "id": "call_add_001",
                    "type": "tool_call",
                },
            ],
        ),
        AIMessage(
            content="Let me continue adding the remaining companies.",
            tool_calls=[
                {
                    "name": "add",
                    "args": {"a": 1618317, "b": 164000},
                    "id": "call_add_002",
                    "type": "tool_call",
                },
            ],
        ),
        AIMessage(
            content="Almost done, adding the last companies.",
            tool_calls=[
                {
                    "name": "add",
                    "args": {"a": 1782317, "b": 195269},
                    "id": "call_add_003",
                    "type": "tool_call",
                },
            ],
        ),
        AIMessage(
            content="The total combined headcount is 1,977,586 employees.",
        ),
    ]

    print("\n📋 Creating specialized agents...")
    
    # Create agents with fake models
    math_agent = create_react_agent(
        model=FakeChatModel(responses=math_agent_messages),
        tools=[add],
        name="math_expert",
    )

    research_agent = create_react_agent(
        model=FakeChatModel(responses=research_agent_messages),
        tools=[web_search],
        name="research_expert",
    )

    print("✅ Math expert and research expert created")

    # Create supervisor workflow
    print("\n🎯 Creating supervisor workflow...")
    workflow = create_supervisor(
        [math_agent, research_agent],
        model=FakeChatModel(responses=supervisor_messages),
        prompt=(
            "You are a team supervisor managing a research expert and a math expert. "
            "For research questions, delegate to research_expert. "
            "For math problems, delegate to math_expert."
        )
    )

    print("✅ Supervisor workflow created")

    # Compile the workflow
    print("\n⚙️  Compiling workflow...")
    app = workflow.compile()
    print("✅ Workflow compiled successfully")

    # Run the demo
    print("\n🚀 Running demo scenario...")
    print("💬 User Question: 'What's the combined headcount of the FAANG companies in 2024?'")
    print("-" * 55)

    try:
        result = app.invoke({
            "messages": [
                HumanMessage(
                    content="What's the combined headcount of the FAANG companies in 2024?"
                )
            ]
        })

        print(f"\n✅ Demo completed successfully!")
        print(f"📊 Total messages in conversation: {len(result['messages'])}")
        
        print("\n📜 Conversation Flow:")
        for i, msg in enumerate(result["messages"], 1):
            msg_type = type(msg).__name__
            agent_name = getattr(msg, 'name', 'User' if i == 1 else 'Unknown')
            if agent_name is None:
                agent_name = 'Unknown'
            content = str(msg.content)
            
            # Truncate long content
            if len(content) > 100:
                content = content[:100] + "..."
            
            # Show tool calls if present
            tool_info = ""
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                tool_names = [tc.get('name', 'unknown') for tc in msg.tool_calls]
                tool_info = f" [Tools: {', '.join(tool_names)}]"
            
            print(f"  {i:2d}. [{msg_type:12}] {agent_name:15}: {content}{tool_info}")

        print(f"\n🎯 Final Answer: {result['messages'][-1].content}")

    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 55)
    print("🎉 Demo completed!")
    print("\n💡 Key Features Demonstrated:")
    print("  • Supervisor orchestrates multiple specialized agents")
    print("  • Research agent handles information gathering")
    print("  • Math agent performs calculations")
    print("  • Tool-based handoff mechanism between agents")
    print("  • Structured conversation flow with message history")


if __name__ == "__main__":
    run_simple_demo() 