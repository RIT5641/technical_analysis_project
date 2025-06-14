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
    n = 20
    n_std = 2

    def init(self):
        close = self.data.Close
        self.sma = self.I(SMA, close, self.n)

        # Calcula y registra el std como indicador
        self.std = self.I(lambda x: pd.Series(x).rolling(self.n).std().to_numpy(), close)

        # Registra bandas como indicadores para que se ploteen
        self.upper_band = self.I(lambda sma, std: sma + self.n_std * std, self.sma, self.std)
        self.lower_band = self.I(lambda sma, std: sma - self.n_std * std, self.sma, self.std)

    def next(self):
        price = self.data.Close[-1]
        upper = self.upper_band[-1]
        lower = self.lower_band[-1]

        if price < lower and not self.position.is_long:
            self.buy()
        elif price > upper and not self.position.is_short:
            self.sell()
        elif lower <= price <= upper:
            self.position.close()



# Función para calcular el RSI
def RSI(series, period=14):
    delta = pd.Series(series).diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.fillna(0).to_numpy()

# Clase de estrategia usando RSI
class RSIStrategy(Strategy):
    period = 14           # Ventana para RSI
    overbought = 70       # Umbral superior
    oversold = 30         # Umbral inferior

    def init(self):
        # Registrar el indicador RSI como un array compatible con backtesting.py
        self.rsi = self.I(RSI, self.data.Close, self.period)

    def next(self):
        rsi = self.rsi[-1]
        price = self.data.Close[-1]

        # Señal de compra si hay sobreventa
        if rsi < self.oversold and not self.position.is_long:
            self.buy()

        # Señal de venta si hay sobrecompra
        elif rsi > self.overbought and not self.position.is_short:
            self.sell()

        # Cerrar posición si RSI vuelve al rango neutral
        elif 40 < rsi < 60:
            self.position.close()
