from flask.ext.script import Manager, Shell
from sris import create_app, db, manager
from settings import DevConfig, ProdConfig
import os

if os.environ.get("ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)


man = Manager(app)


@man.command
def timed_services():
    """
    Required to invoke the daily check to send the initial sms to new patients.
    """
    with app.app_context():
        import threading
        man = manager.Manager()
        man.send_initial_greeting()
        man.send_initial_question_to_all()
        # TODO: Better error checking
        # i.e. do not re-send the daily SMS if it has already been sent.
        threading.Timer(60, timed_services).start()


def _context():
    """
    Expose shell session access to the app and db modules.

    Returns:
        dict: Exposing access to 'app' and 'db'.
    """
    return {'app': app, 'db': db}

man.add_command('shell', Shell(make_context=_context))

if __name__ == '__main__':
    man.run()
