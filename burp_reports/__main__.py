# Help used to build it:
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
# https://docs.python.org/3/distributing/index.html#reading-the-guide

import sys
import os
from argparse import ArgumentParser
from .lib.configs import parse_config
from . reports.clients_reports import BurpReports


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
    
    parser.add_argument('--report', '-r', dest='report', nargs='?', const='print', default='print',
                        help='Report choice, options: '
                             'print: Print txt clients list only')

    parser.add_argument('--debug', dest='debug', nargs='?', default=None, const=True,
                        help='Activate for debugging purposes')

    options = parser.parse_args()

    return options


def bui_api_clients_stats(burpui_apiurl, debug=None):
    """

    :param burpui_apiurl: string to burpui_apiurl, full url http://user:pass@server:port/api/
    :return: dict with clients stats
    """
    from .interfaces.burpui_api_interface import BUIClients
    bui_clients = BUIClients(burpui_apiurl=burpui_apiurl)
    clients_dict = bui_clients.translate_clients_stats()

    if debug:
        from pprint import pprint
        print('List of clients got:')
        pprint(clients_dict)

    return clients_dict


def main():
    """
    Main function
    """
    options = parse_args()

    debug = options.debug

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
        clients_dict = bui_api_clients_stats(burpui_apiurl, debug)
        burp_reports = BurpReports(clients_dict)

    # Add some report option to use, use clients_dict already set
    if options.report == 'print':
        burp_reports.print_basic_txt()







if __name__ == "__main__":
    main()