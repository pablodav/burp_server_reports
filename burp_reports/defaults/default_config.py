import configparser
import socket


def set_defaults():
    """
    Generates the default configuration for all sections.

    :return:
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

    config['common'] = common
    config['inventory_columns'] = inventory_columns
    config['inventory_status'] = inventory_status
    config['email_notification'] = email_notification

    return config
