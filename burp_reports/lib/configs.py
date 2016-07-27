import configparser
from ..defaults.default_config import set_defaults


def parse_config(filename, stats=None):
    """

    :param filename: file name to parse config
    :param stats: only use it to stats file with separator :
    :return: dict with options
    """
    options = {}
    comment_char = '#'
    option_char = '='
    stats_char = ':'
    f = open(filename)
    for line in f:
        # First, remove comments:
        if comment_char in line:
            # split on comment char, keep only the part before
            line, comment = line.split(comment_char, 1)
        # Second, find lines with an option=value:
        if option_char in line and not stats:
            # split on option char:
            option, value = line.split(option_char, 1)
        elif stats_char in line and stats:
            option, value = line.split(stats_char, 1)
        else:
            continue
        if option and value:
            # strip spaces:
            option = option.strip()
            value = value.strip()
            # store in dictionary:
            options[option] = value
    f.close()
    return options


def parse_config2(filename=None):
    """
    https://docs.python.org/3.5/library/configparser.html

    :param filename: filename to parse config
    :return: config_parse result
    """

    config = configparser.ConfigParser(default_section='common')

    if filename:
        config.read_file(open(filename))

    return config


def get_all_config(filename):
    """
    Set default configuration for burp_reports

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
            if not key in config[section]:
                config[section][key] = default_config[section][key]

    return config