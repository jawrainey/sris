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
        # The ontology of emotions & concepts
        ontology = self.__load_ontology()
        # Words in the sentence appear in the ontology regardless of case.
        message = message.lower()
        print 'The message to be summarized is: %s' % message
        # Discover which emotions and concepts are in the patient's sms.
        emotions = self.__category_in_sms(ontology.get('emotions'), message)
        concepts = self.__category_in_sms(ontology.get('concepts'), message)
        from collections import Counter
        if emotions:  # First as emotions are more important than concepts.
            freq = Counter(emotions)
            most_common = freq.most_common()[0]
            # Check if multiple emotions exist with same (max) frequency
            if len([v for v in freq.values() if v == most_common[1]]) >= 2:
                # If they do, select the first that occurs in the ordered list.
                order_of_emotion = self.config['orderOfEmotions']
                emotion = [i for i in order_of_emotion if i in freq.keys()][0]
            else:
                # Otherwise, use the most frequent emotion.
                emotion = most_common[0]
            print 'The most frequent emotion was: %s' % emotion
            response = self.config['emotionResponses'][emotion] % emotion
        elif concepts:
            concept = Counter(concepts).most_common()[0][0]
            print 'The most frequent concept was: %s' % concept
            response = self.config['conceptResponses'][concept] % concept
        else:
            print 'No emotions/concepts were detected.'
            response = self.config['generalResponse']
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
