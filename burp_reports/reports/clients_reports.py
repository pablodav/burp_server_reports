from ..lib.txt import TxtReports
import arrow
from collections import defaultdict
from ..lib.is_up import outdated_pings
from invpy_libs import csv_as_dict, save_csv_data, get_csv_from_url
from ..lib.email import EmailNotifications
import validators
from ..lib.files import temp_file


class BurpReports:
    def __init__(self, clients_dict, days_outdated=31, detail=None, config=None):
        """

        :param clients_dict: list of clients in burp_reports format, example:
        {'client_name':
            { 'b_last'    : 'YYYY-MM-DDTHH:mm:ssZZ',
              'b_state'    : 'working/current',
              'b_phase' : 'phase1/phase2',
              'b_last' : 'date',
            }
        }
        :param days_outdated (int): number to consider days outdated
        :param detail (True/None): Used to print more details or not
        :param config (configparser): configparser formatted config, required sections:
                            inventory_status, inventory_columns, common

        """

        self.clients = clients_dict
        self.days_outdated = days_outdated
        self.detail = detail
        self.config = config

        self.tempfile = temp_file('burp_reports_temp.csv')

        if config:
            # Set dict for from common section
            self.common_config = dict(self.config['common'])
        else:
            self.common_config = {
                'csv_delimiter': ';'
            }

        self.excluded_clients = self.common_config.get('excluded_clients', '').split(',')

    def print_basic_txt(self):
        clients_reports = TxtReports(self.clients,
                                     detail=self.detail)
        clients_reports.report_to_txt()

    def _get_outdated(self):
        """

        :return: only outdated clients with b_status: outdated/never
        """

        outdated_clients = defaultdict(dict)

        for k, v in self.clients.items():
            # Get actual time with arrow module
            # k is client name
            # v is the dict with all data

            # Do not verify excluded clients
            if k in self.excluded_clients:
                continue

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
            client_last = arrow.get(v.get('b_last', None))

            # Ensure client_last is not string now
            if not isinstance(client_last, str):
                # Add client to outdated list if outdated
                if client_last < outdated_time:
                    outdated_clients[k] = v
                    outdated_clients[k]['b_status'] = 'outdated'

        return outdated_clients

    def compare_inventory(self, csv_inventory):
        """

        :param csv_inventory: Input filename to compare from (also can be an url to download it)
        :return: list csv_rows_inventory_status (status of each client) in nested list one row per client
        """

        # Set dict of status from config
        all_status = dict(self.config['inventory_status'])

        # Set variables of status as lists, also enable possibility to have more than one status:
        spare_status = all_status['spare'].split(',')
        active_status = all_status['active'].split(',')

        # Set dict of status from config
        all_columns = dict(self.config['inventory_columns'])

        client_column = all_columns['client_name']
        delimiter = self.common_config['csv_delimiter']

        # Download the csv if it is in a url
        if validators.url(csv_inventory):
            get_csv_from_url(csv_inventory, csv_output=self.tempfile, delimiter=delimiter)
            csv_inventory = self.tempfile

        # Get inventory from CSV file
        inventory = csv_as_dict(csv_inventory, client_column, delimiter=delimiter)
        # Get a list of clients outdated in burp:
        outdated_clients = self._get_outdated()

        csv_rows_inventory_status = []
        headers = []

        headers.insert(0, client_column)  # Change First header column as client
        headers.insert(1, all_columns['status'])  # Change Second header column as status
        headers.insert(2, all_columns['server'])  # Change Third header column as server
        headers.insert(3, all_columns['sub_status'])  # Change Fourth header column as status detailed

        first_client = next(iter(inventory.keys()))  # Gets first key of dict

        for column in sorted(inventory[first_client].keys()):  # Get headers from input inventory sorted
            if column.lower() not in all_columns.values():  # Add to the list only if not in the all_columns defined
                headers.append(column)

        # Prepare the header list to return:
        csv_rows_inventory_status.append(headers)  # First row as headers

        # Verify inventory and compare with clients in burp
        for k in sorted(inventory):
            client = k
            server_name = ''

            # Do not check excluded clients
            if client in self.excluded_clients:
                continue

            # Columns required to verify the status, lowercase and without spaces at end and beginning
            status = inventory[client].get(all_columns['status'], '').lower().strip()
            sub_status = inventory[client].get(all_columns['sub_status'], '').lower().strip()

            # If the client is in burp servers
            if client in self.clients:

                if sub_status in spare_status:
                    burp_status = all_status['spare_in_burp']

                elif status not in active_status:
                    burp_status = all_status['inactive_in_burp']

                else:
                    burp_status = all_status['in_inventory_updated']
                    # Set never/outdated if the client is outdated
                    if client in outdated_clients:
                        burp_status = outdated_clients[client]['b_status']

            # If the client is not in burp servers: ---
            # Define the status as ignored for clients spare
            elif sub_status in spare_status:
                burp_status = all_status['spare_not_in_burp']

            # Define ignored to client not active:
            elif status not in active_status:
                burp_status = all_status['inactive_not_in_burp']

            else:
                # Define absent in burp
                burp_status = all_status['in_inventory_not_in_burp']

            # Add server_name information
            if self.clients[client].get('server', None):
                server_name = self.clients[client]['server']
                # Mark the status of the client as duplicated if there is more than one server on it.
                if len(server_name) > 1:
                    burp_status = all_status['in_many_servers']

            # Generate list row with client's status and other data
            row = [client, burp_status, server_name, sub_status]

            # Add all other columns, starting from fourth column in headers
            for i in range(4, len(headers)):
                row.append(inventory[client].get(headers[i]))  # Insert each value of client to the row

            csv_rows_inventory_status.append(row)

        # Check if there is some client in burp but not in the inventory
        for burp_client in sorted(self.clients):
            # Do not check excluded clients
            if burp_client in self.excluded_clients:
                continue

            if burp_client not in inventory:
                burp_status = all_status['not_inventory_in_burp']
                if self.clients[burp_client].get('server', None):
                    server_name = self.clients[burp_client]['server']
                else:
                    server_name = []
                sub_status = ''
                # Generate list row with client's status and other data
                row = [burp_client, burp_status, server_name, sub_status]

                csv_rows_inventory_status.append(row)

        return csv_rows_inventory_status

    def save_compared_inventory(self, input_file, output_file):
        """

        :param input_file: csv inventory input
        :param output_file: csv filename output
        :return:
        """
        delimiter = self.common_config['csv_delimiter']

        rows_inventory_compared = self.compare_inventory(input_file)
        save_csv_data(rows_inventory_compared, output_file, csv_delimiter=delimiter)

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
            outdated_clients = outdated_pings(outdated_clients)
            # Add the column comments to report
            columns['Comments'] = 'comments'

        # Create the object to export the report
        clients_reports = TxtReports(outdated_clients,
                                     additional_columns=columns,
                                     detail=self.detail)

        if export_txt:
            clients_reports.report_to_txt()

        return outdated_clients

    def email_outdated(self):
        """
        Sends email based on its configuration file
        :return:
        """

        email = self._compose_email(report='outdated')
        return email.send_email()

    def _compose_email(self, report):
        """
        Composes emails

        :param report: (str): outdated to get a list of outdated clients
        :return: EmailNotifications class object
        """
        if self.config:
            if self.config.has_section('email_notification'):
                email_config = dict(self.config['email_notification'])
        else:
            raise SystemExit('email_notification section is required in config')

        if report == 'outdated':
            clients = self._get_outdated()

        else:
            clients = self.clients

        clients_reports = TxtReports(clients,
                                     detail=self.detail,
                                     foot_notes=email_config.get('foot_notes', ''))

        body_str = clients_reports.report_to_txt(print_text=None)

        email = EmailNotifications(email_config, body_str)

        return email
