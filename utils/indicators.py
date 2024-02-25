from ta.volatility import BollingerBands


def bollinger_bands(stock_data):
    
    indicator_bb = BollingerBands(close=stock_data["Close"], window=20, window_dev=2)
    stock_data["bb_lowerband"] = indicator_bb.bollinger_lband()
    stock_data["bb_upperband"] = indicator_bb.bollinger_hband()
    stock_data['bb_lb_cross'] = indicator_bb.bollinger_lband_indicator()
    stock_data['bb_ub_cross'] = indicator_bb.bollinger_hband_indicator()
    
    return stock_data