from ..lib.txt import TxtReports
import arrow


class BurpReports:

    def __init__(self, clients_dict):
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

    def print_basic_txt(self):
        clients_reports = TxtReports(self.clients)
        clients_reports.report_to_txt()

    def report_outdated(self, export_txt=None):
        """

        :param print: if print, it will print the outdated clients
        :return: dict of outdated clients.
        """
        outdated_clients = {}

        for k, v in self.clients.items():
            # Get actual time with arrow module
            actual_time = arrow.get()
            # get date to consider as outdated
            outdated_time = actual_time.replace(days=-1)
            if v.get('b_last') < outdated_time:
                outdated_clients.setdefault(k, v)

        clients_reports =  TxtReports(outdated_clients)

        if export_txt:
            clients_reports.report_to_txt()

        return clients_reports



