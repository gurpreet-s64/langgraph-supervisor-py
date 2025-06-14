"""
Fitness AI Orchestration System

A LangGraph-based multi-agent system for comprehensive fitness consultations.
Combines workout planning and nutrition advice through intelligent agent coordination.

Components:
- Supervisor Agent: Orchestrates fitness consultations
- Workout Specialist: Creates exercise plans and calculates fitness metrics
- Nutritionist: Provides meal plans and nutrition advice

Features:
- Real OpenAI integration
- LangSmith tracing and monitoring
- LangGraph Studio visual debugging
- Multi-agent coordination
- Specialized fitness tools
"""

from .core import create_fitness_ai_system
from .agents import WorkoutSpecialist, Nutritionist, FitnessSupervisor
from .tools import workout_tools, nutrition_tools
from .config import FitnessAIConfig

__version__ = "1.0.0"
__author__ = "Fitness AI Team"

__all__ = [
    "create_fitness_ai_system",
    "WorkoutSpecialist", 
    "Nutritionist",
    "FitnessSupervisor",
    "workout_tools",
    "nutrition_tools",
    "FitnessAIConfig"
] 