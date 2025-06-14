# Fitness AI Orchestration System

A sophisticated LangGraph-based multi-agent system for comprehensive fitness consultations, combining workout planning and nutrition advice through intelligent agent coordination.

## 🎯 **Project Overview**

This project implements a hierarchical multi-agent architecture using LangGraph, where a supervisor agent coordinates between specialized fitness experts to provide personalized health and wellness recommendations.

### **Key Features**

- 🤖 **Multi-Agent Architecture**: Supervisor + 2 specialized agents
- 🏋️ **Workout Specialist**: Exercise plans, fitness metrics, training guidance
- 🥗 **Nutritionist**: Meal plans, nutrition calculations, dietary advice
- 🔗 **Real OpenAI Integration**: Production-ready with gpt-4o-mini
- 📊 **LangSmith Tracing**: Complete monitoring and debugging
- 🎨 **LangGraph Studio**: Visual workflow editor and debugging
- 🛠️ **Specialized Tools**: 4 custom fitness tools with detailed calculations

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    FITNESS AI SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │   SUPERVISOR    │    │         USER QUERY              │ │
│  │   AGENT         │◄───┤  "Create workout & meal plan"   │ │
│  │                 │    │                                 │ │
│  └─────────┬───────┘    └─────────────────────────────────┘ │
│            │                                                │
│            ▼                                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              AGENT COORDINATION                         │ │
│  │  • Analyzes query complexity                           │ │
│  │  • Determines required specialists                     │ │
│  │  • Orchestrates multi-agent workflow                   │ │
│  └─────────┬───────────────────────────┬─────────────────┘ │
│            │                           │                   │
│            ▼                           ▼                   │
│  ┌─────────────────┐         ┌─────────────────────────┐   │
│  │ WORKOUT         │         │ NUTRITIONIST           │   │
│  │ SPECIALIST      │         │ AGENT                  │   │
│  │                 │         │                        │   │
│  │ Tools:          │         │ Tools:                 │   │
│  │ • Workout Plans │         │ • Meal Plans           │   │
│  │ • Fitness Metrics│        │ • Nutrition Needs      │   │
│  └─────────────────┘         └─────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📁 **Project Structure**

```
langgraph-supervisor-py/
├── src/fitness_ai/              # Main fitness AI module
│   ├── __init__.py             # Module exports and version info
│   ├── config.py               # Configuration management
│   ├── core.py                 # Main system orchestration
│   ├── agents.py               # Specialized agent definitions
│   └── tools.py                # Fitness-specific tools
├── examples/                    # Example implementations
│   ├── fitness_ai_with_openai.py
│   ├── fitness_ai_basic_demo.py
│   ├── fitness_ai_simple_demo.py
│   ├── fitness_ai_orchestration.py
│   ├── demo_supervisor.py
│   ├── simple_demo.py
│   └── real_world_example.py
├── docs/                       # Documentation
│   ├── README.md              # This file
│   ├── API.md                 # API documentation
│   ├── SETUP.md               # Setup instructions
│   └── ARCHITECTURE.md        # Technical architecture
├── tests/                      # Test suite
├── langgraph_supervisor/       # Core LangGraph library
├── .env                       # Environment variables
├── .env.example              # Environment template
├── langgraph.json            # LangGraph configuration
├── pyproject.toml            # Project dependencies
└── README.md                 # Project overview
```

## 🚀 **Quick Start**

### **1. Environment Setup**

```bash
# Clone and navigate to project
cd langgraph-supervisor-py

# Install dependencies
pip install -e .
pip install langchain-openai python-dotenv

# Install LangGraph CLI for Studio
pip install --upgrade "langgraph-cli[inmem]"
```

### **2. Configuration**

Create `.env` file with your API keys:

```env
# OpenAI Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=1000

# LangSmith Configuration (Optional but recommended)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=fitness-ai-orchestration

# System Configuration
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### **3. Run the System**

```python
# Interactive consultation
from src.fitness_ai import create_fitness_ai_system
from src.fitness_ai.core import run_interactive_consultation

run_interactive_consultation()
```

### **4. Launch LangGraph Studio**

```bash
# Start the development server
python -m langgraph_cli dev

# Access Studio at: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

## 🛠️ **Core Components**

### **Agents**

1. **🎯 Supervisor Agent** - Orchestrates fitness consultations
2. **🏋️ Workout Specialist** - Creates exercise plans and calculates metrics
3. **🥗 Nutritionist** - Designs meal plans and nutrition calculations

### **Tools**

1. **`create_workout_plan`** - Generate personalized exercise routines
2. **`calculate_training_metrics`** - Compute fitness metrics (BMI, BMR, heart rate zones)
3. **`create_meal_plan`** - Design nutrition plans with macro tracking
4. **`calculate_nutrition_needs`** - Determine caloric and macro requirements

## 📊 **Usage Examples**

### **Weight Loss Consultation**
```python
query = "I'm 30, 180cm, 85kg, want to lose 10kg. Create workout and meal plan. Beginner, 4 days/week."
```

### **Muscle Building Plan**
```python
query = "I'm 25, male, 175cm, 70kg, intermediate. Build muscle, 5 days/week, full gym access."
```

## 🎨 **LangGraph Studio Features**

- Visual Graph Editor with real-time execution tracking
- Step-through debugging and message inspection
- Performance monitoring and error analysis
- Collaborative debugging sessions

## 🧪 **Testing**

```bash
pytest                    # Run all tests
pytest --cov=src/fitness_ai  # Run with coverage
```

## 🔒 **Security**

- API keys in environment variables
- No user data persistence
- HTTPS encrypted communications
- Optional LangSmith tracing

---

**Built with ❤️ using LangGraph, OpenAI, and LangSmith** 