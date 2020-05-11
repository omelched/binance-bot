import pandas as pd
import numpy as np
from app.utils import ConfigClass
from matplotlib.axes import Axes

from app.utils import NonExistingIndicatorParameter


class Indicator(ConfigClass):
    """
    Базовый класс Индикаторов.
    Все классы наследуются от него.
    """

    def __init__(self, model: str, name: str):
        """
        Метод инициализации.
        Устанавливаются наименования модели, наименование индикатора,
        создается пустой словарь параметров, нулевой результат вычисления индикатора.

        :type model: str
        :type name: str
        :param model: — имя модели индикатора
        :param name:
        """
        super().__init__()
        self.model = model
        self.name = name
        self.parameters = {}
        self.result = pd.DataFrame()

    def calculate(self, proxy_df: pd.DataFrame):
        self.result = pd.DataFrame(np.zeros(len(proxy_df.index), 1))

    def plot(self, ax: Axes, ticks: int, colour: str = 'b'):
        df = self.result.tail(ticks)
        ax.plot(df.index, df[0], c=colour, lw=1)

    def _get_parameters_dict(self):
        if self.model == 'SMA':
            return {'length': 0,
                    'target': ''}

    def _fill_in_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.parameters.keys():
                self.parameters.update({key: value})
            else:
                raise NonExistingIndicatorParameter


class SMA(Indicator):
    """
    Класс Индикатора SMA.
    Дочерний класс Indicator
    """

    def __init__(self, length: int = None, target: str = None):
        """
        Метод инициализации.
        Инициализирцется родительский класс.
        Устанавливаются параметры length — "длина" скользящего среднего
        и target — "цель" — атрибут рынка по которому будет строиться скользящее среднее.

        :type length: int
        :type target: str
        :param length: "длина" скользящего среднего, по-умолчанию — 21
        :param target: "цель" скользящего среднего, по-умолчанию — 'Close'
        """
        super().__init__('SMA', '{}_{}'.format('SMA', length))
        if not length:
            length = int(self.config_manager['ANALYSIS']['SMA_default_length'])
            self.name = '{}_{}'.format('SMA', length)
        if not target:
            target = self.config_manager['ANALYSIS']['SMA_default_target']

        self.parameters = self._get_parameters_dict()
        self._fill_in_parameters(length=length, target=target)

    def calculate(self, proxy_df):
        length = self.parameters['length']
        target = self.parameters['target']
        index = proxy_df.columns.get_loc(target)

        column_name = 'SMA_{}'.format(length)
        dif_column_name = 'd(SMA_{})/dT'.format(length)

        proxy_df[column_name] = proxy_df.iloc[:, index].rolling(window=length).mean()[length:]
        proxy_df[dif_column_name] = \
            proxy_df[column_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_name, dif_column_name]]

    def plot(self, ax, ticks, colour='b'):
        df = self.result.tail(ticks)
        ax.plot(df.index, df['SMA_{}'.format(self.parameters['length'])],
                c=colour, lw=1, label=self.name)


class AnalysisHandler(object):
    def __init__(self, app):
        self.app = app
        self.df = pd.DataFrame()
        self.proxy_df = pd.DataFrame()

    def calculate_all(self):
        self._prepare_proxy_df()
        for indicator in self.app.indicators:
            indicator.calculate(self.proxy_df)

    def plot_all(self, ax: Axes, ticks: int = 96):
        for indicator in self.app.indicators:
            indicator.plot(ax, ticks=ticks)

    def _prepare_proxy_df(self):
        self.proxy_df = self.app.mem_df
