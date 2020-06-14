import pandas as pd
import numpy as np
from app.utils import ConfigClass
import math

from app.utils import NonExistingIndicatorParameter


class Indicator(ConfigClass):
    """
    Базовый класс Индикаторов.
    Все классы наследуются от него.
    """
    model = None

    def __init__(self, name: str):
        """
        Метод инициализации.
        Устанавливаются наименования модели, наименование индикатора,
        создается пустой словарь параметров, нулевой результат вычисления индикатора.

        :type name: str
        :param model: — имя модели индикатора
        :param name:
        """
        super().__init__()
        self.name = name
        self.parameters = {}
        self.result = pd.DataFrame()

    def __str__(self):
        return '{}'.format(self.name)

    def calculate(self, proxy_df: pd.DataFrame):
        self.result = pd.DataFrame(np.zeros(len(proxy_df.index), 1))

    def get_parameters_dict(self):

        # TODO: refactor
        if self.model in ['SMA', 'WMA', 'ROC']:
            return {'length': 0,
                    'target': ''}
        elif self.model == 'EMA':
            return {'length': 0,
                    'target': '',
                    'alpha': 0.0}
        elif self.model == 'BB':
            return {'length': 0,
                    'target': '',
                    'multiplicator': 0.0}
        elif self.model == 'MACD':
            return {'lambda_1': 0,
                    'lambda_2': 0,
                    'lambda_3': 0,
                    'target': ''}
        elif self.model == 'Stochastic':
            return {'lambda_1': 0,
                    'lambda_2': 0,
                    'target': ''}
        elif self.model == 'AO':
            return {'lambda_1': 0,
                    'lambda_2': 0,
                    'target_1': '',
                    'target_2': ''}
        else:
            raise Exception('Parameters not created for {}'.format(self.model))

    def _fill_in_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.parameters.keys():
                self.parameters.update({key: type(self.parameters[key])(value)})
            else:
                raise NonExistingIndicatorParameter

    def plot(self, ax, ticks, color=None, style=None):
        df = self.result.tail(ticks)

        if not color and not style:
            color, style = self._get_unused_color_style(ax)

        ax.plot(df.index, df['{}'.format(self.name)],
                c=color, ls=style, lw=1, label=self.name)

    def _get_unused_color_style(self, ax):
        color_sequence = self.config_manager['PLOT']['color_sequence'].split(',')
        style_sequence = self.config_manager['PLOT']['style_sequence'].split(',')
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

        return color, style


class SMA(Indicator):
    """
    Класс Индикатора SMA.
    Дочерний класс Indicator
    """
    model = 'SMA'

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
        super().__init__('{}_{}'.format('SMA', length))
        if not length:
            length = int(self.config_manager['ANALYSIS']['SMA_default_length'])
            self.name = '{}_{}'.format('SMA', length)
        if not target:
            target = self.config_manager['ANALYSIS']['SMA_default_target']

        self.parameters = self.get_parameters_dict()
        self._fill_in_parameters(length=length, target=target)

    def calculate(self, proxy_df):
        length = self.parameters['length']
        target = self.parameters['target']
        col_index = proxy_df.columns.get_loc(target)

        column_name = 'SMA_{}'.format(length)
        dif_column_name = 'd(SMA_{})/dT'.format(length)

        proxy_df[column_name] = proxy_df.iloc[:, col_index].rolling(window=length).mean()[length - 1:]
        proxy_df[dif_column_name] = \
            proxy_df[column_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_name, dif_column_name]]


