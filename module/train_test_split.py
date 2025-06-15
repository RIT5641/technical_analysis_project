import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

class TrainTestSets:
    def __init__(self):
        pass

    def get_interval_dates(self, interval):
        today = datetime.today().date()

        # Intervalos ultra intradía (máximo 7 días)
        if interval == "1m":
            start = today - timedelta(days=6)
        # Intervalos intradía con límite de ~30 días (ajustado por disponibilidad real)
        elif interval in ["2m", "5m"]:
            start = today - timedelta(days=29)
        # Intervalos con límite de ~60 días
        elif interval in ["15m", "30m", "60m", "90m", "1h", "4h"]:
            start = today - timedelta(days=59)
        # Intervalos diarios o mayores sin límite (usamos 2 años)
        else:
            start = today - timedelta(days=730)

        return str(start), str(today)

    def train_test_split(self, ticker, interval):
        start, end = self.get_interval_dates(interval)

        data = yf.download(tickers=ticker, start=start, end=end, interval=interval)

        # Asegura que el DataFrame tenga columnas planas
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)

        # Elimina valores faltantes
        data.dropna(inplace=True)

        split_idx = int(len(data) * 0.7)
        train = data.iloc[:split_idx]
        test = data.iloc[split_idx:]
        return (train, test)

    def interval_train_test_split(self, ticker, intervals):
        all_data = {}
        for interval in intervals:
            train, test = self.train_test_split(ticker, interval)
            all_data[f"{interval}_train"] = train
            all_data[f"{interval}_test"] = test
        return all_data



