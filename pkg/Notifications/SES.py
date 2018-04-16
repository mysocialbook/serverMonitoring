"""
    Email notification system
"""

import os
import boto3
from botocore.exceptions import ClientError


class SES:

    def __init__(self, config):
        if not config['Region']:
            raise RuntimeError('Missing AWS Region.  Please define it in config file ')
        self.client = boto3.client('ses', region_name=config['Region'])
        if not config['Receiver'] or not config['Sender']:
            raise RuntimeError('Required «Sender» and «Receiver» key are not set in config!')
        self.sender = config['Sender']
        self.receiver = config['Receiver']

    def send_mail(self, message):
        try:
            # Provide the contents of the email.
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        self.receiver,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': message,
                        },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': '[Monitoring]',
                    },
                },
                Source=self.sender,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['ResponseMetadata']['RequestId'])

