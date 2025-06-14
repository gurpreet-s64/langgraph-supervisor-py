# Fitness AI API Documentation

Complete API reference for the Fitness AI Orchestration System.

## 🏗️ **Core API**

### **`create_fitness_ai_system(custom_config=None)`**

Creates and initializes the complete fitness AI system.

**Parameters:**
- `custom_config` (dict, optional): Configuration overrides

**Returns:**
- Compiled LangGraph workflow ready for execution

**Example:**
```python
from src.fitness_ai import create_fitness_ai_system

# Basic usage
fitness_ai = create_fitness_ai_system()

# With custom configuration
custom_config = {"openai_temperature": 0.2, "debug_mode": True}
fitness_ai = create_fitness_ai_system(custom_config)
```

### **`run_fitness_consultation(fitness_ai, query)`**

Executes a single fitness consultation query.

**Parameters:**
- `fitness_ai`: Compiled fitness AI system
- `query` (str): User's fitness question or request

**Example:**
```python
from src.fitness_ai.core import run_fitness_consultation

query = "Create a workout plan for weight loss"
run_fitness_consultation(fitness_ai, query)
```

## 🤖 **Agent Classes**

### **`WorkoutSpecialist`**

Specialized agent for exercise planning and fitness metrics.

**Methods:**
- `__init__(model=None)`: Initialize with optional custom model
- `_get_prompt()`: Returns specialized prompt for workout expertise

**Tools:**
- `create_workout_plan`
- `calculate_training_metrics`

**Example:**
```python
from src.fitness_ai.agents import WorkoutSpecialist
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
specialist = WorkoutSpecialist(model)
```

### **`Nutritionist`**

Specialized agent for meal planning and nutrition calculations.

**Methods:**
- `__init__(model=None)`: Initialize with optional custom model
- `_get_prompt()`: Returns specialized prompt for nutrition expertise

**Tools:**
- `create_meal_plan`
- `calculate_nutrition_needs`

### **`FitnessSupervisor`**

Coordinator agent that orchestrates between specialists.

**Methods:**
- `__init__(workout_specialist, nutritionist, model=None)`: Initialize supervisor
- `compile()`: Compile the supervisor workflow
- `_get_prompt()`: Returns coordination prompt

## 🛠️ **Tools API**

### **`create_workout_plan(goal, level, days, equipment="basic")`**

Creates personalized workout plans based on user parameters.

**Parameters:**
- `goal` (str): Primary fitness goal
  - Options: `"weight_loss"`, `"muscle_gain"`, `"strength"`, `"endurance"`, `"general_fitness"`
- `level` (str): Experience level
  - Options: `"beginner"`, `"intermediate"`, `"advanced"`
- `days` (int): Workout days per week (1-7)
- `equipment` (str): Available equipment
  - Options: `"none"`, `"basic"`, `"gym"`, `"home_gym"`

**Returns:**
- Detailed workout plan with schedule and recommendations

**Example:**
```python
from src.fitness_ai.tools import create_workout_plan

plan = create_workout_plan(
    goal="weight_loss",
    level="beginner", 
    days=4,
    equipment="basic"
)
print(plan)
```

### **`calculate_training_metrics(weight, height, age, gender="male")`**

Calculates comprehensive fitness and training metrics.

**Parameters:**
- `weight` (float): Weight in kilograms
- `height` (float): Height in centimeters
- `age` (int): Age in years
- `gender` (str): Gender for BMR calculation
  - Options: `"male"`, `"female"`

**Returns:**
- BMI, BMR, TDEE, heart rate zones, and recommendations

**Example:**
```python
from src.fitness_ai.tools import calculate_training_metrics

metrics = calculate_training_metrics(
    weight=75.0,
    height=175.0,
    age=30,
    gender="male"
)
print(metrics)
```

### **`create_meal_plan(goal, calories, restrictions="none")`**

Creates personalized meal plans with macronutrient breakdowns.

**Parameters:**
- `goal` (str): Dietary goal
  - Options: `"weight_loss"`, `"muscle_gain"`, `"maintenance"`, `"performance"`
- `calories` (int): Target daily calories
- `restrictions` (str): Dietary restrictions
  - Options: `"none"`, `"vegetarian"`, `"vegan"`, `"gluten_free"`, `"dairy_free"`

**Returns:**
- Detailed meal plan with macro breakdown and food recommendations

**Example:**
```python
from src.fitness_ai.tools import create_meal_plan

meal_plan = create_meal_plan(
    goal="muscle_gain",
    calories=2500,
    restrictions="vegetarian"
)
print(meal_plan)
```

### **`calculate_nutrition_needs(weight, height, age, gender, activity, goal)`**

Calculates detailed nutritional requirements.

**Parameters:**
- `weight` (float): Weight in kg
- `height` (float): Height in cm
- `age` (int): Age in years
- `gender` (str): `"male"` or `"female"`
- `activity` (str): Activity level
  - Options: `"sedentary"`, `"light"`, `"moderate"`, `"active"`, `"very_active"`
- `goal` (str): Nutrition goal
  - Options: `"weight_loss"`, `"muscle_gain"`, `"maintenance"`

**Returns:**
- Comprehensive nutritional analysis with calorie and macro requirements

