from unittest import TestCase
import configparser
import os
import pandas as pd

os.environ['UNIT_TEST_IN_PROGRESS'] = '1'
from app import analysis


class TestSMA(TestCase):
    def setUp(self) -> None:
        self.SMA_instance = analysis.SMA()
        self.config_manager = configparser.ConfigParser()
        self.config_manager.read('app/CONFIG.cfg')
        self.proxy_df = pd.DataFrame
        self.golden_result = pd.DataFrame({""})

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.SMA_instance.parameters,
                         {'length': int(self.config_manager['ANALYSIS']['SMA_default_length']),
                          'target': str(self.config_manager['ANALYSIS']['SMA_default_target'])})

    def test_calculate(self):
        self.SMA_instance.calculate()

    def test_plot(self):
        self.fail()
