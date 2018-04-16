"""
    Slack notification system
"""

import os
from slackclient import SlackClient


class Slack:

    def __init__(self, config):
        if not os.environ["SLACK_API_TOKEN"]:
            raise RuntimeError('Missing Slack token.  Please define it as an environment variable named '
                               '«SLACK_API_TOKEN»')
        self.client = SlackClient(os.environ["SLACK_API_TOKEN"])
        if not config['DefaultChannel']:
            self.default_channel = '#general'
            print('NOTICE: missing default Slack channel.  Choosing #general')
        else:
            self.default_channel = config['DefaultChannel']
        self.allow_ping = bool(config['AllowPing'])

    def ping_canal(self, message, channel=''):
        if channel == '':
            channel = self.default_channel
        if channel[0] != '#':
            channel = '#' + channel
        print(self.client.api_call("chat.postMessage", link_names=int(self.allow_ping), channel=channel, text=message))
