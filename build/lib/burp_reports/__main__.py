# Help used to build it:
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
# https://docs.python.org/3/distributing/index.html#reading-the-guide

import sys
import os
import argparse
from burp_reports.lib.configs import parse_config2
from burp_reports.lib.configs import get_all_config
from burp_reports.reports.clients_reports import BurpReports
from collections import defaultdict


def parse_args():
    """
    Information extracted from: https://mkaz.com/2014/07/26/python-argparse-cookbook/
    :return:
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--reports_conf', dest='reports_conf',
                        const=os.path.join(os.sep, 'etc', 'burp', 'burp-reports.conf'),
                        default=None,
                        nargs='?', help='burp-reports.conf configuration file')

    parser.add_argument('-ui', '--burpui_apiurl', dest='burpui_apiurl', nargs='?', default=None, const=None,
                        help='full url to burpui api, like http://user:pass@server:port/api/ ')

    # Adding report choices

    choices_helper = {"print": "Print txt clients list only \n",
                      "outdated": "will print list of outdated clients ",
                      "inventory":
                          'requires -i and -o, check input inventory and generates a comparison\n'
                          '    Input csv headers required: device name; status; Status (detailed) \n'
                          '       Example line:            demo1; active; \n'
                          '                                demo2; active; spare \n',
                      "email_outdated": "Will send email to configured recipients on config file"}

    parser.add_argument("--report", '-r', dest='report', nargs='?', default='print', const='print',
                        choices=choices_helper,
                        help='\n'.join("{}: {}".format(key, value) for key, value in sorted(choices_helper.items())))

    parser.add_argument('--debug', dest='debug', nargs='?', default=None, const=True,
                        help='Activate for debugging purposes')

    parser.add_argument('--detail', dest='detail', nargs='?', default=None, const=True,
                        help='Adds more details to reports')

    parser.add_argument('--ping', dest='ping', nargs='?', default=None, const=True,
                        help='Adds ping check to outdated report only')

    parser.add_argument('--write_config', dest='write_config', default=None, action='store_true',
                        help="Write configuration with default values, useful to get a config file to modify")

    parser.add_argument('-i', nargs='?', default=None, help='Input csv file to use on --report inventory')
    parser.add_argument('-o', nargs='?', default=None, help='Output csv file to use on --report inventory')

    # Print help if no arguments where parsed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()
    return options


def bui_api_clients_stats(burpui_apiurl, debug=None, detail=None):
    """

    :param burpui_apiurl: string to burpui_apiurl, full url http://user:pass@server:port/api/
    :param debug: To activate debug on script
    :param detail: Adds more detailed info, backup_report nested dict with some info like: duration, received, totsize.
    :return: dict with clients stats
    """
    from .interfaces.burpui_api_interface import BUIClients
    bui_clients = BUIClients(burpui_apiurl=burpui_apiurl,
                             debug=debug)

    clients_dict = bui_clients.translate_clients_stats(detail=detail)

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


def get_main_conf(options):
    """

    :param options: options from argparser
    :return: dict with options from config file or defaults
    """
    _options = defaultdict(dict)

    config_options = parse_config2(options.reports_conf)

    # Use general section for general options:
    if config_options.has_section('common'):
        general_config = config_options['common']
    else:
        general_config = {}

    # Creating default values for our config:
    _options['burpui_apiurl'] = general_config.get('burpui_apiurl', None)

    # burpui_apiurl to defined on command line options
    # Override the burpui_apiurl defined before
    if options.burpui_apiurl:
        _options['burpui_apiurl'] = options.burpui_apiurl

    return _options


def main():
    """
    Main function
    """
    clients_dict = {}
    options = parse_args()

    # Configs that can be overwritten by command line options
    config_options = get_main_conf(options)
    debug = options.debug
    burpui_apiurl = config_options.get('burpui_apiurl')

    # Config with defaults settings if no file will be passed
    # Also with defaults sections and defaults keys for missing options in config
    all_config = get_all_config(options.reports_conf)

    if options.write_config:
        if not options.reports_conf:
            raise SystemExit('--write_config requires -c configfile.conf')

        with open(options.reports_conf, 'w', encoding='utf-8') as f:
            all_config.write(f, space_around_delimiters=True)

    days_outdated = all_config.getint('common', 'days_outdated')

    # If there is an option to for burpui_apiurl, get clients from that apiurl
    if burpui_apiurl:
        if burpui_apiurl.lower() == 'dummy':
            clients_dict = bui_dummy_clients_stats()
        else:
            # Get clients stats from burpui_api_interface
            clients_dict = bui_api_clients_stats(burpui_apiurl,
                                                 debug,
                                                 detail=options.detail)
    else:
        raise SystemExit('burpui_apiurl is required in cmd or in config common section')

    # Generate burp_reports object to use for reports.
    burp_reports = BurpReports(clients_dict,
                               days_outdated=days_outdated,
                               detail=options.detail,
                               config=all_config)

    # Add some report option to use, use clients_dict already set
    if options.report == 'print':
        burp_reports.print_basic_txt()

    elif options.report in ['outdated', 'o']:
        burp_reports.report_outdated(export_txt=True,
                                     ping=options.ping)

    elif options.report == 'inventory':
        burp_reports.save_compared_inventory(options.i,
                                             options.o)

    elif options.report == 'email_outdated':
        burp_reports.email_outdated()


if __name__ == "__main__":
    main()
