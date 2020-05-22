import datetime as dt
from app.utils import InvalidResolutionSettings


class TimeHandler(object):
    def __init__(self, app):
        self.app = app

    def file_is_outdated(self, mtime: float):
        age_limit = self.app.resolution[0]
        if self.app.resolution[1] == 'm':
            age_multiplier = 1
        elif self.app.resolution[1] == 'h':
            age_multiplier = 60
        elif self.app.resolution[1] == 'd':
            age_multiplier = 60 * 24
        elif self.app.resolution[1] == 'w':
            age_multiplier = 60 * 20 * 7
        elif self.app.resolution[1] == 'M':
            age_multiplier = 60 * 20 * 7 * 30
        else:
            raise InvalidResolutionSettings

        return mtime < (dt.datetime.now().replace(microsecond=0) -
                        dt.timedelta(minutes=age_limit * age_multiplier)).timestamp()

    @staticmethod
    def time_now(late: bool = False):
        if late:
            return dt.datetime.now().replace(microsecond=0) + dt.timedelta(minutes=-1)
        return dt.datetime.now().replace(microsecond=0)

    @staticmethod
    def get_last_day(time: dt.datetime):
        return time - dt.timedelta(days=1)

    @staticmethod
    def prepare_times(*args: [dt.datetime, int]):
        ret = []
        for time in args:
            if type(time) == int:
                time = dt.datetime.fromtimestamp(time)
            ret.append(int(time.timestamp()))
        return ret

    @staticmethod
    def timestamp_to_datetime(raw_timestamp):
        if len(str(raw_timestamp)) == 13:
            raw_timestamp = raw_timestamp // 1000
        timestamp = dt.datetime.fromtimestamp(raw_timestamp)

        return timestamp

    @staticmethod
    def get_date_for_ticks(time: dt.datetime, resolution: int, tick_num: int):
        return time - dt.timedelta(minutes=resolution * tick_num)
