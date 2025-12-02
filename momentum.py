class MomentumStrategy:

    def __init__(self, window = 20, threshold = 0.04):
        self.window = window
        self.threshold = threshold

    def generate_signals(self, prices):
        price_today = prices
        price_tendays_ago = prices.shift(10)

        roc = (price_today - price_tendays_ago) / price_tendays_ago
        roc_indexed = roc.iloc[self.window:, :]

        momentum_signals = {}
        for ticker in roc_indexed.columns:
            positions = []
            for value in roc_indexed[ticker]:
                if value > self.threshold:
                    positions.append(1)  # upward momentum
                elif value < -self.threshold:
                    positions.append(-1)  # downward momentum
                else:
                    positions.append(0)
            momentum_signals[ticker] = positions
        return momentum_signals