from module.strategies import SmaCross, BollingerBandsStrategy, RSIStrategy
from module.optimization import SMAOptTechAnalysis, BB_Opt, RSI_Opt
from module.train_test_split import TrainTestSets
from backtesting import Backtest

import warnings
warnings.filterwarnings("ignore")

# Se separan los datos en train y test
tts = TrainTestSets()
ticker = 'AAPL'
intervals = ["1m", "2m", "5m", "15m", "30m", "1h", "4h", "1d"]
#intervals = ["1h", "4h", "1d", "5d", "1wk"]

data = tts.interval_train_test_split(ticker, intervals)

results_summary = []

# SMA Strategy
sma_opt = SMAOptTechAnalysis(SmaCross)
# Se optimizan primero los parámetros del SMA
sma_results = sma_opt.sma_strategy_opt(
    data,
    n1=range(5, 21, 2),
    n2=range(10, 31, 2))
# Se extrae la fila de la combinación de parámetros e intervalo con mayor 'Return [%]'
sma_best = sma_results.iloc[0]
# Se reemplaza "_train" por "_test" para obtener el nombre del conjunto de prueba correspondiente a la mejor temporalidad
sma_interval = sma_best['interval'].replace('_train', '_test')
# Se corre el backtesting con los parámetros e intervalo óptimo
bt = Backtest(
    data[sma_interval],
    SmaCross,
    cash=10000000,
    commission=0.002)

sma_stats = bt.run(
    n1=int(sma_best['n1']),
    n2=int(sma_best['n2']))
results_summary.append({'Strategy': 'SMA', 'Return [%]': sma_stats['Return [%]'], 'Trades': sma_stats['# Trades']})
bt.plot()

# Bollinger Bands Strategy
bb_opt = BB_Opt(BollingerBandsStrategy)
# Se optimizan primero los parámetros de BB
bb_results = bb_opt.bb_strategy_opt(
    data,
    n_range=range(10, 30, 5),
    std_range=[1.5, 2, 2.5, 3])

# Se extrae la fila de la combinación de parámetros e intervalo con mayor 'Return [%]'
bb_best = bb_results.iloc[0]
# Se reemplaza "_train" por "_test" para obtener el nombre del conjunto de prueba correspondiente a la mejor temporalidad
bb_interval = bb_best['interval'].replace('_train', '_test')
# Se corre el backtesting con los parámetros e intervalo óptimo
bt = Backtest(
    data[bb_interval],
    BollingerBandsStrategy,
    cash=10000000,
    commission=0.002)

bb_stats = bt.run(n=int(bb_best['n']), n_std=float(bb_best['n_std']))
results_summary.append({'Strategy': 'Bollinger Bands', 'Return [%]': bb_stats['Return [%]'], 'Trades': bb_stats['# Trades']})
bt.plot()

# RSI Strategy
rsi_opt = RSI_Opt(RSIStrategy)

# Se optimizan primero los parámetros del RSI
rsi_results = rsi_opt.rsi_strategy_opt(
    data,
    period_range=range(10, 21),
    overbought_range=[65, 70, 75],
    oversold_range=[25, 30, 35]
)

# Se extrae la fila de la combinación de parámetros e intervalo con mayor 'Return [%]'
rsi_best = rsi_results.iloc[0]

# Se reemplaza "_train" por "_test" para obtener el nombre del conjunto de prueba correspondiente a la mejor temporalidad
rsi_interval = rsi_best['interval'].replace('_train', '_test')

# Se corre el backtesting con los parámetros e intervalo óptimo
bt = Backtest(data[rsi_interval], RSIStrategy, cash=10000000, commission=0.002)
rsi_stats = bt.run(
    period=int(rsi_best['period']),
    overbought=float(rsi_best['overbought']),
    oversold=float(rsi_best['oversold'])
)
results_summary.append({'Strategy': 'RSI', 'Return [%]': rsi_stats['Return [%]'], 'Trades': rsi_stats['# Trades']})
bt.plot()

# Comparación final
import pandas as pd
comparison_df = pd.DataFrame(results_summary)
print("\n🔍 Comparativa Final entre Estrategias:\n")
print(comparison_df.sort_values(by='Return [%]', ascending=False))


