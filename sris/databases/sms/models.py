from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    Stores patient mobile numbers, which can be used to lookup details in the
    client specific database, and to associate one number to many SMS messages.
    Note: this is required to 'diff' against the patient database to nightly.
    """
    __tablename__ = 'users'

    mobile = Column(String, nullable=False, unique=True, primary_key=True)
    messages = relationship("Message", cascade="all,delete", backref="users")


class Message(Base):
    """
    Stores SMS messages sent/received to the patient.
    Note: A user table is not required as the mobile number can uniquely
    identify a user within the client's plugin database (e.g. ATC).
    """
    __tablename__ = 'messages'

    import datetime
    import calendar

    now = datetime.datetime.utcnow()  # utcnow as that's what returned by API

    id = Column(Integer, primary_key=True)
    mobile = Column(String, ForeignKey('users.mobile'))
    message = Column(String)
    status = Column(String)  # Used to differentiate between SMS sent/received.
    timestamp = Column(Integer, default=calendar.timegm(now.timetuple()))
