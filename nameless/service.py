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
        for num, messages in self.__check_inbox().iteritems():
            if num == number:
                return messages
        return []

    def __check_inbox(self):
        """
        Obtains ALL messages from the inbox, AND* saves the results to an
        appropriate data structure.

        *TODO: refactor separate functionality to appropriate methods.

        Returns:
            list: List of dictionaries containing messages for each mobile num.

        Note: There is no simple way to get all messages for a specific number.
        Instead, we obtain ALL messages in the inbox, then filter it.

        The structure returned is of the format:
        [
         {'01111111111', # e.g. the mobile number is unique key
          'messages': [
            {'message': 'Hello world', 'date': '2014-07-15',
               ...
              'message': }
           ]},
           ...
         ]

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
        all_messages = json.loads(req.text)['messages']

        import collections
        patient_messages = collections.defaultdict(list)
        for message in all_messages:
            # TODO: Add date (UNIX timestamp) to msg.
            msg = {'message': message['message']}
            patient_messages[message['number']].append(msg)
        return patient_messages
