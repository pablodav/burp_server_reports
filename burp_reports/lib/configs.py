#! python3
import configparser
from ..defaults.default_config import set_defaults
import os


def parse_config2(filename=None):
    """
    https://docs.python.org/3.5/library/configparser.html

    :param filename: filename to parse config
    :return: config_parse result
    """

    config = configparser.ConfigParser(allow_no_value=True)

    if filename:
        # ConfigParser does not create a file if it doesn't exist, so I will create an empty one.
        if not os.path.isfile(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                print('', file=f)

        config.read_file(open(filename))

    return config


def get_all_config(filename=None):
    """
    Set default configuration for burp_reports
    Config with defaults settings if no file will be passed
    Also with defaults sections and defaults keys for missing options in config

    :param filename: options config file to read
    :return: config with default config for missing sections
    """

    config = parse_config2(filename)
    default_config = set_defaults()

    # Verify each section in default_config
    for s in range(len(default_config.sections())):
        section = default_config.sections()[s]

        # Add the missing section to the config obtained
        if not config.has_section(section):
            config.add_section(section)

        # Add missing keys to config obtained
        for key in default_config[section]:
            if not config.has_option(section, key):
                config[section][key] = default_config[section][key]

    return config
