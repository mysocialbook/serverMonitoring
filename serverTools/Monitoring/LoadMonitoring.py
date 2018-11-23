#!/usr/bin/python3
# coding=utf-8
"""
    This script monitor the the load of the server and trigger and alarm if a value is too high
"""

import os
import socket

from Tools.System import System


class LoadMonitoring:

    def __init__(self, config, notifier):
        self.notifier = notifier

        # Check disk space
        if System.get_free_disk_space('/') < (System.get_total_disk_space('/')/5):
            self.trigger_alarm('*Disk space* is too low. on instance ' + socket.gethostname() + '.  Only ' + str(System.get_free_disk_space('/') // (2**30)) +
                               'GB are left')
        # Check load average
        one_minute, five_minutes, fifteen_minutes = System.get_load_average()
        if five_minutes > System.get_cpu_count():
            self.trigger_alarm('*Overload detected*  Load of ' + str(five_minutes) + ' for max of ' + str(System.get_cpu_count()))

        if 'SendNotificationIfNoError' in config and bool(config['SendNotificationIfNoError']):
            self.display_status_message()

    def display_status_message(self):
        message = ':info: *Server ' + socket.gethostname() + '*'
        message += self.get_status_message()
        self.notifier.send_notification(message)

    def get_status_message(self):
        status_msg = "\n *Status* \n"
        status_msg += ':gear: *CPU* : ' + str(System.get_cpu_usage()) + "%\n"
        status_msg += ':chart_with_upwards_trend: *RAM* : ' + str(round(System.get_used_memory()/float(2**30), 2)) + \
                      'GB of ' + str(round(System.get_total_memory()/float(2**30))) + "GB \n"
        status_msg += ':bar_chart: *Load* : ' + str(System.get_load_average()) + ' of max ' + str(System.get_cpu_count()) + "\n"
        status_msg += ':card_file_box: *Disk usage* : _Used_ : ' + str(System.get_used_disk_space('/') // (2**30)) + \
                      'GB _Free_ : ' + str(System.get_free_disk_space('/') // (2**30)) + \
                      'GB _Total_ : ' + str(System.get_total_disk_space('/') // (2**30)) + "GB\n"
        return status_msg

    def trigger_alarm(self, message):
        message = ':warn: *Server ' + socket.gethostname() + '* is in danger zone ' + message
        self.notifier.send_notification(message)
