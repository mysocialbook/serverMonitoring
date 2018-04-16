import configparser
import os


class ConfigLoader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.dirname(os.path.realpath(__file__)) + '/../../config.ini')

    def get_section(self, section):
        if section in self.config:
            return self.config[section]
        else:
            return []
