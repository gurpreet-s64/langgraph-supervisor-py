"""
Fitness AI Agents

Specialized agents for the fitness AI orchestration system.
Each agent has specific expertise and tools for their domain.
"""

from typing import List, Optional
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from .tools import workout_tools, nutrition_tools
from .config import config


class WorkoutSpecialist:
    """
    Workout Specialist Agent
    
    Specializes in:
    - Creating personalized workout plans
    - Calculating fitness metrics (BMI, BMR, heart rate zones)
    - Exercise form and technique guidance
    - Training progression recommendations
    """
    
    def __init__(self, model: Optional[ChatOpenAI] = None):
        """Initialize the Workout Specialist agent."""
        self.model = model or ChatOpenAI(
            model=config.openai_model,
            temperature=config.openai_temperature,
            api_key=config.openai_api_key
        )
        
        self.agent = create_react_agent(
            model=self.model,
            tools=workout_tools,
            name="workout_specialist",
            prompt=self._get_prompt()
        )
    
    def _get_prompt(self) -> str:
        """Get the specialized prompt for the workout specialist."""
        return """You are a certified personal trainer and workout specialist with expertise in:

CORE COMPETENCIES:
- Exercise physiology and biomechanics
- Personalized workout plan creation
- Fitness assessment and metrics calculation
- Progressive overload principles
- Injury prevention and safety protocols

SPECIALIZATIONS:
- Weight loss training programs
- Muscle building and hypertrophy
- Strength and powerlifting
- Cardiovascular endurance
- Functional fitness and mobility

APPROACH:
- Always prioritize safety and proper form
- Provide evidence-based recommendations
- Consider individual limitations and goals
- Ask clarifying questions when needed
- Use available tools to create comprehensive plans

TOOLS AVAILABLE:
- create_workout_plan: Design personalized exercise routines
- calculate_training_metrics: Compute BMI, BMR, heart rate zones

Remember to be encouraging, professional, and focus on sustainable fitness practices.
Use the tools when appropriate to provide detailed, actionable workout recommendations."""


class Nutritionist:
    """
    Nutritionist Agent
    
    Specializes in:
    - Creating personalized meal plans
    - Calculating nutritional needs and macros
    - Accommodating dietary restrictions
    - Sports nutrition and timing
    """
    
    def __init__(self, model: Optional[ChatOpenAI] = None):
        """Initialize the Nutritionist agent."""
        self.model = model or ChatOpenAI(
            model=config.openai_model,
            temperature=config.openai_temperature,
            api_key=config.openai_api_key
        )
        
        self.agent = create_react_agent(
            model=self.model,
            tools=nutrition_tools,
            name="nutritionist",
            prompt=self._get_prompt()
        )
    
    def _get_prompt(self) -> str:
        """Get the specialized prompt for the nutritionist."""
        return """You are a registered dietitian and sports nutritionist with expertise in:

CORE COMPETENCIES:
- Clinical nutrition and metabolism
- Personalized meal planning
- Macronutrient and micronutrient optimization
- Dietary restriction accommodation
- Sports nutrition and performance

SPECIALIZATIONS:
- Weight management nutrition
- Muscle building nutrition
- Performance and endurance nutrition
- Medical nutrition therapy
- Sustainable eating habits

APPROACH:
- Focus on evidence-based nutrition science
- Consider individual needs, preferences, and restrictions
- Promote sustainable and enjoyable eating patterns
- Provide practical, actionable meal planning advice
- Ask clarifying questions about dietary preferences

TOOLS AVAILABLE:
- create_meal_plan: Design personalized nutrition plans
- calculate_nutrition_needs: Compute caloric and macro requirements

Remember to be supportive, non-judgmental, and focus on long-term health outcomes.
Use the tools when appropriate to create detailed, personalized nutrition recommendations."""


class FitnessSupervisor:
    """
    Fitness Supervisor Agent
    
    Coordinates between workout and nutrition specialists to provide
    comprehensive fitness consultations and integrated recommendations.
    """
    
    def __init__(self, 
                 workout_specialist: WorkoutSpecialist,
                 nutritionist: Nutritionist,
                 model: Optional[ChatOpenAI] = None):
        """Initialize the Fitness Supervisor agent."""
        self.model = model or ChatOpenAI(
            model=config.openai_model,
            temperature=config.openai_temperature,
            api_key=config.openai_api_key
        )
        
        self.workout_specialist = workout_specialist
        self.nutritionist = nutritionist
        
        self.supervisor = create_supervisor(
            agents=[workout_specialist.agent, nutritionist.agent],
            model=self.model,
            prompt=self._get_prompt()
        )
    
    def _get_prompt(self) -> str:
        """Get the specialized prompt for the fitness supervisor."""
        return """You are a fitness AI coordinator managing a team of specialized experts:

TEAM MEMBERS:
🏋️ WORKOUT SPECIALIST: Handles exercise plans, training metrics, and workout guidance
🥗 NUTRITIONIST: Manages meal plans, nutrition calculations, and dietary recommendations

YOUR ROLE:
1. Analyze user requests and determine which specialist(s) to involve
2. Coordinate between specialists when comprehensive plans are needed
3. Ensure all aspects of fitness and nutrition are addressed
4. Provide cohesive, integrated recommendations
5. Maintain a holistic view of the user's health and fitness journey

DELEGATION STRATEGY:
- Workout-related questions → delegate to workout_specialist
- Nutrition-related questions → delegate to nutritionist
- Comprehensive fitness plans → coordinate both specialists
- General fitness advice → use your expertise to guide appropriately

COMMUNICATION STYLE:
- Be helpful, professional, and encouraging
- Provide clear, actionable guidance
- Ensure user safety is always the top priority
- Promote sustainable, long-term lifestyle changes
- Ask clarifying questions when needed

INTEGRATION FOCUS:
- Ensure workout and nutrition plans complement each other
- Consider timing of meals around workouts
- Balance caloric intake with exercise expenditure
- Provide holistic lifestyle recommendations

Remember: You're not just delegating tasks, you're orchestrating a comprehensive
fitness consultation that addresses the user's complete health and wellness needs."""
    
    def compile(self):
        """Compile the supervisor workflow."""
        return self.supervisor.compile()


def create_fitness_agents(model: Optional[ChatOpenAI] = None) -> tuple[WorkoutSpecialist, Nutritionist, FitnessSupervisor]:
    """
    Create all fitness AI agents.
    
    Args:
        model: Optional ChatOpenAI model to use for all agents
    
    Returns:
        Tuple of (workout_specialist, nutritionist, supervisor)
    """
    # Create individual specialists
    workout_specialist = WorkoutSpecialist(model)
    nutritionist = Nutritionist(model)
    
    # Create supervisor that coordinates them
    supervisor = FitnessSupervisor(workout_specialist, nutritionist, model)
    
    return workout_specialist, nutritionist, supervisor 