from app.time import TimeHandler
from app.url import URLHandler
from app.analysis import AnalysisHandler, SMA, WMA, EMA, ROC, MACD
from app.database import DatabaseHandler
from app.plotter import Plotter
from app.utils import ConfigClass


class Application(ConfigClass):
    def __init__(self):
        super().__init__()
        self.pair = self.config_manager['APPLICATION']['pair']
        self.resolution = (int(self.config_manager['APPLICATION']['resolution_number']),
                           self.config_manager['APPLICATION']['resolution_base'])

        self.start_timestamp = int(self.config_manager['APPLICATION']['start_timestamp'])

        self.mem_df = None
        self.indicators = [MACD()]

        self.time_handler = TimeHandler(self)
        self.url_handler = URLHandler(self)
        self.analysis_handler = AnalysisHandler(self)
        self.plotter = Plotter(self)
        self.database_handler = DatabaseHandler(self)

        self.interface_loop()

    def interface_loop(self):
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
                self.plot(96)
            elif cmd == 'show':
                pass
            elif cmd == 'q':
                exit()
            elif cmd == 'print':
                print(self.mem_df)
            elif cmd == 'upd':
                self.database_handler.prepare_df()
            else:
                print('wrong cmd')

    def plot(self, ticks: int = 96):

        self.plotter.plot_all(ticks)
