from Notifications.Slack import Slack
from Notifications.SES import SES


class NotificationManager:
    def __init__(self, config):
        self.config = config
        self.notifications = self.config.get_section('Notifications')

        if 'Slack' in self.notifications['Notifications']:
            self.slack = Slack(self.config.get_section('Slack'))
        if 'SES' in self.notifications['Notifications']:
            self.ses = SES(self.config.get_section('SES'))

    def send_notification(self, message):
        sent = False
        if 'Slack' in self.notifications['Notifications']:
            self.slack.ping_channel(message)
            sent = True
        elif 'SES' in self.notifications['Notifications']:
            self.ses.send_mail(message)
            sent = True

        if not sent:
            print('No notification channel defined')
