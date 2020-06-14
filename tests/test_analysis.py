import os
import unittest

import matplotlib.pyplot as mplplt
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

os.environ['UNIT_TEST_IN_PROGRESS'] = '1'
from app import analysis, utils

proxy_df = pd.DataFrame({'Close': [46, 80, 19, 76, 83, 6, 36, 70, 90, 52, 62, 28, 54, 75, 9, 60, 25, 93,
                                   86, 48, 17, 71, 45, 54, 77, 52, 19, 22, 30, 11, 70, 82, 61, 65, 17, 22,
                                   37, 43, 2, 73, 4, 24]},
                        index=np.asarray(pd.date_range('1/1/2000', periods=42)))
golden_result = pd.DataFrame({"SMA_21": [None, None, None, None, None, None, None, None, None, None, None,
                                         None, None, None, None, None, None, None, None, None, None,
                                         54.28571429, 52.61904762, 54.28571429, 54.33333333, 52.85714286,
                                         53.47619048, 52.80952381, 50.9047619, 47.14285714, 48,
                                         48.95238095, 50.52380952, 51.04761905, 48.28571429, 48.9047619,
                                         47.80952381, 48.66666667, 44.33333333, 43.71428571, 41.61904762,
                                         41.95238095],
                              "d(SMA_21)/dT": [None, None, None, None, None, None, None, None, None, None,
                                               None, None, None, None, None, None, None, None, None, None,
                                               None, None, -0.00001929, 0.00001929, 0.00000055,
                                               -0.00001709, 0.00000716, -0.00000772, -0.00002205,
                                               -0.00004354, 0.00000992, 0.00001102, 0.00001819, 0.00000606,
                                               -0.00003197, 0.00000716, -0.00001268, 0.00000992,
                                               -0.00005015, -0.00000716, -0.00002425, 0.00000386]},
                             index=np.asarray(pd.date_range('1/1/2000', periods=42)))
golden_ax_xydata = pd.DataFrame([[7.30141000e+05, 5.42857143e+01],
                                 [7.30142000e+05, 5.26190476e+01],
                                 [7.30143000e+05, 5.42857143e+01],
                                 [7.30144000e+05, 5.43333333e+01],
                                 [7.30145000e+05, 5.28571429e+01],
                                 [7.30146000e+05, 5.34761905e+01],
                                 [7.30147000e+05, 5.28095238e+01],
                                 [7.30148000e+05, 5.09047619e+01],
                                 [7.30149000e+05, 4.71428571e+01],
                                 [7.30150000e+05, 4.80000000e+01],
                                 [7.30151000e+05, 4.89523810e+01],
                                 [7.30152000e+05, 5.05238095e+01],
                                 [7.30153000e+05, 5.10476190e+01],
                                 [7.30154000e+05, 4.82857143e+01],
                                 [7.30155000e+05, 4.89047619e+01],
                                 [7.30156000e+05, 4.78095238e+01],
                                 [7.30157000e+05, 4.86666667e+01],
                                 [7.30158000e+05, 4.43333333e+01],
                                 [7.30159000e+05, 4.37142857e+01],
                                 [7.30160000e+05, 4.16190476e+01],
                                 [7.30161000e+05, 4.19523810e+01]])

test_fig, test_ax = mplplt.subplots()
# TODO: change to multiple subplots

config_manager = utils.ConfigClass().config_manager


class ProxyApp(object):
    def __init__(self, df: pd.DataFrame):
        self.mem_df = df
        self.active_indicators = [analysis.SMA()]


class TestSMA(unittest.TestCase):
    def setUp(self) -> None:
        self.SMA_instance = analysis.SMA()

    def tearDown(self) -> None:
        test_ax.clear()
        pass

    def test_init(self):
        self.assertEqual(self.SMA_instance.parameters,
                         {'length': int(config_manager['ANALYSIS']['SMA_default_length']),
                          'target': str(config_manager['ANALYSIS']['SMA_default_target'])})

    def test_calculate(self):
        self.SMA_instance.calculate(proxy_df)
        assert_frame_equal(self.SMA_instance.result,
                           golden_result, check_less_precise=3)  # increase precise. Fails if > 3

    def test_plot(self):
        self.SMA_instance.calculate(proxy_df)
        self.SMA_instance.plot(test_ax, 21)
        assert_frame_equal(golden_ax_xydata, pd.DataFrame(test_ax.lines[0].get_xydata()))


class TestAnalysisHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.proxy_app = ProxyApp(proxy_df)
        self.analysis_handler_instance = analysis.AnalysisHandler(self.proxy_app)

    def tearDown(self) -> None:
        test_ax.clear()

    def test_init(self):
        self.assertEqual(self.analysis_handler_instance.app, self.proxy_app)
        assert_frame_equal(self.analysis_handler_instance.df, pd.DataFrame())
        assert_frame_equal(self.analysis_handler_instance.proxy_df, pd.DataFrame())

    def test_calculate_all(self):
        self.analysis_handler_instance.calculate_all()
        assert_frame_equal(self.proxy_app.mem_df, proxy_df)
        assert_frame_equal(self.proxy_app.active_indicators[0].result,
                           golden_result, check_less_precise=3)  # increase precise. Fails if > 3

    def test_plot_all(self):
        self.analysis_handler_instance.calculate_all()
        self.analysis_handler_instance.plot_all(test_ax, ticks=21)
        for indicator in self.proxy_app.active_indicators:
            line = [line for line in test_ax.lines if line.get_label() == indicator.name][0]
            assert_frame_equal(golden_ax_xydata, pd.DataFrame(line.get_xydata()))

