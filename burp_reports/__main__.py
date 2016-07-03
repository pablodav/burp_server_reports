# Help used to build it:
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
# https://docs.python.org/3/distributing/index.html#reading-the-guide

import sys
import os
from argparse import ArgumentParser
from .lib.configs import parse_config

def parse_args():
    """
    Information extracted from: https://mkaz.com/2014/07/26/python-argparse-cookbook/
    :return:
    """
    compare_result = []
    parser = ArgumentParser()
    parser.add_argument('-c', '--reports_conf', dest='reports_conf',
                        const=os.path.join(os.sep, 'etc', 'burp', 'burp-reports.conf'),
                        default=os.path.join(os.sep, 'etc', 'burp', 'burp-reports.conf'),
                        nargs='?', help='burp-reports.conf configuration file')
    parser.add_argument('--outdated', '-o', dest='outdated', nargs='?', const='print',
                        help='Report outdated or --outdated=file')

    options = parser.parse_args()

    return options


def main():
    """
    Main function
    """
    options = parse_args()

    # Define the configuration file to use.
    config_file = options.reports_conf

    # Get a configuration options from config_file
    try:
        config_options = parse_config(config_file)
    except:
        raise Exception("NoConfigFile: Try to define a config file for burp_api.conf")

    # If there is an option to for burpui_apiurl, get clients from that apiurl
    if config_options.get('burpui_apiurl'):
        from .interfaces.burpui_api_interface import BUIClients
        bui_clients = BUIClients()
        clients_dict = bui_clients.translate_clients()





if __name__ == "__main__":
    main()