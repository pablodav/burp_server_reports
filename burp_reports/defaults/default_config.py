"""
Generates the default configuration for all sections.
"""
import configparser
import socket


def set_defaults():
    """
    Generates the default configuration for all sections.

    :return: configparser.ConfigParser object
    """

    config = configparser.ConfigParser(allow_no_value=True)

    inventory_status = {
        'spare': 'spare',
        'active': 'active',
        'inactive_in_burp': 'wrong not active',
        'inactive_not_in_burp': 'ignored inactive',
        'spare_in_burp': 'wrong spare in burp',
        'not_inventory_in_burp': 'not in inventory',
        'in_inventory_updated': 'ok',
        'spare_not_in_burp': 'ignored spare',
        'in_inventory_not_in_burp': 'absent',
        'in_many_servers': 'duplicated'
    }

    # Set dict of columns
    inventory_columns = {
        'client_name': 'device name',
        'status': 'status',
        'server': 'server',
        'sub_status': 'status (detailed)'
    }

    common = {
        'days_outdated': '31',
        'csv_delimiter': ';',
        # Options: https://docs.python.org/3.5/library/codecs.html#text-encodings
        # use mbcs for ansi on python prior 3.6
        'csv_encoding': 'utf-8',
        'excluded_clients': 'monitor,agent'
    }

    email_notification = {
        'email_to': 'root@localhost',
        'email_from': '{}@domain.com'.format(socket.gethostname()),
        'smtp_server': 'localhost',
        'smtp_port': '25',
        'smtp_login': '',
        'smtp_password': '',
        'smtp_mode': 'normal',
        'subject': 'burp report from {}'.format(socket.gethostname()),
        'foot_notes': 'A sample notes'
    }

    format_text = {
        'name_length': '15',
        'all_column_length': '11'
    }

    email_inventory = {
        'imap_host': 'localhost',
        'imap_password': 'password',
        'imap_user': 'username', # You can use 'domain\\user'
        'imap_folder': 'INBOX',
        'email_subject': 'inventory',
        'imap_search': 'TODAY', # TODAY will set today date in
        # format: "SENTON 23-Sep-2017 Subject \"inventory\"" (subject comes from email_subject key)
        # you could filter using the IMAP rules here (check
        # http://www.example-code.com/csharp/imap-search-critera.asp)
        'imap_port': '993',
        'attachment_save_directory': '/tmp',
        'attachment_filename': 'inventory.csv'
    }

    config['common'] = common
    config['inventory_columns'] = inventory_columns
    config['inventory_status'] = inventory_status
    config['email_notification'] = email_notification
    config['format_text'] = format_text
    config['email_inventory'] = email_inventory

    return config
