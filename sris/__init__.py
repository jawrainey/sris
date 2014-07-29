from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from sris import views, models, manager


def check_for_new_patients():
    """
    Required to invoke the daily check to send the initial sms to new patients.
    """
    import threading
    threading.Timer(30, check_for_new_patients).start()
    from datetime import datetime
    import config
    if str(datetime.now().time())[0:5] == config.NEW_PATIENT_CHECK:
        manager.Manager().send_initial_sms()

check_for_new_patients()
