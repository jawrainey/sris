import os


class Config(object):
    """
    The shared configuration settings for the flask app.
    """
    # Service settings
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    SERVICE_ONTOLOGY = PROJECT_ROOT + '/sris/config/ontology.json'

    # Database settings
    CLIENT_NAME = 'client'
    SERVICE_NAME = 'service'

    # These need to be set by you!
    ACCOUNT_SID = os.environ.get('ACCOUNT_SID', None)
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN', None)
    NUM = os.environ.get('NUM', None)


class ProdConfig(Config):
    """
    Setup the production configuration for the flask app.

    Args:
        Config (object): Inherit the default shared configuration settings.
    """
    DEBUG = False
    # These are set server-side for ease-of-use when using PaaS.
    SQLALCHEMY_BINDS = {
        Config.CLIENT_NAME: os.environ.get('CLIENT_DATABASE_URL', None),
        Config.SERVICE_NAME: os.environ.get('SERVICE_DATABASE_URL', None)
    }


class DevConfig(Config):
    """
    Setup the development configuration for the flask app.

    Args:
        Config (object): Inherit the default shared configuration settings.
    """
    DEBUG = True
    # Store these in the root directly.
    CLIENT_DB = os.path.join(Config.PROJECT_ROOT, Config.CLIENT_NAME + '.db')
    SERVICE_DB = os.path.join(Config.PROJECT_ROOT, Config.SERVICE_NAME + '.db')
    # Support for multiple databases (client & service)
    SQLALCHEMY_BINDS = {
        Config.CLIENT_NAME: 'sqlite:///{0}'.format(CLIENT_DB),
        Config.SERVICE_NAME: 'sqlite:///{0}'.format(SERVICE_DB)
    }
