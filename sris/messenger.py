from sentiment import Sentiment


class Messenger:
    """
    Generates messages to send to a patient.
    """
    def __init__(self, config):
        """
        Populate attributes on initialisation.

        Args:
            config (json): Client specific configuration file that contains
            the responses to pass to the service.
        """
        self.config = config

    def initial_message(self):
        """
        The first message and interaction from the service to the patient.

        Returns:
            str: The predefined message to send to new patients.
        """
        print "The initial message is being sent."
        return self.config['initialQuestion']

    def respond(self, number, message):
        """
        Obtains a suitable response from the client defined settings based on
        the sentiment (positive/negative) of the message that the patient sent.

        Args:
            number (str): The mobile number of the patient.
            message (str): The last message received from the patient.

        Returns:
            str: A message to continue the conversation with the patient.
        """
        print "The message from the patient was: %s" % (message)
        sentiment = Sentiment().determine_sentiment(message)
        print "The sentiment generated for the response was: %s" % (sentiment)
        import random

        # TODO:
        #   - Filter so all interventions/responses are used before repeating.
        #   - Select a response for the given message (rather than randomly).
        if sentiment is 'pos':
            return self.config['positiveResponses'][random.randint(0, 1)]
        else:
            return self.config['interventionQuestions'][random.randint(0, 1)]

    def __download_url(self):
        """
        ???????

        Returns:
            str: An SMS message containing the download url of the mobile app,
            otherwise None.
        """
        download_url = self.config['downloadURL']
        if download_url:
            return 'A mobile app has been developed to enhance this service,' \
                ' which can be downloaded at:' + download_url
        return None

    def __opt_out(self):
        return ''

    def __respond_to_daily(self):
        # if previous message in db,
        # find it + 1 (e.g. the response)
        # parse respond and find 'scale' level
        # use this level to lookup the 'response' from the config file.
        return ''


class QuestionTypes:

    def defined(self):
        # if day in response in config['questions']['question']['responses']
        # then send an intervention
        return ''

    def scale(self):
        # get scale that they responded with...
        # lookup response for the scale in the json file
        # return said response
        # (Ideally, it should be an 'open' 'emotionally based' question?)
        return ''

    def polar(self):
        # get their response
        # lookup question object & store it
        # if their response contains yes (or a varient) then return config['yes]
        # Otherwise, we return the related 'no' question.
        return ''
