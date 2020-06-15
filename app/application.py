import sys
import webbrowser
import argparse

from PyQt5.QtWidgets import QApplication

from app.time import TimeHandler
from app.network import NetworkHandler
from app.analysis import AnalysisHandler, SMA, WMA, EMA, ROC, MACD, BB, Stochastic, AO, Indicator
from app.database import DatabaseHandler
from app.plotter import Plotter
from app.utils import ConfigClass
from app.gui import MainGUI


class ApplicationClass(ConfigClass):
    def __init__(self):
        super().__init__()
        self.active_pair = self.config_manager['APPLICATION']['pairs'].split(',')[0]
        self.resolution = (int(self.config_manager['APPLICATION']['resolution_number']),
                           self.config_manager['APPLICATION']['resolution_base'])

        self.start_timestamp = int(self.config_manager['APPLICATION']['start_timestamp'])

        self.mem_df = None
        self.args = None
        self.exchange_info = None
        self.mode = None
        self.active_indicators = [SMA(21)]
        self.indicator_models = [cls for cls in Indicator.__subclasses__()]

        self.time_handler = TimeHandler(self)
        self.network_handler = NetworkHandler(self)
        self.analysis_handler = AnalysisHandler(self)
        self.plotter = Plotter(self)
        self.database_handler = DatabaseHandler(self)

        self.pairs = ['{}'.format(pair['symbol']) for pair in self.exchange_info['symbols']
                      if pair['status'] == 'TRADING']

        self._parse_args()
        self.interface_loop()

    def _parse_args(self):
        parser = argparse.ArgumentParser(description='Launch market analyzer app.')
        parser.add_argument('--cli', dest='mode', action='store_const', const='cli', default='gui',
                            help='launch with CLI (default: launch with MainGUI)')
        self.args = parser.parse_args()
        self.mode = self.args.mode

    def interface_loop(self):
        if self.mode == 'gui':
            _app = QApplication(sys.argv)
            window = MainGUI(self)
            window.show()
            _app.exec_()
        else:
            print('Запустились')
            print("Доступные команды:\n"
                  "\tplot — обновить файл графика\n"
                  "\tshow - показать график\n"
                  "\tprint — напечатать аналитические данные\n"
                  "\tq — выключить программу\n"
                  "\tupd — обновить входные данные")
            while True:
                input_line = input().split(':')
                cmd = input_line[0]
                if cmd == 'plot':
                    self.plot()
                elif cmd == 'show':
                    pass
                elif cmd == 'q':
                    self.exit()
                elif cmd == 'print':
                    print(self.mem_df)
                elif cmd == 'upd':
                    self.update()
                else:
                    print('wrong cmd')

    def plot(self, ticks: int = 96):
        self.plotter.plot_all(ticks)

    def update(self):
        self.database_handler.prepare_df(True)

    @staticmethod
    def exit():
        exit()

    def open(self):
        webbrowser.get(self.config_manager['APPLICATION']['chrome_path']) \
            .open(self.config_manager['PLOT']['filepath'])


