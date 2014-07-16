from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # Used to interact with the clients ORM.


class Patient(Base):
    """
    This is used by the SMS service to communication with a patient.
    Note: This is required by each client specific applications.
    """
    __tablename__ = 'patients'

    mobile = Column(String, nullable=False, unique=True, primary_key=True)
    forename = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    dob = Column(Integer)
