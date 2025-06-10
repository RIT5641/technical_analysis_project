import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from module.train_test_split import TrainTestSets

tts = TrainTestSets()
ticker = "BTC-USD"
intervals = ["4h", "1d", "1mo", "1wk"]

data = tts.interval_train_test_split(ticker, intervals)
print(data.keys)