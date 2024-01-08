from yahoo_fin.stock_info import *
import pandas as pd

df_tickers = pd.read_excel('Data/nasdaq_ticker.xlsx')
df_tickers = df_tickers['Symbol']

tickers = df_tickers.tolist()
date = '2023-12-08'

def get_ticker_history(ticker, date, df):
    df_data = get_data(ticker)
    df_data.reset_index(inplace=True)
    df_data = df_data[df_data['index'] >= date]
    return pd.concat([df, df_data], axis=0, ignore_index=True)

df = pd.DataFrame()
for ticker in tickers:
    df = get_ticker_history(ticker, date, df)

df = df.rename(columns={'index': 'date'})
df.to_csv('Data/ticker_history.csv', index=False)
df = pd.read_csv('Data/ticker_history.csv')
print(df.head())
