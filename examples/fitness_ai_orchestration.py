#!/usr/bin/env python3
"""
Fitness AI Orchestration Workflow
A LangGraph multi-agent system with:
- Supervisor Agent: Orchestrates fitness consultations
- Workout Specialist Agent: Creates exercise plans and routines
- Nutritionist Agent: Provides diet plans and nutrition advice
"""

import os
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from langgraph_supervisor import create_supervisor


# =============================================================================
# WORKOUT SPECIALIST TOOLS
# =============================================================================

@tool
def create_workout_plan(
    fitness_goal: str, 
    experience_level: str, 
    available_days: int,
    equipment: str = "basic"
) -> str:
    """Create a personalized workout plan based on user's goals and constraints.
    
    Args:
        fitness_goal: Primary fitness goal (weight_loss, muscle_gain, strength, endurance, general_fitness)
        experience_level: User's experience (beginner, intermediate, advanced)
        available_days: Number of days per week available for workouts (1-7)
        equipment: Available equipment (none, basic, gym, home_gym)
    """
    print(f"💪 Workout Specialist: Creating {fitness_goal} plan for {experience_level} level")
    
    # Workout plan templates based on goals
    workout_plans = {
        "weight_loss": {
            "beginner": "3-day full body circuit training with cardio intervals",
            "intermediate": "4-day upper/lower split with HIIT sessions",
            "advanced": "5-day push/pull/legs with daily cardio"
        },
        "muscle_gain": {
            "beginner": "3-day full body strength training",
            "intermediate": "4-day upper/lower split with progressive overload",
            "advanced": "6-day push/pull/legs with isolation work"
        },
        "strength": {
            "beginner": "3-day compound movement focus",
            "intermediate": "4-day powerlifting style training",
            "advanced": "5-day strength specialization program"
        },
        "endurance": {
            "beginner": "3-day cardio base building",
            "intermediate": "4-day mixed cardio training",
            "advanced": "6-day endurance specialization"
        },
        "general_fitness": {
            "beginner": "3-day balanced fitness routine",
            "intermediate": "4-day functional fitness program",
            "advanced": "5-day comprehensive fitness plan"
        }
    }
    
    base_plan = workout_plans.get(fitness_goal, workout_plans["general_fitness"])
    plan_description = base_plan.get(experience_level, base_plan["beginner"])
    
    # Adjust for available days
    if available_days < 3:
        plan_description = f"Modified 2-day version: {plan_description}"
    elif available_days > 5:
        plan_description = f"Extended {available_days}-day version: {plan_description}"
    
    # Equipment considerations
    equipment_notes = {
        "none": "Bodyweight exercises only",
        "basic": "Using dumbbells, resistance bands, and bodyweight",
        "gym": "Full gym equipment available",
        "home_gym": "Home gym setup with weights and machines"
    }
    
    equipment_note = equipment_notes.get(equipment, equipment_notes["basic"])
    
    return f"""
🏋️ WORKOUT PLAN CREATED:
Goal: {fitness_goal.replace('_', ' ').title()}
Level: {experience_level.title()}
Schedule: {available_days} days per week
Equipment: {equipment_note}

Plan: {plan_description}

Key Focus Areas:
- Progressive overload principles
- Proper form and technique
- Recovery and rest days
- Injury prevention strategies

Recommended duration: 8-12 weeks before reassessment
"""


@tool
def suggest_exercise_modifications(
    exercise_name: str,
    limitation: str,
    fitness_level: str = "intermediate"
) -> str:
    """Suggest exercise modifications for injuries, limitations, or equipment constraints.
    
    Args:
        exercise_name: Name of the exercise to modify
        limitation: Type of limitation (knee_injury, back_pain, no_equipment, etc.)
        fitness_level: User's fitness level for appropriate modifications
    """
    print(f"💪 Workout Specialist: Modifying {exercise_name} for {limitation}")
    
    modifications = {
        "squats": {
            "knee_injury": "Wall sits, chair squats, or partial range squats",
            "back_pain": "Goblet squats with proper form, box squats",
            "no_equipment": "Bodyweight squats, jump squats, single-leg squats"
        },
        "deadlifts": {
            "back_pain": "Romanian deadlifts, trap bar deadlifts, or hip hinges",
            "knee_injury": "Single-leg RDLs, good mornings",
            "no_equipment": "Single-leg deadlifts, glute bridges"
        },
        "push_ups": {
            "wrist_pain": "Push-ups on fists, incline push-ups",
            "shoulder_injury": "Wall push-ups, chest press with bands",
            "too_difficult": "Knee push-ups, incline push-ups"
        },
        "running": {
            "knee_injury": "Swimming, cycling, elliptical training",
            "back_pain": "Walking, water jogging, recumbent bike",
            "no_equipment": "Walking, stair climbing, bodyweight cardio"
        }
    }
    
    exercise_mods = modifications.get(exercise_name.lower(), {})
    modification = exercise_mods.get(limitation, f"Consult with a physical therapist for {exercise_name} modifications")
    
    return f"""
🔧 EXERCISE MODIFICATION:
Original Exercise: {exercise_name.title()}
Limitation: {limitation.replace('_', ' ').title()}
Fitness Level: {fitness_level.title()}

Recommended Modification: {modification}

Additional Tips:
- Start with lower intensity and progress gradually
- Focus on proper form over speed or weight
- Listen to your body and stop if pain occurs
- Consider working with a qualified trainer
"""


