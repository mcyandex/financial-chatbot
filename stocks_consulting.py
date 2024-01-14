from datetime import *
import pandas as pd
import warnings
from yahoofinancials import YahooFinancials

warnings.simplefilter(action='ignore', category=FutureWarning)


def get_previous_day():
    previous_day = str(date.today() - timedelta(days=1))
    return previous_day


def request_data(ticker):
    yf = YahooFinancials(ticker)
    data_income = yf.get_financial_stmts('annual', 'income')['incomeStatementHistory'][ticker]
    data_cash = yf.get_financial_stmts('annual', 'cash')['cashflowStatementHistory'][ticker]
    data_balance = yf.get_financial_stmts('annual', 'balance')['balanceSheetHistory'][ticker]
    stock_history = \
        yf.get_historical_price_data(start_date=get_previous_day(), end_date=str(date.today()), time_interval="daily")[
            ticker]
    return data_income, data_cash, data_balance, stock_history


def get_most_recent_report(data):
    all_dates = [key for dico in data for key in dico.keys()]
    max_date = max(all_dates)
    report_last_date = next((entry for entry in data if max_date in entry), None)[max_date]
    return report_last_date


def get_turnover():
    turnover = get_most_recent_report(data_income)['totalRevenue']
    return str(round(turnover,2)) + " $"


def get_free_cash_flow():
    free_cash_flow = get_most_recent_report(data_cash)['freeCashFlow']
    return str(round(free_cash_flow,2)) + " $"


def get_gross_margin():
    turnover = get_most_recent_report(data_income)['totalRevenue']
    gross_profit = get_most_recent_report(data_income)['grossProfit']

    gross_margin = gross_profit / turnover * 100

    return str(round(gross_margin,2)) + " %"


def get_net_turnover():
    net_turnover = get_most_recent_report(data_income)['netIncome']
    return str(round(net_turnover,2)) + " $"


def get_net_margin():
    net_turnover = get_most_recent_report(data_income)['netIncome']
    turnover = get_most_recent_report(data_income)['totalRevenue']

    net_margin = net_turnover / turnover * 100

    return str(round(net_margin,2)) + " %"


def get_roe():
    stockholders_equity = get_most_recent_report(data_balance)['stockholdersEquity']
    net_turnover = get_most_recent_report(data_income)['netIncome']
    roe = net_turnover / stockholders_equity * 100
    return str(round(roe,2)) + " %"


def get_operating_margin():
    ebit = get_most_recent_report(data_income)['ebit']
    turnover = get_most_recent_report(data_income)['totalRevenue']
    operating_margin = ebit / turnover * 100
    return str(round(operating_margin,2)) + " %"


def get_roa():
    total_assets = get_most_recent_report(data_balance)['totalAssets']
    net_turnover = get_most_recent_report(data_income)['netIncome']
    roa = net_turnover / total_assets * 100
    return str(round(roa,2)) + " %"


def get_payout_ratio():
    total_dividend_paid = get_most_recent_report(data_cash)['cashDividendsPaid']
    net_turnover = get_most_recent_report(data_income)['netIncome']
    payout_ratio = - total_dividend_paid / net_turnover * 100
    return str(round(payout_ratio,2)) + " %"


def get_ratio_equity_debt():
    stockholders_equity = get_most_recent_report(data_balance)['stockholdersEquity']
    debt = get_most_recent_report(data_balance)['longTermDebt']
    ratio_debt_equity = debt / stockholders_equity * 100
    return str(round(ratio_debt_equity,2)) + " %"


def get_per():
    total_cap = get_most_recent_report(data_balance)['totalCapitalization']
    net_turnover = get_most_recent_report(data_income)['netIncome']
    per = total_cap / net_turnover * 100
    return str(round(per,2)) + " %"


def get_today_stock():
    return str(round(stock_history['prices'][0]['close'],2)) + " $"


def get_all_indicators():
    global ticker_status
    print("\nTry one of this functionality")
    print("0) Change ticker")
    print("1) Stock price")
    print("2) Turnover")
    print("3) Net Turnover")
    print("4) Gross margin")
    print("5) Net margin")
    print("6) Operating margin")
    print("7) ROE (Return on Equity)")
    print("8) ROA (Return on Assets)")
    print("9) Payout Ratio")
    print("10) PER (Price Earnings Ratio)")
    print("11) Free Cash-Flow")
    print("12) Ratio Equity/Debt")
    print("13) All of above indicators")
    number = input('\nChatbot: Enter the number of indicator you want to retrieve\nUser: ')
    if number == "1":
        print(get_today_stock())
    elif number == "2":
        print(get_turnover())
    elif number == "3":
        print(get_net_turnover())
    elif number == "4":
        print(get_gross_margin())
    elif number == "5":
        print(get_net_margin())
    elif number == "6":
        print(get_operating_margin())
    elif number == "7":
        print(get_roe())
    elif number == "8":
        print(get_roa())
    elif number == "9":
        print(get_payout_ratio())
    elif number == "10":
        print(get_per())
    elif number == "11":
        print(get_free_cash_flow())
    elif number == "12":
        print(get_ratio_equity_debt())
    elif number == "13":
        df = pd.DataFrame({
            "Stock of the day": [get_today_stock()],
            "Gross turnover": [get_turnover()],
            "Net turnover": [get_net_turnover()],
            "Gross margin": [get_gross_margin()],
            "Net margin": [get_net_margin()],
            "Operating margin": [get_operating_margin()],
            "ROE (Return on Equity) ": [get_roe()],
            "ROA (Return on Assets)": [get_roa()],
            "Payout Ratio": [get_payout_ratio()],
            "PER (Price Earnings Ratio)": [get_per()],
            "Free Cash-Flow": [get_free_cash_flow()],
            "Ratio Debt/Equity": [get_ratio_equity_debt()]
        })
        df_melted = pd.melt(df, var_name='Indicators', value_name='Values')
        df_melted.index = df_melted.index.map(lambda x : x+1)
        print(df_melted)
    elif number == "0":
        ticker_status = False



def get_stocks_report():
    global data_income, data_cash, data_balance, stock_history
    global ticker_status
    exit_conditions = ("q", "quit", "exit", 'bye')
    while True:
        ticker_status = True
        ticker = input('\nChatbot: Enter your ticker please\nUser: ')
        if ticker in exit_conditions:
            break
        while ticker_status:
            try:
                data_income, data_cash, data_balance, stock_history = request_data(ticker.strip())
                get_all_indicators()
            except:
                ticker_yahoo = pd.read_excel("tickers_yahoo.xlsx")[['Ticker', 'Name']]
                print('\nChatbot: Bad ticker. Try one of this please')
                print(ticker_yahoo.head(10))
                ticker_status = False