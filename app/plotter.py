import matplotlib.pyplot as mplplt
import matplotlib.dates as mdates
import matplotlib as mpl
import numpy as np
import pandas as pd
import datetime
import math

from app.utils import InvalidResolutionSettings, ConfigClass


class Plotter(ConfigClass):
    def __init__(self, app):
        super().__init__()
        self.plt = mplplt
        self.app = app
        self.axs = None
        self.fig = None
        self.main_ax = None
        self.ticks = 0
        self.proxy_df = pd.DataFrame()
        mpl.rcParams.update(mpl.rcParamsDefault)

    def plot_all(self, ticks: int):

        timer = datetime.datetime.now()
        self.fig, self.axs = self.plt.subplots(2,
                                               sharex='all',
                                               gridspec_kw={'height_ratios': [3, 1],
                                                            'wspace': 0.025,
                                                            'hspace': 0.05})
        # self.fig, self.axs = self.plt.subplots()
        # self.axs = (self.axs,)
        self.main_ax = self.axs[0]
        self.ticks = ticks

        self._prepare_proxy_df()
        self.app.analysis_handler.calculate_all()

        self._plot_candles()
        self.app.analysis_handler.plot_all(self.axs, self.ticks)
        self._configure_figure()
        self.plt.savefig(self.config_manager['PLOT']['filepath'], bbox_inches='tight',
                         pad_inches=0, dpi=int(self.app.config_manager['PLOT']['DPI']))
        print('plot end in {}'.format(datetime.datetime.now() - timer))

    def _configure_figure(self):
        self.fig.set_figwidth(int(self.app.config_manager['PLOT']['figwidth']))
        self.fig.set_figheight(int(self.app.config_manager['PLOT']['figheight']))

        for ax in self.axs:
            ax.grid()
            ax.legend()
            if not ax.lines or ax == self.axs[0]:
                continue
            max_point = 0
            min_point = 0
            for line in ax.lines:
                if line.get_label()[:5] == 'Stoch':
                    ax.set_ylim(0, 100)
                    return
                _max = max(max(line.get_ydata()), math.fabs(min(line.get_ydata())))
                max_point = max(max_point, _max)
                min_point = min(min_point, - _max)
            ax.set_ylim(min_point, max_point)

    def _plot_candles(self):
        plot_df = self.proxy_df.tail(self.ticks)
        # TODO: refactor this
        if self.app.resolution == (4, 'h'):
            self.axs[-1].xaxis.set_major_locator(mdates.DayLocator())
            self.axs[-1].xaxis.set_minor_locator(mdates.HourLocator(byhour=[0, 12]))
            bar_width = 0.8 * 4 / 24
            thin_bar_width = 0.1 * 4 / 24
            self.axs[-1].xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            self.axs[-1].xaxis.set_minor_formatter(mdates.DateFormatter(''))
        elif self.app.resolution == (1, 'd'):
            self.axs[-1].xaxis.set_major_locator(mdates.DayLocator(interval=10))
            self.axs[-1].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
            bar_width = 0.8 * 1
            thin_bar_width = 0.1 * 1
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
        # TODO: watch!
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

    def _prepare_proxy_df(self):
        self.proxy_df = self.app.mem_df

        self.proxy_df['min_Candle'] = self.proxy_df[['Open', 'Close']].min(axis=1)
        self.proxy_df['max_Candle'] = self.proxy_df[['Open', 'Close']].max(axis=1)
        self.proxy_df['clr_Candle'] = np.where((self.proxy_df['Open'] <= self.proxy_df['Close']), 'g', 'r')
        self.proxy_df['min_Shadow'] = self.proxy_df[['Low', 'High']].min(axis=1)
        self.proxy_df['max_Shadow'] = self.proxy_df[['Low', 'High']].max(axis=1)
