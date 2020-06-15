import datetime as dt
from app.utils import InvalidResolutionSettings, ConfigClass


class TimeHandler(ConfigClass):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.logger.debug('{} initialized'.format(self))

    def file_is_outdated(self, mtime: float):

        self.logger.debug('method call with {}'.format([mtime]))

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
        result = mtime < (dt.datetime.now().replace(microsecond=0) -
                          dt.timedelta(minutes=age_limit * age_multiplier)).timestamp()

        self.logger.debug('method result is {}'.format(result))
        return result

    def time_now(self, late: bool = False):

        self.logger.debug('method call with {}'.format([late]))

        if late:
            result = dt.datetime.now().replace(microsecond=0) + dt.timedelta(minutes=-1)

            self.logger.debug('method result is {}'.format(result))
            return result

        result = dt.datetime.now().replace(microsecond=0)

        self.logger.debug('method result is {}'.format(result))
        return result

    def get_last_day(self, time: dt.datetime):
        self.logger.debug('method call with {}'.format([time]))

        result = time - dt.timedelta(days=1)

        self.logger.debug('method result is {}'.format(result))
        return time - dt.timedelta(days=1)

    def prepare_times(self, *args: [dt.datetime, int]):
        self.logger.debug('method call with {}'.format([*args]))

        result = []
        for time in args:
            if type(time) == int:
                time = dt.datetime.fromtimestamp(time)
            result.append(int(time.timestamp()))

        self.logger.debug('method result is {}'.format(result))
        return result

    def timestamp_to_datetime(self, raw_timestamp):
        self.logger.debug('method call with {}'.format([raw_timestamp]))

        if len(str(raw_timestamp)) == 13:
            raw_timestamp = raw_timestamp // 1000
        timestamp = dt.datetime.fromtimestamp(raw_timestamp)

        self.logger.debug('method result is {}'.format(timestamp))
        return timestamp

    def get_date_for_ticks(self, time: dt.datetime, resolution: int, tick_num: int):
        self.logger.debug('method call with {}'.format([time, resolution, tick_num]))

        result = time - dt.timedelta(minutes=resolution * tick_num)

        self.logger.debug('method result is {}'.format(result))
        return result
