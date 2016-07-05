

class BurpReports:

    def __init__(self, clients_dict):
        """

        :param clients_dict: list of clients in burp_reports format, example:
        {'client_name':
            { 'b_last'    : 'date',
              'b_state'    : 'working/current',
              'b_phase' : 'phase1/phase2',
              'b_last' : 'date',
            }
        }

        """

        self.clients = clients_dict

