import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import numpy as np
import datetime

import pandas as pd


class CandleAnalysisHandler(object):
    def __init__(self, app):
        self.plot_df = pd.DataFrame()
        self.app = app
        self.type = 'candle'
        self.df = pd.DataFrame()

        mpl.rcParams.update(mpl.rcParamsDefault)

    def plot_candles(self, candles_list: list):
        self.df = pd.DataFrame(candles_list)
        self.prepare_df()

        fig, ax = plt.subplots()

        fig.autofmt_xdate()
        fig.set_figwidth(12)
        fig.set_figheight(6)
        dates = [mdates.date2num(datetime.datetime.fromtimestamp(ts)) for ts in self.plot_df.index]

        ax.bar(dates, self.plot_df['max_Candle'], color=self.plot_df['clr_Candle'])
        ax.bar(dates, self.plot_df['min_Candle'], color='b')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())

        plt.ylim(min(self.plot_df['min_Candle']) * (1 - 0.001), max(self.plot_df['max_Candle']) * (1 + 0.001))


        plt.savefig('test.png')


    def prepare_df(self):
        self.df.columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'Volume']
        self.df['Timestamp'] = [int(value) // 1000 for value in self.df['Timestamp']]
        self.df.set_index('Timestamp', inplace=True, drop=True)

        self.plot_df = self.df
        self.plot_df['min_Candle'] = self.plot_df[['Open', 'Close']].min(axis=1)
        self.plot_df['max_Candle'] = self.plot_df[['Open', 'Close']].max(axis=1)
        self.plot_df['clr_Candle'] = np.where((self.plot_df['Open'] <= self.plot_df['Close']), 'g', 'r')
        self.plot_df['min_Shadow'] = self.plot_df[['Low', 'High']].min(axis=1)
        self.plot_df['max_Shadow'] = self.plot_df[['Low', 'High']].max(axis=1)
        # self.plot_df = self.plot_df.drop(['Open', 'Close', 'High', 'Low'], axis=1)
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.max_colwidth', -1,
                               'chained_assignment', None,
                               'expand_frame_repr', False):
            print(self.plot_df)



        # print(self.df)
