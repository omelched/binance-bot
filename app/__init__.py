from app.application import Application
import os

try:
    _ = os.environ['PRODUCTION']
    App = Application()
except KeyError:
    print('Запущено в режиме тестирования.')
    pass

