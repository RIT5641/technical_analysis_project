import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import warnings
warnings.filterwarnings('ignore')

class SmaCross(Strategy):
    '''
    En esta estrategiam se usan dos medias móviles simples (SMA) con diferentes periodos:
    - Una rápida (5 días)
    - Una lenta (13 días)
    Se compra cuando la media rápida cruza por encima de la lenta (señal alcista),
    y se cierra la posición cuando la media rápida cruza por debajo (señal bajista).
    Es una estrategia basada en la detección de tendencias.
    '''
    n1 = 5
    n2 = 13
    def init(self):
        # Registra la media móvil rápida (n1)
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        # Registra la media móvil lenta (n2)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        # Compra si la media rápida cruza por encima de la lenta
        if crossover(self.sma1, self.sma2):
            self.buy()
        # Cierra la posición si la lenta cruza por encima de la rápida
        elif crossover(self.sma2, self.sma1):
            self.position.close()

class BollingerBandsStrategy(Strategy):
    '''
    Calcula una media móvil simple (SMA) y dos bandas que se sitúan a cierta cantidad
    de desviaciones estándar por encima y por debajo de la SMA.
    Se compra cuando el precio atraviesa la banda inferior (sobreventa), y se vende
    cuando el precio atraviesa la banda superior (sobrecompra).
    La posición se cierra cuando el precio vuelve a moverse dentro de las bandas.
    Es una estrategia de reversión a la media, útil en mercados laterales.
    '''
    n = 20
    n_std = 2

    def init(self):
        close = self.data.Close
        self.sma = self.I(SMA, close, self.n)

        # Calcula y registra el std como indicador
        self.std = self.I(lambda x: pd.Series(x).rolling(self.n).std().to_numpy(), close)

        # Registra bandas superiores e inferiores como indicadores para que se ploteen
        self.upper_band = self.I(lambda sma, std: sma + self.n_std * std, self.sma, self.std)
        self.lower_band = self.I(lambda sma, std: sma - self.n_std * std, self.sma, self.std)

    def next(self):
        price = self.data.Close[-1]
        upper = self.upper_band[-1]
        lower = self.lower_band[-1]

        # Se ejecuta una compra cuando el precio rompe la banda inferior
        if price < lower and not self.position.is_long:
            self.buy()
        # Se ejecuta una venta cuando el precio rompe la banda superior
        elif price > upper and not self.position.is_short:
            self.sell()
        # Cierra la posición si el precio vuelve dentro del canal
        elif lower <= price <= upper:
            self.position.close()

# Función para calcular el RSI
def RSI(series, period=14):
    # Cambios entre precios consecutivos
    delta = pd.Series(series).diff()
    # Se conservan los valores positivos en "gain", mostrando en dónde el precio subió.
    gain = delta.clip(lower=0)
    # Se conservan los valores negativos en "loss", mostrando en dónde el precio bajó.
    loss = -delta.clip(upper=0)

    # Promedios móviles de ganancias y pérdidas
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    # Cálculo del RS y RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.fillna(0).to_numpy()

# Clase de estrategia usando RSI
class RSIStrategy(Strategy):
    '''
    Usa el indicador RSI para medir la fuerza del impulso del precio en una escala de 0 a 100.
    Se compra cuando el RSI cae por debajo de 30 (sobreventa), y se vende cuando el RSI supera 70 (sobrecompra).
    La posición se cierra cuando el RSI vuelve a una zona neutral (por ejemplo, entre 40 y 60).
    Esta estrategia intenta capturar puntos de reversión en el mercado.
    '''
    period = 14           # Ventana para RSI
    # Umbral superior
    overbought = 70
    # Umbral inferior
    oversold = 30

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

class passive_strategy(Strategy):
    '''
    Compra el activo una sola vez al inicio del periodo y mantiene la posición abierta sin venderla.
    Esta estrategia no reacciona al mercado ni genera señales; sirve como punto de comparación base
    para evaluar si las estrategias activas realmente aportan valor extra
    '''
    def init(self):
        pass
    def next(self):
        if not self.position:
            self.buy()
