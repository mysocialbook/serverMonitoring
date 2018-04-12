# coding=utf-8
"""
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
from slackclient import SlackClient
import os, socket, psutil, multiprocessing, shutil


class ServerStatus:
    """
        TOGGLES
    """
    relaunch_toggle = True  # If True, failed services will be automatically reloaded
    allow_ping = True  # Allow @canal ping in Slack messages
    send_notification_only_on_error = False  # Send a notification even if everything is OK
    send_status_info = True  # Send information about server (CPU, RAM and Load Average)

    # Internal variable.  DO NOT EDIT
    relaunch_status = False
    overall_status = True

    def __init__(self):
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
                error_msg = '@canal :bangbang: *System is unstable* but I don\'t detect any failed service.\n\n' \
                            'Current status is «' + status + '»'
            else:
                error_msg = '@david :bangbang: *Server is unstable* '+"\n"
                failed_process = subprocess.Popen("systemctl --failed | grep failed | awk '{print $2}'", shell=True,
                                                  stdout=subprocess.PIPE)
                failed_units = failed_process.stdout.read().decode('UTF-8').strip()
                failed_process.stdout.close()
                failed_units = failed_units.split('\n')
                error_msg += str(failing_units) + " failed services have been found.\n\n"
                error_msg += 'Following units are in «failed» state:\n'

                for unit in failed_units:
                    if self.relaunch_toggle:
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

            if self.send_status_info:
                error_msg += self.get_status_info()
            # Sending notification
            self.send_notification(error_msg)
        else:
            error_msg = '*Server ' +  socket.gethostname() + '* is running.'
            if self.send_status_info:
                error_msg += self.get_status_info()
            if not self.send_notification_only_on_error:
                self.send_notification(error_msg)


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

    def get_status_info(self):
        status_msg = "\n *Status* \n"
        status_msg += '*CPU* : ' + str(psutil.cpu_percent()) + "\n"
        memory = psutil.virtual_memory()
        status_msg += '*RAM* : ' + str(memory.used // (2**30)) + ' of ' + str(memory.total // (2**30)) + "\n"
        status_msg += '*Load* : ' + str(os.getloadavg()) + ' of max ' + str(multiprocessing.cpu_count()) + "\n"
        total, used, free = shutil.disk_usage('/')
        status_msg += '*Disk usage* : _Used_ : ' + str(used // (2**30)) + 'GB _Free_ : ' + str(free // (2**30)) + 'GB _Total_ : ' + str(total // (2**30)) + "GB\n"
        return status_msg

    def send_notification(self, message):
        slack_token = os.environ["SLACK_API_TOKEN"]
        slack = SlackClient(slack_token)

        print(slack.api_call("chat.postMessage", link_names=int(self.allow_ping), channel="#devnotif", text=message))


def main():
    ServerStatus()


if __name__ == "__main__":
    main()
