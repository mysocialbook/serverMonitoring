from Monitoring import LoadMonitoring, ServicesMonitoring
from Tools import ConfigLoader


def main():
    config = ConfigLoader.ConfigLoader()
    LoadMonitoring.LoadMonitoring(config.get_section('LoadMonitoring'))
    ServicesMonitoring.ServicesMonitoring(config.get_section['ServicesMonitoring'])


if __name__ == "__main__":
    main()
