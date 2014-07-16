from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from service import SMSService
from messenger import Messenger
from databases.databases import Databases
import config

# The client specific database.
atc_engine = create_engine(config.SQLALCHEMY_BINDS['atc'])
atc_session = sessionmaker(bind=atc_engine)()

# This is the 'on-going' service specific database that
# saves messages sent and received from the client.
sms_engine = create_engine(config.SQLALCHEMY_BINDS['sms'])
sms_session = sessionmaker(bind=sms_engine)()

# Use a wrapper to import ALL databases.
db = Databases()


def __new_patients():
    """
    Checks to see if any new patients have been added to the client DB.

    Returns:
        list: Contains mobile numbers the client knows & the service does not.
    """
    # ALL numbers obtained from the client (ATC).
    atc_numbers = atc_session.query(db.atc.Patient.mobile).all()
    # The numbers the service has to date.
    have_numbers = sms_session.query(db.sms.User.mobile).all()
    # The numbers the client has, but the service does not.
    numbers = set(atc_numbers).difference(have_numbers)
    print 'There was %s new patients' % str(len(numbers))
    # Convert SQLAlchemy KeyedTuple to ordinary list.
    return [item.mobile for item in numbers]


def __create_new_patient(number):
    """
    Adds the patient to the service database.

    Args:
        number (str): The mobile number of the patient.
    """
    sms_session.add(db.sms.User(mobile=number))
    sms_session.commit()


def __save_message(number, message, status, timestamp=None):
    """
    Save the SMS message (sent or received) to the service database.

    Args:
        number (str): The mobile number of the patient.
        message (str): The SMS message content.
        status (str): The status of the message, e.g. 'sent' or 'received'.
        timestamp (int): The UNIX timestamp of the message.
    """
    if timestamp:
        sms_session.add(db.sms.Message(mobile=number, message=message,
                                       status=status, timestamp=timestamp))
    else:
        # Instead of inserting 'None' use the default (current time)
        sms_session.add(db.sms.Message(mobile=number, message=message,
                                       status=status))
    sms_session.commit()


def __save_messages(number, messages):
    """
    Saves received messages to the service database.

    Args:
        number (str): The mobile number of the patient.
        messages (list): All messages received that the service does not have.
    """
    for message in messages:
        print "The message being saved is: " + message['message']
        __save_message(number, message['message'], 'received', message['date'])


def send_sms_to_new_patients():
    """
    Sends an 'initial' SMS to new patients of the client.
    """
    message = Messenger().initial_message()
    # 'New patients' are those that have recently been added
    # to the clients database, which the service does not know.
    for number in __new_patients():
        SMSService().send_sms(number, message)
        __create_new_patient(number)
        # TODO: Is it necessary to save the initial message?
        __save_message(number, message, 'sent')


def reply_to_new_sms():
    """
    Checks if a new sms has been received, and responds accordingly.
    """
    all_patients = sms_session.query(db.sms.User.mobile).all()
    for patient in all_patients:
        number = patient.mobile
        client_messages = SMSService().all_messages(int(number))
        service_messages = sms_session.query(db.sms.Message).filter(
            and_(db.sms.Message.mobile == number,
                 db.sms.Message.status == 'received')).all()
        print "Count of messages for %d in INBOX is: %s\n" \
              "Count of messages received in the service db is: %s" \
              % (int(number), len(client_messages), len(service_messages))
        if len(client_messages) > len(service_messages):
            print "New messages received."
            message = Messenger().ongoing_message()
            SMSService().send_sms(number, message)
            # For now, we do not want to save OUR conversation. Just clients.
            __save_message(number, message, 'sent')
            # Save the messages the service do not know about.
            messages_to_save = (len(client_messages) - len(service_messages))
            print "Saving %d message(s) to the database: %s" \
                % (messages_to_save, client_messages[0:messages_to_save])
            __save_messages(number, client_messages[0:messages_to_save])

if __name__ == "__main__":
    from twisted.internet import task
    from twisted.internet import reactor

    when_to_check = 10  # Is in seconds, and low for testing.
    # Check nightly for new client patients and automatically SMS.
    task.LoopingCall(send_sms_to_new_patients).start(when_to_check)
    # Check the service SMS INBOX for NEW messages then respond accordingly
    task.LoopingCall(reply_to_new_sms).start(when_to_check)
    reactor.run()
