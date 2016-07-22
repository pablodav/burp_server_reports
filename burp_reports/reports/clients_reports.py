from ..lib.txt import TxtReports
import arrow
from collections import defaultdict
from ..lib.is_up import is_up
from invpy_libs import csv_as_dict


class BurpReports:

    def __init__(self, clients_dict, days_outdated=31, detail=None):
        """

        :param clients_dict: list of clients in burp_reports format, example:
        {'client_name':
            { 'b_last'    : 'YYYY-MM-DD HH:mm:ssZZ',
              'b_state'    : 'working/current',
              'b_phase' : 'phase1/phase2',
              'b_last' : 'date',
            }
        }
        :param days_outdated: number to consider days outdated
        :param detail: Used to print more details or not

        """

        self.clients = clients_dict
        self.days_outdated = days_outdated
        self.detail = detail

    def print_basic_txt(self):
        clients_reports = TxtReports(self.clients,
                                     detail=self.detail)
        clients_reports.report_to_txt()

    def report_outdated(self, export_txt=None, ping=None):
        """

        :param export_txt: use it if you want to print on screen, used with cli
        :param ping: Tries to ping the host to check it's availability
        :return: dict of outdated clients.
        """

        # Create a list of additional columns to add to the report
        columns = {'Status': 'b_status'}

        outdated_clients = self._get_outdated()

        if ping:
            # Check ping on each outdated client
            for k in outdated_clients.keys():
                if is_up(k):
                    comments = 'ping ok'
                else:
                    comments = ' - '
                # Append ping information to outdated_clients
                outdated_clients[k]['comments'] = comments
                # Add the column comments to report
                columns['Comments'] = 'comments'

        # Create the object to export the report
        clients_reports = TxtReports(outdated_clients,
                                     additional_columns=columns,
                                     detail=self.detail)

        if export_txt:
            clients_reports.report_to_txt()

        return outdated_clients

    def _get_outdated(self):
        """

        :return: only outdated clients with b_status: outdated/never
        """

        outdated_clients = defaultdict(dict)

        for k, v in self.clients.items():
            # Get actual time with arrow module
            # k is client name
            # v is the dict with all data
            actual_time = arrow.get()
            # get date to consider as outdated
            outdated_time = actual_time.replace(days=-self.days_outdated)
            client_last = v.get('b_last', None)

            # Add client to outdated list if not backup
            if client_last.lower() in 'never' or not client_last:
                outdated_clients[k] = v
                outdated_clients[k]['b_status'] = 'never'
                # Go to next client
                continue

            # Convert client_last to arrow date
            client_last = arrow.get(v.get('b_last', None), 'YYYY-MM-DD HH:mm:ssZZ')

            # Ensure client_last is not string now
            if not isinstance(client_last, str):
                # Add client to outdated list if outdated
                if client_last < outdated_time:
                    outdated_clients[k] = v
                    outdated_clients[k]['b_status'] = 'outdated'

        return outdated_clients

    def compare_inventory(self, csv_inventory, client_column='device name', separator=';'):
        """

        :param csv_inventory: Input filename to compare from
        :param client_column: reference column to use in csv
        :param separator: csv separator, like ;
        :return: list csv_rows_inventory_status (status of each client) in nested list one row per client
        """

        # Get inventory from CSV file
        inventory = csv_as_dict(csv_inventory, client_column, separator)
        outdated_clients = self._get_outdated()

        # Set a list of status:
        spare_status = ['spare']
        active_status = ['active']

        csv_rows_inventory_status = []

        first_client = next(iter(inventory.keys()))  # Gets first key of dict
        headers = list(inventory[first_client].keys())  # Get headers from input dict
        headers.insert(0, 'client')  # Change First header column as client
        headers.insert(1, 'status')  # Change Second header column as status
        headers.insert(2, 'serverinv_status')  # Change Third header column as server
        headers.insert(3, 'status (detailed)')  # Change Fourth header column as status detailed
        # Prepare the header list to return:
        csv_rows_inventory_status.append(headers)  # First row as headers

        # Verify inventory and compare with clients in burp
        for k in sorted(inventory):
            client = k
            status = inventory[client].get('status', '')
            det_status = inventory[client].get('status (detailed)')

            if client in self.clients:

                if det_status.lower() in spare_status:
                    burp_status = 'wrong spare in burp'

                elif status.lower() not in active_status:
                    burp_status = 'wrong not active'

                else:
                    burp_status = 'ok'
                    # Set never/outdated if the client is outdated
                    if client in outdated_clients:
                        burp_status = outdated_clients[client]['b_status']

            # Define the status as ignored for clients spare
            elif det_status.lower() in spare_status:
                burp_status = 'ignored spare'

            else:
                burp_status = 'absent'

            # Generate list row with client's status and other data
            row = [client, burp_status, server_name, det_status]

            for i in range(4, len(headers)):  # Start from fourth column in headers
                row.append(inventory[client].get(headers[i]))  # Insert each value of client to the row

            csv_rows_inventory_status.append(row)

        return csv_rows_inventory_status



