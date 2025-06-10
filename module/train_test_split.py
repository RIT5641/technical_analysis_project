import yfinance as yf

class TrainTestSets:
    def __init__(self):
        pass

    def train_test_split(self, ticker, interval):
        if interval in ["1m", "2m", "5m", "30m"]:
            start = "2025-05-31"
            end = "2025-06-06"
        elif interval in ["15m", "60m", "90m"]:
            start = "2025-04-28"
            end = "2025-05-31"
        elif interval in ["1h", "4h", "1d", "5d", "1wk"]:
            start = "2024-06-06"
            end = "2025-06-06"

        data = yf.download(tickers=ticker, start=start, end=end, interval=interval)
        data.columns = data.columns.droplevel(1)

        split_idx = int(len(data) * 0.7)

        train = data.iloc[:split_idx]
        test = data.iloc[split_idx:]
        return train, test

    def interval_train_test_split(self, ticker, intervals):
        all_data = {}
        #intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "4h", "1d", "5d", "1wk"]
        intervals = ["1h", "4h"]
        for interval in intervals:
            data_from_split = self.train_test_split(ticker, interval)
            all_data[f"{interval}_train"] = data_from_split[0]
            all_data[f"{interval}_test"] = data_from_split[1]

        return all_data



