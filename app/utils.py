import configparser
import os
import sys
import pathlib


class ConfigClass(object):
    def __init__(self):
        self.config_manager = configparser.ConfigParser()
        self.cfg_file_name = 'CONFIG.cfg'
        self.cfg_path = ''
        self.init_from_cfg()

    def init_from_cfg(self):
        abs_cfg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', self.cfg_file_name))
        self.cfg_path = os.path.relpath(abs_cfg_path, sys.argv[0])

        self.config_manager.read(self.cfg_path)


def concat_uri(main_url: str, **kwargs):
    url = main_url + '?'
    for key, value in kwargs.items():
        if key[:1] == '_':
            key = key[1:]
        if type(value) == float:
            value = int(value)
        url = url + ('&' + key + '=' + str(value))
    return url


class Exception40014(BaseException):
    pass


class NonExistingIndicatorParameter(BaseException):
    pass
