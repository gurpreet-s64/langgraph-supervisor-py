#!/usr/bin/env python3
"""
Fitness AI Orchestration with Real OpenAI
Production-ready LangGraph multi-agent system
"""

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

# Load environment variables
load_dotenv()

# =============================================================================
# WORKOUT SPECIALIST TOOLS
# =============================================================================

@tool
def create_workout_plan(goal: str, level: str, days: int, equipment: str = "basic") -> str:
    """Create a personalized workout plan."""
    print(f"💪 Workout Specialist: Creating {goal} plan for {level} level")
    
    plans = {
        "weight_loss": f"{days}-day fat burning program with cardio and strength training",
        "muscle_gain": f"{days}-day muscle building program with progressive overload",
        "strength": f"{days}-day strength training program focusing on compound movements",
        "general_fitness": f"{days}-day balanced fitness routine for overall health"
    }
    
    plan = plans.get(goal, plans["general_fitness"])
    
    return f"""
🏋️ WORKOUT PLAN CREATED:
Goal: {goal.replace('_', ' ').title()}
Level: {level.title()}
Schedule: {days} days per week
Equipment: {equipment}

Program: {plan}

Key Components:
- Progressive overload principles
- Proper form and technique focus
- Adequate recovery periods
- Injury prevention strategies

Duration: 8-12 weeks with regular assessments
"""

@tool
def calculate_training_metrics(weight: float, height: float, age: int, gender: str = "male") -> str:
    """Calculate fitness and training metrics."""
    print(f"💪 Workout Specialist: Calculating metrics for {age}yr old {gender}")
    
    # BMI calculation
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    
    # BMR calculation (Mifflin-St Jeor)
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Heart rate zones
    max_hr = 220 - age
    fat_burn = (int(max_hr * 0.6), int(max_hr * 0.7))
    cardio = (int(max_hr * 0.7), int(max_hr * 0.85))
    
    return f"""
📊 FITNESS METRICS CALCULATED:

Body Composition:
- BMI: {bmi:.1f}
- Classification: {'Normal' if 18.5 <= bmi < 25 else 'Overweight' if bmi >= 25 else 'Underweight'}

Metabolic Rate:
- BMR: {bmr:.0f} calories/day
- TDEE (moderate activity): {bmr * 1.55:.0f} calories/day

Heart Rate Zones:
- Fat Burn Zone: {fat_burn[0]}-{fat_burn[1]} bpm
- Cardio Zone: {cardio[0]}-{cardio[1]} bpm
- Max Heart Rate: {max_hr} bpm

Training Recommendations:
- Track progress weekly
- Adjust calories based on results
- Monitor heart rate during workouts
"""

# =============================================================================
# NUTRITIONIST TOOLS
# =============================================================================

@tool
def create_meal_plan(goal: str, calories: int, restrictions: str = "none") -> str:
    """Create a personalized meal plan."""
    print(f"🥗 Nutritionist: Creating {goal} meal plan with {calories} calories")
    
    # Macro ratios based on goals
    ratios = {
        "weight_loss": {"protein": 30, "carbs": 35, "fat": 35},
        "muscle_gain": {"protein": 25, "carbs": 45, "fat": 30},
        "maintenance": {"protein": 20, "carbs": 50, "fat": 30}
    }
    
    ratio = ratios.get(goal, ratios["maintenance"])
    protein_g = (calories * ratio["protein"] / 100) / 4
    carbs_g = (calories * ratio["carbs"] / 100) / 4
    fat_g = (calories * ratio["fat"] / 100) / 9
    
    return f"""
🍽️ MEAL PLAN CREATED:
Goal: {goal.replace('_', ' ').title()}
Daily Calories: {calories}
Restrictions: {restrictions.replace('_', ' ').title()}

MACRONUTRIENT BREAKDOWN:
- Protein: {protein_g:.0f}g ({ratio['protein']}%)
- Carbohydrates: {carbs_g:.0f}g ({ratio['carbs']}%)
- Fats: {fat_g:.0f}g ({ratio['fat']}%)

MEAL STRUCTURE:
- 3 main meals + 2 snacks
- Protein with every meal
- Vegetables with lunch and dinner
- Pre/post workout nutrition timing

HYDRATION:
- 8-10 glasses of water daily
- Extra water around workouts

Duration: Follow for 2-4 weeks, then reassess
"""

