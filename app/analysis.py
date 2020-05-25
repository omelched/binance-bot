import pandas as pd
import numpy as np
from app.utils import ConfigClass, gaussian
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

    def _get_parameters_dict(self):
        if self.model in ['SMA', 'WMA', 'ROC']:
            return {'length': 0,
                    'target': ''}
        elif self.model == 'EMA':
            return {'length': 0,
                    'target': '',
                    'alpha': 0}
        else:
            raise Exception('Parameters not created for {}'.format(self.model))

    def _fill_in_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.parameters.keys():
                self.parameters.update({key: value})
            else:
                raise NonExistingIndicatorParameter

    def plot(self, ax, ticks, color=None, style=None):
        df = self.result.tail(ticks)

        color_sequence = self.config_manager['PLOT']['color_sequence'].split(',')
        style_sequence = self.config_manager['PLOT']['style_sequence'].split(',')
        if not color and not style:
            used_c_ls = {line.get_linestyle(): [_line.get_color() for _line in ax.lines
                                                if _line.get_linestyle() == line.get_linestyle()] for line in ax.lines}
            if not used_c_ls:
                color = color_sequence[0]
                style = style_sequence[0]
            else:
                style = list(used_c_ls.keys())[-1]
                try:
                    color = color_sequence[len(used_c_ls[style])]
                except IndexError:
                    try:
                        style = style_sequence[len(used_c_ls)]
                        color = color_sequence[0]
                    except IndexError:
                        color = color_sequence[0]
                        style = style_sequence[0]

        ax.plot(df.index, df['{}'.format(self.name)],
                c=color, ls=style, lw=1, label=self.name)


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
        col_index = proxy_df.columns.get_loc(target)

        column_name = 'SMA_{}'.format(length)
        dif_column_name = 'd(SMA_{})/dT'.format(length)

        proxy_df[column_name] = proxy_df.iloc[:, col_index].rolling(window=length).mean()[length:]
        proxy_df[dif_column_name] = \
            proxy_df[column_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_name, dif_column_name]]


class WMA(Indicator):

    def __init__(self, length: int = None, target: str = None):

        super().__init__('WMA', '{}_{}'.format('WMA', length))
        if not length:
            length = int(self.config_manager['ANALYSIS']['WMA_default_length'])
            self.name = '{}_{}'.format('WMA', length)
        if not target:
            target = self.config_manager['ANALYSIS']['WMA_default_target']

        self.parameters = self._get_parameters_dict()
        self._fill_in_parameters(length=length, target=target)

    def calculate(self, proxy_df):
        length = self.parameters['length']
        target = self.parameters['target']
        col_index = proxy_df.columns.get_loc(target)

        column_name = 'WMA_{}'.format(length)
        dif_column_name = 'd(WMA_{})/dT'.format(length)

        average_result = [None] * (length - 1)
        for i in range(length - 1, len(proxy_df.index)):
            average_result.append(2 / (length * (length + 1)) *
                                  sum([(length - ii) * proxy_df.iloc[i - ii, col_index] for ii in range(length)]))

        proxy_df[column_name] = average_result
        proxy_df[dif_column_name] = \
            proxy_df[column_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_name, dif_column_name]]


class EMA(Indicator):

    def __init__(self, length: int = None, target: str = None, alpha: int = None):

        super().__init__('EMA', '{}_{}'.format('EMA', length))
        if not length:
            length = int(self.config_manager['ANALYSIS']['EMA_default_length'])
            self.name = '{}_{}'.format('EMA', length)
        if not target:
            target = self.config_manager['ANALYSIS']['EMA_default_target']
        if not alpha:
            alpha = 2 / (length + 1)

        self.parameters = self._get_parameters_dict()
        self._fill_in_parameters(length=length, target=target, alpha=alpha)

    def calculate(self, proxy_df):
        length = self.parameters['length']
        target = self.parameters['target']
        alpha = self.parameters['alpha']
        col_index = proxy_df.columns.get_loc(target)

        column_name = 'EMA_{}'.format(length)
        dif_column_name = 'd(EMA_{})/dT'.format(length)

        average_result = [proxy_df.iloc[0, col_index]]
        for i in range(1, len(proxy_df.index)):
            average_result.append(alpha * proxy_df.iloc[i, col_index] + (1 - alpha) * average_result[i - 1])

        proxy_df[column_name] = average_result
        proxy_df[dif_column_name] = \
            proxy_df[column_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_name, dif_column_name]]


