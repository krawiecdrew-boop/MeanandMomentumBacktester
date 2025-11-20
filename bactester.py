import yfinance as glhf

stocks = ["SPY", "QQQ", "DIA", "IWM", "EFA",
    "EEM", "TLT", "IEF", "GLD", "XLP"]

data = glhf.download(stocks, start="2015-01-01", end="2025-01-01", threads = True)
print(data.tail())

close_prices = data["Close"]
rolling_mean = close_prices.rolling(window=20).mean()
rolling_std = close_prices.rolling(window=20).std()


z_score = (close_prices - rolling_mean) / rolling_std

upper_threshold = 1
lower_threshold = -1

signals = {}
for ticker in z_score.columns:
    positions = []
    for z in z_score[ticker]:
        if z > 1:
            positions.append(-1)
        elif z < -1:
            positions.append(1)
        else:
            positions.append(0)
    signals[ticker] = positions


#Momentum Trading Use ROC
price_today = close_prices
price_tendays_ago = close_prices.shift(10)
roc = (price_today-price_tendays_ago)/price_tendays_ago


momentum_signals = {}
for ticker in roc.columns:
    positions =[]
    for value in roc[ticker]:
        if value > 1:
            positions.append(1) #upward momentum
        elif value < -1:
            positions.append(-1) #downward momentum
        else:
            positions.append(0)
    momentum_signals[ticker] = positions