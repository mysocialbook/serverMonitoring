# coding=utf-8
"""
    This script monitor the status of all services and, if one is detected as «failed»
    will try to relaunch it.
    Whatever the relaunch status is, a notification will be sent.
    If relaunch has failed, logs of failed service are retrieved and sent as part of message


    This code reuse part of the server-tools by David Lumaye, code available here
    https://github.com/chindit/server-tools
    In order to respect the license of this tool, this code MUST
    - Display license & copyright notice
    - Make public any change in source
    - Keep GNU Affero GPL v3 as a license

    If you don't want to respect any of these points, please rewrite this tool immediately !
"""

import subprocess
from datetime import datetime, timedelta
from time import sleep

# Import custom classes
from Notifications.NotificationManager import NotificationManager


class ServicesMonitoring:
    # Internal variable.  DO NOT EDIT
    relaunch_status = False
    overall_status = True

    def __init__(self, config):
        # Call for general status
        main_process = subprocess.Popen("systemctl status | grep State: | head -1 | awk '{print $2}'", shell=True,
                                        stdout=subprocess.PIPE)
        status = main_process.stdout.read().decode('UTF-8').strip()
        main_process.stdout.close()

        if status != "running":
            failing_process = subprocess.Popen("systemctl --failed | grep failed | wc -l", shell=True,
                                               stdout=subprocess.PIPE)
            failing_units = int(failing_process.stdout.read().decode('UTF-8').strip())
            failing_process.stdout.close()
            if failing_units == 0:
                error_msg = '@channel :bangbang: *System is unstable* but I don\'t detect any failed service.\n\n' \
                            'Current status is «' + status + '»'
            else:
                error_msg = '@channel :bangbang: *Server is unstable* '+"\n"
                failed_process = subprocess.Popen("systemctl --failed | grep failed | awk '{print $2}'", shell=True,
                                                  stdout=subprocess.PIPE)
                failed_units = failed_process.stdout.read().decode('UTF-8').strip()
                failed_process.stdout.close()
                failed_units = failed_units.split('\n')
                error_msg += str(failing_units) + " failed services have been found.\n\n"
                error_msg += 'Following units are in «failed» state:\n'

                relaunch_toggle = False
                if 'RelaunchJobs' in config and config['RelaunchJobs'] == 'yes':
                    relaunch_toggle = True

                for unit in failed_units:
                    if relaunch_toggle:
                        # Attempting unit restart
                        result = self.relaunch_unit(unit)
                        if self.relaunch_status:
                            error_msg += '- ' + unit + ': RELAUNCHED on ' + datetime.now().strftime(
                                "%Y-%m-%d %H:%I:%S") + "\n"
                            if result:
                                error_msg += "This message was returned while reloading service:\n"
                                error_msg += result + "\n\n"
                            else:
                                self.overall_status = False
                                error_msg += '- ' + unit + ': FAILED on ' + datetime.now().strftime("%Y-%m-%d %H:%I:%S") + "\n"
                                error_msg += "Message returned while reloading unit:\n"
                                error_msg += result + "\n"
                                error_msg += "This is the last error log we have about this failure:\n"
                                error_msg += self.get_log_for_unit(unit) + "\n\n"
                    else:
                        error_msg += '- ' + unit + "\n"

            # Sending notification
            notification = NotificationManager()
            notification.send_notification(error_msg)


    @staticmethod
    def get_log_for_unit(unit):
        previous_hour = datetime.now() - timedelta(hours=1)
        unit_log_process = subprocess.Popen(
            "journalctl -u " + unit + " --since '" + previous_hour.strftime("%Y-%m-%d %H:%I:%S") + "'", shell=True,
            stdout=subprocess.PIPE)
        logs = unit_log_process.stdout.read().decode('UTF-8').strip()
        unit_log_process.stdout.close()
        return logs

    """
        Will not be called if toggle is switched off
    """
    def relaunch_unit(self, unit):
        self.relaunch_status = False
        unit_reload_process = subprocess.Popen("systemctl start " + unit, shell=True, stdout=subprocess.PIPE)
        unit_restart_result = unit_reload_process.stdout.read().decode('UTF-8').strip()
        relaunch_message = ''
        if unit_restart_result:
            relaunch_message = unit_restart_result
        unit_reload_process.stdout.close()
        sleep(15)  # Waiting 15 sec for process to restart
        unit_status_process = subprocess.Popen("systemctl status " + unit + " | grep Active: | awk '{print $2}'",
                                               shell=True, stdout=subprocess.PIPE)
        if unit_status_process.stdout.read().decode('UTF-8').strip() == "active":
            self.relaunch_status = True
        unit_status_process.stdout.close()
        return relaunch_message
