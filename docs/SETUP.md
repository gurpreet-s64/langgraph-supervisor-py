# Fitness AI Setup Guide

Complete setup instructions for the Fitness AI Orchestration System.

## 🚀 **Quick Setup**

### **1. Prerequisites**

- Python 3.8+ installed
- OpenAI API account with credits
- LangSmith account (optional but recommended)

### **2. Installation**

```bash
# Navigate to project directory
cd langgraph-supervisor-py

# Install the project in editable mode
pip install -e .

# Install required dependencies
pip install langchain-openai python-dotenv

# Install LangGraph CLI for Studio support
pip install --upgrade "langgraph-cli[inmem]"
```

### **3. Environment Configuration**

Create a `.env` file in the project root:

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

### **4. Verify Installation**

```bash
# Test the system
python fitness_ai_main.py info

# Run a quick demo
python fitness_ai_main.py demo
```

## 🔧 **Detailed Setup**

### **OpenAI API Key Setup**

1. **Create OpenAI Account**
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in to your account

2. **Generate API Key**
   - Go to API Keys section
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)

3. **Add Credits**
   - Go to Billing section
   - Add payment method and credits
   - Minimum $5 recommended for testing

### **LangSmith Setup (Optional)**

1. **Create LangSmith Account**
   - Visit [LangSmith](https://smith.langchain.com/)
   - Sign up with your email

2. **Get API Key**
   - Go to Settings → API Keys
   - Create new API key
   - Copy the key (starts with `lsv2_`)

3. **Create Project**
   - Go to Projects
   - Create new project named "fitness-ai-orchestration"

### **Environment Variables**

#### **Required Variables**
- `OPENAI_API_KEY`: Your OpenAI API key

#### **Optional Variables**
- `OPENAI_MODEL`: Model to use (default: gpt-4o-mini)
- `OPENAI_TEMPERATURE`: Response creativity 0.0-1.0 (default: 0.1)
- `OPENAI_MAX_TOKENS`: Maximum response length (default: 1000)
- `LANGCHAIN_TRACING_V2`: Enable LangSmith tracing (default: true)
- `LANGCHAIN_API_KEY`: Your LangSmith API key
- `LANGCHAIN_PROJECT`: Project name for tracing
- `DEBUG_MODE`: Enable debug logging (default: false)
- `LOG_LEVEL`: Logging level (default: INFO)

## 🎯 **Usage Modes**

### **Interactive Mode**
```bash
python fitness_ai_main.py
# or
python fitness_ai_main.py interactive
```

### **Demo Mode**
```bash
python fitness_ai_main.py demo
```

### **System Information**
```bash
python fitness_ai_main.py info
```

### **LangGraph Studio**
```bash
# Start development server
python -m langgraph_cli dev

# Access Studio at:
# https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

## 🐍 **Python API Usage**

### **Basic Usage**
```python
from src.fitness_ai import create_fitness_ai_system
from src.fitness_ai.core import run_fitness_consultation

# Create the system
fitness_ai = create_fitness_ai_system()

# Run a consultation
query = "I want to lose weight and build muscle"
run_fitness_consultation(fitness_ai, query)
```

### **Advanced Usage**
```python
from src.fitness_ai.agents import create_fitness_agents
from langchain_openai import ChatOpenAI

# Custom model configuration
model = ChatOpenAI(
    model="gpt-4",
    temperature=0.2,
    max_tokens=1500
)

# Create agents with custom model
workout_specialist, nutritionist, supervisor = create_fitness_agents(model)

# Use individual agents
from langchain_core.messages import HumanMessage

response = workout_specialist.agent.invoke({
    "messages": [HumanMessage(content="Create a strength training plan")]
})
```

## 🧪 **Testing Setup**

### **Run Tests**
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=src/fitness_ai

# Run specific test files
pytest tests/test_agents.py
pytest tests/test_tools.py
```

### **Test Configuration**
Create `tests/.env.test` for testing:
```env
OPENAI_API_KEY=test_key_here
OPENAI_MODEL=gpt-3.5-turbo
LANGCHAIN_TRACING_V2=false
DEBUG_MODE=true
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Solution: Install in editable mode
pip install -e .
```

#### **API Key Not Found**
```bash
# Check .env file exists and has correct format
cat .env

# Verify environment variables are loaded
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

#### **LangGraph CLI Not Found**
```bash
# Install with inmem support
pip install --upgrade "langgraph-cli[inmem]"

# Verify installation
python -m langgraph_cli --help
```

#### **Module Not Found Errors**
```bash
# Add project to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or use the main entry point
python fitness_ai_main.py
```

### **Debug Mode**

Enable debug mode for detailed logging:
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

### **API Rate Limits**

If you hit OpenAI rate limits:
1. Add delays between requests
2. Use a higher tier API key
3. Implement exponential backoff

### **Memory Issues**

For large conversations:
1. Reduce `OPENAI_MAX_TOKENS`
2. Clear conversation history periodically
3. Use streaming responses

## 🔒 **Security Best Practices**

### **API Key Security**
- Never commit `.env` files to version control
- Use environment variables in production
- Rotate API keys regularly
- Monitor API usage and costs

### **Production Deployment**
- Use secure environment variable management
- Implement rate limiting
- Add authentication for multi-user scenarios
- Monitor and log all interactions

### **Data Privacy**
- No user data is stored by default
- LangSmith tracing can be disabled
- All communications are encrypted via HTTPS

## 📊 **Performance Optimization**

### **Model Selection**
- `gpt-4o-mini`: Fast, cost-effective (recommended)
- `gpt-4`: Higher quality, slower, more expensive
- `gpt-3.5-turbo`: Fastest, lowest cost, good quality

### **Token Management**
- Set appropriate `OPENAI_MAX_TOKENS`
- Use streaming for long responses
- Implement conversation summarization

### **Caching**
- Enable LangSmith for response caching
- Implement local caching for repeated queries
- Cache fitness calculations

## 🆘 **Getting Help**

### **Documentation**
- `docs/README.md`: Project overview
- `docs/API.md`: Complete API reference
- `examples/`: Working code examples

### **Debugging**
- Enable `DEBUG_MODE=true`
- Use LangSmith tracing
- Check LangGraph Studio for visual debugging

### **Community**
- Check GitHub issues
- Review LangGraph documentation
- OpenAI API documentation

---

**Ready to get started? Run `python fitness_ai_main.py` to begin your fitness AI journey!** 