@tool
def calculate_nutrition_needs(weight: float, height: float, age: int, gender: str, activity: str, goal: str) -> str:
    """Calculate detailed nutritional needs."""
    print(f"🥗 Nutritionist: Calculating nutrition needs for {gender}, {age} years old")
    
    # BMR calculation
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Activity multipliers
    multipliers = {
        "sedentary": 1.2, "light": 1.375, "moderate": 1.55, 
        "active": 1.725, "very_active": 1.9
    }
    
    tdee = bmr * multipliers.get(activity, 1.55)
    
    # Goal adjustments
    adjustments = {"weight_loss": -500, "muscle_gain": +300, "maintenance": 0}
    target_calories = tdee + adjustments.get(goal, 0)
    
    # Protein needs
    protein_per_kg = 2.2 if goal in ["muscle_gain", "weight_loss"] else 1.6
    protein_grams = weight * protein_per_kg
    
    return f"""
🧮 NUTRITIONAL NEEDS:

Personal Info:
- Gender: {gender.title()}, Age: {age}, Weight: {weight}kg, Height: {height}cm
- Activity: {activity.replace('_', ' ').title()}

Caloric Needs:
- BMR: {bmr:.0f} calories/day
- TDEE: {tdee:.0f} calories/day
- Target for {goal.replace('_', ' ').title()}: {target_calories:.0f} calories/day

Protein Requirements:
- Daily Protein: {protein_grams:.0f}g
- Per meal: {protein_grams/3:.0f}g (3 meals)

Hydration:
- Daily Water: {weight * 35:.0f}ml ({weight * 35/250:.1f} glasses)
"""

# =============================================================================
# FITNESS AI SYSTEM WITH REAL OPENAI
# =============================================================================

def create_fitness_ai_system():
    """Create fitness AI system with real OpenAI."""
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables!")
    
    try:
        from langchain_openai import ChatOpenAI
        
        # Create OpenAI model
        model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
            api_key=api_key
        )
        
        # Create agents
        workout_specialist = create_react_agent(
            model=model,
            tools=[create_workout_plan, calculate_training_metrics],
            name="workout_specialist",
            prompt="You are a certified personal trainer. Create workout plans and calculate fitness metrics. Use tools when appropriate and provide detailed, actionable advice."
        )
        
        nutritionist = create_react_agent(
            model=model,
            tools=[create_meal_plan, calculate_nutrition_needs],
            name="nutritionist",
            prompt="You are a registered dietitian. Create meal plans and provide nutrition advice. Use tools when appropriate and focus on evidence-based recommendations."
        )
        
        # Create supervisor
        workflow = create_supervisor(
            agents=[workout_specialist, nutritionist],
            model=model,
            prompt="""You coordinate fitness consultations with specialists:
            
            - workout_specialist: handles exercise plans and fitness metrics
            - nutritionist: handles meal plans and nutrition advice
            
            Analyze user requests and delegate to appropriate specialists.
            For comprehensive plans, coordinate both specialists.
            Be helpful, professional, and encouraging."""
        )
        
        # Return compiled workflow for LangGraph Studio
        return workflow.compile()
        
    except Exception as e:
        raise RuntimeError(f"Error creating fitness AI system: {e}")

