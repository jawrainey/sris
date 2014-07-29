from sris import db


class User(db.Model):
    """
    Stores patient mobile numbers, which can be used to lookup details in the
    client specific database, and to associate one number to many SMS messages.
    Note: this is required to 'diff' against the patient database to nightly.
    """
    __tablename__ = 'users'
    __bind_key__ = 'sms'

    mobile = db.Column(db.String, nullable=False, unique=True, primary_key=True)
    messages = db.relationship("Message", cascade="all,delete", backref="users")


class Message(db.Model):
    """
    Stores SMS messages sent/received to the patient.
    Note: A user table is not required as the mobile number can uniquely
    identify a user within the client's plugin database (e.g. ATC).
    """
    __tablename__ = 'messages'
    __bind_key__ = 'sms'

    import datetime
    import calendar

    now = datetime.datetime.utcnow()  # utcnow as that's what returned by API

    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String, db.ForeignKey('users.mobile'))
    message = db.Column(db.String)
    status = db.Column(db.String)  # Used to differentiate SMS sent/received.
    timestamp = db.Column(db.Integer, default=calendar.timegm(now.timetuple()))


class Patient(db.Model):
    """
    This is used by the SMS service to communication with a patient.
    Note: This is required by each client specific application.
    """
    __tablename__ = 'patients'
    __bind_key__ = 'atc'

    mobile = db.Column(db.String, nullable=False, unique=True, primary_key=True)
    forename = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    dob = db.Column(db.Integer)
