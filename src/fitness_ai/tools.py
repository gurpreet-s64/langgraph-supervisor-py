"""
Fitness AI Tools

Specialized tools for workout planning and nutrition advice.
Each tool is designed to provide specific fitness-related functionality.
"""

from typing import Dict, Any
from langchain_core.tools import tool


# =============================================================================
# WORKOUT SPECIALIST TOOLS
# =============================================================================

@tool
def create_workout_plan(goal: str, level: str, days: int, equipment: str = "basic") -> str:
    """
    Create a personalized workout plan based on user's fitness goals and constraints.
    
    Args:
        goal: Primary fitness goal (weight_loss, muscle_gain, strength, endurance, general_fitness)
        level: User's experience level (beginner, intermediate, advanced)
        days: Number of days per week available for workouts (1-7)
        equipment: Available equipment (none, basic, gym, home_gym)
    
    Returns:
        Detailed workout plan with schedule, exercises, and recommendations
    """
    print(f"💪 Workout Specialist: Creating {goal} plan for {level} level")
    
    # Workout plan templates based on goals
    plans = {
        "weight_loss": f"{days}-day fat burning program with cardio and strength training",
        "muscle_gain": f"{days}-day muscle building program with progressive overload",
        "strength": f"{days}-day strength training program focusing on compound movements",
        "endurance": f"{days}-day cardiovascular endurance program",
        "general_fitness": f"{days}-day balanced fitness routine for overall health"
    }
    
    plan = plans.get(goal, plans["general_fitness"])
    
    # Equipment considerations
    equipment_notes = {
        "none": "Bodyweight exercises only - no equipment needed",
        "basic": "Using dumbbells, resistance bands, and bodyweight exercises",
        "gym": "Full gym equipment available - machines, free weights, cardio",
        "home_gym": "Home gym setup with weights, machines, and accessories"
    }
    
    equipment_note = equipment_notes.get(equipment, equipment_notes["basic"])
    
    return f"""
🏋️ WORKOUT PLAN CREATED:
Goal: {goal.replace('_', ' ').title()}
Level: {level.title()}
Schedule: {days} days per week
Equipment: {equipment_note}

Program: {plan}

Key Components:
- Progressive overload principles
- Proper form and technique focus
- Adequate recovery periods
- Injury prevention strategies
- Flexibility and mobility work

Recommendations:
- Start with lighter weights and focus on form
- Gradually increase intensity over time
- Include warm-up and cool-down in each session
- Track progress weekly

Duration: 8-12 weeks with regular assessments and adjustments
"""


@tool
def calculate_training_metrics(weight: float, height: float, age: int, gender: str = "male") -> str:
    """
    Calculate comprehensive fitness and training metrics.
    
    Args:
        weight: Current weight in kg
        height: Height in centimeters
        age: Age in years
        gender: Gender (male/female) for accurate BMR calculation
    
    Returns:
        Detailed fitness metrics including BMI, BMR, heart rate zones, and recommendations
    """
    print(f"💪 Workout Specialist: Calculating metrics for {age}yr old {gender}")
    
    # BMI calculation
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    
    # BMI classification
    if bmi < 18.5:
        bmi_category = "Underweight"
    elif 18.5 <= bmi < 25:
        bmi_category = "Normal weight"
    elif 25 <= bmi < 30:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obese"
    
    # BMR calculation using Mifflin-St Jeor equation
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Heart rate zones
    max_hr = 220 - age
    fat_burn_zone = (int(max_hr * 0.6), int(max_hr * 0.7))
    cardio_zone = (int(max_hr * 0.7), int(max_hr * 0.85))
    peak_zone = (int(max_hr * 0.85), int(max_hr * 0.95))
    
    # TDEE estimates for different activity levels
    tdee_sedentary = bmr * 1.2
    tdee_moderate = bmr * 1.55
    tdee_active = bmr * 1.725
    
    return f"""
📊 FITNESS METRICS CALCULATED:

Body Composition:
- BMI: {bmi:.1f} ({bmi_category})
- Height: {height} cm
- Weight: {weight} kg

Metabolic Rate:
- BMR (Base Metabolic Rate): {bmr:.0f} calories/day
- TDEE Estimates:
  • Sedentary: {tdee_sedentary:.0f} calories/day
  • Moderate Activity: {tdee_moderate:.0f} calories/day
  • Very Active: {tdee_active:.0f} calories/day

Heart Rate Training Zones:
- Fat Burn Zone: {fat_burn_zone[0]}-{fat_burn_zone[1]} bpm (60-70% max HR)
- Cardio Zone: {cardio_zone[0]}-{cardio_zone[1]} bpm (70-85% max HR)
- Peak Zone: {peak_zone[0]}-{peak_zone[1]} bpm (85-95% max HR)
- Maximum Heart Rate: {max_hr} bpm

Training Recommendations:
- Monitor heart rate during workouts
- Track progress with weekly measurements
- Adjust calorie intake based on activity level
- Focus on consistency over intensity for beginners
"""


