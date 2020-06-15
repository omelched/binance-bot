import configparser
import logging
import os
import sys
import numpy as np
from logging.handlers import TimedRotatingFileHandler
import errno

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
LOG_FILE = "logs/my_app.log"


def _get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def _get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        try:
            os.makedirs(os.path.dirname(LOG_FILE))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if logger.handlers:
        logger.handlers = []
    logger.addHandler(_get_file_handler())
    logger.propagate = False
    return logger


class BaseClass(object):
    def __init__(self):
        self._logger = get_logger(self.__class__.__name__)


class ConfigClass(object):
    def __init__(self):
        self.config_manager = configparser.ConfigParser()
        self.cfg_file_name = 'CONFIG.cfg'
        self.cfg_path = ''
        self._init_from_cfg()

        self.logger = get_logger('Logger')
        self.logger.setLevel(logging.DEBUG)

    def _init_from_cfg(self):
        abs_cfg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', self.cfg_file_name))
        self.cfg_path = os.path.relpath(abs_cfg_path, sys.argv[0])

        try:
            _ = os.environ["UNIT_TEST_IN_PROGRESS"]
            self.config_manager.read(self.cfg_path)
        except KeyError:
            self.config_manager.read(self.cfg_file_name)


def concat_url(main_url: str, **kwargs):
    url = main_url + '?'
    for key, value in kwargs.items():
        if not value:
            continue
        if key[:1] == '_':
            key = key[1:]
        if type(value) == float:
            value = int(value)
        url = url + ('&' + key + '=' + str(value))
    return url


def gaussian(x, amp=1, mean=0, sigma=1):
    return amp * np.exp(-(x - mean) ** 2 / (2 * sigma ** 2))


class LoggedBaseException(BaseException):
    def __init__(self):
        self._logger = get_logger(self.__class__.__name__)


class APIError(LoggedBaseException):
    pass


class APIError404(APIError):
    def __init__(self, url: str, text: str):
        super().__init__()
        self._logger.error('APIError404:\turl:\t{}\ttext:\t{}'.format(url, text))


class APIError418(APIError):
    def __init__(self, url: str, text: str, headers):
        super().__init__()
        self._logger.error('APIError418:\t\turl:\t{}\ttext:\t:{}\theaders:\t{}'.format(url, text, headers))


class APIWarning429(APIError):
    def __init__(self, url: str, text: str, headers):
        super().__init__()
        self._logger.warning('APIWarning429:\turl:\t{}\ttext:\t:{}\theaders:\t{}'.format(url, text, headers))


class ConfigError(LoggedBaseException):
    pass


class InvalidResolutionSettings(ConfigError):
    def __init__(self):
        super().__init__()
        self._logger.error('InvalidResolutionSettings')


class NetworkHandlerError(LoggedBaseException):
    def __init__(self):
        self._logger.error('NetworkHandlerError')


class NonExistingIndicatorParameter(BaseException):
    pass
