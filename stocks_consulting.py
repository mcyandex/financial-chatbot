from yahoo_fin.stock_info import *
import pandas as pd
import openpyxl
import shutil
import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import xlwings as xw
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

filename = ''
modele = 'Modele//Evaluer_une_action.xlsx'

def get_connection(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        soup = 'none'
    return soup

def get_moning_ticker(stock):
    try:
        stock = stock.lower()
        selected_url = f'https://moning.co/fr/actions?q={stock}'
        action_soup = get_connection(selected_url)
        moning_ticker = action_soup.find_all('div', id='stocks-list')[0].find('a')['href'].rsplit('/', 1)[-1]
        return moning_ticker
    except (IndexError) as e:
        print('Ticker not found')

def get_yahoo_ticker(stock):
    try:
        df = pd.read_excel('tickers_yahoo.xlsx')
        stock = stock.lower()
        yahoo_ticker = df[df['Name'].str.lower().str.contains(stock) & df['Name'].notna()]['Ticker'].iloc[0]
        return yahoo_ticker  
    except (IndexError) as e:
        print('Ticker not found')

def get_sub_elements(tab):
    return [element.text for element in tab]

def get_attributes(tab, attribute):
    return [element[attribute] for element in tab]
    
def combine_tab(liste1, liste2):
    liste = []
    for i in range(len(liste1)):
        tuple_combine = (liste1[i], liste2[i])
        liste.append(tuple_combine)
    return liste

def extract_graph(soup, libelle):
    liste = soup.find_all('canvas', id=libelle)[0]['data-graph']

    # Analyse de la chaîne JSON
    data = json.loads(liste)

    # Récupération d'un tuple (valeur, year) pour chaque objet
    tuples = [(item["value"], item["year"]) for item in data]

    # Créez un DataFrame à partir de la liste de tuples
    df = pd.DataFrame(tuples, columns=['value', 'year'])

    return df

def copy_paste(workbook, copy_sheet, copy_cell, paste_sheet, paste_cell):

    # Spécifiez la feuille d'origine et la cellule à copier
    source_sheet_name = paste_sheet  # Remplacez par le nom de la feuille d'origine
    source_cell = paste_cell  # Remplacez par la cellule d'origine que vous souhaitez copier

    # Spécifiez la feuille de destination et la cellule de destination
    destination_sheet_name = copy_sheet  # Remplacez par le nom de la feuille de destination
    destination_cell = copy_cell  # Remplacez par la cellule de destination où vous souhaitez coller

    # Accédez aux feuilles source et de destination
    source_sheet = workbook[source_sheet_name]
    destination_sheet = workbook[destination_sheet_name]

    # Lisez la valeur de la cellule source
    source_value = source_sheet[source_cell].value

    # Écrivez la valeur de la cellule source dans la cellule de destination
    destination_sheet[destination_cell] = source_value

def create_report(ticker):
    ticker = ticker.replace('.', '_')
    global filename
    filename = 'Analyses//' + ticker + '_analyse.xlsx'
    # Utilisez shutil pour copier le fichier
    shutil.copy(modele, filename)

def import_data(filename):

    # yahoo

    ticker = yahoo_ticker

    df_analysts_info = get_analysts_info(ticker)

    df_earnings_estimate = df_analysts_info['Earnings Estimate']
    df_revenue_estimate = df_analysts_info['Revenue Estimate']
    df_earning_history = df_analysts_info['Earnings History']
    #df_eps_trend = df_analysts_info['EPS Trend']
    df_eps_revisions = df_analysts_info['EPS Revisions']
    df_growth_estimates = df_analysts_info['Growth Estimates']

    df_data = get_data(ticker)
    df_data.reset_index(inplace=True)
    df_data = df_data[df_data['index'] >= '2013-01-01']

    df_holders = get_holders(ticker)

    df_top_institutional_holders = df_holders['Top Institutional Holders']
    df_direct_holders = df_holders['Direct Holders (Forms 3 and 4)']
    df_major_holders = df_holders['Major Holders']

    df_quote = pd.DataFrame(get_quote_table(ticker), index=[0])

    df_stats = get_stats(ticker)

    df_valuation = get_stats_valuation(ticker)

    # moning

    ticker = moning_ticker

    selected_url = f'https://moning.co/fr/actions/{ticker.upper()}'
    action_soup = get_connection(selected_url)

    data = get_sub_elements(action_soup.find_all('p', class_='stats-display-text'))
    liste1 = ['Rendement', 'Croissance div. / 5 ans', 'Capitalisation', 'Ratio cours/bénéfices', 'Beta (volatilité)', 'Bénéfice par action', 'Dividende sans interruption', 'Fréquence', 'Montant Annuel à terme', 'Ex-dividende']
    liste2 = [re.search(r'[-+]?\d*\.\d+|\d+', item).group() if not re.search(r'\d{2}/\d{2}/\d{4}', item) else item.strip() for item in data]
    stats = pd.DataFrame(combine_tab(liste1, liste2), columns=['indicateur', 'unité'])

    data = get_sub_elements(action_soup.find_all('div', class_='inline-flex px-3 py-1 text-sm font-medium leading-none bg-emerald-100 text-emerald-800 rounded-sm'))
    liste1 = ['Retour sur 1 an', 'Retour sur 5 ans']
    liste2 = [re.search(r'[-+]?\d*\.\d+|\d+', item).group() for item in data if re.search(r'[-+]?\d*\.\d+|\d+', item)]
    performances = pd.DataFrame(combine_tab(liste1, liste2), columns=['années', '%'])

    dividendChart = extract_graph(action_soup, 'dividendChart')
    yoyRevenueChart = extract_graph(action_soup, 'yoyRevenueChart')
    FCFPerShareChart= extract_graph(action_soup, 'FCFPerShareChart')
    EPSChart = extract_graph(action_soup, 'EPSChart')
    yoyFCFPerShareChart = extract_graph(action_soup, 'yoyFCFPerShareChart')
    totalRevenueChart = extract_graph(action_soup, 'totalRevenueChart')
    yoyEPSChart = extract_graph(action_soup, 'yoyEPSChart')
    operatingMarginChart = extract_graph(action_soup, 'operatingMarginChart')
    netMarginChart = extract_graph(action_soup, 'netMarginChart')
    returnOnEquityChart = extract_graph(action_soup, 'returnOnEquityChart')
    debtCapitalChart = extract_graph(action_soup, 'debtCapitalChart')
    debtEbitdaChart = extract_graph(action_soup, 'debtEbitdaChart')

    data = get_sub_elements(action_soup.find_all('span', class_='text-sm text-gray-500'))
    liste1 = ['PRICE TO BOOK', 'PAYOUT RATIO', 'RATIO COURS/BÉNÉFICES', 'PEG RATIO', 'PRICE TO SALES', 'PRICE / FCF', 'ENTERPRISE VALUE REVENUE']
    liste2 = [re.search(r'[-+]?\d*\.\d+|\d+', item).group() for item in data if re.search(r'[-+]?\d*\.\d+|\d+', item)]
    #valorisation = pd.DataFrame(combine_tab(liste1, liste2), columns=['indicateur', 'unité'])

    with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:

        # Enregistrez chaque DataFrame dans une feuille Excel distincte
        df_earnings_estimate.to_excel(writer, sheet_name='earnings_estimate', index=False)
        df_revenue_estimate.to_excel(writer, sheet_name='revenue_estimate', index=False)
        df_earning_history.to_excel(writer, sheet_name='earning_history', index=False)
        #df_eps_trend.to_excel(writer, sheet_name='eps_trend', index=False)
        df_eps_revisions.to_excel(writer, sheet_name='eps_revisions', index=False)
        df_growth_estimates.to_excel(writer, sheet_name='growth_estimates', index=False)
        df_data.to_excel(writer, sheet_name='data', index=False)
        df_top_institutional_holders.to_excel(writer, sheet_name='top_institutional_holders', index=False)
        df_direct_holders.to_excel(writer, sheet_name='direct_holders', index=False)
        df_major_holders.to_excel(writer, sheet_name='major_holders', index=False)
        df_quote.to_excel(writer, sheet_name='quote', index=False)
        df_stats.to_excel(writer, sheet_name='stats', index=False)
        df_valuation.to_excel(writer, sheet_name='valuation', index=False)
        stats.to_excel(writer, sheet_name='moning_stats', index=False)
        performances.to_excel(writer, sheet_name='performances', index=False)
        dividendChart.to_excel(writer, sheet_name='dividendChart', index=False)
        yoyRevenueChart.to_excel(writer, sheet_name='yoyRevenueChart', index=False)
        FCFPerShareChart.to_excel(writer, sheet_name='FCFPerShareChart', index=False)
        EPSChart.to_excel(writer, sheet_name='EPSChart', index=False)
        yoyFCFPerShareChart.to_excel(writer, sheet_name='yoyFCFPerShareChart', index=False)
        totalRevenueChart.to_excel(writer, sheet_name='totalRevenueChart', index=False)
        yoyEPSChart.to_excel(writer, sheet_name='yoyEPSChart', index=False)
        operatingMarginChart.to_excel(writer, sheet_name='operatingMarginChart', index=False)
        netMarginChart.to_excel(writer, sheet_name='netMarginChart', index=False)
        returnOnEquityChart.to_excel(writer, sheet_name='returnOnEquityChart', index=False)
        debtCapitalChart.to_excel(writer, sheet_name='debtCapitalChart', index=False)
        debtEbitdaChart.to_excel(writer, sheet_name='debtEbitdaChart', index=False)
        #valorisation.to_excel(writer, sheet_name='valorisation', index=False)

def calculate_score(filename):

    # Chargez le fichier Excel existant
    workbook = openpyxl.load_workbook(filename)

    df = pd.read_excel(filename, sheet_name='yoyRevenueChart')  # Remplacez 'votre_fichier.xlsx' par le chemin vers votre fichier Excel
    dernieres_valeurs = df['value'].tail(5)  # Remplacez 'value' par 'year' si vous souhaitez calculer la moyenne de 'year'
    moyenne_ca = dernieres_valeurs.mean()

    df = pd.read_excel(filename, sheet_name='FCFPerShareChart')  # Remplacez 'votre_fichier.xlsx' par le chemin vers votre fichier Excel
    dernieres_valeurs = df['value'].tail(5)  # Remplacez 'value' par 'year' si vous souhaitez calculer la moyenne de 'year'
    moyenne_fcf = dernieres_valeurs.mean()

    workbook['Score']['M1'].value =  str(round(float(workbook['quote']['P2'].value), 2)).replace('.', ',') # Prix de l'action

    workbook['Score']['B5'].value = str(round(float(moyenne_ca), 2)).replace('.', ',') # Chiffre d'affaire

    workbook['Score']['B7'].value = str(round(float(moyenne_fcf), 2)).replace('.', ',')  # Free Cash Flow

    value_B37 = float(str(workbook['stats']['B37'].value.replace('B', '').replace('M', '')))
    value_B40 = float(str(workbook['stats']['B40'].value.replace('B', '').replace('M', '')))
    marge_brute = (value_B40 / value_B37) * 100
    workbook['Score']['B14'].value = str(round(float(marge_brute), 2)).replace('.', ',') # Marge brute

    workbook['Score']['B18'].value =  str(round(float(workbook['stats']['B33'].value.replace('%', '')), 2)).replace('.', ',') # Marge nette
    workbook['Score']['B16'].value =  str(round(float(workbook['stats']['B34'].value.replace('%', '')), 2)).replace('.', ',') # Marge d’exploitation
    workbook['Score']['B20'].value =  str(round(float(workbook['stats']['B36'].value.replace('%', '')), 2)).replace('.', ',') # ROE 
    workbook['Score']['B22'].value =  str(round(float(workbook['stats']['B35'].value.replace('%', '')), 2)).replace('.', ',') # ROA
    workbook['Score']['B28'].value =  str(round(float(workbook['moning_stats']['B3'].value), 2)).replace('.', ',') # Croissance du dividende
    workbook['Score']['B30'].value =  str(round(float(workbook['stats']['B26'].value.replace('%', '')), 2)).replace('.', ',') # Payout Ratio
    workbook['Score']['B32'].value =  str(round(float(workbook['moning_stats']['B2'].value), 2)).replace('.', ',') # Rendement de l'action
    workbook['Score']['B34'].value =  str(round(float(workbook['moning_stats']['B8'].value), 2)).replace('.', ',') # Versement du dividende sans interruption
    workbook['Score']['B40'].value =  str(round(float(workbook['stats']['B48'].value.replace('%', '')), 2)).replace('.', ',') # Dette / Equity
    workbook['Score']['B42'].value =  str(round(float(workbook['debtEbitdaChart']['A7'].value), 2)).replace('.', ',') # Dette / EBITDA (Leverage)
    workbook['Score']['B48'].value =  str(round(float(workbook['quote']['N2'].value), 2)).replace('.', ',') # PER
    #workbook['Score']['B50'].value =  str(workbook['valorisation']['B5'].value) # PEG
    #workbook['Score']['B52'].value =  str(workbook['valorisation']['B2'].value) # P/B
    
    workbook['Valeur Intrasèque']['B3'].value =  str(workbook['Score']['M1'].value).replace('.', ',')
    workbook['Valeur Intrasèque']['B4'].value =  str(round(float(workbook['stats']['B50'].value), 2)).replace('.', ',')
    workbook['Valeur Intrasèque']['B5'].value = '5.21'.replace('.', ',').replace('.', ',')
    workbook['Valeur Intrasèque']['B6'].value =  str(round(float(workbook['moning_stats']['B7'].value), 2)).replace('.', ',')
    workbook['Valeur Intrasèque']['B7'].value =  str(round(float(workbook['growth_estimates']['B6'].value.replace('%', '')), 2)).replace('.', ',')
    workbook['Valeur Intrasèque']['B9'].value =  str(workbook['Score']['B48'].value).replace('.', ',')

    workbook.save(filename)
    workbook = openpyxl.load_workbook(filename)

    #print(workbook['Valeur Intrasèque']['E4'].value)

    app = xw.App(visible=True)
    wb = xw.Book(filename)
    #print(filename)
    worksheet = wb.sheets['Valeur Intrasèque']
    #print(worksheet.range('E4').value, type(worksheet.range('E4').value))
    val_intraseque = (worksheet.range('E4').value + worksheet.range('F4').value + worksheet.range('G4').value) / 3
    #print(f'valeur intras {val_intraseque} + {worksheet.range("E4").value}')
    wb.close()
    app.quit()

    #workbook['Score']['P1'].value = val_intraseque # Valeur Intrasèque
    #workbook['Score']['B54'].value = 100 - (workbook['Score']['P1'].value * 100 / workbook['Score']['M1'].value) # Valorisation
    #workbook['Score']['Q1'].value = workbook['Score']['P1'].value * workbook['Valeur Intrasèque']['B10'].value # Marge de sécurité
    
    workbook.save(filename)

def get_stocks_report():
    global yahoo_ticker, moning_ticker
    print('\nChatbot: Enter stock name to analyze')
    stock_name = input('\nYou: ')
    yahoo_ticker = get_yahoo_ticker(stock_name)
    moning_ticker = get_moning_ticker(stock_name)
    create_report(yahoo_ticker)
    import_data(filename)
    calculate_score(filename)
    print('\nChatbot: Report uploaded successfully !')

