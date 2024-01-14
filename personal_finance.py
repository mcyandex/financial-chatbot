import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Ask questions and store responses
questions = [
    "How much is your net fixed income per month?",
    "Transportation costs per month?",
    "Food costs per month?",
    "Outing expenses per month?",
    "Other fixed costs per month?",
    "Do you have any variable costs this year?",
    "How much available savings do you have?",
]

months = [
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"
]

#Dictionary to store each users answers to the according question
user_responses = {}

def get_variable_costs(user_responses):
    months_dict={}
    for m in months:
        resp = input(f"{m} : ")
        months_dict[m] = resp
    user_responses["Variable costs per month"] = months_dict
    return months_dict

def calculate_available_amount_to_invest(user_responses):
    savings = int(user_responses.get("How much available savings do you have?")) if user_responses.get("How much available savings do you have?", 0) else 0
    income = int(user_responses.get("How much is your net fixed income per month?")) if user_responses.get("How much is your net fixed income per month?", 0) else 0
    return (savings - income)

def calculate_savings_per_month(user_responses):
    income = int(user_responses.get("How much is your net fixed income per month?")) if user_responses.get("How much is your net fixed income per month?", 0) else 0
    transportation_costs = int(user_responses.get("Transportation costs per month?", 0)) if user_responses.get("Transportation costs per month?", 0) else 0
    food_costs = int(user_responses.get("Food costs per month?", 0)) if user_responses.get("Food costs per month?", 0) else 0
    outing_expenses = int(user_responses.get("Outing expenses per month?", 0)) if user_responses.get("Outing expenses per month?", 0) else 0
    other_costs = int(user_responses.get("Other fixed costs per month?", 0)) if user_responses.get("Other fixed costs per month?", 0) else 0
    total_costs = (transportation_costs + food_costs + outing_expenses + other_costs)
    return (income - total_costs)

def calculate_savings_per_year(user_responses):
    return (calculate_savings_per_month(user_responses) * 12)

def calculate_income_and_costs(user_responses):
    variable_costs = user_responses.get("Do you have any variable costs this year?") if user_responses.get("Do you have any variable costs this year?", 0) else {}

    yearly_income = []
    monthly_income = int(user_responses.get("How much is your net fixed income per month?", 0)) if user_responses.get("How much is your net fixed income per month?", 0) else 0
    yearly_income = [monthly_income] * len(months)
    
    total_costs_per_year = []
    transportation_costs = int(user_responses.get("Transportation costs per month?", 0)) if user_responses.get("Transportation costs per month?", 0) else 0
    food_costs = int(user_responses.get("Food costs per month?", 0)) if user_responses.get("Food costs per month?", 0) else 0
    outing_expenses = int(user_responses.get("Outing expenses per month?", 0)) if user_responses.get("Outing expenses per month?", 0) else 0
    other_costs = int(user_responses.get("Other fixed costs per month?", 0)) if user_responses.get("Other fixed costs per month?", 0) else 0
    total_costs = (transportation_costs + food_costs + outing_expenses + other_costs)
    total_costs_per_year += [total_costs] * len(months)
    #add charges variables
    if variable_costs != {}:
        for month, costs in variable_costs.items():
            monthly_costs = int(costs) if costs is not None and str(costs).strip() != '' else 0
            if month == "january":
                total_costs_per_year[0] += monthly_costs
            elif month ==  "february":
                total_costs_per_year[1] += monthly_costs
            elif month == "march":
                total_costs_per_year[2] += monthly_costs
            elif month == "april":
                total_costs_per_year[3] += monthly_costs
            elif month == "may":
                total_costs_per_year[4] += monthly_costs
            elif month == "june":
                total_costs_per_year[5] += monthly_costs
            elif month == "july":
                total_costs_per_year[6] += monthly_costs
            elif month == "august":
                total_costs_per_year[7] += monthly_costs
            elif month == "september":
                total_costs_per_year[8] += monthly_costs
            elif month == "october":
                total_costs_per_year[9] += monthly_costs
            elif month == "november":
                total_costs_per_year[10] += monthly_costs
            else:
                total_costs_per_year[11] += monthly_costs
    return yearly_income, total_costs_per_year

def plot_monthly_breakdown(user_responses):
    revenus, charges = calculate_income_and_costs(user_responses)

    # Adjust bar width and spacing
    bar_width = 0.35
    index = np.arange(len(months))
    # Plotting the grouped bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    income_bars = ax.bar(index - bar_width/4, revenus, bar_width/2, label='Income', color='green')
    costs_bars = ax.bar(index + bar_width/4, charges, bar_width/2, label='Costs', color='red')

    # Adding labels and title
    ax.set_xlabel('Month')
    ax.set_ylabel('Value (EUR)')
    ax.set_title('Income and Costs Breakdown (per Month)')
    ax.set_xticks(index)
    ax.set_xticklabels(months)

    # Adding totals on top of each bar
    for bar, data in zip(income_bars, revenus):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(data), ha='center', va='bottom')

    for bar, data in zip(costs_bars, charges):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(data), ha='center', va='bottom')

    ax.legend()
    # Display the bar chart
    plt.show()

