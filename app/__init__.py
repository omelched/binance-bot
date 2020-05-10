from app.application import Application
import os

if os.environ["UNIT_TEST_IN_PROGRESS"] == "1":
    pass
else:
    App = Application()
