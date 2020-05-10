from app.time import TimeHandler
from app.url import URLHandler
from app.analysis import AnalysisHandler, SMA
from app.database import DatabaseHandler
from app.plotter import Plotter
from app.utils import ConfigClass


class Application(ConfigClass):
    def __init__(self):
        self.pair = 'BTC_RUB'
        self.resolution = 15
        self.start_timestamp = 1588032000
        self.mem_df = None
        self.indicators = [SMA(), SMA(length=15)]

        self.time_handler = TimeHandler(self)
        self.url_handler = URLHandler(self)
        self.analysis_handler = AnalysisHandler(self)
        self.plotter = Plotter(self)
        self.database_handler = DatabaseHandler(self)

        self.interface_loop()

    def interface_loop(self):
        print('Запустились')
        print("Доступные команды:\n"
              "\tplot: — обновить файл графика\n"
              "\tshow: - показать график\n"
              "\tprint: — напечатать аналитические данные\n"
              "\tq: — выключить программу\n")
        while True:
            input_line = input().split(':')
            cmd = input_line[0]
            if cmd == 'plot':
                self.plot()
            elif cmd == 'show':
                pass
            elif cmd == 'q':
                exit()
            elif cmd == 'print':
                print(self.mem_df)
            else:
                print('wrong cmd')

    def plot(self):

        self.plotter.plot_all()
