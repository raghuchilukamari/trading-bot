import os
from dotenv import load_dotenv
import pandas as pd
import requests, csv
from yahoo_fin import stock_info as si
import yfinance as yf

load_dotenv()

sp500 = pd.DataFrame( si.tickers_sp500() )
dow = pd.DataFrame( si.tickers_dow())

# nasdaq_del = pd.DataFrame() if os.stat("../input/tickers_del.csv").st_size == 0 else pd.read_csv('../input/tickers_del.csv',header=None)
# tickers_del_list = list(nasdaq_del.iloc[:,0].values)

def get_all_active_stocks():
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    CSV_URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}'
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        df = pd.DataFrame(my_list)
        headers = df.iloc[0]
        listings = pd.DataFrame(df.values[1:], columns=headers)
        listings = listings.set_index('symbol')

    return listings

all_stocks = get_all_active_stocks()
all_stocks.to_csv('../output/all_stocks.csv')

nasdaq = list(all_stocks[(all_stocks['exchange'] == 'NASDAQ') & (all_stocks['assetType'] == 'Stock')].index.values)
# nasdaq_del_list = list(nasdaq_del.iloc[:,0].values)
# nasdaq_final = [t for t in nasdaq if t not in nasdaq_del_list]
pd.DataFrame(nasdaq).to_csv('../output/nasdaq.csv',index=False, header=False)

sp500_dow = set(list(dow.loc[:,0].values) + list(sp500.loc[:,0].values))
pd.DataFrame(sp500_dow).to_csv('../output/sp500_dow.csv',index=False, header=False)

def getstockinfo(tickers):
    stock_info = {}
    tickers_delete = []

    for stock in tickers:
        try:
            # Create a Ticker object for the stock
            ticker = yf.Ticker(stock)
            stock_info[stock] = ticker.info
        except Exception as e:
            # Handle any other exceptions
            print(f"An error occurred for {stock}: {str(e)}")
            tickers_delete.append(stock)

        continue

    pd.DataFrame(tickers_delete).to_csv('tickers_del.csv', index=False, header=False)
    stock_info_df = pd.DataFrame(stock_info).T.convert_dtypes()
    stock_info_df = stock_info_df.round(2)

    return  stock_info_df

stock_info_df = getstockinfo(nasdaq)

stock_info_df.head()

