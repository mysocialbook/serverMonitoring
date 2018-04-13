import configparser


class ConfigLoader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini')

    def get_section(self, section):
        if section in self.config:
            return self.config[section]
        else:
            return []
