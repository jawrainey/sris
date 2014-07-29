from sris import db, models
from messenger import Messenger
from service import SMSService


class Manager:
    """
    The middle-man of interaction between messenger and the SMS service.
    """
    def __init__(self):
        self.config = self.__load_config_file()
        self.messenger = Messenger(self.config)
        self.sms_service = SMSService()

    def send_initial_sms(self):
        """
        Sends an 'initial' SMS to new patients of the client.
        """
        # New patients are those that have recently been added
        # to the clients database, which the service does not know.
        for number in self.__new_patients():
            message = self.messenger.initial_message()
            self.sms_service.send(number, message)
            self.__create_new_patient(number)
            self.__save_message(number, message, 'sent')

    def respond(self, patient_response):
        """
        Respond to new SMS when it is received.

        Args:
            patient_message (dict): Contains the number, and message sent to
            the service by a patient.
        """
        number = patient_response['number']
        patient_message = patient_response['message']
        # Generate a response based on the sentiment of the patient's message.
        message = self.messenger.respond(number, patient_message)
        self.__save_message(number, patient_message, 'received')
        self.__save_message(number, message, 'sent')
        return self.sms_service.reply(message)

    def send_sms_at_config_time(self, number):
        """
        Sends a question/message to a patient at a pre-defined time.

        Args:
            number (str): The mobile number to send the message.
        """
        from datetime import datetime
        for question in self.config['dailyQuestions']:
            if str(datetime.now().time())[0:5] == str(question['time']):
                message = question['question']
                print "Sending a client-defined question (%s) " \
                    "at a defined time (%s)" % (question['time'], message)
                self.__save_message(number, message, 'sent')
                self.sms_service.send(number, message)

    def __load_config_file(self):
        """
        Stores the contents of the client-defined config file to a json object.

        Returns:
            json: A json object of the user-defined config file.
        """
        import config
        import json
        config_file = config.CLIENT_NAME + '.json'
        basedir = '/Users/jawrainey/Dropbox/dev/summer-ra/sris/sris/'
        with open(basedir + 'config/' + config_file) as json_settings:
            return json.load(json_settings)

    def __new_patients(self):
        """
        Checks to see if any new patients have been added to the client DB.

        Returns:
            list: Mobile numbers the client knows & the service does not.
        """
        # ALL numbers obtained from the client.
        client_numbers = db.session.query(models.Patient.mobile).all()
        # The numbers the service has to date.
        service_numbers = db.session.query(models.User.mobile).all()
        # The numbers the client has, but the service does not.
        numbers = set(client_numbers).difference(service_numbers)
        print 'There was %s new patients' % str(len(numbers))
        # Convert SQLAlchemy KeyedTuple to ordinary list.
        return [item.mobile for item in numbers]

    def __create_new_patient(self, number):
        """
        Adds the patient to the service database.

        Args:
            number (str): The mobile number of the patient.
        """
        db.session.add(models.User(mobile=number))
        db.session.commit()

    def __save_message(self, number, message, status):
        """
        Save the SMS message (sent or received) to the service database.

        Args:
            number (str): The mobile number of the patient.
            message (str): The SMS message content.
            status (str): The status of the message, e.g. 'sent' or 'received'.
        """
        db.session.add(models.Message(mobile=number, message=message,
                                      status=status))
        db.session.commit()
