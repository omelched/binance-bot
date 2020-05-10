import pandas as pd
import os
import sys
import numpy as np
import io


class DatabaseHandler(object):
    def __init__(self, app):
        self.app = app
        self.raw_file_path = 'input.csv'

        self.prepare_df()

    @staticmethod
    def save_to_csv(df: pd.DataFrame, path: str):
        df.to_csv(path,
                  encoding='UTF-8',
                  sep='\t')

    @staticmethod
    def load_from_csv(file_to_path: str):
        return pd.read_csv(io.StringIO(open(file_to_path, encoding="UTF-8").read()),
                           sep='\t',
                           index_col=0)

    @staticmethod
    def JSON_to_df(json_list: dict):
        df = pd.DataFrame(json_list)
        return df

    def update_input(self):
        self.save_to_csv(self.JSON_to_df(self.app.url_handler.get_candles(self.app.pair,
                                                                          self.app.resolution,
                                                                          start=self.app.start_timestamp)),
                         self.raw_file_path)

    def prepare_files(self):
        try:
            mtime = os.stat(self.raw_file_path).st_mtime
            if self.app.time_handler.file_is_outdated(mtime):
                # TO-DO: изменить с полной замены на догрузку недостающих частей - если resolution не поменялся
                self.update_input()
        except FileNotFoundError:
            self.update_input()

    def prepare_df(self):

        self.prepare_files()

        df = self.load_from_csv(self.raw_file_path)

        df.columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'Volume']
        df['Timestamp'] = [self.app.time_handler.timestamp_to_datetime(ts) for ts in df['Timestamp']]
        df.set_index('Timestamp', inplace=True, drop=True)

        self.app.mem_df = df
