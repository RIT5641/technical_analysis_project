import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import warnings
warnings.filterwarnings('ignore')

class SmaCross(Strategy):
    n1 = 5
    n2 = 13
    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()

class BollingerBandsStrategy(Strategy):
    n = 20  # lookback para SMA y desviación
    n_std = 2  # desviaciones estándar

    def init(self):
        self.sma = self.I(SMA, self.data.Close, self.n)
        self.std = self.I(lambda x: pd.Series(x).rolling(self.n).std().to_numpy(), self.data.Close)

    def next(self):
        price = self.data.Close[-1]
        upper = self.sma[-1] + self.n_std * self.std[-1]
        lower = self.sma[-1] - self.n_std * self.std[-1]

        if price < lower and not self.position.is_long:
            self.buy()
        elif price > upper and not self.position.is_short:
            self.sell()
        elif lower <= price <= upper:
            self.position.close()
