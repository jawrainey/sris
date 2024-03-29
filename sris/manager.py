from sris import db, models
from messenger import Messenger
from service import SMSService
from datetime import datetime


class Manager:
    """
    The middle-man of interaction between messenger and the SMS service.
    """
    def __init__(self):
        self.config = self.__load_config_file()
        self.messenger = Messenger(self.config)
        self.sms_service = SMSService()

    def send_initial_greeting(self):
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
        if current_time == self.config['initialQuestion']['time']:
            for number in self.__new_patients():
                message = self.messenger.initial_message()
                self.sms_service.send(number, message)
                self.__create_new_patient(number)
                self.__save_message(number, message, 'sent')

    def respond(self, patient_response):
        """
        Respond to new SMS when it is received via a POST request.

        Args:
            patient_message (dict): Contains the number, and message sent to
            the service by a patient.

        Returns:
            response (XML): twilio formatted response.
        """
        number = patient_response['number']
        patient_message = patient_response['message']
        # Generate a reflective summary based on the patient's response.
        summary = self.messenger.summary(patient_message)

        # TODO: Fix this with the system set time (i.e. UTC)
        midnight = int(datetime.today().strftime("%s")) - 24*60*60
        # The number of questions sent since last night.
        _questions = db.session.query(models.Message).filter(
            models.Message.mobile == number,
            models.Message.status == 'sent',
            models.Message.timestamp >= midnight).all()

        all_sent = [item.message for item in _questions]
        # The number of OEQ sent since last night.
        num_oeq = len([i for i in self.config['questions'] if i in all_sent])

        print 'Number OEQ sent since last night was: %s' % str(num_oeq)

        response = None

        # Do not send a response if initial daily conversation not started.
        if num_oeq >= 1:
            print 'The last sms sent was: %s' % all_sent[-1]
            if all_sent[-1] in self.config['questions']:
                print 'Last message sent was an OEQ. Sending a RS to patient.'
                response = summary
            else:
                print 'Inside the else..'
                if (num_oeq >= int(self.config['limit'])):  # True: OEQ >= LIMIT
                    print 'Inside the else... in the if...'
                    if self.config['endQuestion'] not in all_sent:
                        print 'Sending the conversation closer as limit met.'
                        response = self.config['endQuestion']
                else:
                    print 'Message received was response to a RS. Sending OEQ.'
                    response = self.__select_question(number)

        if response:
            self.__save_message(number, patient_message, 'received')
            self.__save_message(number, response, 'sent')
            print 'The response (%s) has been saved to the database.' % response
            return self.sms_service.reply(response)
        else:
            print 'No response was created.'
            return ''  # Prevents a 500 error code returned to POST.

    def send_initial_question_to_all(self):
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
                message = self.__select_question(number)
                print "OEQ (%s) to patient (%s)." % (message, number)
                self.__save_message(number, message, 'sent')
                self.sms_service.send(number, message)

    def __select_question(self, number):
        """
        Select a client-defined open-ended question that has not been previously
        selected at random. If all have been sent then select one at random.

        Args:
            number (str): The mobile number of the patient.

        Returns:
            str: An open-ended question to ask the patient.
        """
        questions = self.config['questions']
        sent_questions = [item.message for item in db.session.query(
            models.Message).filter(models.Message.mobile == number).all()]
        unsent_questions = list(set(questions).difference(sent_questions))
        # TODO: Select most important question based on client's situation
        import random
        if unsent_questions:
            print "Sending a message that HAS NOT been previously sent."
            message = random.choice(unsent_questions)
        else:
            print "Sending a message that HAS been previously sent."
            message = random.choice(questions)
        return message

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
