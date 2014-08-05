from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()


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

    return app
