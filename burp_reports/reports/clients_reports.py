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

    def report_outdated(self):
        outdated_clients = {}
        for k, v in self.clients.items():
            actual_time = arrow.get()
            outdated_time = actual_time.replace(days=-1)
            if v.get('b_last') < outdated_time:
                outdated_clients.setdefault(k, v)

        client_reports =  TxtReports(outdated_clients)
        client_reports.report_to_txt()



