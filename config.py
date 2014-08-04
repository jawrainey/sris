import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Database settings
CLIENT_NAME = 'client'
SERVICE_NAME = 'service'
CLIENT_DB = os.path.join(BASEDIR, 'sris/db/' + CLIENT_NAME + '.db')
SERVICE_DB = os.path.join(BASEDIR, 'sris/db/' + SERVICE_NAME + '.db')
SQLALCHEMY_BINDS = {
    CLIENT_NAME: 'sqlite:///' + CLIENT_DB,
    SERVICE_NAME: 'sqlite:///' + SERVICE_DB
}

# Service settings
NEW_PATIENT_CHECK = '10:00'

# Flask specific settings
DEBUG = True
