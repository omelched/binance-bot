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
