'''
The purpose of this script is to produce nutrition-based information regarding a user's input, such as their weight, height, goals, allergies, etc. 
This information includes calorie-intake suggestions, a line graph for weight change, BMI and its comparisons to other people, and finally a list of meals the user could consume. 
'''
import pandas as pd
import random
import numpy as np
from datascience import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

class User:
    def get_user_info(self):
        self.name = input("Name: ")
        self.height = float(input("Height (in meters): "))
        self.weight = float(input("Weight (in kg): "))
        self.age = int(input("Age: "))
        self.sport = input("Sport (high-intensity/moderate-intensity): ")
        self.daily_activity = input("Daily Activities (lightly active/average/very active): ")

        print(f"This is {self.name}. Their height is {self.height}. Their weight is {self.weight}. Their age is {self.age}. The sport they play is {self.sport}. Their daily activities include {self.daily_activity}.")

class Calories:
    def __init__(self, guidelines_file, user_height, user_weight, user_age, user_sport, user_daily_activity):
        self.guidelines_file = guidelines_file
        self.height = user_height
        self.weight = user_weight
        self.age = user_age  # Add user's age as an attribute
        self.sport = user_sport
        self.daily_activity = user_daily_activity

    def _read_guidelines(self, goal):
        with open(self.guidelines_file, 'r', encoding='utf-8') as file:
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

    def calculate_custom_calories(self, guidelines):
        # Split the guidelines string by commas and skip the first element
        guideline_values = [float(val) for val in guidelines.split(',')[1:]]
    # Rest of the method...

        maintenance_calories = (10 * self.weight) + (6.25 * self.height * 100) - (5 * self.age) + 5
        shred_calories = maintenance_calories - 500
        bulk_calories = maintenance_calories + 500

        if self.sport.lower() == "high-intensity":
            maintenance_calories *= 1.3
            shred_calories *= 1.3
            bulk_calories *= 1.3
        elif self.sport.lower() == "moderate-intensity":
            maintenance_calories *= 1.1
            shred_calories *= 1.1
            bulk_calories *= 1.1

        if self.daily_activity.lower() == "lightly active":
            maintenance_calories *= 1.2
            shred_calories *= 1.2
            bulk_calories *= 1.2
        elif self.daily_activity.lower() == "average":
            maintenance_calories *= 1.5
            shred_calories *= 1.5
            bulk_calories *= 1.5
        elif self.daily_activity.lower() == "very active":
            maintenance_calories *= 1.8
            shred_calories *= 1.8
            bulk_calories *= 1.8

        return {
            "maintenance": maintenance_calories,
            "shred": shred_calories,
            "bulk": bulk_calories
        }
        
    def bmi_calculation(self): 
        '''
        This method calculates the Body Mass Index (BMI) of the user and compare it with the average BMI of their age group based on a small sample dataset. 

        This method reads BMI data from a CSV file, calculates the user's BMI using their stored height and weight attributes, 
        retrieves the average BMI of their age group from the dataset, and compares the user's BMI with the average.
        '''
        
        df = pd.read_csv("bmi.csv")

        new = df.groupby('Age')['Bmi'].mean()

        real_age = int(self.age)

        calculated_bmi = (self.weight) / ((self.height)**2)

        mean_bmi = new.loc[real_age]

        if int(calculated_bmi) >= int(mean_bmi): 
            print(f"The user's calculated BMI is {calculated_bmi}. The user's BMI is less than or equal to the average BMI of their age group.")
        else: 
            print(f"The user's calculated BMI is {calculated_bmi}. The user's BMI is greater than the average BMI of their age group.")

class Meals:
    def get_meal_options(user_allergies=None, user_preferences=None):
        meals_data = {
            "Meal 1": ["chicken", "rice", "broccoli"],
            "Meal 2": ["beef", "potatoes", "carrots"],
            "Meal 3": ["salmon", "quinoa", "asparagus"],
            "Meal 4": ["pasta", "tomatoes", "spinach"],
            "Meal 5": ["tofu", "brown rice", "green beans"]
        }

        if user_allergies is None:
            user_allergies = input("Enter your allergies (comma-separated): ").strip().split(', ')
        if user_preferences is None:
            user_preferences = input("Enter your meal preferences (comma-separated): ").strip().split(', ')

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
        num_meals_to_select = min(3, len(sorted_meals))
        meal_options = random.sample(sorted_meals[:num_meals_to_select], num_meals_to_select)

        if meal_options:
            print("Here are your meal options for today:")
            for meal_index in range(len(meal_options)):
                meal, ingredients, _ = meal_options[meal_index]
                print(f"{meal}: {', '.join(ingredients)}")
        else:
            print("Sorry, we couldn't find suitable meal options for your allergies and preferences.")
        return meal_options

    def graph(self, current_weight, goal, calories):
        '''
        This method creates a line graph illustrating the expected weight change over time based on the user's current weight,
        weight change goal, and estimated caloric deficit or surplus.

        Parameters:
        - current_weight (float): The user's current weight in kilograms.
        - goal (str): The user's weight change goal. Should be one of: "lose" or "gain".
        - calories (int): The estimated caloric deficit (if goal is "lose") or surplus (if goal is "gain") per day.
        '''
        change = make_array()
        graph = Table.read_table('graph - Sheet1.csv')
        pounds = int(calories) / 3500
        pounds_per_week = pounds / graph.num_rows

        if goal == "lose":
            for i in range(graph.num_rows):
                x_val = current_weight - pounds_per_week * i
                change = np.append(change, x_val)

        if goal == "gain":
            for i in range(graph.num_rows):
                x_val = current_weight + pounds_per_week * i
                change = np.append(change, x_val)

        x = np.arange(0, len(change), 1)

        new_graph = graph.with_column("Pounds", change)

        plt.plot(x, change)
        plt.xlabel("Weeks")
        plt.ylabel("Weight (kgs)")
        plt.title("Weight Change Over Time")
        plt.show()

class Nutrition:
    def calculate_nutrition_plan(calories, goal):
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
        calories, advice = Nutrition.calculate_nutrition_plan(calories, goal)
        caloric_intake_info = f"Your daily caloric intake should be approximately {calories['maintenance']:.2f} calories."

        if detailed:
            print(f"For your goal to {goal}, {caloric_intake_info}")
            print(advice)
        else:
            print(caloric_intake_info)

# Example usage:
user = User()
user.get_user_info()

calories = Calories("guidelines.txt", user.height, user.weight, user.age, user.sport, user.daily_activity)
Calories.bmi_calculation()
Nutrition.display_nutrition_calories(calories, 'shred')
Meals.get_meal_options()
meals_instance = Meals()
meals_instance.graph(user.weight, "lose", 500)  # Assuming 500 calories deficit for illustration