def create_fitness_ai_system_with_logging():
    """Create fitness AI system with console logging for direct execution."""
    
    print("🤖 FITNESS AI WITH REAL OPENAI")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("📝 Please check your .env file contains:")
        print("   OPENAI_API_KEY=your_api_key_here")
        return None
    
    print(f"🔑 API Key: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        from langchain_openai import ChatOpenAI
        
        # Create OpenAI model
        model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
            api_key=api_key
        )
        
        print("✅ OpenAI model initialized")
        
        # Create agents
        print("📋 Creating agents...")
        
        workout_specialist = create_react_agent(
            model=model,
            tools=[create_workout_plan, calculate_training_metrics],
            name="workout_specialist",
            prompt="You are a certified personal trainer. Create workout plans and calculate fitness metrics. Use tools when appropriate and provide detailed, actionable advice."
        )
        
        nutritionist = create_react_agent(
            model=model,
            tools=[create_meal_plan, calculate_nutrition_needs],
            name="nutritionist",
            prompt="You are a registered dietitian. Create meal plans and provide nutrition advice. Use tools when appropriate and focus on evidence-based recommendations."
        )
        
        print("✅ Agents created")
        
        # Create supervisor
        print("🎯 Creating supervisor...")
        workflow = create_supervisor(
            agents=[workout_specialist, nutritionist],
            model=model,
            prompt="""You coordinate fitness consultations with specialists:
            
            - workout_specialist: handles exercise plans and fitness metrics
            - nutritionist: handles meal plans and nutrition advice
            
            Analyze user requests and delegate to appropriate specialists.
            For comprehensive plans, coordinate both specialists.
            Be helpful, professional, and encouraging."""
        )
        
        print("✅ Supervisor created")
        
        # Compile workflow
        app = workflow.compile()
        print("✅ System ready!")
        
        return app
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def run_fitness_consultation():
    """Run interactive fitness consultation."""
    
    fitness_ai = create_fitness_ai_system_with_logging()
    if not fitness_ai:
        return
    
    print("\n💬 INTERACTIVE FITNESS CONSULTATION")
    print("=" * 50)
    print("Ask about workouts, nutrition, or both!")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    session_count = 0
    
    while True:
        try:
            user_input = input("\n🤔 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using Fitness AI!")
                break
            
            if not user_input:
                continue
            
            session_count += 1
            print(f"\n🔄 Processing... (Session #{session_count})")
            
            result = fitness_ai.invoke({
                "messages": [HumanMessage(content=user_input)]
            })
            
            # Show response
            final_response = result["messages"][-1]
            print(f"\n🎯 Fitness AI Response:")
            print(final_response.content)
            
            # Show specialists involved
            specialists = []
            for msg in result["messages"]:
                if hasattr(msg, 'name') and msg.name in ['workout_specialist', 'nutritionist']:
                    specialists.append(msg.name)
            
            if specialists:
                unique = list(set(specialists))
                names = {'workout_specialist': '💪 Workout Specialist', 'nutritionist': '🥗 Nutritionist'}
                involved = [names.get(s, s) for s in unique]
                print(f"\n👥 Consulted: {', '.join(involved)}")
            
            print(f"📊 Messages: {len(result['messages'])}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Session ended!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def run_demo_scenarios():
    """Run demo scenarios with real OpenAI."""
    
    fitness_ai = create_fitness_ai_system_with_logging()
    if not fitness_ai:
        return
    
    print("\n🧪 DEMO SCENARIOS WITH REAL OPENAI")
    print("=" * 50)
    
    scenarios = [
        {
            "name": "Weight Loss Plan",
            "query": "I'm 30 years old, want to lose 10kg. Create a workout plan for a beginner, 3 days per week with basic equipment."
        },
        {
            "name": "Muscle Gain Nutrition", 
            "query": "I'm 25, male, 70kg, 175cm, very active. I want to gain muscle. Calculate my nutrition needs and create a meal plan."
        },
        {
            "name": "Complete Fitness Plan",
            "query": "I'm 28, 80kg, 180cm, moderately active. I want to lose fat and gain muscle. Create both workout and nutrition plans."
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🧪 SCENARIO {i}: {scenario['name']}")
        print(f"💬 Query: {scenario['query']}")
        print("-" * 50)
        
        try:
            result = fitness_ai.invoke({
                "messages": [HumanMessage(content=scenario["query"])]
            })
            
            print(f"✅ Completed!")
            
            # Show AI response
            final_response = result["messages"][-1]
            print(f"\n🎯 AI Response:")
            print(final_response.content)
            
            # Show specialists
            specialists = []
            for msg in result["messages"]:
                if hasattr(msg, 'name') and msg.name in ['workout_specialist', 'nutritionist']:
                    specialists.append(msg.name)
            
            if specialists:
                unique = list(set(specialists))
                names = {'workout_specialist': '💪 Workout Specialist', 'nutritionist': '🥗 Nutritionist'}
                involved = [names.get(s, s) for s in unique]
                print(f"\n👥 Involved: {', '.join(involved)}")
            
            print(f"📊 Messages: {len(result['messages'])}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 50)
    
    print("\n🎉 DEMO COMPLETED!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo_scenarios()
    else:
        run_fitness_consultation()
