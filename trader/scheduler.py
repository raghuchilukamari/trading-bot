import datetime, schedule, time
from daysniper import day_sniper_strategy
from utils.logger import get_logger

logger = get_logger()

market_open_time = datetime.time(hour=13, minute=21)
market_close_time = datetime.time(hour=16)

stock_symbols = ['RIVN']
quantities = [1]

def run_day_sniper_every_15min(symbol, quantity, market_open_time, market_close_time):
    # Get current time and check if it's within the desired time range (6:30 AM to 1:00 PM MST)
    current_time = datetime.datetime.now().time()

    if market_open_time <= current_time <= market_close_time:
        day_sniper_strategy(
            symbol, quantity, market_open_time, market_close_time)
    else:
        schedule.clear('15m')


def trigger_day_sniper_strategy(symbol, quantity, market_open_time, market_close_time):

    # trigger day sniper strategy first time
    day_sniper_strategy(symbol, quantity, market_open_time, market_close_time)

    # Schedule the strategy to run every 15 minutes for each stock symbol after first run
    schedule.every(1).minutes.until(market_close_time).do(
        run_day_sniper_every_15min, symbol=symbol, quantity=quantity,market_close_time=market_close_time, market_open_time=market_open_time).tag('15m')

# Schedule the strategy to run at the market start time for each stock symbol
for symbol, quantity in zip(stock_symbols, quantities):
    schedule.every().day.at(str(market_open_time)).do(
        trigger_day_sniper_strategy, symbol=symbol, quantity=quantity, market_close_time=market_close_time, market_open_time=market_open_time).tag('daily')
    
# # Schedule the strategy to run every 15 minutes for each stock symbol
# for symbol, quantity in zip(stock_symbols, quantities):
#     schedule.every(15).minutes.until(market_close_time).do(
#         run_day_sniper_every_15min, symbol=symbol, quantity=quantity).tag('15m')
    
# Keep the program running and execute scheduled tasks
while True:
    current_time = datetime.datetime.now().time()

    # logger.info(f"Current time: {current_time}")
    if current_time > market_close_time:
        logger.info("After market hours, exiting loop")
        break

    schedule.run_pending()
    time.sleep(1)
