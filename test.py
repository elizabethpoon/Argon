import random
import numpy as np
from datascience import *
import matplotlib
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

class Calories: 
    """
    This class allows users to obtain personalized calorie plans based on their input and the guidelines provided in the text file. The calculation considers factors such as user's height, weight, sport intensity, and daily activity level to provide tailored calorie plans for maintenance, shredding, and bulking.
    """
    #Michael: f-strings and input() function
    
    def __init__(self, name, height, weight, age, allergies, sport, daily_activity):
        self.name = input("Name: ")
        self.height = input("Height: ")
        self.weight = input("Weight: ")
        self.age = input("Age: ")
        self.allergies = input("Allergies: ")
        self.sport = input("Sport: ")
        self.daily_activity = input("Daily Activities: ")

        print (f"This is {name}. Their height is {height}. Their weight is {weight}. Their age is {age}. The allergies that they have are {allergies}. The sport they play is {sport}. Their daily activities include {daily_activity}.")

    def _read_guidelines(self, goal):
        with open(self.guidelines_file, 'r', encoding = 'utf-8') as file:
            for line in file:
                if line.startswith(goal):
                    return next(file).strip()

    def calculate_maintenance_calories(self):
        guidelines = self._read_guidelines("maintenance")
        return self.calculate_custom_calories(guidelines)

    def calculate_shred_calories(self):
        guidelines = self._read_guidelines("shred")
        return self.calculate_custom_calories(guidelines)

    def calculate_bulk_calories(self):
        guidelines = self._read_guidelines("bulk")
        return self.calculate_custom_calories(guidelines)

    def calculate_custom_calories(self):
        height_meters = self.height
        weight_kg = self.weight
        activity_level = self.daily_activity
        maintenance_calories = (10 * weight_kg) + (6.25 * height_meters * 100)
        - (5 * 25) + 5
        shred_calories = maintenance_calories - 500  
        bulk_calories = maintenance_calories + 500 
        
        if  self.sport.lower() == "high-intensity":
            maintenance_calories *= 1.3
            shred_calories *= 1.3
            bulk_calories *= 1.3    
        elif activity_level.lower() == "moderate-intensity":
            maintenance_calories *= 1.1
            shred_calories *= 1.1
            bulk_calories *= 1.1
        if activity_level.lower() == "lightly active":
            maintenance_calories *= 1.2
            shred_calories *= 1.2
            bulk_calories *= 1.2  
        elif activity_level.lower() == "average":
            maintenance_calories *= 1.5
            shred_calories *= 1.5
            bulk_calories *= 1.5   
        elif activity_level.lower() == "very active":
            maintenance_calories *= 1.8
            shred_calories *= 1.8
            bulk_calories *= 1.8
        return {
            "maintenance": maintenance_calories,
            "shred": shred_calories,
            "bulk": bulk_calories
        }
#Elizabeth: f-strings, optional parameters, sequence unpacking
    def calculate_nutrition_plan(self, calories, goal):
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
        calories, advice = Calories.calculate_nutrition_plan(calories, goal)
        caloric_intake_info = f"Your daily caloric intake should be approximately {calories} calories."
        if detailed:
            print(f"For your goal to {goal}, {caloric_intake_info}")
            print(advice)
        else:
            print(caloric_intake_info)

    def graph(self, calories):
        '''
        This method seeks to determine how many pounds a person needs to lose per week to get to their desired weight. 

        Args: 
        calories(int): this variable is how many calories a person wants to lose. 
        
        Side effects: 
        Prints a graph to the console
        
        '''
        x = 0
        change = make_array()
        graph = Table.read_table('graph - Sheet1.csv')
        #want this graph to be of four months time, with a tick every week on the x-axis 
        pounds = int(calories) / 3500 
        pounds_per_week = pounds / 16 #this will give the pound change per week 
        
        if goal == "shred": 
            for i in graph.num_rows: 
                x = current_weight - pounds_per_week*i
                change = np.append(change, x)
            
        if goal == "bulk": 
            for i in range(graph.num_rows): 
                x = current_weight + pounds_per_week*i
                change = np.append(change, x)

        new_graph = graph.with_column("Pounds", change)

        print(new_graph.plot("Weekly Basis", "Pounds"))
    
class Meals: 
#Colby: optional parameters and/or keyword arguments, Conditional Expressions,
#F-strings Containing Expressions, Comprehensions or Generator Expressions,
#Use of a Key Function with Sorting/Min/Max Functions

#possible use of JSON once file implementation is complete

#To get meal data it will be given in a different method
#that will be able to read from a file of different meals
#with open(file_path, mode = "r", encoding = "utf-8") as file:
    def give_meal_options(user_allergies=None, user_preferences=None):
        """
        Provides meal options based on user's allergies and preferences

        Args:
            user_allergies (list, optional): A list of user's allergies.
            Defaults to None
            user_preferences (list, optional): A list of user's meal preferences.
            Defaults to None

        Returns:
            list or None: A list of tuples containing meal options (meal name and ingredients),
            or None if no suitable meal options are found
        """
        
        meals_data = {
            "Meal 1": ["chicken", "rice", "broccoli"], 
            "Meal 2": ["beef", "potatoes," "carrots"], 
            "Meal 3": ["salmon, quinoa, asparagus", "peanuts"], 
            "Meal 4": ["pasta", "tomatoes", "spinach"], 
            "Meal 5": ["tofu", "brown rice", "green beans"]
            
        }
#Prompt user to input allergies and preferences
        if user_allergies is None:
            user_allergies = input("Enter your allergies (separate by comma):").strip().split(", ")
        if user_preferences is None:
            user_preferences = input("Enter your meal preferences (separate by comma):").strip().split(", ")

        possible_meals = []
        for meal, ingredients in meals_data.items():
            allergies_present = any(allergy in ingredients for allergy in user_allergies)

            if allergies_present:
                continue
            match_count = sum(1 for preference in user_preferences if preference in ingredients)
            possible_meals.append((meal, ingredients, match_count))

        if len(possible_meals) == 0:
            return None
        sorted_meals = sorted(possible_meals, key=lambda x: (x[2], x[0]), reverse=True)
        num_meals_to_select = min(3, len(possible_meals))
        meal_options = random.sample(sorted_meals[:num_meals_to_select], num_meals_to_select)
        
        if meal_options:
            print("Here are your 3 meal options:")
            for meal_index in range(len(meal_options)):
                meal, ingredients, _ = meal_options[meal_index]
                print(f"{meal}: {', '.join(ingredients)}")
        else:
            print("Sorry, we couldn't find suitable meal options for your allergies and preferences.")
        return meal_options
        # Usage example:
    give_meal_options()
#no file path has been created yet