@tool
def calculate_training_metrics(
    current_weight: float,
    target_weight: float,
    height_cm: float,
    age: int,
    activity_level: str = "moderate"
) -> str:
    """Calculate training metrics like BMI, target heart rate zones, and calorie burn estimates.
    
    Args:
        current_weight: Current weight in kg
        target_weight: Target weight in kg
        height_cm: Height in centimeters
        age: Age in years
        activity_level: Activity level (sedentary, light, moderate, active, very_active)
    """
    print(f"💪 Workout Specialist: Calculating training metrics for user")
    
    # Calculate BMI
    height_m = height_cm / 100
    current_bmi = current_weight / (height_m ** 2)
    target_bmi = target_weight / (height_m ** 2)
    
    # Calculate target heart rate zones
    max_hr = 220 - age
    fat_burn_zone = (int(max_hr * 0.6), int(max_hr * 0.7))
    cardio_zone = (int(max_hr * 0.7), int(max_hr * 0.85))
    peak_zone = (int(max_hr * 0.85), int(max_hr * 0.95))
    
    # Estimate daily calorie burn for exercise
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    
    # Basic metabolic rate (Mifflin-St Jeor equation - simplified)
    bmr = 10 * current_weight + 6.25 * height_cm - 5 * age + 5  # Male formula
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    
    return f"""
📊 TRAINING METRICS CALCULATED:

Body Composition:
- Current BMI: {current_bmi:.1f}
- Target BMI: {target_bmi:.1f}
- Weight Goal: {abs(target_weight - current_weight):.1f} kg to {'lose' if target_weight < current_weight else 'gain'}

Heart Rate Zones:
- Fat Burn Zone: {fat_burn_zone[0]}-{fat_burn_zone[1]} bpm (60-70% max HR)
- Cardio Zone: {cardio_zone[0]}-{cardio_zone[1]} bpm (70-85% max HR)
- Peak Zone: {peak_zone[0]}-{peak_zone[1]} bpm (85-95% max HR)
- Maximum HR: {max_hr} bpm

Calorie Information:
- Estimated BMR: {bmr:.0f} calories/day
- Estimated TDEE: {tdee:.0f} calories/day
- Activity Level: {activity_level.replace('_', ' ').title()}

Training Recommendations:
- Use heart rate zones to optimize workout intensity
- Track progress with weekly measurements
- Adjust calorie intake based on goals and activity
"""


# =============================================================================
# NUTRITIONIST TOOLS
# =============================================================================