class WMA(Indicator):
    model = 'WMA'

    def __init__(self, length: int = None, target: str = None):

        super().__init__('{}_{}'.format('WMA', length))
        if not length:
            length = int(self.config_manager['ANALYSIS']['WMA_default_length'])
            self.name = '{}_{}'.format('WMA', length)
        if not target:
            target = self.config_manager['ANALYSIS']['WMA_default_target']

        self.parameters = self.get_parameters_dict()
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
    model = 'EMA'

    def __init__(self, length: int = None, target: str = None, alpha: float = None):

        super().__init__('{}_{}'.format('EMA', length))
        if not length:
            length = int(self.config_manager['ANALYSIS']['EMA_default_length'])
            self.name = '{}_{}'.format('EMA', length)
        if not target:
            target = self.config_manager['ANALYSIS']['EMA_default_target']
        if not alpha:
            alpha = 2 / (int(length) + 1)

        self.parameters = self.get_parameters_dict()
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
    model = 'ROC'

    def __init__(self, length: int = None, target: str = None):

        super().__init__('{}_{}'.format('ROC', length))
        if not length:
            length = int(self.config_manager['ANALYSIS']['ROC_default_length'])
            self.name = '{}_{}'.format('ROC', length)
        if not target:
            target = self.config_manager['ANALYSIS']['ROC_default_target']

        self.parameters = self.get_parameters_dict()
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
    model = 'MACD'

    def __init__(self,
                 lambda_1: int = None,
                 lambda_2: int = None,
                 lambda_3: int = None,
                 target: str = None):

        super().__init__('{}({}, {}, {})'.format('MACD', lambda_1, lambda_2, lambda_3))
        # TODO: refactor - ugly!
        if not lambda_1:
            lambda_1 = int(self.config_manager['ANALYSIS']['MACD_default_lambda_1'])
            self.name = '{}({}, {}, {})'.format('MACD', lambda_1, lambda_2, lambda_3)
        if not lambda_2:
            lambda_2 = int(self.config_manager['ANALYSIS']['MACD_default_lambda_2'])
            self.name = '{}({}, {}, {})'.format('MACD', lambda_1, lambda_2, lambda_3)
        if not lambda_3:
            lambda_3 = int(self.config_manager['ANALYSIS']['MACD_default_lambda_3'])
            self.name = '{}({}, {}, {})'.format('MACD', lambda_1, lambda_2, lambda_3)
        if not target:
            target = self.config_manager['ANALYSIS']['MACD_default_target']

        self.parameters = self.get_parameters_dict()
        self._fill_in_parameters(lambda_1=lambda_1,
                                 lambda_2=lambda_2,
                                 lambda_3=lambda_3,
                                 target=target)

    def calculate(self, proxy_df):
        lambda_1 = self.parameters['lambda_1']
        alpha_1 = 2 / (lambda_1 + 1)
        lambda_2 = self.parameters['lambda_2']
        alpha_2 = 2 / (lambda_2 + 1)
        lambda_3 = self.parameters['lambda_3']
        alpha_3 = 2 / (lambda_3 + 1)
        target = self.parameters['target']
        col_index = proxy_df.columns.get_loc(target)

        column_1_name = '{}_line'.format(self.name)
        dif_column_1_name = 'd({}_line)/dT'.format(self.name)
        column_2_name = '{}_signal'.format(self.name)
        dif_column_2_name = 'd({}_signal)/dT'.format(self.name)
        column_3_name = '{}_hist'.format(self.name)
        dif_column_3_name = 'd({}_hist)/dT'.format(self.name)

        macd_line = [0]
        signal_line = [0]
        hist = [0]

        macd_lambda_1 = [proxy_df.iloc[0, col_index]]
        macd_lambda_2 = [proxy_df.iloc[0, col_index]]
        for i in range(1, len(proxy_df.index)):
            macd_lambda_1.append(alpha_1 * proxy_df.iloc[i, col_index] + (1 - alpha_1) * macd_lambda_1[i - 1])
            macd_lambda_2.append(alpha_2 * proxy_df.iloc[i, col_index] + (1 - alpha_2) * macd_lambda_2[i - 1])

            macd_line.append(macd_lambda_1[-1] - macd_lambda_2[-1])
            signal_line.append(alpha_3 * macd_line[-1] + (1 - alpha_3) * signal_line[-1])
            hist.append(macd_line[-1] - signal_line[-1])

        proxy_df[column_1_name] = macd_line
        proxy_df[column_2_name] = signal_line
        proxy_df[column_3_name] = hist
        proxy_df[dif_column_1_name] = \
            proxy_df[column_1_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()
        proxy_df[dif_column_2_name] = \
            proxy_df[column_2_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()
        proxy_df[dif_column_3_name] = \
            proxy_df[column_3_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_1_name, dif_column_1_name,
                                column_2_name, dif_column_2_name,
                                column_3_name, dif_column_3_name]]

    def plot(self, ax, ticks, color=None, style=None):
        df = self.result.tail(ticks)

        for i in ['line', 'signal']:
            color, style = self._get_unused_color_style(ax)
            ax.plot(df.index, df['{}_{}'.format(self.name, i)],
                    c=color, ls=style, lw=1, label='{}_{}'.format(self.name, i))

        ax.bar(df.index, df['{}_hist'.format(self.name)], color='r', width=0.5 * 4 / 24)


class BB(Indicator):
    model = 'BB'

    def __init__(self,
                 length: int = None,
                 multiplicator: float = None,
                 target: str = None):

        super().__init__('{}({}, {})'.format('BB', length, multiplicator))
        # TODO: refactor - ugly!
        if not length:
            length = int(self.config_manager['ANALYSIS']['BB_default_length'])
            self.name = '{}({}, {})'.format('BB', length, multiplicator)
        if not multiplicator:
            multiplicator = int(self.config_manager['ANALYSIS']['BB_default_multiplicator'])
            self.name = '{}({}, {})'.format('BB', length, multiplicator)
        if not target:
            target = self.config_manager['ANALYSIS']['BB_default_target']

        self.parameters = self.get_parameters_dict()
        self._fill_in_parameters(length=length,
                                 multiplicator=multiplicator,
                                 target=target)

    def calculate(self, proxy_df):
        length = self.parameters['length']
        multiplicator = self.parameters['multiplicator']
        target = self.parameters['target']
        col_index = proxy_df.columns.get_loc(target)

        column_up_name = '{}_up'.format(self.name)
        column_mid_name = '{}_middle'.format(self.name)
        column_down_name = '{}_down'.format(self.name)
        dif_column_up_name = 'd({}_up)/dT'.format(self.name)
        dif_column_mid_name = 'd({}_middle)/dT'.format(self.name)
        dif_column_down_name = 'd({}_down)/dT'.format(self.name)

        bb_up = []
        bb_down = []

        proxy_df[column_mid_name] = proxy_df.iloc[:, col_index].rolling(window=length).mean()[length - 1:]
        sma_col_index = proxy_df.columns.get_loc(column_mid_name)
        for i in range(len(proxy_df.index)):
            _slice = proxy_df.iloc[i - length + 1: i + 1, col_index]
            bb_up.append(proxy_df.iloc[i, sma_col_index] + (multiplicator * _slice.std()))
            bb_down.append(proxy_df.iloc[i, sma_col_index] - (multiplicator * _slice.std()))

        proxy_df[column_up_name] = bb_up
        proxy_df[column_down_name] = bb_down
        proxy_df[dif_column_up_name] = \
            proxy_df[column_up_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()
        proxy_df[dif_column_mid_name] = \
            proxy_df[column_mid_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()
        proxy_df[dif_column_down_name] = \
            proxy_df[column_down_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_up_name, dif_column_up_name,
                                column_mid_name, dif_column_mid_name,
                                column_down_name, dif_column_down_name]]

    def plot(self, ax, ticks, color=None, style=None):
        df = self.result.tail(ticks)
        color, style = self._get_unused_color_style(ax)

        for i in ['up', 'down']:
            ax.plot(df.index, df['{}_{}'.format(self.name, i)],
                    c=color, ls=style, lw=1, label='{}_{}'.format(self.name, i))

        ax.fill_between(df.index, df['{}_up'.format(self.name)], df['{}_down'.format(self.name)],
                        facecolor=color, alpha=0.2, zorder=10)
        color, style = self._get_unused_color_style(ax)
        ax.plot(df.index, df['{}_middle'.format(self.name)],
                c=color, ls=style, lw=1, label='{}_middle'.format(self.name))


class Stochastic(Indicator):
    model = 'Stochastic'

    def __init__(self,
                 lambda_1: int = None,
                 lambda_2: int = None,
                 target: str = None):

        super().__init__('{}({}, {})'.format('Stochastic', lambda_1, lambda_2))
        # TODO: refactor - ugly!
        if not lambda_1:
            lambda_1 = int(self.config_manager['ANALYSIS']['Stoch_default_lambda_1'])
            self.name = '{}({}, {})'.format('Stochastic', lambda_1, lambda_2)
        if not lambda_2:
            lambda_2 = int(self.config_manager['ANALYSIS']['Stoch_default_lambda_2'])
            self.name = '{}({}, {})'.format('Stochastic', lambda_1, lambda_2)
        if not target:
            target = self.config_manager['ANALYSIS']['Stoch_default_target']

        self.parameters = self.get_parameters_dict()
        self._fill_in_parameters(lambda_1=lambda_1,
                                 lambda_2=lambda_2,
                                 target=target)

    def calculate(self, proxy_df):
        lambda_1 = self.parameters['lambda_1']
        lambda_2 = self.parameters['lambda_2']
        target = self.parameters['target']
        target_index = proxy_df.columns.get_loc(target)
        min_index = proxy_df.columns.get_loc('Low')
        max_index = proxy_df.columns.get_loc('High')

        column_k_name = '{}_K'.format(self.name)
        column_d_name = '{}_D'.format(self.name)
        dif_column_k_name = 'd({}_K)/dT'.format(self.name)
        dif_column_d_name = 'd({}_D)/dT'.format(self.name)

        proxy_df[column_k_name] = [
            (proxy_df.iloc[i, target_index] - proxy_df.iloc[i - lambda_1:i + 1, min_index].min()) /
            (proxy_df.iloc[i - lambda_1:i + 1, max_index].max()
             - proxy_df.iloc[i - lambda_1:i + 1, min_index].min()) * 100
            for i in range(len(proxy_df.index))]
        column_k_name_index = proxy_df.columns.get_loc(column_k_name)
        proxy_df[column_d_name] = proxy_df.iloc[:, column_k_name_index].rolling(window=lambda_2).mean()[lambda_2 - 1:]

        proxy_df[dif_column_k_name] = \
            proxy_df[column_k_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()
        proxy_df[dif_column_d_name] = \
            proxy_df[column_d_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_k_name, dif_column_k_name,
                                column_d_name, dif_column_d_name]]

    def plot(self, ax, ticks, color=None, style=None):
        df = self.result.tail(ticks)

        for i in ['K', 'D']:
            color, style = self._get_unused_color_style(ax)
            ax.plot(df.index, df['{}_{}'.format(self.name, i)],
                    c=color, ls=style, lw=1, label='{}_{}'.format(self.name, i))

        ax.fill_between(df.index, 20, 80,
                        facecolor=color, alpha=0.1, zorder=10)


class AO(Indicator):
    model = 'AO'

    def __init__(self):
        super().__init__('{}'.format('AO'))
        # TODO: refactor - ugly!
        lambda_1 = int(self.config_manager['ANALYSIS']['AO_default_lambda_fast'])
        lambda_2 = int(self.config_manager['ANALYSIS']['AO_default_lambda_slow'])
        target_1 = self.config_manager['ANALYSIS']['AO_default_target_high']
        target_2 = self.config_manager['ANALYSIS']['AO_default_target_low']

        self.parameters = self.get_parameters_dict()
        self._fill_in_parameters(lambda_1=lambda_1,
                                 lambda_2=lambda_2,
                                 target_1=target_1,
                                 target_2=target_2)

    def calculate(self, proxy_df):
        lambda_1 = self.parameters['lambda_1']
        lambda_2 = self.parameters['lambda_2']
        target_1 = self.parameters['target_1']
        target_2 = self.parameters['target_2']

        target_1_col_index = proxy_df.columns.get_loc(target_1)
        target_2_col_index = proxy_df.columns.get_loc(target_2)

        column_name = '{}'.format(self.name)
        dif_column_name = 'd({})/dT'.format(self.name)

        proxy_df['hl2'] = (proxy_df.iloc[:, target_1_col_index] + proxy_df.iloc[:, target_2_col_index]) / 2
        hl2_index = proxy_df.columns.get_loc('hl2')

        proxy_df[column_name] = proxy_df.iloc[:, hl2_index].rolling(window=lambda_1).mean()[lambda_1 - 1:] - \
                                proxy_df.iloc[:, hl2_index].rolling(window=lambda_2).mean()[lambda_2 - 1:]

        proxy_df[dif_column_name] = \
            proxy_df[column_name].diff() / \
            proxy_df.index.to_series().diff().dt.total_seconds()

        self.result = proxy_df[[column_name, dif_column_name]]

    def plot(self, ax, ticks, color=None, style=None):
        df = self.result.tail(ticks)

        ax.bar(df.index, df['{}'.format(self.name)], color=np.where(df['d({})/dT'.format(self.name)] > 0, 'g', 'r'),
               width=0.5)


class AnalysisHandler(object):
    def __init__(self, app):
        self.app = app
        self.df = pd.DataFrame()
        self.proxy_df = pd.DataFrame()

    def calculate_all(self):
        self._prepare_proxy_df()
        for indicator in self.app.active_indicators:
            indicator.calculate(self.proxy_df)

    def plot_all(self, axs: tuple, ticks: int):
        for indicator in self.app.active_indicators:
            if indicator.model in ['ROC', 'MACD', 'Stoch', 'AO']:
                indicator.plot(axs[1], ticks=ticks)
            else:
                indicator.plot(axs[0], ticks=ticks)

    def _prepare_proxy_df(self):
        self.proxy_df = self.app.mem_df
