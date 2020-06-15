import pandas as pd
import os
import io
import json
import datetime


class DatabaseHandler(object):
    def __init__(self, app):
        self.app = app
        self.raw_file_path = 'input.csv'

        self.prepare_exchange_info()
        self.prepare_df()

    @staticmethod
    def _save_to_csv(df: pd.DataFrame, path: str):
        df.to_csv(path,
                  encoding='UTF-8',
                  sep='\t')

    @staticmethod
    def _load_from_csv(file_to_path: str):
        return pd.read_csv(io.StringIO(open(file_to_path, encoding="UTF-8").read()),
                           sep='\t',
                           index_col=0)

    @staticmethod
    def _response_to_df(json_list: dict):
        df = pd.DataFrame(json_list)
        df = df.iloc[:, :-1]
        df.columns = ['t', 'o', 'h', 'l', 'c', 'v', '_t', '_v', 'n', 'tv', '_tv']
        return df

    def _update_input(self):
        self._save_to_csv(self._response_to_df(self.app.network_handler.get_klines(self.app.active_pair,
                                                                                   self.app.resolution)),
                          self.raw_file_path)

    def _prepare_files(self, is_forced: bool):
        try:
            mtime = os.stat(self.raw_file_path).st_mtime
            if self.app.time_handler.file_is_outdated(mtime) or is_forced:
                # TODO: изменить с полной замены на догрузку недостающих частей - если resolution не поменялся
                self._update_input()
        except FileNotFoundError:
            self._update_input()
        except ConnectionError:
            pass
        except Exception as e:
            raise e

    def prepare_exchange_info(self):
        file_path = self.app.config_manager['APPLICATION']['exchangeInfo_filepath']

        if not os.path.isfile(file_path) \
                or os.stat(file_path).st_size == 0 \
                or datetime.datetime.now().timestamp() - os.stat(file_path).st_mtime > 86400:
            with open(file_path, 'w+') as file:
                file.write(json.dumps(self.app.network_handler.call_API('exchangeInfo'), indent=4, sort_keys=True))

        with open(file_path, 'r') as read_file:
            self.app.exchange_info = json.load(read_file)

    def prepare_df(self, is_forced: bool = False):

        self._prepare_files(is_forced)

        df = self._load_from_csv(self.raw_file_path)[['t', 'o', 'h', 'l', 'c', 'v']]

        df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Timestamp'] = [self.app.time_handler.timestamp_to_datetime(ts) for ts in df['Timestamp']]
        df.set_index('Timestamp', inplace=True, drop=True)

        self.app.mem_df = df
