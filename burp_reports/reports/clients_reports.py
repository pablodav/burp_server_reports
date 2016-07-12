from ..lib.txt import TxtReports
import arrow


class BurpReports:

    def __init__(self, clients_dict, days_outdated=31):
        """

        :param clients_dict: list of clients in burp_reports format, example:
        {'client_name':
            { 'b_last'    : 'YY-MM-DD HH:mm:ssZZ',
              'b_state'    : 'working/current',
              'b_phase' : 'phase1/phase2',
              'b_last' : 'date',
            }
        }

        """

        self.clients = clients_dict
        self.days_outdated = days_outdated

    def print_basic_txt(self):
        clients_reports = TxtReports(self.clients)
        clients_reports.report_to_txt()

    def report_outdated(self, export_txt=None):
        """

        :param print: if print, it will print the outdated clients
        :param export_txt: use it if you want to print on screen, used with cli
        :return: dict of outdated clients.
        """
        outdated_clients = {}

        for k, v in self.clients.items():
            # Get actual time with arrow module
            actual_time = arrow.get()
            # get date to consider as outdated
            outdated_time = actual_time.replace(days=-self.days_outdated)
            client_last = v.get('b_last', None)

            # Add client to outdated list if not backup
            if client_last.lower() in 'never' or not client_last:
                outdated_clients.setdefault(k, v)
                outdated_clients[k]['b_state'] = 'never'
                continue

            # Convert client_last to arrow date
            client_last = arrow.get(v.get('b_last', None), 'YY-MM-DD HH:mm:ssZZ')
            
            # Add client to outdated list if outdated
            if not isinstance(client_last, str):
                if client_last < outdated_time:
                    outdated_clients.setdefault(k, v)
                    outdated_clients[k]['b_state'] = 'outdated'

        clients_reports = TxtReports(outdated_clients)

        if export_txt:
            clients_reports.report_to_txt()

        return clients_reports



