from Monitoring import LoadMonitoring, ServicesMonitoring
from Tools import ConfigLoader
from Notifications import NotificationManager

import cli.app


@cli.app.CommandLineApp
def monitor(app):
    config = ConfigLoader.ConfigLoader(app.params.config)
    notifier = NotificationManager.NotificationManager(config)
    LoadMonitoring.LoadMonitoring(config.get_section('LoadMonitoring'), notifier)
    ServicesMonitoring.ServicesMonitoring(config.get_section('ServicesMonitoring'), notifier)


monitor.add_param('-c', '--config', help="Config file", default=False)

if __name__ == "__main__":
    monitor.run()