@tool
def create_meal_plan(
    dietary_goal: str,
    dietary_restrictions: str,
    meals_per_day: int = 3,
    calorie_target: int = 2000
) -> str:
    """Create a personalized meal plan based on dietary goals and restrictions.
    
    Args:
        dietary_goal: Primary goal (weight_loss, muscle_gain, maintenance, performance)
        dietary_restrictions: Any restrictions (vegetarian, vegan, gluten_free, dairy_free, none)
        meals_per_day: Number of meals per day (3-6)
        calorie_target: Target daily calories
    """
    print(f"🥗 Nutritionist: Creating {dietary_goal} meal plan with {dietary_restrictions} restrictions")
    
    # Macronutrient ratios based on goals
    macro_ratios = {
        "weight_loss": {"protein": 30, "carbs": 35, "fat": 35},
        "muscle_gain": {"protein": 25, "carbs": 45, "fat": 30},
        "maintenance": {"protein": 20, "carbs": 50, "fat": 30},
        "performance": {"protein": 20, "carbs": 55, "fat": 25}
    }
    
    ratios = macro_ratios.get(dietary_goal, macro_ratios["maintenance"])
    
    # Calculate macros in grams
    protein_cals = calorie_target * (ratios["protein"] / 100)
    carb_cals = calorie_target * (ratios["carbs"] / 100)
    fat_cals = calorie_target * (ratios["fat"] / 100)
    
    protein_grams = protein_cals / 4
    carb_grams = carb_cals / 4
    fat_grams = fat_cals / 9
    
    # Sample meal suggestions based on restrictions
    meal_suggestions = {
        "none": {
            "protein": "Chicken, fish, eggs, Greek yogurt, lean beef",
            "carbs": "Rice, oats, sweet potato, quinoa, fruits",
            "fats": "Avocado, nuts, olive oil, salmon"
        },
        "vegetarian": {
            "protein": "Eggs, Greek yogurt, legumes, tofu, cheese",
            "carbs": "Rice, oats, sweet potato, quinoa, fruits",
            "fats": "Avocado, nuts, olive oil, seeds"
        },
        "vegan": {
            "protein": "Legumes, tofu, tempeh, seitan, protein powder",
            "carbs": "Rice, oats, sweet potato, quinoa, fruits",
            "fats": "Avocado, nuts, olive oil, seeds, tahini"
        },
        "gluten_free": {
            "protein": "Chicken, fish, eggs, Greek yogurt, legumes",
            "carbs": "Rice, quinoa, sweet potato, fruits, GF oats",
            "fats": "Avocado, nuts, olive oil, salmon"
        }
    }
    
    suggestions = meal_suggestions.get(dietary_restrictions, meal_suggestions["none"])
    
    return f"""
🍽️ PERSONALIZED MEAL PLAN:

Goal: {dietary_goal.replace('_', ' ').title()}
Restrictions: {dietary_restrictions.replace('_', ' ').title()}
Daily Calories: {calorie_target}
Meals per Day: {meals_per_day}

MACRONUTRIENT BREAKDOWN:
- Protein: {protein_grams:.0f}g ({ratios['protein']}% of calories)
- Carbohydrates: {carb_grams:.0f}g ({ratios['carbs']}% of calories)
- Fats: {fat_grams:.0f}g ({ratios['fat']}% of calories)

FOOD RECOMMENDATIONS:
Protein Sources: {suggestions['protein']}
Carbohydrate Sources: {suggestions['carbs']}
Healthy Fats: {suggestions['fats']}

MEAL TIMING TIPS:
- Eat protein with every meal
- Have carbs around workouts
- Include vegetables with most meals
- Stay hydrated (8-10 glasses water/day)
- Plan and prep meals in advance

Duration: Follow for 2-4 weeks, then reassess and adjust
"""


@tool
def calculate_nutrition_needs(
    weight: float,
    height_cm: float,
    age: int,
    gender: str,
    activity_level: str,
    goal: str
) -> str:
    """Calculate detailed nutritional needs including calories, macros, and hydration.
    
    Args:
        weight: Weight in kg
        height_cm: Height in centimeters
        age: Age in years
        gender: Gender (male/female)
        activity_level: Activity level (sedentary, light, moderate, active, very_active)
        goal: Nutrition goal (weight_loss, muscle_gain, maintenance)
    """
    print(f"🥗 Nutritionist: Calculating nutrition needs for {gender}, {age} years old")
    
    # Calculate BMR using Mifflin-St Jeor equation
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
    
    # Activity multipliers
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    
    # Adjust calories based on goal
    goal_adjustments = {
        "weight_loss": -500,  # 1 lb per week loss
        "muscle_gain": +300,  # Lean bulk
        "maintenance": 0
    }
    
    target_calories = tdee + goal_adjustments.get(goal, 0)
    
    # Calculate protein needs (higher for muscle gain/weight loss)
    if goal in ["muscle_gain", "weight_loss"]:
        protein_per_kg = 2.2  # Higher protein
    else:
        protein_per_kg = 1.6  # Moderate protein
    
    protein_grams = weight * protein_per_kg
    
    # Calculate hydration needs
    base_water = weight * 35  # 35ml per kg
    exercise_water = 500 if activity_level in ["active", "very_active"] else 250
    total_water = base_water + exercise_water
    
    return f"""
🧮 NUTRITIONAL NEEDS CALCULATED:

Personal Info:
- Gender: {gender.title()}
- Age: {age} years
- Weight: {weight} kg
- Height: {height_cm} cm
- Activity: {activity_level.replace('_', ' ').title()}

Caloric Needs:
- BMR (Base Metabolic Rate): {bmr:.0f} calories/day
- TDEE (Total Daily Energy): {tdee:.0f} calories/day
- Target Calories for {goal.replace('_', ' ').title()}: {target_calories:.0f} calories/day

Protein Requirements:
- Recommended Protein: {protein_grams:.0f}g per day
- Protein per meal: {protein_grams/3:.0f}g (if 3 meals/day)

Hydration Needs:
- Daily Water Target: {total_water:.0f}ml ({total_water/250:.1f} glasses)
- Pre-workout: 250ml (1 hour before)
- During workout: 150-250ml every 15-20 minutes
- Post-workout: 150% of fluid lost through sweat

Micronutrient Focus:
- Vitamin D, B12, Iron (especially for active individuals)
- Omega-3 fatty acids for recovery
- Antioxidants from colorful fruits and vegetables
"""


