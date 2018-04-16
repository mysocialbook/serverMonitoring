import os

from Notifications.Slack import Slack
form Notifications.SES import SES
from Tools.ConfigLoader import ConfigLoader

class NotificationManager:
    def __init__(self):
        self.config = ConfigLoader().get_section('Notifications')

        if 'Slack' in self.config['Notifications']:
            self.slack = Slack(ConfigLoader().get_section('Slack'))
        if 'SES' in self.config['Notifications']:
            self.ses = SES(ConfigLoader().get_section('SES'))

    def send_notification(self, message):
        sent = False
        if 'Slack' in self.config['Notifications']:
            self.slack.ping_channel(message)
            sent = True
        elif 'SES' in self.config['Notifications']:
            self.ses.send_mail(message)
            sent = True

        if not sent:
            print('No notification channel defined')
