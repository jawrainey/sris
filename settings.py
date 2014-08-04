import os


class Config(object):
    """
    The shared configuration settings for the flask app.
    """
    # Service settings
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    NEW_PATIENT_CHECK = '10:00'

    # Database settings
    CLIENT_NAME = 'client'
    SERVICE_NAME = 'service'

    # These need to be set by you!
    ACCOUNT_SID = 'ACe5aeca75999845ce0130f7176cae9e6d'
    AUTH_TOKEN = '905ec14da5a8c4a121b88ec0dbbf6bb3'
    NUM = '+441508292049'


class ProdConfig(Config):
    """
    Setup the production configuration for the flask app.

    Args:
        Config (object): Inherit the default shared configuration settings.
    """
    DEBUG = True
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
