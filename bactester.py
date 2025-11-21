import yfinance as glhf

etfs = ["SPY", "QQQ", "DIA", "IWM", "EFA",
    "EEM", "TLT", "IEF", "GLD", "XLP"]



data_etfs = glhf.download(etfs, start="2024-11-15", end="2025-01-01", threads = True)
print(data_etfs.tail())

close_etfs = data_etfs["Close"].dropna()
volume = data_etfs["Volume"]
#Momentum Trading Use ROC
price_today = close_etfs
price_tendays_ago = close_etfs.shift(10)
roc = (close_etfs-price_tendays_ago)/price_tendays_ago
roc_indexed = roc.iloc[20:]

momentum_signals = {}
for ticker in roc_indexed.columns:
    positions =[]
    for value in roc_indexed[ticker]:
        if value > 0.05:
            positions.append(1) #upward momentum
        elif value < -0.05:
            positions.append(-1) #downward momentum
        else:
            positions.append(0)
    momentum_signals[ticker] = positions


print ("Momentum symbols: ")
for ticker in momentum_signals:
    positions = momentum_signals[ticker]
    print (f"{ticker}: {positions}")




volatile_stocks = ["AMD", "NVDA", "TSLA", "SHOP", "AAPL",
                   "SNAP", "ZM", "ROKU", "PINS", "UBER"]

data_volatile = glhf.download(volatile_stocks, start="2024-11-15", end="2025-01-01", threads = True)
print(data_volatile.tail())

close_vol = data_volatile["Close"].dropna()
volume = data_volatile["Volume"]

rolling_mean = close_vol.rolling(window=20).mean() #mean inside current 20day window
rolling_std = close_vol.rolling(window=20).std() #std deviation inside current 20day window

z_score = (close_vol - rolling_mean) / rolling_std
z_score_indexed = z_score.iloc[20:] # Ignores first 19 days when rolling mean and std can't be calculated
upper_threshold = 1
lower_threshold = -1
#Mean revision
signals = {}
for ticker in z_score_indexed.columns:
    positions = []
    for z in z_score_indexed[ticker]:
        if z > 1:
            positions.append(-1) #z-score greater than one so we sell bc stock will drop down in price to return to average
        elif z < -1:
            positions.append(1) #z-score less than one so we buy bc stock will increase in price to return to average
        else:
            positions.append(0) #z-score not strong enough to warrant a trade (not far enough away from average)
    signals[ticker] = positions

print ("Mean revision symbols: ")
for ticker in signals:
    positions = signals[ticker]
    print (f"{ticker}: {positions}")
