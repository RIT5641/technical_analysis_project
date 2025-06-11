import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

# Estrategia 1: Bandas de Bollinger (Overlay)
class BBandsStrategy(Strategy):
    def init(self):
        close = self.data.Close
        # Media móvil simple de 20 periodos
        self.ma20 = self.I(pd.Series.rolling, close, 20).mean()
        # Desviación estándar de 20 periodos
        self.std20 = self.I(pd.Series.rolling, close, 20).std()
        # Bandas superior e inferior
        self.upper = self.I(lambda m, s: m + 2 * s, self.ma20, self.std20)
        self.lower = self.I(lambda m, s: m - 2 * s, self.ma20, self.std20)

    def next(self):
        price = self.data.Close[-1]
        # Señal de compra: precio cruza por encima de la banda superior
        if crossover(self.data.Close, self.upper):
            self.position.close()
            self.buy()
        # Señal de venta: precio cruza por debajo de la banda inferior
        elif crossover(self.lower, self.data.Close):
            self.position.close()
            self.sell()

# Estrategia 2: RSI (Oscilador)
class RSIStrategy(Strategy):
    def init(self):
        close = self.data.Close
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        # Media móvil de ganancias y pérdidas (14 periodos)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        # RSI
        self.rsi = self.I(lambda x: 100 - (100 / (1 + x)), rs)

    def next(self):
        # Entrada en sobreventa (RSI cruza al alza 30)
        if self.rsi[-1] < 30 and self.rsi[-2] >= 30:
            self.position.close()
            self.buy()
        # Salida en sobrecompra (RSI cruza a la baja 70)
        elif self.rsi[-1] > 70 and self.rsi[-2] <= 70:
            self.position.close()
            self.sell()

if __name__ == "__main__":
    # Descargar datos de Bitcoin (BTC-USD)
    data = yf.download("BTC-USD", start="2020-01-01", end="2025-06-10")

    # Backtest para Bandas de Bollinger
    bt_bb = Backtest(data, BBandsStrategy, cash=10000, commission=0.002)
    stats_bb = bt_bb.run()
    print("=== Resultados Bollinger Bands ===")
    print(stats_bb)
    bt_bb.plot()

    # Backtest para RSI
    bt_rsi = Backtest(data, RSIStrategy, cash=10000, commission=0.002)
    stats_rsi = bt_rsi.run()
    print("=== Resultados RSI ===")
    print(stats_rsi)
    bt_rsi.plot()