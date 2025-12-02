class MeanReversion:
    def __init__(self, window = 20, upper = 1, lower = -1):
        self.window = window
        self.upper = upper
        self.lower = lower
    def generate_signals(self,close_vol):
        rolling_mean = close_vol.rolling(window=20).mean()  # mean inside current 20day window
        rolling_std = close_vol.rolling(window=20).std()  # std deviation inside current 20day window

        z_score = (close_vol - rolling_mean) / rolling_std
        z_score_indexed = z_score.iloc[self.window:, :]

        signals = {}
        for ticker in z_score_indexed.columns:
            positions = []
            for z in z_score_indexed[ticker]:
                if z > 1:
                    positions.append(
                        -1)  # z-score greater than one so we sell bc stock will drop down in price to return to average
                elif z < -1:
                    positions.append(
                        1)  # z-score less than one so we buy bc stock will increase in price to return to average
                else:
                    positions.append(
                        0)  # z-score not strong enough to warrant a trade (not far enough away from average)
            signals[ticker] = positions
        return signals