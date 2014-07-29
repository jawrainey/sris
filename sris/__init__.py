from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from sris import views, models, manager


def perform_timed_services():
    """
    Required to invoke the daily check to send the initial sms to new patients.
    """
    import threading
    import config
    from datetime import datetime
    man = manager.Manager()
    # Send client-defined SMS to all patients at pre-defined time.
    man.send_daily_sms()
    # Sends the initial SMS to all new patients.
    if str(datetime.now().time())[0:5] == config.NEW_PATIENT_CHECK:
        man.send_initial_sms()
    threading.Timer(30, perform_timed_services).start()

perform_timed_services()
