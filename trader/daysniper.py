import datetime,schedule
from utils.logger import get_logger
import yfinance as yf
import pandas as pd

# Configure the logger

logger = get_logger()

buy_order_placed = False
stop_loss_order_placed = False

def day_sniper_strategy(symbol, quantity, market_open_time, market_close_time):

    global buy_order_placed
    global stop_loss_order_placed 

    current_time = datetime.datetime.now().time()
    logger.info(f"current time is : {current_time}")

    market_open_time_with_15m_buffer = (datetime.datetime.combine(
        datetime.date.today(), market_open_time) + datetime.timedelta(minutes=1)).time()
    market_last_15m_candle_time = (datetime.datetime.combine(
        datetime.date.today(), market_close_time) - datetime.timedelta(minutes=1)).time()

    try:
        logger.info(f"Running day sniper strategy for symbol: {symbol}")

        # Get historical data using yfinance or provide sample data for testing
        data = yf.download(symbol, period='1d', interval='15m')
        data = pd.read_csv('../data.csv', header=0)
        print(data)

        # Extract the close price and low price of the first 15-minute candle
        first_candle = data.iloc[0]
        close_price = first_candle['Close']
        low_price = first_candle['Low']

        if market_open_time <= current_time <= market_open_time_with_15m_buffer and not buy_order_placed:

            logger.info(
                f"Placing buy order for symbol: {symbol}, quantity: {quantity}, price: {close_price}")

            # Place the order with the close price of the first 15-minute candle
            # r.order_buy_limit(symbol, quantity, close_price)
            buy_order_placed = True

            logger.info(
                f"Setting stop loss order for symbol: {symbol}, quantity: {quantity}, stop price: {low_price}")

            # Set the stop loss at the low price of the first 15-minute candle
            # r.order_sell_stop_loss(symbol, quantity, low_price)

            logger.info(
                f"Stop loss order placed for symbol: {symbol}, quantity: {quantity}, stop price: {low_price}")

            stop_loss_order_placed = True
        else:
            logger.info("Not placing any order, outside the time range of first candle") 

        logger.info("Checking if stop loss order got executed")
        stop_loss_order = None

        if stop_loss_order_placed:
            
            stop_loss_order = 'set'
            # Check if the stop loss order is still open
            open_orders = []
            # open_orders = r.orders.get_open_stock_orders()
            # stop_loss_order_status = r.orders.get_stock_order_info(stop_loss_order['id'])['state']
            # stop_loss_order = next((order for order in open_orders if order['side'] == 'sell' and order['stop_price'] == low_price), None)

            for order in open_orders:
                if order['symbol'] == symbol and order['stop_price'] == low_price:
                    stop_loss_order = order
                    break

        if stop_loss_order is None:
            logger.info(f"Stop loss order for symbol: {symbol} got executed")
            schedule.clear('15m')
        else:
            logger.info(f"Stop loss order for symbol: {symbol} is still open")

            # Check if it is the last candle of the day
            last_candle = data.iloc[-1]
            datetime_obj = datetime.datetime.strptime(
                last_candle['Datetime'], "%Y-%m-%d %H:%M:%S")
            current_last_candle_time = datetime_obj.time()
 
            if current_last_candle_time >= market_last_15m_candle_time:
                logger.info(f"Last candle of the day for symbol: {symbol}")

                # The stop loss order didn't get executed, place a market sell order
                logger.info(f"Placing market sell order for symbol: {symbol}, quantity: {quantity}")
                # r.order_sell_market(symbol, quantity)
                logger.info(f"Strategy execution completed for symbol: {symbol}")
                schedule.clear('15m')

            else:
                logger.info("Regular market hours, waiting until close to check stop loss")


    except Exception as e:
        logger.error(f"Error occurred while running strategy for symbol: {symbol}")
        logger.error(str(e))

