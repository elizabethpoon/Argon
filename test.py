#Elizabeth: f-strings, optional parameters, sequence unpacking
def calculate_nutrition_plan(calories, goal):
    calories = calories.calculate_maintenance_calories()
    if goal == 'shred':
        calories = calories.calculate_shred_calories()
        advice = "Focus on high protein intake and increase cardio."
    elif goal == 'bulk':
        calories = calories.calculate_bulk_calories()
        advice = "Ensure you are getting enough carbs and protein for recovery."
    else: 
        advice = "Maintain a balanced diet to keep your current body weight."
    return calories, advice
def display_nutrition_calories(calories, goal, detailed=True):
    calories, advice = calculate_nutrition_plan(calories, goal)
    caloric_intake_info = f"Your daily caloric intake should be approximately {calories} calories."
    if detailed:
        print(f"For your goal to {goal}, {caloric_intake_info}")
        print(advice)
    else:
        print(caloric_intake_info)