class ROC(Indicator):

    def __init__(self, length: int = None, target: str = None):

        super().__init__('ROC', '{}_{}'.format('ROC', length))
        if not length:
            length = int(self.config_manager['ANALYSIS']['ROC_default_length'])
            self.name = '{}_{}'.format('ROC', length)
        if not target:
            target = self.config_manager['ANALYSIS']['ROC_default_target']

        self.parameters = self._get_parameters_dict()
        self._fill_in_parameters(length=length, target=target)

    def calculate(self, proxy_df):
        length = self.parameters['length']
        target = self.parameters['target']
        col_index = proxy_df.columns.get_loc(target)

        column_name = '{}'.format(self.name)
        dif_column_name = 'd({})/dT'.format(self.name)

        average_result = [None] * (length - 1)
        for i in range(length - 1, len(proxy_df.index)):
            average_result.append(
                (proxy_df.iloc[i, col_index] - proxy_df.iloc[i - length, col_index])
                / proxy_df.iloc[i - length, col_index] * 100
            )

        proxy_df[column_name] = average_result
        proxy_df[dif_column_name] = \
            proxy_df[column_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_name, dif_column_name]]


class MACD(Indicator):

    def __init__(self,
                 fast_length: int = None,
                 slow_length: int = None,
                 signal_length: int = None,
                 target: str = None):

        if not fast_length:
            fast_length = int(self.config_manager['ANALYSIS']['MACD_default_fast_length'])
        if not slow_length:
            slow_length = int(self.config_manager['ANALYSIS']['MACD_default_slow_length'])
        if not signal_length:
            signal_length = int(self.config_manager['ANALYSIS']['MACD_default_signal_length'])
        if not target:
            target = self.config_manager['ANALYSIS']['ROC_default_target']

        super().__init__('MACD', '{}_({}, {}, {})'.format('MACD', fast_length, slow_length, signal_length))

        self.parameters = self._get_parameters_dict()
        self._fill_in_parameters(fast_length=fast_length,
                                 slow_length=slow_length,
                                 signal_length=signal_length,
                                 target=target)

    def calculate(self, proxy_df):
        fast_length = self.parameters['fast_length']
        slow_length = self.parameters['slow_length']
        signal_length = self.parameters['signal_length']
        target = self.parameters['target']
        col_index = proxy_df.columns.get_loc(target)

        column_name = '{}'.format(self.name)
        dif_column_name = 'd({})/dT'.format(self.name)

        average_result = [None] * (length - 1)
        for i in range(length - 1, len(proxy_df.index)):
            average_result.append(
                (proxy_df.iloc[i, col_index] - proxy_df.iloc[i - length, col_index])
                / proxy_df.iloc[i - length, col_index] * 100
            )

        proxy_df[column_name] = average_result
        proxy_df[dif_column_name] = \
            proxy_df[column_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_name, dif_column_name]]


class AnalysisHandler(object):
    def __init__(self, app):
        self.app = app
        self.df = pd.DataFrame()
        self.proxy_df = pd.DataFrame()

    def calculate_all(self):
        self._prepare_proxy_df()
        for indicator in self.app.indicators:
            indicator.calculate(self.proxy_df)

    def plot_all(self, axs: tuple, ticks: int):
        for indicator in self.app.indicators:
            if indicator.model == 'ROC':
                indicator.plot(axs[1], ticks=ticks)
            else:
                indicator.plot(axs[0], ticks=ticks)

    def _prepare_proxy_df(self):
        self.proxy_df = self.app.mem_df
