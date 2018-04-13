"""
    Slack notification system
"""

import os
from slackclient import SlackClient


class SlackNotification:

    """
        TOGGLES
    """
    allow_ping = True

    def __init__(self):
        self.client = SlackClient(os.environ["SLACK_API_TOKEN"])

    def pingCanal(self, message, canal):
        if canal[0] != '#':
            canal = '#' + canal
        print(self.client.api_call("chat.postMessage", link_names=int(self.allow_ping), channel=canal, text=message))
