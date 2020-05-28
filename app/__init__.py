from app.application import Application
import os

try:
    a = os.environ['PRODUCTION']
except KeyError:
    a = None
    print('Запущено в режиме тестирования.')

if a:
    App = Application()
