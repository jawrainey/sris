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
            return self.config['positiveResponses'][0]
        else:
            return self.config['interventionQuestions'][random.randint(0, 1)]
