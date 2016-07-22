from ..lib.txt import TxtReports
import arrow
from collections import defaultdict
from ..lib.is_up import is_up


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
        outdated_clients = defaultdict(dict)
        # Create a list of additional columns to add to the report
        columns = {'Status': 'b_status'}

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
                columns['comments'] = 'comments'

        # Create the object to export the report
        clients_reports = TxtReports(outdated_clients,
                                     additional_columns=columns,
                                     detail=self.detail)

        if export_txt:
            clients_reports.report_to_txt()

        return outdated_clients