**Example:**
```python
from src.fitness_ai.tools import calculate_nutrition_needs

nutrition = calculate_nutrition_needs(
    weight=70.0,
    height=165.0,
    age=25,
    gender="female",
    activity="moderate",
    goal="weight_loss"
)
print(nutrition)
```

## ⚙️ **Configuration API**

### **`FitnessAIConfig`**

Configuration management class for the fitness AI system.

**Class Methods:**
- `from_env()`: Create configuration from environment variables
- `validate()`: Validate configuration settings
- `to_dict()`: Convert to dictionary representation

**Properties:**
- `openai_api_key`: OpenAI API key (required)
- `openai_model`: Model name (default: "gpt-4o-mini")
- `openai_temperature`: Response creativity (default: 0.1)
- `openai_max_tokens`: Token limit (default: 1000)
- `langchain_tracing_v2`: Enable tracing (default: True)
- `langchain_project`: Project name for tracing
- `debug_mode`: Enable debug logging (default: False)
- `log_level`: Logging level (default: "INFO")

**Example:**
```python
from src.fitness_ai.config import FitnessAIConfig

# Create from environment
config = FitnessAIConfig.from_env()

# Validate settings
config.validate()

# Get as dictionary
config_dict = config.to_dict()
```

## 🔄 **Workflow API**

### **Streaming Responses**

The fitness AI system supports streaming responses for real-time interaction.

**Example:**
```python
from langchain_core.messages import HumanMessage

# Stream a consultation
for chunk in fitness_ai.stream(
    {"messages": [HumanMessage(content="Create a workout plan")]},
    {"configurable": {"thread_id": "consultation_1"}}
):
    if "__end__" not in chunk:
        for node, messages in chunk.items():
            print(f"{node}: {messages}")
```

### **Thread Management**

Each consultation can have its own thread for context management.

**Example:**
```python
# Different threads for different users
thread_configs = [
    {"configurable": {"thread_id": "user_1"}},
    {"configurable": {"thread_id": "user_2"}}
]

for config in thread_configs:
    response = fitness_ai.stream(
        {"messages": [HumanMessage(content=query)]},
        config
    )
```

## 🎯 **Usage Patterns**

### **Simple Consultation**
```python
from src.fitness_ai import create_fitness_ai_system
from src.fitness_ai.core import run_fitness_consultation

fitness_ai = create_fitness_ai_system()
run_fitness_consultation(fitness_ai, "I want to lose weight")
```

### **Interactive Session**
```python
from src.fitness_ai.core import run_interactive_consultation

run_interactive_consultation()
```

### **Demo Scenarios**
```python
from src.fitness_ai.core import run_demo_scenarios

run_demo_scenarios()
```

### **Custom Agent Creation**
```python
from src.fitness_ai.agents import create_fitness_agents
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4", temperature=0.2)
workout_specialist, nutritionist, supervisor = create_fitness_agents(model)

# Use individual agents
workout_plan = workout_specialist.agent.invoke({
    "messages": [HumanMessage(content="Create a strength training plan")]
})
```

## 🚨 **Error Handling**

### **Common Exceptions**

**`ValueError`**: Configuration validation errors
```python
try:
    config = FitnessAIConfig.from_env()
    config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
```

**`ConnectionError`**: API connection issues
```python
try:
    fitness_ai = create_fitness_ai_system()
except ConnectionError as e:
    print(f"API connection failed: {e}")
```

### **Best Practices**

1. **Always validate configuration** before creating the system
2. **Handle API rate limits** with appropriate delays
3. **Use thread IDs** for multi-user scenarios
4. **Enable tracing** for debugging complex workflows
5. **Check API key validity** before deployment

## 📊 **Response Formats**

### **Workout Plan Response**
```
🏋️ WORKOUT PLAN CREATED:
Goal: Weight Loss
Level: Beginner
Schedule: 4 days per week
Equipment: Basic equipment

Program: 4-day fat burning program with cardio and strength training

Key Components:
- Progressive overload principles
- Proper form and technique focus
- Adequate recovery periods
- Injury prevention strategies

Duration: 8-12 weeks with regular assessments
```

### **Fitness Metrics Response**
```
📊 FITNESS METRICS CALCULATED:

Body Composition:
- BMI: 24.5 (Normal weight)
- Height: 175 cm
- Weight: 75 kg

Metabolic Rate:
- BMR: 1,680 calories/day
- TDEE (moderate activity): 2,604 calories/day

Heart Rate Zones:
- Fat Burn Zone: 114-133 bpm
- Cardio Zone: 133-162 bpm
- Max Heart Rate: 190 bpm
```

### **Meal Plan Response**
```
🍽️ MEAL PLAN CREATED:
Goal: Muscle Gain
Daily Calories: 2500
Restrictions: Vegetarian

MACRONUTRIENT BREAKDOWN:
- Protein: 156g (25%)
- Carbohydrates: 281g (45%)
- Fats: 83g (30%)

MEAL STRUCTURE:
- 3 main meals + 2 snacks
- Protein with every meal
- Pre/post workout nutrition timing

Duration: Follow for 2-4 weeks, then reassess
```

---

**For more examples, see the `examples/` directory in the project repository.** 