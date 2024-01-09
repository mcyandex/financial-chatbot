import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Ask questions and store responses
questions = [
    "A combien s'élèvent tes revenus fixes nets par mois ?",
    "Charges liées aux transports par mois ?",
    "Charges liées aux nourritures par mois ?",
    "Charges liées aux sorties par mois ?",
    "Autres coûts fixes par mois ?",
    "As-tu des charges variables cette année ?",
    "Combien d'épargne disponible as-tu ? (mettre une valeur numérique)",
]

months = [
    "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"
]

#Dictionary to store each users answers to the according question
user_responses = {}

def get_charges_variables(user_responses):
    months_dict={}
    for m in months:
        resp = input(f"{m} : ")
        months_dict[m] = resp
    user_responses["Charges variables par mois"] = months_dict
    return months_dict

def montant_dispo_investir(user_responses):
    epargne = int(user_responses.get("Combien d'épargne disponible as-tu ? (mettre une valeur numérique)")) if user_responses.get("Combien d'épargne disponible as-tu ? (mettre une valeur numérique)", 0) else 0
    fixe = int(user_responses.get("A combien s'élèvent tes revenus fixes nets par mois ?")) if user_responses.get("A combien s'élèvent tes revenus fixes nets par mois ?", 0) else 0
    return (epargne - fixe)

def capacite_investissement_mois(user_responses):
    fixe = int(user_responses.get("A combien s'élèvent tes revenus fixes nets par mois ?")) if user_responses.get("A combien s'élèvent tes revenus fixes nets par mois ?", 0) else 0
    transport = int(user_responses.get("Charges liées aux transports par mois ?", 0)) if user_responses.get("Charges liées aux transports par mois ?", 0) else 0
    nourritures = int(user_responses.get("Charges liées aux nourritures par mois ?", 0)) if user_responses.get("Charges liées aux nourritures par mois ?", 0) else 0
    sorties = int(user_responses.get("Charges liées aux sorties par mois ?", 0)) if user_responses.get("Charges liées aux sorties par mois ?", 0) else 0
    couts = int(user_responses.get("Autres coûts fixes par mois ?", 0)) if user_responses.get("Autres coûts fixes par mois ?", 0) else 0
    charges = (transport + nourritures + sorties + couts)
    return (fixe - charges)

def capacite_investissement_an(user_responses):
    mois = capacite_investissement_mois(user_responses)
    return (mois*12)

def calculer_revenues_et_charges(user_responses):
    charges_variables = user_responses.get("As-tu des charges variables cette année ?") if user_responses.get("As-tu des charges variables cette année ?", 0) else {}

    revenus = []
    fixe = int(user_responses.get("A combien s'élèvent tes revenus fixes nets par mois ?", 0)) if user_responses.get("A combien s'élèvent tes revenus fixes nets par mois ?", 0) else 0
    revenus = [fixe] * len(months)
    
    charges = []
    transport = int(user_responses.get("Charges liées aux transports par mois ?", 0)) if user_responses.get("Charges liées aux transports par mois ?", 0) else 0
    nourritures = int(user_responses.get("Charges liées aux nourritures par mois ?", 0)) if user_responses.get("Charges liées aux nourritures par mois ?", 0) else 0
    sorties = int(user_responses.get("Charges liées aux sorties par mois ?", 0)) if user_responses.get("Charges liées aux sorties par mois ?", 0) else 0
    couts = int(user_responses.get("Autres coûts fixes par mois ?", 0)) if user_responses.get("Autres coûts fixes par mois ?", 0) else 0
    charges_total = (transport + nourritures + sorties + couts)
    charges += [charges_total] * len(months)
    #add charges variables
    if charges_variables != {}:
        for month, charge in charges_variables.items():
            charge_value = int(charge) if charge is not None and str(charge).strip() != '' else 0
            if month == "janvier":
                charges[0] += charge_value
            elif month ==  "février":
                charges[1] += charge_value
            elif month == "mars":
                charges[2] += charge_value
            elif month == "avril":
                charges[3] += charge_value
            elif month == "mai":
                charges[4] += charge_value
            elif month == "juin":
                charges[5] += charge_value
            elif month == "juillet":
                charges[6] += charge_value
            elif month == "août":
                charges[7] += charge_value
            elif month == "septembre":
                charges[8] += charge_value
            elif month == "octobre":
                charges[9] += charge_value
            elif month == "novembre":
                charges[10] += charge_value
            else:
                charges[11] += charge_value
    return revenus, charges

def plot_repartitions_par_mois(user_responses):
    revenus, charges = calculer_revenues_et_charges(user_responses)

    # Adjust bar width and spacing
    bar_width = 0.35
    index = np.arange(len(months))
    # Plotting the grouped bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    revenus_bars = ax.bar(index - bar_width/4, revenus, bar_width/2, label='Revenues', color='green')
    charges_bars = ax.bar(index + bar_width/4, charges, bar_width/2, label='Charges', color='red')

    # Adding labels and title
    ax.set_xlabel('Mois')
    ax.set_ylabel('Montant (en EUR)')
    ax.set_title('Distribution des Revenues et Charges par Mois')
    ax.set_xticks(index)
    ax.set_xticklabels(months)

    # Adding totals on top of each bar
    for bar, data in zip(revenus_bars, revenus):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(data), ha='center', va='bottom')

    for bar, data in zip(charges_bars, charges):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(data), ha='center', va='bottom')

    ax.legend()
    # Display the bar chart
    plt.show()

