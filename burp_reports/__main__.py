# Help used to build it:
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
# https://docs.python.org/3/distributing/index.html#reading-the-guide

import sys
import os
from argparse import ArgumentParser
from . lib.configs import parse_config
from . reports.clients_reports import BurpReports


def parse_args():
    """
    Information extracted from: https://mkaz.com/2014/07/26/python-argparse-cookbook/
    :return:
    """
    parser = ArgumentParser()
    parser.add_argument('-c', '--reports_conf', dest='reports_conf',
                        const=os.path.join(os.sep, 'etc', 'burp', 'burp-reports.conf'),
                        default=None,
                        nargs='?', help='burp-reports.conf configuration file')
    
    parser.add_argument('-ui', '--burpui_apiurl', dest='burpui_apiurl', nargs='?', default=None, const=None,
                        help='full url to burpui api, like http://user:pass@server:port/api/ ')
    
    # Adding report choices with subcommand
    parser.add_argument('--report', '-r', dest='report', nargs='?', const='print', default='print',
                        choices=['print', 'outdated'],
                        help='Report choice, options: \n\n'
                             'print: Print txt clients list only \n'
                             'outdated: will print list of outdated clients')

    parser.add_argument('--debug', dest='debug', nargs='?', default=None, const=True,
                        help='Activate for debugging purposes')

    parser.add_argument('--detail', dest='detail', nargs='?', default=None, const=True,
                        help='Adds more details to reports')
    
    # Print help if no arguments where parsed
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()
    return options


def bui_api_clients_stats(burpui_apiurl, debug=None):
    """

    :param burpui_apiurl: string to burpui_apiurl, full url http://user:pass@server:port/api/
    :param debug: To activate debug on script
    :return: dict with clients stats
    """
    from .interfaces.burpui_api_interface import BUIClients
    bui_clients = BUIClients(burpui_apiurl=burpui_apiurl,
                             debug=debug)
    clients_dict = bui_clients.translate_clients_stats()

    if debug:
        from pprint import pprint
        print('List of clients got:')
        pprint(clients_dict)

    return clients_dict


def bui_dummy_clients_stats():
    # Get data from dummy module (for testing the functions only)
    from .dummy.burpui_api_translate_dummy import BUIClients
    clients_dict = BUIClients()
    clients_dict = clients_dict.translate_clients_stats()
    return clients_dict


def get_burpui_apiurl(options):
    """

    :param options: options from argparse
    :return: burpui_apiurl from conf or cmdline args.
    """
    burpui_apiurl = None

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

    return burpui_apiurl


def get_main_conf(options):
    """

    :param options: options from argparse
    :return: dict with options from config file or defaults
    """
    _options = {}
    config_options = {}

    if options.reports_conf:
        config_options = parse_config(options.reports_conf)

    # Creating default values for our config:
    _options.setdefault('days_outdated', int(config_options.get('days_outdated', 30)))

    return _options


def main():
    """
    Main function
    """
    clients_dict = {}
    options = parse_args()
    config_options = get_main_conf(options)

    debug = options.debug

    burpui_apiurl = get_burpui_apiurl(options)

    # If there is an option to for burpui_apiurl, get clients from that apiurl
    if burpui_apiurl:
        if burpui_apiurl.lower() == 'dummy':
            clients_dict = bui_dummy_clients_stats()
        else:
            # Get clients stats from burpui_api_interface
            clients_dict = bui_api_clients_stats(burpui_apiurl, debug)

    burp_reports = BurpReports(clients_dict,
                               days_outdated=config_options.get('days_outdated'),
                               detail=options.detail)

    # Add some report option to use, use clients_dict already set
    if options.report == 'print':
        burp_reports.print_basic_txt()

    elif options.report in ['outdated', 'o']:
        burp_reports.report_outdated(export_txt=True)



if __name__ == "__main__":
    main()
