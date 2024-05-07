import pandas as pd
import random
import json
import numpy as np
from datascience import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

class User: 
    #Michael's code. 
    pass 

class Calories: 
    #Matt's code. 
    
    def bmi_calculation(self): 
        #Pragya: using grouby for pandas dataframes
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
    #Colby's code. 
    
    def graph(self, current_weight, goal, calories):
        #Pragya: visualization using pyplot
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
        #want this graph to be of fifteen months time, with a tick every week on the x-axis 
        kilos = int(calories) / 3500
        kilos_per_week = kilos / graph.num_rows #this will give the pound change per week

        if goal == "maintenance":
            for i in range(graph.num_rows):
                x_val = current_weight
                change = np.append(change, x_val)
        if goal == "shred":
            for i in range(graph.num_rows):
                x_val = current_weight - kilos_per_week * i
                change = np.append(change, x_val)

        if goal == "bulk":
            for i in range(graph.num_rows):
                x_val = current_weight + kilos_per_week * i
                change = np.append(change, x_val)

        x = np.arange(0, len(change), 1)

        new_graph = graph.with_column("Kilos", change)

        plt.plot(x, change)
        plt.xlabel("Weeks")
        plt.ylabel("Weight (kgs)")
        plt.title("Weight Change Over Time")
        plt.show()

class Nutrition: 
    #Elizabeth's code. 
    pass 

# Calls:
if __name__ == "__main__":
    user = User()
    user.get_user_info()
    calories = Calories("guidelines.txt", user.height, user.weight, user.age, user.sport, user.daily_activity, user.goal)
    Calories.bmi_calculation(self=user)
    nutrition = Nutrition()
    nutrition.display_nutrition_calories(calories, user.goal)
    Meals.get_meal_options()
    meals_instance = Meals()
    meals_instance.graph(user.weight, user.goal, calories.caloriechange)  