def plot_investment_capacity(user_responses):
    income, costs = calculate_income_and_costs(user_responses)
    invest_capacity = []
    for i in range(len(income)):
        invest_capacity.append(income[i] - costs[i])

    # Adjust bar width and spacing
    bar_width = 0.35
    index = np.arange(len(months))
    # Plotting the grouped bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    capacity_bars = ax.bar(index - bar_width/4, income, bar_width/2, label='Capacity', color='green')

    # Adding labels and title
    ax.set_xlabel('Month')
    ax.set_ylabel('Value (EUR)')
    ax.set_title('Investment Capacity (per month)')
    ax.set_xticks(index)
    ax.set_xticklabels(months)

    # Adding totals on top of each bar
    for bar, data in zip(capacity_bars, invest_capacity):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(data), ha='center', va='bottom')

    ax.legend()
    # Display the bar chart
    plt.show()

def plot_pie_chart(user_responses):
    variable_costs = user_responses.get("Do you have any variable costs this year?") if user_responses.get("Do you have any variable costs this year?", 0) else {}


    income, _ = calculate_income_and_costs(user_responses)
    total_income = sum(income)

    costs = []
    transportation_costs = int(user_responses.get("Transportation costs per month?", 0)) if user_responses.get("Transportation costs per month?", 0) else 0
    food_costs = int(user_responses.get("Food costs per month?", 0)) if user_responses.get("Food costs per month?", 0) else 0
    outing_expenses = int(user_responses.get("Outing expenses per month?", 0)) if user_responses.get("Outing expenses per month?", 0) else 0
    other_costs = int(user_responses.get("Other fixed costs per month?", 0)) if user_responses.get("Other fixed costs per month?", 0) else 0
    total_costs = (transportation_costs + food_costs + outing_expenses + other_costs)
    costs += [total_costs] * len(months)

    total_costs = sum(costs)

    costs_var = 0
    if variable_costs != {}:
        for month, cost in variable_costs.items():
            cost_value = int(cost) if cost is not None and str(cost).strip() != '' else 0
            costs_var += cost_value

    invesment_capacity = total_income - total_costs - costs_var

    # Data for the pie chart
    sizes = [costs_var, transportation_costs, food_costs, outing_expenses, other_costs, total_costs, invesment_capacity]
    labels = ["Variable", "Transportation", "Food", "Outing", "Other", "Total", "Investment Capacity"]

    if len(np.unique(sizes)) != 1 or np.unique(sizes)[0] != 0 :
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  #Ensures that pie is drawn as a circle.
        plt.title('Distribution of Costs and Investment capacity')
        plt.show()
    else:
        return 

def check_integer(user_response, question):
    if user_response == "":
        return 0
    try:
        user_response = int(user_response)
        return user_response
    except ValueError:
        print("Error: Please enter a valid integer.")
        while True:
            try:
                user_response = int(input(f"Chatbot: {question}"))
                return user_response
            except ValueError:
                print("Error: Please enter a valid integer.")

def check_string(user_response, question):
    if user_response == "":
        return "no"
    try:
        if user_response.lower() == "yes" or user_response.lower() == "no":
            return user_response
    except ValueError:
        print("Error: Please enter either 'yes' or 'no'.")
        while True:
            try:
                user_response = str(input(f"Chatbot: {question}"))
                return user_response
            except ValueError:
                print("Error: Please enter either 'yes' or 'no'.")
        

#Interaction with the user
def get_personal_finance():
    exit_conditions = ("q", "quit", "exit")
    print("Type q / quit / exit to exit the program.")
    print("Chatbot: Welcome to personal finance module !")
    for question in questions:
        keywords = ["income", "transportation", "food", "outing", "other", "savings"]
        print(f"Chatbot: {question}")
        user_response = input("User: ")
        if user_response in exit_conditions:
            print("ATTENTION : QUITTING PERSONAL FINANCE !!")
            return 
        elif any(keyword in question.lower() for keyword in keywords):                
            user_responses[question] = check_integer(user_response, question)
        elif question == "Do you have any variable costs this year?" :
            #print(user_response)
            user_responses[question] = check_string(user_response, question)
            try: 
                if user_response.lower() == "no" or user_response == "" :
                    user_responses[question] = {}
                else :
                    user_responses[question] = get_variable_costs(user_responses)
            except ValueError:
                # If conversion fails, print an error message and continue the loop
                print("Error: Please enter a valid string.")
    #Metrics
    print("Safety savings : ", int(user_responses.get("How much is your net fixed income per month?")) if user_responses.get("How much is your net fixed income per month?", 0) else 0)
    print("Available amount to invest : ",calculate_available_amount_to_invest(user_responses))
    print("Investment capacity (per month) : ", calculate_savings_per_month(user_responses))
    print("Investment capacity (per year) : ", calculate_savings_per_year(user_responses))
    print(plot_monthly_breakdown(user_responses))
    print(plot_investment_capacity(user_responses))
    print(plot_pie_chart(user_responses))