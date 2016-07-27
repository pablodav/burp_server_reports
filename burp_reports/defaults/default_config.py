import configparser


def set_defaults():
    """
    Generates the default configuration for all sections.

    :return:
    """

    config = configparser.ConfigParser()

    inventory_status = {
        'spare': ['spare'],
        'active': ['active'],
        'inactive_in_burp': 'wrong not active',
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
        'csv_delimiter': ';'
    }

    config['common'] = common
    config['inventory_columns'] = inventory_columns
    config['inventory_status'] = inventory_status

    return config