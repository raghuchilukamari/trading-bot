import yfinance as yf
import pandas as pd

def get_data(tickers, start_date, end_date):
    date_range = pd.date_range(start_date, end_date)
    prices = pd.DataFrame(index=date_range)

    for ticker in tickers:
        try:
            data = yf.download(ticker,start_date,end_date)[['Adj Close','Volume']]
            print('fetched data for {0} from {1} to {2}'.format(ticker, data.index.min(), data.index.max()))
            data = data.rename(columns = {'Adj Close': 'Close'})
            prices = prices.join(data)
            prices = prices.dropna()
            # tickers_got.append(ticker)
         
        except Exception as e:
        # Handle any other exceptions
            print(f"An error occurred for {ticker}: {str(e)}")
            # tickers_delete.append(ticker)
    
    return prices


def get_daily_returns(data):
    rets = (data/data.shift(1)) -1
    rets.iloc[0,:]= 0
    rets.columns = rets.columns + '_Chg'
    return pd.concat([data, rets], axis=1)