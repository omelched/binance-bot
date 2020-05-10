from app.utils import concat_uri, Exception40014
import requests
import json


class URLHandler(object):
    def __init__(self, app):
        self.app = app

        self.candle_url = 'https://api.exmo.com/v1.1/candles_history'
        self.public_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def get_candles(self, symbol, resolution, start=None, end=None, tick_num: int = None):
        if not end:
            end = self.app.time_handler.time_now()
        if not start and not tick_num:
            start = self.app.time_handler.get_date_for_ticks(self.app.time_handler.get_last_day(end), resolution, 21)
        elif tick_num:
            start = self.app.time_handler.get_date_for_ticks(end, resolution, tick_num)

        end, start = self.app.time_handler.prepare_times(end, start)
        url = concat_uri(self.candle_url, symbol=symbol, resolution=resolution,
                         _from=start, to=end)
        print(url)

        response = requests.request('GET', url, headers=self.public_headers, data={}).json()

        if 'result' in response.keys():
            raise Exception40014
        print(response)
        return response['candles']

        # for key in dir(response):
        #     print(key + ":\t" + str(getattr(response, key)))

#
# now = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(minutes=0)
#
# url = concat_uri(main_url,
#                  symbol='BTC_RUB',
#                  resolution=1,
#                  _from=(now - datetime.timedelta(minutes=30)).timestamp(),
#                  to=now.timestamp())
#
# print(url)
#
# payload = {}
# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded'
#
# }
# response = requests.request('GET',
#                             url,
#                             headers=headers,
#                             data=payload)
