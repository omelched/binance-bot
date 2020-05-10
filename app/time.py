import datetime


class TimeHandler(object):
    def __init__(self, app):
        self.app = app

    @staticmethod
    def time_now(late: bool = False):
        if late:
            return datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(minutes=-1)
        return datetime.datetime.now().replace(microsecond=0)

    @staticmethod
    def get_last_day(time: datetime.datetime):
        return time - datetime.timedelta(days=1)

    @staticmethod
    def prepare_times(*args: datetime.datetime):
        ret = []
        for time in args:
            ret.append(int(time.timestamp()))
        return ret

    @staticmethod
    def timestamp_to_string(raw_timestamp):
        if len(str(raw_timestamp)) == 13:
            raw_timestamp = raw_timestamp // 1000
        timestamp = datetime.datetime.fromtimestamp(raw_timestamp)

        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
    @staticmethod
    def get_date_for_ticks(time: datetime.datetime, resolution: int, tick_num: int):
        return time - datetime.timedelta(minutes=resolution*tick_num)

    @staticmethod
    def string_to_datetime(time: str):
        return datetime.datetime(time)
