from Monitoring import LoadMonitoring, ServicesMonitoring
from Tools import ConfigLoader

import cli.app

@cli.app.CommandLineApp
def monitor(app):
    config = ConfigLoader.ConfigLoader()
    LoadMonitoring.LoadMonitoring(config.get_section('LoadMonitoring'))
    ServicesMonitoring.ServicesMonitoring(config.get_section('ServicesMonitoring'))


if __name__ == "__main__":
    monitor.run()
