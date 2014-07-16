class Messenger:
    """
    Generates messages to send to a patient.
    """
    def initial_message(self):
        """
        The first message and interaction from the service to the patient.

        Returns:
            str: The predefined message to send to new patients.
        """
        return "Hello, world! -- Initial text message."

    def ongoing_message(self):
        """
        Generates a message suitable for a user based on their history.

        Returns:
            str: The generated message.

        TODO:

        This method needs to be made intelligent to suggest interventions.
        There are multiple ways to achieve this, which include:

            1. Use a pre-defined set (JSON) of responses with associated times.
            2. Generate a suitable message based on previous conversations.
        """
        import datetime  # Used for testing.
        return "It's me again." + str(datetime.datetime.utcnow())
