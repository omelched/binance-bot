import requests
from app.utils import concat_uri
import datetime
from app.time import TimeHandler
from app.url import URLHandler
from app.analysis import CandleAnalysisHandler


class Application(object):
    def __init__(self):
        self.time_handler = TimeHandler(self)
        self.url_handler = URLHandler(self)
        self.analysis_handler = CandleAnalysisHandler(self)
        self.analysis_handler.plot_candles(self.url_handler.get_candles('BTC_RUB', 15, tick_num=5))
