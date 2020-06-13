import sys
import webbrowser
import argparse

from PyQt5 import QtWidgets

from app.time import TimeHandler
from app.url import URLHandler
from app.analysis import AnalysisHandler, SMA, WMA, EMA, ROC, MACD, BB, Stochastic, AO
from app.database import DatabaseHandler
from app.plotter import Plotter
from app.utils import ConfigClass
import app.qtui.design


class ApplicationClass(ConfigClass):
    def __init__(self):
        super().__init__()
        self.pair = self.config_manager['APPLICATION']['pairs'].split(',')[0]
        self.resolution = (int(self.config_manager['APPLICATION']['resolution_number']),
                           self.config_manager['APPLICATION']['resolution_base'])

        self.start_timestamp = int(self.config_manager['APPLICATION']['start_timestamp'])

        self.mem_df = None
        self.args = None
        self.mode = None
        self.indicators = [AO()]

        self.time_handler = TimeHandler(self)
        self.url_handler = URLHandler(self)
        self.analysis_handler = AnalysisHandler(self)
        self.plotter = Plotter(self)
        self.database_handler = DatabaseHandler(self)

        self._parse_args()
        self.interface_loop()

    def _parse_args(self):
        parser = argparse.ArgumentParser(description='Launch market analyzer app.')
        parser.add_argument('--cli', dest='mode', action='store_const', const='cli', default='gui',
                            help='launch with CLI (default: launch with GUI)')
        self.args = parser.parse_args()
        self.mode = self.args.mode

    def interface_loop(self):
        if self.mode == 'gui':
            _app = QtWidgets.QApplication(sys.argv)
            window = GUI(self)
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


class GUI(QtWidgets.QMainWindow, app.qtui.design.Ui_MainWindow):
    def __init__(self, application: ApplicationClass):
        super().__init__()
        self.app = application
        self.setupUi(self)

        self._setup_comboBoxes()

        self.plot_pushButton.clicked.connect(self.plot_pushButton_click)
        self.open_pushButton.clicked.connect(self.open_pushButton_click)
        self.update_pushButton.clicked.connect(self.update_pushButton_click)
        self.exit_pushButton.clicked.connect(self.exit_pushButton_click)

    def _setup_comboBoxes(self):
        [self.pair_comboBox.addItem(pair) for pair in self.app.config_manager['APPLICATION']['pairs'].split(',')]
        [self.resolution_comboBox.addItem(res) for res in self.app.config_manager['APPLICATION']['resolutions']
            .split(',')]

    def plot_pushButton_click(self):
        self.app.plot()

    def update_pushButton_click(self):
        self.app.update()

    def open_pushButton_click(self):
        self.app.open()

    def exit_pushButton_click(self):
        self.app.exit()
