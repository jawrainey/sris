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
        Sends the initial SMS to new* patients at a pre-defined client time.

        *New patients are those that have recently been added
        to the clients database, which the service does not know.

        Note: this is REQUIRED otherwise 'respond' & other services do not
        function as database errors are thrown (understandably).
        """
        from datetime import datetime
        current_time = str(datetime.now().time())[0:5]
        # Send the message to new patients at the defined time.
        if current_time == self.config['initialQuestion'][0]['time']:
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
        # Generate a reflective summary based on the patient's response.
        message = self.messenger.summary(patient_message)
        self.__save_message(number, patient_message, 'received')
        self.__save_message(number, message, 'sent')
        print 'Response constructed and about to be sent.'
        return self.sms_service.reply(message)

    def send_question_sms(self):
        """
        Sends a question to all patients at a pre-defined day and time.
        """
        known_patients = [item.mobile for item in
                          db.session.query(models.Patient.mobile).all()]
        from datetime import datetime
        print "Checking to see if open-ended question should be sent."
        isDay = datetime.now().strftime("%A") in self.config["daysToSend"]
        isTime = str(datetime.now().time())[0:5] == self.config["sendTime"]
        if isDay and isTime:
            for number in known_patients:
                client_questions = self.config['questions']
                sent_questions = [item.message for item in db.session.query(
                    models.Message).filter_by(mobile=number).all()]
                unsent_questions = list(
                    set(client_questions).difference(sent_questions))

                import random
                if unsent_questions:
                    print "Sending a message that HAS NOT been previously sent."
                    message = random.choice(unsent_questions)
                else:
                    print "Sending a message that HAS been previously sent."
                    message = random.choice(client_questions)

                print "Sending open-ended question (%s) to client (%s)." \
                    % (message, number)
                self.__save_message(number, message, 'sent')
                self.sms_service.send(number, message)

    def __load_config_file(self):
        """
        Stores the contents of the client-defined config file to a json object.

        Returns:
            json: A json object of the user-defined config file.
        """
        import json
        from flask import current_app
        config_file = current_app.config['PROJECT_ROOT'] + '/sris/config/' + \
            current_app.config['CLIENT_NAME'] + '.json'
        with open(config_file) as json_settings:
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
