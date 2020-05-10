import configparser


class ConfigClass(object):
    def __init__(self):
        self.config_manager = configparser.ConfigParser()
        self.init_from_cfg()

    def init_from_cfg(self):
        self.config_manager.read('app/CONFIG.cfg')


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