# =============================================================================
# NUTRITIONIST TOOLS
# =============================================================================

@tool
def create_meal_plan(goal: str, calories: int, restrictions: str = "none") -> str:
    """
    Create a personalized meal plan based on dietary goals and restrictions.
    
    Args:
        goal: Primary dietary goal (weight_loss, muscle_gain, maintenance, performance)
        calories: Target daily calories
        restrictions: Dietary restrictions (vegetarian, vegan, gluten_free, dairy_free, none)
    
    Returns:
        Detailed meal plan with macronutrient breakdown and food recommendations
    """
    print(f"🥗 Nutritionist: Creating {goal} meal plan with {calories} calories")
    
    # Macronutrient ratios based on goals
    ratios = {
        "weight_loss": {"protein": 30, "carbs": 35, "fat": 35},
        "muscle_gain": {"protein": 25, "carbs": 45, "fat": 30},
        "maintenance": {"protein": 20, "carbs": 50, "fat": 30},
        "performance": {"protein": 20, "carbs": 55, "fat": 25}
    }
    
    ratio = ratios.get(goal, ratios["maintenance"])
    
    # Calculate macros in grams
    protein_g = (calories * ratio["protein"] / 100) / 4
    carbs_g = (calories * ratio["carbs"] / 100) / 4
    fat_g = (calories * ratio["fat"] / 100) / 9
    
    # Food recommendations based on restrictions
    food_recommendations = {
        "none": {
            "protein": "Chicken, fish, eggs, Greek yogurt, lean beef, cottage cheese",
            "carbs": "Rice, oats, sweet potato, quinoa, fruits, whole grain bread",
            "fats": "Avocado, nuts, olive oil, salmon, seeds"
        },
        "vegetarian": {
            "protein": "Eggs, Greek yogurt, legumes, tofu, cheese, protein powder",
            "carbs": "Rice, oats, sweet potato, quinoa, fruits, whole grains",
            "fats": "Avocado, nuts, olive oil, seeds, nut butters"
        },
        "vegan": {
            "protein": "Legumes, tofu, tempeh, seitan, plant protein powder, nuts",
            "carbs": "Rice, oats, sweet potato, quinoa, fruits, whole grains",
            "fats": "Avocado, nuts, olive oil, seeds, tahini, coconut"
        },
        "gluten_free": {
            "protein": "Chicken, fish, eggs, Greek yogurt, legumes, quinoa",
            "carbs": "Rice, quinoa, sweet potato, fruits, GF oats, potatoes",
            "fats": "Avocado, nuts, olive oil, salmon, seeds"
        },
        "dairy_free": {
            "protein": "Chicken, fish, eggs, legumes, tofu, plant protein",
            "carbs": "Rice, oats, sweet potato, quinoa, fruits, vegetables",
            "fats": "Avocado, nuts, olive oil, coconut oil, seeds"
        }
    }
    
    foods = food_recommendations.get(restrictions, food_recommendations["none"])
    
    return f"""
🍽️ PERSONALIZED MEAL PLAN:
Goal: {goal.replace('_', ' ').title()}
Daily Calories: {calories}
Dietary Restrictions: {restrictions.replace('_', ' ').title()}

MACRONUTRIENT BREAKDOWN:
- Protein: {protein_g:.0f}g ({ratio['protein']}% of calories)
- Carbohydrates: {carbs_g:.0f}g ({ratio['carbs']}% of calories)
- Fats: {fat_g:.0f}g ({ratio['fat']}% of calories)

MEAL STRUCTURE:
- 3 main meals + 2 healthy snacks
- Protein with every meal (aim for {protein_g/5:.0f}g per meal/snack)
- Vegetables with lunch and dinner
- Pre/post workout nutrition timing

FOOD RECOMMENDATIONS:
Protein Sources: {foods['protein']}
Carbohydrate Sources: {foods['carbs']}
Healthy Fats: {foods['fats']}

HYDRATION & TIMING:
- 8-10 glasses of water daily
- Extra water around workouts
- Eat protein within 2 hours post-workout
- Space meals 3-4 hours apart

Duration: Follow for 2-4 weeks, then reassess and adjust based on progress
"""


