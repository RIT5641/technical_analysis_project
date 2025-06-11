import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from backtesting import Backtest
from module.train_test_split import TrainTestSets
from module.strategies import BollingerBandsStrategy
from module.optimization import BB_Opt
import warnings
warnings.filterwarnings("ignore")

tts = TrainTestSets()
ticker = 'BTC-USD'
intervals = ["1h", "4h", "1d", "5d", "1wk"]
# Este es un diccionario
data = tts.interval_train_test_split(ticker, intervals)

bb_optimizer = BB_Opt(BollingerBandsStrategy)
results = bb_optimizer.bb_strategy_opt(data, n_range=range(10,31,2),std_range=[1.5,2,2.5])
##print(results)

best_params = results[results['interval'] == '1d_train'].iloc[0]
n_opt = int(best_params['n'])
n_std_opt = float(best_params['n_std'])
print(data)

'''
bt = Backtest(data, BollingerBandsStrategy, cash=10000, commission=0.002)
stats = bt.run(n=n_opt, n_std=n_std_opt)
bt.plot()

'''



