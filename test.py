import numpy as np
from datascience import *
import matplotlib
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

class Calories: 

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

class Meals: 
    
    def graph(calories):
        '''
        This method seeks to determine how many pounds a person needs to lose per week to get to their desired weight. 

        Args: 
        calories(int): this variable is how many calories a person wants to lose. 
        
        '''
        x = 0
        change = make_array()
        graph = Table.read_table('graph - Sheet1.csv')
        #want this graph to be of four months time, with a tick every week on the x-axis 
        pounds = int(calories) / 3500 
        pounds_per_week = pounds / 16 #this will give the pound change per week 
        
        if goal == "lose": 
            for i in graph.num_rows: 
                x = current_weight - pounds_per_week*i
                change = np.append(change, x)
            
        if goal == "gain": 
            for i in range(graph.num_rows): 
                x = current_weight + pounds_per_week*i
                change = np.append(change, x)

        new_graph = graph.with_column("Pounds", change)

        print(new_graph.plot("Weekly Basis", "Pounds"))