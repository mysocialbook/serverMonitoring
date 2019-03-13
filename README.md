# Status Watcher

**License**: GNU Affero v3

**Author**: David Lumaye

### Installation

1) Make sure you are using Python 3 and not Python 2

2) Install *pip* `sudo apt-get install python3-pip`

3) Install following packages via *pip*
    `psutil`, `slackclient`, `awscli`
    
4) Define `SLACK_API_TOKEN` as an environment variable

### Configuration

Configuration is set in `config.ini` file.
Following values are available

```
[LoadMonitoring]
; Send a notification if server status is OK
SendNotificationIfNoError = no
; Send a critical Slack error if remaining space is lower than 20GB or this value
; Any value above 20 will be ignored
MinimalDiskSpace = 10

[ServicesMonitoring]
; If a failed service is detected, it will be automatically relaunched
; otherwise, the alarm will be triggered but service will remain untouched
RelaunchJobs = no

[Slack]
; Default channel in which notification will be sent
DefaultChannel = devnotif
```
