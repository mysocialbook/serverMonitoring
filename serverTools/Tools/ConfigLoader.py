import configparser
import os


class ConfigLoader:
    def __init__(self, config):
        self.config = configparser.ConfigParser()
        config_file = os.path.realpath(__file__) + '/../../config.ini'
        if config:
            config_file = config
        if not os.path.isfile(config):
            raise RuntimeError('«'+config_file+'» is not a valid config file.  Please use full path')
        self.config.read(config_file)

    def get_section(self, section):
        if section in self.config:
            return self.config[section]
        else:
            return []