def plot_repartition_capacite_invest(user_responses):
    revenus, charges = calculer_revenues_et_charges(user_responses)
    capacite = []
    for i in range(len(revenus)):
        capacite.append(revenus[i] - charges[i])

    # Adjust bar width and spacing
    bar_width = 0.35
    index = np.arange(len(months))
    # Plotting the grouped bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    capacite_bars = ax.bar(index - bar_width/4, revenus, bar_width/2, label='Capacité', color='green')

    # Adding labels and title
    ax.set_xlabel('Mois')
    ax.set_ylabel('Montant (en EUR)')
    ax.set_title('Capacité par Mois')
    ax.set_xticks(index)
    ax.set_xticklabels(months)

    # Adding totals on top of each bar
    for bar, data in zip(capacite_bars, capacite):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(data), ha='center', va='bottom')

    ax.legend()
    # Display the bar chart
    plt.show()

def plot_camembert(user_responses):
    charges_variables = user_responses.get("As-tu des charges variables cette année ?") if user_responses.get("As-tu des charges variables cette année ?", 0) else {}

    revenus, charges_non = calculer_revenues_et_charges(user_responses)
    total_revenus = sum(revenus)

    charges = []
    transport = int(user_responses.get("Charges liées aux transports par mois ?", 0)) if user_responses.get("Charges liées aux transports par mois ?", 0) else 0
    nourritures = int(user_responses.get("Charges liées aux nourritures par mois ?", 0)) if user_responses.get("Charges liées aux nourritures par mois ?", 0) else 0
    sorties = int(user_responses.get("Charges liées aux sorties par mois ?", 0)) if user_responses.get("Charges liées aux sorties par mois ?", 0) else 0
    couts = int(user_responses.get("Autres coûts fixes par mois ?", 0)) if user_responses.get("Autres coûts fixes par mois ?", 0) else 0
    charges_total = (transport + nourritures + sorties + couts)
    charges += [charges_total] * len(months)

    total_charges = sum(charges)

    charges_var = 0
    if charges_variables != {}:
        for month, charge in charges_variables.items():
            charge_value = int(charge) if charge is not None and str(charge).strip() != '' else 0
            charges_var += charge_value

    capacite_investissement = total_revenus - total_charges - charges_var

    # Data for the pie chart
    sizes = [charges_var, transport, nourritures, sorties, couts, total_charges, capacite_investissement]
    labels = ["Charges Variables", "Transport", "Nourritures", "Sorties", "Autres", "Charges", "Capacité d'Investissement"]

    if len(np.unique(sizes)) != 1 or np.unique(sizes)[0] != 0 :
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  #Ensures that pie is drawn as a circle.
        plt.title('Distribution of Charges and Capacité d\'Investissement')
        plt.show()
    else:
        return 
    
"""# Display collected information
st.write("\nRésumé des informations collectées :")
for question, response in user_responses.items():
    st.write(f"{question}: {response}")"""

def check_integer(user_response, question):
    if user_response == "":
        return 0
    try:
        user_response = int(user_response)
        return user_response
    except ValueError:
        st.write("Error: Please enter a valid integer.")
        while True:
            try:
                user_response = int(input(f"Chatbot: {question}"))
                return user_response
            except ValueError:
                st.write("Error: Please enter a valid integer.")

def check_string(user_response, question):
    if user_response == "":
        return "non"
    try:
        if user_response.lower() == "oui" or user_response.lower() == "non":
            return user_response
    except ValueError:
        st.write("Error: Please enter either 'oui' or 'non'.")
        while True:
            try:
                user_response = str(input(f"Chatbot: {question}"))
                return user_response
            except ValueError:
                st.write("Error: Please enter either 'oui' or 'non'.")
        

#Interaction with the user
def get_personal_finance():
    exit_conditions = ("q", "quit", "exit")
    st.write("Appuyer sur q / quit / exit pour quitter !")
    for question in questions:
        keywords = ["revenus", "transports", "nourritures", "sorties", "coûts", "épargne"]
        st.write(f"Chatbot: {question}")
        user_response = input("User: ")
        if user_response in exit_conditions:
            return
        elif any(keyword in question.lower() for keyword in keywords):                
            user_responses[question] = check_integer(user_response, question)
        elif question == "As-tu des charges variables cette année ?" :
            #st.write(user_response)
            user_responses[question] = check_string(user_response, question)
            try: 
                if user_response.lower() == "non" or user_response == "" :
                    user_responses[question] = {}
                else :
                    user_responses[question] = get_charges_variables(user_responses)
            except ValueError:
                # If conversion fails, st.write an error message and continue the loop
                st.write("Error: Please enter a valid string.")
    #Metrics
    st.write("Ta réserve de secours : ", int(user_responses.get("A combien s'élèvent tes revenus fixes nets par mois ?")) if user_responses.get("A combien s'élèvent tes revenus fixes nets par mois ?", 0) else 0)
    st.write("Montant disponible à investir : ",montant_dispo_investir(user_responses))
    st.write("Ta capacité d'investissements par mois : ", capacite_investissement_mois(user_responses))
    st.write("Ta capacité d'investissements par an : ", capacite_investissement_an(user_responses))
    st.write(plot_repartitions_par_mois(user_responses))
    st.write(plot_repartition_capacite_invest(user_responses))
    st.write(plot_camembert(user_responses))