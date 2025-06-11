from backtesting import Backtest
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class SMAOptTechAnalysis:
    def __init__(self, Strategy):
        self.Strategy = Strategy

    def sma_params_n_tf_opt(self, set_type, data, n1, n2):
        bt = Backtest(data, self.Strategy, cash=10000000, commission=0.002)
        stats, heatmap = bt.optimize(
            n1=n1,
            n2=n2,
            constraint=lambda p: p.n1 < p.n2,
            maximize='Return [%]',  # Se pueden usar metricas de rendimiento de stats
            return_heatmap=True
        )

        best_params = heatmap.sort_values(ascending=False)
        best_results = {'interval': set_type,
                        'n1': best_params.index[0][0],
                        'n2': best_params.index[0][1],
                        'Return [%]': best_params.iloc[0],
                        'No. Tradees': stats['# Trades']
                        }
        return best_results

    def sma_strategy_opt(self, all_data, n1, n2):
        train_results = []
        for set_type, df in all_data.items():
            if "train" in set_type:
                train_results.append(self.sma_params_n_tf_opt(set_type, df, n1, n2))
        optimal_tf_df = pd.DataFrame(train_results)
        return optimal_tf_df.sort_values(by='Return [%]', ascending=False)


class BB_Opt:
    def __init__(self, Strategy):
        self.Strategy = Strategy

    def bb_params_opt(self, set_type, data, n_range, std_range):
        bt = Backtest(data, self.Strategy, cash=10000000, commission=0.002)
        stats, heatmap = bt.optimize(
            n=n_range,
            n_std=std_range,
            maximize='Return [%]',
            return_heatmap=True
        )

        best_params = heatmap.sort_values(ascending=False)
        best_results = {
            'interval': set_type,
            'n': best_params.index[0][0],
            'n_std': best_params.index[0][1],
            'Return [%]': best_params.iloc[0],
            'No. Trades': stats['# Trades']
        }
        return best_results

    def bb_strategy_opt(self, all_data, n_range, std_range):
        train_results = []
        for set_type, df in all_data.items():
            if "train" in set_type:
                train_results.append(self.bb_params_opt(set_type, df, n_range, std_range))
        optimal_tf_df = pd.DataFrame(train_results)
        return optimal_tf_df.sort_values(by='Return [%]', ascending=False)
