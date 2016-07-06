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
    
    parser.add_argument('-ui', '--burpui_apiurl', dest='burpui_apiurl', nargs='?', default=False, const=False,
                        help='full url to burpui api, like http://user:pass@server:port/api/')
    
    parser.add_argument('--outdated', '-o', dest='outdated', nargs='?', const='print',
                        help='Report outdated or --outdated=file')

    options = parser.parse_args()

    return options


def main():
    """
    Main function
    """
    options = parse_args()

    if options.reports_conf:
        # Define the configuration file to use.
        config_file = options.reports_conf
        # Get a configuration options from config_file
        config_options = parse_config(config_file)

        # burpui_apiurl from config file
        if config_options.get('burpui_apiurl', False):
            burpui_apiurl = config_options.get('burpui_apiurl')

    # burpui_apiurl to defined on command line options
    if options.burpui_apiurl:
        burpui_apiurl = options.burpui_apiurl

    # If there is an option to for burpui_apiurl, get clients from that apiurl
    if burpui_apiurl:
        # Get clients stats from burpui_api_interface
        from .interfaces.burpui_api_interface import BUIClients
        bui_clients = BUIClients(burpui_apiurl=burpui_apiurl)
        clients_dict = bui_clients.translate_clients_stats()

    # Add some report option to use, use clients_dict already set





if __name__ == "__main__":
    main()