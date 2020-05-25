from app.application import Application
import os

# TODO: сделать адекватную проверку
try:
    _ = os.environ['PRODUCTION']
    App = Application()
except KeyError:
    print('Запущено в режиме тестирования.')
    pass

