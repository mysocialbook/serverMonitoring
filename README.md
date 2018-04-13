# Status Watcher

**License**: GNU Affero v3

**Author**: David Lumaye

### Installation

1) Make sure you are using Python 3 and not Python 2

2) Install *pip* `sudo apt-get install python3-pip`

3) Install following packages via *pip*
    `psutil`, `slackclient`
    
4) Define `SLACK_API_TOKEN` as an environment variable

### Configuration

Configuration is set in `config.ini` file.
Following values are available

```
[LoadMonitoring]
; Send a notification if server status is OK
SendNotificationIfNoError = no

[ServicesMonitoring]
; If a failed service is detected, it will be automatically relaunched
; otherwise, the alarm will be triggered but service will remain untouched
RelaunchJobs = no

[Slack]
; Default channel in which notification will be sent
DefaultChannel = devnotif
```
