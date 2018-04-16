import os

from Notifications.Slack import Slack
from Tools.ConfigLoader import ConfigLoader

class NotificationManager:
    def __init__(self):
        self.config = ConfigLoader().get_section('Notifications')

        if 'Slack' in self.config['Notifications']:
            self.slack = Slack(ConfigLoader().get_section('Slack'))

    def send_notification(self, message):
        if 'Slack' in self.config['Notifications']:
            self.slack.ping_canal(message)
        else:
            print('No notification channel defined')