@tool
def suggest_pre_post_workout_nutrition(
    workout_type: str,
    workout_duration: int,
    time_of_day: str,
    dietary_restrictions: str = "none"
) -> str:
    """Suggest optimal pre and post-workout nutrition based on workout details.
    
    Args:
        workout_type: Type of workout (strength, cardio, hiit, endurance)
        workout_duration: Duration in minutes
        time_of_day: When working out (morning, afternoon, evening)
        dietary_restrictions: Any dietary restrictions
    """
    print(f"🥗 Nutritionist: Creating pre/post workout nutrition for {workout_type} training")
    
    # Pre-workout recommendations
    pre_workout = {
        "strength": {
            "timing": "30-60 minutes before",
            "foods": "Banana with almond butter, oatmeal with berries, Greek yogurt with honey"
        },
        "cardio": {
            "timing": "30-45 minutes before", 
            "foods": "Toast with jam, banana, small smoothie with fruit"
        },
        "hiit": {
            "timing": "30-45 minutes before",
            "foods": "Apple with small amount of nut butter, dates, small energy bar"
        },
        "endurance": {
            "timing": "1-2 hours before",
            "foods": "Oatmeal with banana, whole grain toast with honey, energy bar"
        }
    }
    
    # Post-workout recommendations
    post_workout = {
        "strength": {
            "timing": "Within 30-60 minutes",
            "foods": "Protein shake with banana, chicken with rice, Greek yogurt with granola"
        },
        "cardio": {
            "timing": "Within 30-45 minutes",
            "foods": "Chocolate milk, smoothie with protein, turkey sandwich"
        },
        "hiit": {
            "timing": "Within 30 minutes",
            "foods": "Protein shake, eggs with toast, recovery smoothie"
        },
        "endurance": {
            "timing": "Within 30 minutes",
            "foods": "Recovery drink, pasta with protein, quinoa bowl with vegetables"
        }
    }
    
    pre_rec = pre_workout.get(workout_type, pre_workout["strength"])
    post_rec = post_workout.get(workout_type, post_workout["strength"])
    
    # Adjust for time of day
    time_adjustments = {
        "morning": "Consider lighter pre-workout options, focus on easily digestible carbs",
        "afternoon": "Normal pre/post workout nutrition timing applies",
        "evening": "Lighter post-workout meals, avoid heavy foods close to bedtime"
    }
    
    time_note = time_adjustments.get(time_of_day, time_adjustments["afternoon"])
    
    # Dietary restriction modifications
    restriction_mods = {
        "vegan": "Replace dairy with plant-based alternatives, use plant proteins",
        "vegetarian": "Include eggs and dairy, focus on complete proteins",
        "gluten_free": "Use gluten-free grains and certified products",
        "dairy_free": "Use non-dairy milk alternatives and dairy-free proteins"
    }
    
    restriction_note = restriction_mods.get(dietary_restrictions, "No special modifications needed")
    
    return f"""
🏃‍♂️ PRE & POST WORKOUT NUTRITION:

Workout Details:
- Type: {workout_type.title()}
- Duration: {workout_duration} minutes
- Time: {time_of_day.title()}
- Restrictions: {dietary_restrictions.replace('_', ' ').title()}

PRE-WORKOUT NUTRITION:
Timing: {pre_rec['timing']}
Recommended Foods: {pre_rec['foods']}
Goal: Provide energy, prevent hunger, optimize performance

POST-WORKOUT NUTRITION:
Timing: {post_rec['timing']}
Recommended Foods: {post_rec['foods']}
Goal: Muscle recovery, glycogen replenishment, adaptation

TIME-SPECIFIC CONSIDERATIONS:
{time_note}

DIETARY MODIFICATIONS:
{restriction_note}

HYDRATION REMINDERS:
- Pre-workout: 250ml water 1 hour before
- During: 150-250ml every 15-20 minutes
- Post: 150% of fluid lost through sweat

GENERAL TIPS:
- Avoid high fiber/fat foods immediately pre-workout
- Include both carbs and protein post-workout
- Listen to your body and adjust portions as needed
"""


