from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def __perform_timed_services():
    """
    Required to invoke the daily check to send the initial sms to new patients.
    """
    import threading
    from sris import manager
    man = manager.Manager()
    # Send client-defined SMS to all patients at pre-defined time.
    man.send_daily_sms()
    # Sends the initial SMS to all new patients.
    man.send_initial_sms()
    threading.Timer(30, __perform_timed_services).start()


def create_app(config):
    """
    Creates a flask app that does not initially bundle the extensions with it,
    which allows them to easily be used elsewhere.

    Args:
        config (object): The configuration object to use.

    Returns:
        app (object): The Python Flask object.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    from sris.views import bp
    app.register_blueprint(bp)

    # __perform_timed_services()

    return app
