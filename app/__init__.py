from app.application import Application
import os

try:
    _ = os.environ["UNIT_TEST_IN_PROGRESS"]
except KeyError:
    App = Application()
