import matplotlib.pyplot as mplplt
import matplotlib.dates as mdates
import matplotlib as mpl
import numpy as np
import pandas as pd

from app.utils import InvalidResolutionSettings


class Plotter(object):
    def __init__(self, app):
        self.plt = mplplt
        self.app = app
        self.fig = None
        self.axs = None
        self.main_ax = None
        self.ticks = 0
        self.proxy_df = pd.DataFrame()
        mpl.rcParams.update(mpl.rcParamsDefault)

    def plot_all(self, ticks: int):
        self.fig, self.axs = self.plt.subplots(2, sharex='all', gridspec_kw={'height_ratios': [4, 1]})
        self.main_ax = self.axs[0]
        self.ticks = ticks

        self._prepare_proxy_df()
        self.app.analysis_handler.calculate_all()

        self.app.analysis_handler.plot_all(self.axs, self.ticks)
        self._plot_candles()

        self.plt.savefig('test.png', bbox_inches='tight',
                         pad_inches=0, dpi=int(self.app.config_manager['PLOT']['DPI']))

    def _plot_candles(self):
        plot_df = self.proxy_df.tail(self.ticks)
        self.fig.set_figwidth(int(self.app.config_manager['PLOT']['figwidth']))
        self.fig.set_figheight(int(self.app.config_manager['PLOT']['figheight']))

        # TODO: make adequate parsing
        if self.app.resolution == (4, 'h'):
            self.axs[-1].xaxis.set_major_locator(mdates.DayLocator())
            self.axs[-1].xaxis.set_minor_locator(mdates.HourLocator(byhour=[0, 12]))
            bar_width = 0.8 * 4 / 24
            thin_bar_width = 0.1 * 4 / 24
            self.axs[-1].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            self.axs[-1].xaxis.set_minor_formatter(mdates.DateFormatter(''))
        elif self.app.resolution == (15, 'm'):
            self.axs[-1].xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 4, 8, 12, 16, 20]))
            self.axs[-1].xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0, 30]))
            bar_width = 0.8 * 15 / 24 / 60
            thin_bar_width = 0.1 * 15 / 24 / 60
            self.axs[-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            self.axs[-1].xaxis.set_minor_formatter(mdates.DateFormatter(''))
        else:
            raise InvalidResolutionSettings

        self.axs[-1].tick_params(axis='x', which='major', labelsize=6)

        self.axs[-1].xaxis.grid(True, which='minor', c='silver', lw=.1, ls='-')

        self.main_ax.bar(plot_df.index,
                         plot_df['max_Candle'],
                         color=plot_df['clr_Candle'],
                         width=bar_width)
        self.main_ax.bar(plot_df.index,
                         plot_df['min_Candle'],
                         color='w',
                         width=bar_width)
        self.main_ax.bar(plot_df.index,
                         plot_df['max_Shadow'],
                         color=plot_df['clr_Candle'],
                         width=thin_bar_width)
        self.main_ax.bar(plot_df.index,
                         plot_df['min_Shadow'],
                         color='w',
                         width=thin_bar_width)
        self.main_ax.set_ylim(min(plot_df['min_Shadow']) * (1 - 0.001),
                              max(plot_df['max_Shadow']) * (1 + 0.001))
        self.axs[-1].set_ylim(-max(self.axs[-1].lines[0].get_ydata()), max(self.axs[-1].lines[0].get_ydata()))
        for ax in self.axs:
            ax.grid()
            ax.legend()



    def _prepare_proxy_df(self):
        self.proxy_df = self.app.mem_df

        self.proxy_df['min_Candle'] = self.proxy_df[['Open', 'Close']].min(axis=1)
        self.proxy_df['max_Candle'] = self.proxy_df[['Open', 'Close']].max(axis=1)
        self.proxy_df['clr_Candle'] = np.where((self.proxy_df['Open'] <= self.proxy_df['Close']), 'g', 'r')
        self.proxy_df['min_Shadow'] = self.proxy_df[['Low', 'High']].min(axis=1)
        self.proxy_df['max_Shadow'] = self.proxy_df[['Low', 'High']].max(axis=1)
