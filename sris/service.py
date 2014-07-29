class SMSService:
    """
    Send and reply to SMS messages received.
    """
    def send(self, number, message):
        """
        Sends the SMS message to the given number.

        Args:
            number (str): The mobile number of the patient.
            message (str): The SMS message content.
        """
        from twilio.rest import TwilioRestClient
        import config
        client = TwilioRestClient(config.ACCOUNT_SID, config.AUTH_TOKEN)
        message = client.messages.create(to=number, from_=config.NUM,
                                         body=message)

    def reply(self, message):
        """
        Respond to an SMS message via the POST service.

        Args:
            message (str): The message to send.

        Returns:
            response (str): XML twilio formatted response.
        """
        import twilio.twiml
        response = twilio.twiml.Response()
        response.message(message)
        return str(response)