# =============================================================================
# FITNESS AI ORCHESTRATION SYSTEM
# =============================================================================

def create_fitness_ai_system():
    """Create the complete fitness AI orchestration system."""
    
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        print("🔑 OpenAI API key found - using real OpenAI models")
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    else:
        print("⚠️  No OpenAI API key found - using mock model for demo")
        print("   Set OPENAI_API_KEY environment variable to use real OpenAI")
        
        # Use mock model for demo
        from simple_demo import FakeChatModel
        
        # Predefined responses for demo
        workout_responses = [
            AIMessage(content="I'll create a personalized workout plan for you."),
            AIMessage(content="Let me analyze your fitness metrics and suggest modifications."),
            AIMessage(content="Here's your customized exercise program.")
        ]
        
        nutrition_responses = [
            AIMessage(content="I'll design a nutrition plan tailored to your goals."),
            AIMessage(content="Let me calculate your specific nutritional needs."),
            AIMessage(content="Here are my pre and post-workout nutrition recommendations.")
        ]
        
        supervisor_responses = [
            AIMessage(content="I'll coordinate your fitness consultation with our specialists."),
            AIMessage(content="Let me connect you with the right expert for your needs."),
            AIMessage(content="Your comprehensive fitness plan is ready.")
        ]
        
        workout_model = FakeChatModel(responses=workout_responses)
        nutrition_model = FakeChatModel(responses=nutrition_responses)
        supervisor_model = FakeChatModel(responses=supervisor_responses)
    
    if api_key:
        # Use same model for all agents when using real OpenAI
        workout_model = nutrition_model = supervisor_model = model
    
    print("\n📋 Creating specialized fitness agents...")
    
    # Create Workout Specialist Agent
    workout_specialist = create_react_agent(
        model=workout_model,
        tools=[
            create_workout_plan,
            suggest_exercise_modifications,
            calculate_training_metrics
        ],
        name="workout_specialist",
        prompt="""You are a certified personal trainer and workout specialist. Your expertise includes:
        - Creating personalized workout plans for all fitness levels
        - Modifying exercises for injuries and limitations
        - Calculating training metrics and heart rate zones
        - Providing exercise form and technique guidance
        
        Always prioritize safety and proper progression. Ask clarifying questions when needed
        and provide detailed, actionable workout recommendations."""
    )
    
    # Create Nutritionist Agent
    nutritionist = create_react_agent(
        model=nutrition_model,
        tools=[
            create_meal_plan,
            calculate_nutrition_needs,
            suggest_pre_post_workout_nutrition
        ],
        name="nutritionist",
        prompt="""You are a registered dietitian and sports nutritionist. Your expertise includes:
        - Creating personalized meal plans for various goals
        - Calculating precise nutritional needs
        - Optimizing pre and post-workout nutrition
        - Accommodating dietary restrictions and preferences
        
        Focus on evidence-based nutrition recommendations that support the user's fitness goals.
        Always consider individual needs, preferences, and any dietary restrictions."""
    )
    
    print("✅ Created workout_specialist and nutritionist agents")
    
    # Create Supervisor Agent
    print("\n🎯 Creating fitness AI supervisor...")
    workflow = create_supervisor(
        agents=[workout_specialist, nutritionist],
        model=supervisor_model,
        prompt="""You are a fitness AI coordinator managing a team of specialists:
        
        🏋️ WORKOUT SPECIALIST: Handles exercise plans, workout modifications, training metrics
        🥗 NUTRITIONIST: Manages meal plans, nutrition calculations, pre/post workout nutrition
        
        Your role is to:
        1. Analyze user requests and determine which specialist(s) to involve
        2. Coordinate between specialists when comprehensive plans are needed
        3. Ensure all aspects of fitness and nutrition are addressed
        4. Provide cohesive, integrated recommendations
        
        For workout-related questions → delegate to workout_specialist
        For nutrition-related questions → delegate to nutritionist
        For comprehensive fitness plans → coordinate both specialists
        
        Always ensure user safety and provide holistic fitness guidance."""
    )
    
    print("✅ Fitness AI supervisor created")
    
    # Compile the workflow
    print("\n⚙️  Compiling fitness AI workflow...")
    app = workflow.compile()
    print("✅ Fitness AI orchestration system ready!")
    
    return app


