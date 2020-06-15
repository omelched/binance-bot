from app.utils import concat_url, ConfigClass, NetworkHandlerError, APIError404, APIWarning429, APIError418
import requests


class NetworkHandler(ConfigClass):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.base_endpoint = 'https://api.binance.com'
        self.methods = {
            'klines': {'url': '/api/v3/klines', 'method': 'GET'},
            'ping': {'url': '/api/v3/ping', 'method': 'GET'},
            'exchangeInfo': {'url': '/api/v3/exchangeInfo', 'method': 'GET'}
        }
        self.logger.debug('{} initialized'.format(self))

    def call_API(self, command: str = 'ping', **kwargs):
        self.logger.debug('method call with {}'.format([command, *kwargs]))
        api_url = concat_url(self.base_endpoint + self.methods[command]['url'], **kwargs)

        response = requests.request(method=self.methods[command]['method'],
                                    url=api_url,
                                    timeout=float(self.config_manager['APPLICATION']['connection_timeout']))

        self.logger.debug('sent request {} {}'.format(self.methods[command]['method'], api_url))
        self.logger.debug('got response {}'.format(response))
        if response.status_code == 404:
            raise APIError404(response.url, response.text)
        elif response.status_code == 429:
            raise APIWarning429(response.url, response.text, response.headers)
        elif response.status_code == 418:
            raise APIError418(response.url, response.text, response.headers)
        elif response.status_code == 200:
            result = response.json()
            self.logger.debug('method result is {}'.format(result))
            return result

    def get_klines(self,
                   pair: str,
                   resolution: str,
                   start=None,
                   end=None,
                   limit: int = 1000):

        self.logger.debug('method call with {}'.format([pair, resolution, start, end, limit]))
        if pair and resolution:
            try:
                result = self.call_API('klines',
                                       symbol=pair,
                                       interval='{}{}'.format(resolution[0], resolution[1]),
                                       startTime=start,
                                       endTime=end,
                                       limit=limit)

                self.logger.debug('method result is {}'.format(result))
                return result
            except Exception as e:
                self.logger.exception('Exception {}'.format(e))
                raise e
        else:
            raise NetworkHandlerError
