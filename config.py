import os
_basedir = os.path.abspath(os.path.dirname(__file__))

# Database settings
CLIENT_NAME = 'atc'
SERVICE_NAME = 'sms'
CLIENT_DB = os.path.join(_basedir, 'sris/db/' + CLIENT_NAME + '.db')
SERVICE_DB = os.path.join(_basedir, 'sris/db/' + SERVICE_NAME + '.db')
SQLALCHEMY_BINDS = {
    CLIENT_NAME: 'sqlite:///' + CLIENT_DB,
    SERVICE_NAME: 'sqlite:///' + SERVICE_DB
}

# Flask specific settings
DEBUG = True