def run_fitness_ai_demo():
    """Run comprehensive fitness AI orchestration demo."""
    print("🤖 FITNESS AI ORCHESTRATION SYSTEM")
    print("=" * 60)
    print("🏋️ Workout Specialist + 🥗 Nutritionist + 🎯 AI Supervisor")
    print("=" * 60)
    
    try:
        # Create the fitness AI system
        fitness_ai = create_fitness_ai_system()
        
        # Demo scenarios
        scenarios = [
            {
                "name": "Beginner Weight Loss Plan",
                "query": "I'm a 30-year-old beginner who wants to lose 10kg. I can workout 3 days a week and have basic equipment at home. Can you create a complete fitness and nutrition plan?",
                "description": "Comprehensive plan requiring both workout and nutrition expertise"
            },
            {
                "name": "Muscle Gain Nutrition",
                "query": "I'm trying to gain muscle mass. I'm 25 years old, 70kg, 175cm tall, and very active. What should my daily nutrition look like?",
                "description": "Nutrition-focused query for muscle gain"
            },
            {
                "name": "Exercise Modification",
                "query": "I have a knee injury but want to keep training my legs. Can you suggest safe alternatives to squats and lunges?",
                "description": "Workout modification for injury"
            },
            {
                "name": "Pre-Workout Nutrition",
                "query": "I do HIIT workouts in the morning for 45 minutes. What should I eat before and after my workout?",
                "description": "Specific nutrition timing question"
            },
            {
                "name": "Complete Fitness Assessment",
                "query": "I'm 28 years old, 80kg, 180cm, moderately active. I want to lose fat and gain muscle. Create a complete plan with workouts, nutrition, and metrics tracking.",
                "description": "Full orchestration requiring all specialists"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🧪 SCENARIO {i}: {scenario['name']}")
            print(f"📝 Description: {scenario['description']}")
            print(f"💬 User Query: {scenario['query']}")
            print("-" * 60)
            
            try:
                result = fitness_ai.invoke({
                    "messages": [HumanMessage(content=scenario["query"])]
                })
                
                print(f"✅ Scenario {i} completed successfully!")
                print(f"📊 Messages in conversation: {len(result['messages'])}")
                
                # Show the final comprehensive response
                final_response = result["messages"][-1]
                print(f"\n🎯 AI Coordinator Response:")
                print(f"{final_response.content}")
                
                # Show which specialists were involved
                specialist_calls = []
                for msg in result["messages"]:
                    if hasattr(msg, 'name') and msg.name in ['workout_specialist', 'nutritionist']:
                        specialist_calls.append(msg.name)
                
                if specialist_calls:
                    unique_specialists = list(set(specialist_calls))
                    print(f"\n👥 Specialists Involved: {', '.join(unique_specialists)}")
                
            except Exception as e:
                print(f"❌ Error in scenario {i}: {e}")
            
            print("\n" + "=" * 60)
        
        print("\n🎉 FITNESS AI ORCHESTRATION DEMO COMPLETED!")
        print("\n💡 System Capabilities Demonstrated:")
        print("  🏋️ Personalized workout plan creation")
        print("  🥗 Custom nutrition and meal planning")
        print("  🔧 Exercise modifications for limitations")
        print("  📊 Training metrics and calculations")
        print("  🎯 Intelligent task delegation")
        print("  🤝 Multi-agent coordination")
        print("  🔄 Comprehensive fitness orchestration")
        
        if not os.getenv("OPENAI_API_KEY"):
            print("\n🔧 To use with real AI:")
            print("   export OPENAI_API_KEY=your_api_key_here")
            print("   python fitness_ai_orchestration.py")
            
    except Exception as e:
        print(f"❌ Error running fitness AI demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_fitness_ai_demo() 