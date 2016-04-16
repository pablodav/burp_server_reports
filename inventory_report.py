#!/usr/bin/python3

def inventory_of_servers(result_csv=None , servers=None ):
    """

    :param result_csv: csv output with compared inventory of each server
    :param servers: python list with servers list
    :return:
    """

    from inv_automation.parse_csv import get_csv_from_url
    from inv_automation.parse_csv import csv_as_dict
    from inv_automation.parse_csv import save_csv_data


    import os
    import sys


    if not servers:
        servers = ['10.196.77.19', '10.100.66.83', '10.196.78.17', '10.100.66.84']

    if not result_csv:
        result_csv = 'test.csv'
    debug = False
    all_clients = {}
    for v in range(len(servers)):
        server = servers[v]
        url = 'http://' + server + '/inventory_status.csv'
        if sys.platform.startswith('win'):
            temp_folder = 'temp'
        elif sys.platform.startswith('linux'):
            temp_folder = 'tmp'

        output_file = os.path.join(os.sep, temp_folder, server + '_inventory_status.csv')

        if os.path.isfile(output_file):
            os.remove(output_file)

        get_from_url = get_csv_from_url(csv_url=url, csv_output=output_file, delimiter=';')
        if not get_from_url:
            print("Not found in: {}".format(url))
            continue

        clients_status = csv_as_dict(output_file, ref_header='client', delimiter=';')

        # For each client in the dictionary

        for k in sorted(clients_status):
            client = k
            client_status = clients_status[client].get('status', '')
            client_server = clients_status[client].get('serverinv_status')

            # Check if exist from other server, if not add to all_clients
            if client not in all_clients:
                all_clients.setdefault(client, clients_status[client])
                # Example: {'client': {'serverinv_status': 'server', 'status': 'absent', None: [' ', 'Online',...
            else:
                # status:
                status_compared_inventory = ['spare in burp', 'wrong not active', 'ignored spare']
                # absent,
                status_in_burp = ['outdated', 'new', 'UNKNOWN', 'ok']

                status_in_all_clients = all_clients[client].get('status')

                if debug:  # Only for debug purposes
                    print('client: {}, server: {}, status: {}, {} '.format(
                        client, client_server, client_status, status_in_all_clients
                    ))

                if client_status in status_in_burp and client_status not in status_compared_inventory:

                    if status_in_all_clients in status_in_burp:
                        server_in_all_clients = all_clients[client].get('serverinv_status')

                        if debug:  # Only for debug purposes
                            print('duplicated client: {}, server: {}, status: {}, {} '.format(
                                client, client_server, client_status, status_in_all_clients
                            ))

                        # if not absent or ignored but is also on other server, is duplicated
                        servers_duplicated = client_server + ' ' + server_in_all_clients
                        all_clients.setdefault(client, {})['serverinv_status'] = servers_duplicated
                        all_clients.setdefault(client, {})['status'] = 'duplicated'
                        status_in_all_clients = all_clients[client].get('status')

                    else:

                        all_clients[client].update(clients_status[client])
                        status_in_all_clients = all_clients[client].get('status')

                if debug:  # Only for debug purposes
                    print('client: {}, server: {}, status: {}, {} '.format(
                        client, client_server, client_status, status_in_all_clients
                    ))

    # fields = ['client', 'status', 'serverinv_status', 'sub_status', None]

    first_client = next (iter (all_clients.keys()))  # Gets first key of dict
    headers = list(all_clients[first_client].keys())  # Get headers from input dict
    headers.insert(0, 'client')  # First header column as client
    headers.insert(1, 'status')  # Second header column as status
    headers.insert(2, 'serverinv_status')  # Third header column as server
    headers.insert(3, 'status (detailed)')  # Fourth header column as status detailed (Status (detailed))
    # Prepare the header list to return:

    lista1 = []
    lista1.append(headers)

    for k in sorted(all_clients):
        k_status = all_clients[k].get('status')
        k_serverinv_status = all_clients[k].get('serverinv_status')
        k_sub_status = all_clients[k].get('status (detailed)')

        row = [k, k_status, k_serverinv_status, k_sub_status]  # Adds client at the first column, plus fixed columns

        # Previously: others = all_clients[k].get(None)
        for i in range(4, len(headers)):  # Start from fourth column in headers
            row.append(all_clients[k].get(headers[i]))  # Insert each value of client to the row

        if debug:  # DEBUG LINE
            print('row to append: {}'.format(row))

        if 'duplicated' in row[1]:
            print(row[0:3])

        lista1.append(row)
    save_csv_data(lista1, csv_delimiter=";", csv_filename=result_csv)


def get_config_file(config_file):
    import configparser
    # Help from: https://docs.python.org/3.4/library/configparser.html
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_file)
    return config


def parser_commandline():
    """
    Information extracted from: https://mkaz.com/2014/07/26/python-argparse-cookbook/
    :return:
    """
    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('--reports_conf', const=os.path.join(os.sep, 'etc', 'burp', 'burp-reports.conf'),
                        default=os.path.join(os.sep, 'etc', 'burp', 'burp-reports.conf'),
                        nargs='?', help='burp-reports.conf file')
    # Always set reports config with or without --reports_conf
    parser.add_argument('--inv_central', default=None, action='store_true')

    args = parser.parse_args()


    if args.inv_central:
        reports_config = get_config_file(args.reports_conf)
        burp_servers = reports_config['default']['burp_servers'].split()
        burp_www_reports = reports_config['default']['burp_www_reports']
        csv_export = os.path.join(burp_www_reports, 'inventory_central.csv')
        inventory_of_servers(result_csv=csv_export, servers=burp_servers)



if __name__ == "__main__":
    parser_commandline()


