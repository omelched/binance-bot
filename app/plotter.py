import matplotlib.pyplot as mplplt
import matplotlib.dates as mdates
import matplotlib as mpl
import numpy as np

import pandas as pd


class Plotter(object):
    def __init__(self, app):
        self.plt = mplplt
        self.app = app
        self.fig = None
        self.ax = None
        self.proxy_df = pd.DataFrame()
        mpl.rcParams.update(mpl.rcParamsDefault)

    def plot_all(self):
        self.fig, self.ax = self.plt.subplots()

        self._prepare_proxy_df()

        self._plot_candles()

        self.app.analysis_handler.calculate_all()
        self.app.analysis_handler.plot_all(self.ax)

        # with pd.option_context('display.max_rows', None,
        #                        'display.max_columns', None,
        #                        'display.max_colwidth', -1,
        #                        'chained_assignment', None,
        #                        'expand_frame_repr', False):
        #     print(self.analysis_metrics_df)

        self.plt.savefig('test.png', bbox_inches='tight',
                         pad_inches=0, dpi=int(self.app.config_manager['PLOT']['DPI']))

    def _plot_candles(self):
        self.fig.set_figwidth(int(self.app.config_manager['PLOT']['figwidth']))
        self.fig.set_figheight(int(self.app.config_manager['PLOT']['figheight']))

        self.ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 4, 8, 12, 16, 20]))
        self.ax.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0, 30]))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.ax.xaxis.set_minor_formatter(mdates.DateFormatter(''))
        self.ax.xaxis.grid(True, which='minor', c='silver', lw=.1, ls='-')

        self.ax.bar(self.proxy_df.index,
                    self.proxy_df['max_Candle'],
                    color=self.proxy_df['clr_Candle'],
                    width=12 / 24 / 60)
        self.ax.bar(self.proxy_df.index,
                    self.proxy_df['min_Candle'],
                    color='w',
                    width=12 / 24 / 60)
        self.ax.bar(self.proxy_df.index,
                    self.proxy_df['max_Shadow'],
                    color=self.proxy_df['clr_Candle'],
                    width=1.5 / 24 / 60)
        self.ax.bar(self.proxy_df.index,
                    self.proxy_df['min_Shadow'],
                    color='w',
                    width=1.5 / 24 / 60)

        self.plt.ylim(min(self.proxy_df['min_Shadow']) * (1 - 0.001),
                      max(self.proxy_df['max_Shadow']) * (1 + 0.001))
        self.plt.grid()

    def _prepare_proxy_df(self):
        self.proxy_df = self.app.mem_df.tail(96)

        self.proxy_df['min_Candle'] = self.proxy_df[['Open', 'Close']].min(axis=1)
        self.proxy_df['max_Candle'] = self.proxy_df[['Open', 'Close']].max(axis=1)
        self.proxy_df['clr_Candle'] = np.where((self.proxy_df['Open'] <= self.proxy_df['Close']), 'g', 'r')
        self.proxy_df['min_Shadow'] = self.proxy_df[['Low', 'High']].min(axis=1)
        self.proxy_df['max_Shadow'] = self.proxy_df[['Low', 'High']].max(axis=1)
