import yfinance as glhf

from momentum import MomentumStrategy
from reversion import MeanReversion

choice = input("What stocks would you like to analyse? Type 'E' for ETFS or 'V' for Volatile Stocks ")

if choice == 'E':
    etfs = ["SPY", "QQQ", "DIA", "IWM", "EFA",
    "EEM", "TLT", "IEF", "GLD", "XLP"]

    data_etfs = glhf.download(etfs, start="2024-11-15", end="2025-01-01", threads = True)

    close_etfs = data_etfs["Close"].dropna()
    volume = data_etfs["Volume"]
    strategy_name = "Momentum Strategy"

    momentum = MomentumStrategy()
    signals = momentum.generate_signals(close_etfs)

elif choice == 'V':
    volatile_stocks = ["AMD", "NVDA", "TSLA", "SHOP", "AAPL",
                       "SNAP", "ZM", "ROKU", "PINS", "UBER"]

    data_volatile = glhf.download(volatile_stocks, start="2024-11-15", end="2025-01-01", threads=True)
    close_vol = data_volatile["Close"].dropna()
    volume = data_volatile["Volume"]
    reversion = MeanReversion()
    signals = reversion.generate_signals(close_vol)
    strategy_name = "Mean Reversion Strategy"

else:
    print("Invalid choice")
    quit()

print (f"{strategy_name} Signals:")
print("Key buy = 1, sell = -1, hold = 0 ")
for ticker in signals:
    signal = signals[ticker]
    print(f"{ticker}: {signal}")


















