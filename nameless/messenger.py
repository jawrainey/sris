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

    def predefined_message(self, time):
        """
        ?????

        Args:
            time (string): ???

        Returns:
            str: ???
        """
        return ''

    def ongoing_message(self):
        """
        Generates a message suitable for a user based on their history.

        Returns:
            str: The generated message.

        TODO:

        This method needs to be made intelligent to suggest interventions.

            1. Generate a suitable message based on previous conversations.
            2. Personalise message through location based & NHS data.
        """
        print "The ongoing message is being sent."
        import random
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
