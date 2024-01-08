from yahoo_fin.stock_info import *
import pandas as pd

tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META']

def get_ticker_history(ticker, df):
    print(ticker)
    df_data = get_data(ticker)
    df_data.reset_index(inplace=True)
    df_data = df_data[df_data['index'] >= '2023-01-01']
    return pd.concat([df, df_data], axis=0, ignore_index=True)

df = pd.DataFrame()
for ticker in tickers:
    df = get_ticker_history(ticker, df)

print(df.head())
print(df.tail())