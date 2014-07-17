import os
_basedir = os.path.abspath(os.path.dirname(__file__))
# Plugin settings
DATABASE_NAMES = ['atc', 'sms']
# Using sqlite for local development, will be SQL on production.
SQLALCHEMY_BINDS = {
    'atc': 'sqlite:///' + os.path.join(_basedir, 'db/atc.db'),
    'sms': 'sqlite:///' + os.path.join(_basedir, 'db/sms.db')
}

# TxtLocal SMS settings
SENDER = '447786202240'
INBOX_ID = '498863'
API_KEY = 'Sap3A0EaE2k-xL6d4nLJuQdZriNxBByUjRhOCHM5X0'
API_URI = 'https://api.txtlocal.com/'
API_SEND_URI = API_URI + 'send/?'
API_RECEIVE_URI = API_URI + 'get_messages/?'
TEST_MODE = 1  # 1 (True) to enable test mode & 0 to disable.
