# A simple Slack ping system

import os
import socket
from slackclient import SlackClient
import argparse

parser = argparse.ArgumentParser(description='Send a message to slack')
parser.add_argument('type', metavar='Context', type=str,
                   help='The context')

args = parser.parse_args()
message = '@channel :info: *Server ' + socket.gethostname() + ' '

if args.type == 'boot':
    message += 'has just booted.  Deployment notification should arrive soon in this channel'
elif args.type == 'shutdown':
    message += 'is shutting down.  Please ensure everything is still OK!'
elif args.type == 'reboot':
    message += 'is rebooting.  Due to AWS, IP may change.  You should receive a start notification and a deployment ' \
               'notification soon '
else:
    message += 'wanted to send an unknown notification of type «' + args.type + '».  Please have a look'

print(args.type)

slack_token = os.environ["SLACK_API_TOKEN"]
slack = SlackClient(slack_token)
print(slack.api_call("chat.postMessage", channel="#servernotifs", text=message))
