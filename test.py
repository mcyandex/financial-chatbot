from yahoo_fin.stock_info import *
import pandas as pd

#df_tickers = pd.read_excel('tickers_yahoo.xlsx')
#df_tickers = df_tickers['Ticker']

tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META']#df_tickers.tolist()#
date = '2023-01-01'#'2023-12-08'#

def get_ticker_history(ticker, date, df):
    #print(ticker)
    df_data = get_data(ticker)
    df_data.reset_index(inplace=True)
    df_data = df_data[df_data['index'] >= date]
    return pd.concat([df, df_data], axis=0, ignore_index=True)

df = pd.DataFrame()
for ticker in tickers:
    df = get_ticker_history(ticker, date, df)

#df.drop(df.columns[0], axis=1, inplace=True)
df = df.rename(columns={'index': 'date'})
df.to_csv('ticker_history.csv', index=False)
df = pd.read_csv('ticker_history.csv')
