from app.application import ApplicationClass
import os

try:
    a = os.environ['PRODUCTION']
except KeyError:
    a = None
    print('Запущено в режиме тестирования.')

if a:
    App = ApplicationClass()
