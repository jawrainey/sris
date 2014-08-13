class Messenger:
    """
    Generates messages to send to a patient.
    """
    def __init__(self, config):
        """
        Populate attributes on initialisation.

        Args:
            config (json): Client specific configuration file that contains
            the questions to send to the user.
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

    def summary(self, message):
        """
        Constructs a reflective summary of the message received. This is used
        to empathises with the patient, and highlight understanding of the
        problem from the service side by providing a reflection summary.

        This method uses the Bag-of-words model to obtain emotions & concepts of
        the message, which is then used to select an appropriate response.

        Args:
            message (str): The message received from the patient.

        Returns:
            str: A reflective summary of the message received.
        """
        # The client defined reflective responses.
        concept_responses = self.config['conceptResponses']
        emotion_responses = self.config['emotionResponses']
        # The ontology of emotions & concepts
        ontology = self.__load_ontology()
        # Words in the sentence appear in the ontology regardless of case.
        message = message.lower()
        # Discover which emotions and concepts are in the patient's sms.
        emotions = self.__category_in_sms(ontology.get('emotions'), message)
        concepts = self.__category_in_sms(ontology.get('concepts'), message)
        # Select a reflective summary as a response best suited to the category
        import random
        if concepts:
            response = random.choice(concept_responses) % (concepts[0])
        elif emotions:
            response = random.choice(emotion_responses) % (emotions[0])
        else:
            # A naive general response if no emotions or concepts detected.
            response = ("Could you explain that further?")

        return response

    def __load_ontology(self):
        """
        Stores the contents of the service-defined ontology in a json object.

        Returns:
            json: A json object of the user-defined config file.
        """
        import settings
        import json
        with open(settings.Config.SERVICE_ONTOLOGY) as ontology:
            return json.load(ontology)

    def __category_in_sms(self, category, message):
        """
        Obtain the specific category/categories (emotions or concepts)

        Args:
            category (json): Categories (i.e. emotions) and related words
            message (str): The message received from the patient.

        Returns:
            categories (list): The categories found in the ontology.
        """
        categories = []
        for conemo, words in category.iteritems():
            for word in words:
                if word in message:
                    categories.append(conemo)
        return categories
