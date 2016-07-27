import configparser


def set_defaults():
    """
    Generates the default configuration for all sections.

    :return:
    """

    config = configparser.ConfigParser(default_section='general')

    all_status = {
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
    all_columns = {
        'client_name': 'device name',
        'status': 'status',
        'server': 'server',
        'sub_status': 'status (detailed)'
    }

    common = {
        'days_outdated': '31'
    }

    config['common'] = common
    config['inventory_columns'] = all_columns
    config['inventory_status'] = all_status

    return config