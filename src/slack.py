from enum import Enum


class response_types(Enum):
    """response_types enumeration that can be exported and used to avoid typos when setting a
    response_type

    :param in_channel: Sends a message visible to all
    :type in_channel: str
    :param ephemeral: Sends a message only to the user who sent the message
    """

    in_channel = 'in_channel'
    ephemeral = 'ephemeral'


def build_message(text: str, **kwargs: dict) -> dict:
    """Builds and returns a dict to be sent to Slack as a message

    :param text: 
    :key response_type: Enum {ephemeral | in_channel }
    """

    # Defaults to in_channel
    response_type = 'in_channel'
    if 'response_type' in kwargs and kwargs['response_type'] in response_types:
        response_type = str(kwargs['response_type'])

    return {'text': text, 'response_type': response_type}
