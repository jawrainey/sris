from flask.ext.script import Manager, Shell
from sris import create_app, db
from settings import DevConfig, ProdConfig
import os

if os.environ.get("ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)


def _context():
    """
    Expose shell session access to the app and db modules.

    Returns:
        dict: Exposing access to 'app' and 'db'.
    """
    return {'app': app, 'db': db}

manager = Manager(app)
manager.add_command('shell', Shell(make_context=_context))

if __name__ == '__main__':
    manager.run()
