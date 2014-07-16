import config
import json
import requests


class SMSService:
    """
    Sends and obtains SMS messages using the txtLocal REST API.
    """
    def send_sms(self, number, message):
        """
        Sends the SMS message to the given number.

        Args:
            number (str): The mobile number of the patient.
            message (str): The SMS message content.
        """
        payload = ({'apiKey': config.API_KEY, 'numbers': [number],
                    'message': message, 'sender': config.SENDER,
                    'test': config.TEST_MODE})
        requests.post(config.API_SEND_URI, params=payload)
        # TODO: Error checking in req.text

    def all_messages(self, number):
        """
        Obtains all received messages from the INBOX for a specific number.

        Args:
            number (int): The mobile number to obtain messages for.

        Returns:
            list: contains all the messages for a given number, other empty.
        """
        for num, messages in self.__messages_by_patient().iteritems():
            if num == number:
                return messages
        return []

    def __all_sms_from_inbox(self):
        """
        Obtains ALL SMS messages from the INBOX for the service.

        Returns:
            list: list containing all messages from the INBOX.

        Note: There is no simple way to get all messages for a specific number.
        Instead, we obtain ALL messages in the inbox, then filter it below.

        An alternative approach, which may be implemented later, is to hook
        into the POST service provided by the API (which gets notified when
        an SMS is received). This service can then automagically respond
        via the REST hook.

        This has the advantage of not having to manually filter the INBOX, but
        instead respond when automatically to the user.
        However, this service then becomes dependant on the REST/POST service.
        """
        payload = ({'apiKey': config.API_KEY, 'inbox_id': config.INBOX_ID,
                    'sort_order': 'desc'})  # Latest message first.
        req = requests.post(config.API_RECEIVE_URI, params=payload)
        return json.loads(req.text)['messages']

    def __messages_by_patient(self):
        """
        Filters the list of ALL messages by mobile number.

        Returns:
            list: List of dictionaries containing messages for each mobile num.

        The structure returned is of the format:
        [
         {'01111111111', # e.g. the mobile number is unique key
          [
            {'message': 'Hello world', 'date': '2014-07-15'},
            ...
            {'message': 'Hello world', 'date': '2014-07-18'},
           ]
         },
        ]
        """
        import collections
        import datetime
        import time

        patient_messages = collections.defaultdict(list)
        for message in self.__all_sms_from_inbox():
            tt = datetime.datetime.strptime(message['date'],
                                            "%Y-%m-%d %H:%M:%S").timetuple()
            msg = {'message': message['message'], 'date': time.mktime(tt)}
            patient_messages[message['number']].append(msg)
        return patient_messages