@tool
def calculate_nutrition_needs(weight: float, height: float, age: int, gender: str, activity: str, goal: str) -> str:
    """
    Calculate detailed nutritional needs including calories, macros, and hydration.
    
    Args:
        weight: Weight in kg
        height: Height in centimeters
        age: Age in years
        gender: Gender (male/female)
        activity: Activity level (sedentary, light, moderate, active, very_active)
        goal: Nutrition goal (weight_loss, muscle_gain, maintenance)
    
    Returns:
        Comprehensive nutritional analysis with personalized recommendations
    """
    print(f"🥗 Nutritionist: Calculating nutrition needs for {gender}, {age} years old")
    
    # BMR calculation using Mifflin-St Jeor equation
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Activity multipliers
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    
    tdee = bmr * multipliers.get(activity, 1.55)
    
    # Goal adjustments
    adjustments = {
        "weight_loss": -500,  # 1 lb per week loss
        "muscle_gain": +300,  # Lean bulk
        "maintenance": 0
    }
    
    target_calories = tdee + adjustments.get(goal, 0)
    
    # Protein needs (higher for muscle gain/weight loss)
    if goal in ["muscle_gain", "weight_loss"]:
        protein_per_kg = 2.2  # Higher protein for body composition goals
    else:
        protein_per_kg = 1.6  # Moderate protein for maintenance
    
    protein_grams = weight * protein_per_kg
    
    # Hydration needs
    base_water = weight * 35  # 35ml per kg base requirement
    exercise_water = 500 if activity in ["active", "very_active"] else 250
    total_water = base_water + exercise_water
    
    return f"""
🧮 COMPREHENSIVE NUTRITIONAL NEEDS:

Personal Information:
- Gender: {gender.title()}
- Age: {age} years
- Weight: {weight} kg
- Height: {height} cm
- Activity Level: {activity.replace('_', ' ').title()}

Caloric Requirements:
- BMR (Base Metabolic Rate): {bmr:.0f} calories/day
- TDEE (Total Daily Energy): {tdee:.0f} calories/day
- Target Calories for {goal.replace('_', ' ').title()}: {target_calories:.0f} calories/day

Protein Requirements:
- Daily Protein Target: {protein_grams:.0f}g
- Protein per meal (5 meals): {protein_grams/5:.0f}g
- Protein per kg body weight: {protein_per_kg:.1f}g/kg

Hydration Requirements:
- Daily Water Target: {total_water:.0f}ml ({total_water/250:.1f} glasses)
- Base requirement: {base_water:.0f}ml
- Exercise addition: {exercise_water}ml
- Pre-workout: 250ml (1 hour before)
- During workout: 150-250ml every 15-20 minutes
- Post-workout: 150% of fluid lost through sweat

Micronutrient Focus Areas:
- Vitamin D: Bone health and immune function
- B-Complex: Energy metabolism
- Iron: Oxygen transport (especially for active individuals)
- Omega-3: Anti-inflammatory and recovery
- Magnesium: Muscle function and recovery
- Zinc: Immune function and protein synthesis

Meal Timing Recommendations:
- Eat within 1 hour of waking
- Pre-workout: Carbs 1-2 hours before
- Post-workout: Protein + carbs within 30 minutes
- Last meal: 2-3 hours before bed
"""


# =============================================================================
# TOOL COLLECTIONS
# =============================================================================

# Workout specialist tools
workout_tools = [
    create_workout_plan,
    calculate_training_metrics
]

# Nutritionist tools
nutrition_tools = [
    create_meal_plan,
    calculate_nutrition_needs
]

# All fitness tools
all_fitness_tools = workout_tools + nutrition_tools 