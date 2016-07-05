# -*- coding: utf8 -*-


class TranslateBurpuiAPI:
    """
    Translate data from burpui_api to burp_reports
    """

    def __init__(self, clients):
        """
        Initialize vars
        :param: clients list of clients coming from burp_api
        """
        self.clients = clients

    def translate_clients_function(self, data_t):
        """

        :param data_t: list of clients dicts to use for translation
        :return: d_clients dictionary of clients translated to use in burp_reports
        example from clients stats:

        {'client_name':
            { 'b_last'    : 'date',
              'b_state'    : 'working/current',
              'b_phase' : 'phase1/phase2',
              'b_last' : 'date',
            }
        }
        """
        d_clients = {}

        for cli in range(len(self.clients)):
            # Get the client dict data from list of clients
            client_data = self.clients[cli]

            # Translate and define variables:
            # Define a dict with data to clients
            for k, v in data_t.items():
                client_name = client_data.get(data_t['client_name'])
                if k is not 'client_name':
                    # similar and simplified to: d_clients.setdefault(client_name, {})['b_phase'] = b_phase
                    d_clients.setdefault(client_name, {})[k] = client_data.get(data_t[k])

        # Return dictionary of clients expected to use in burp_reports
        return d_clients

    def translate_clients(self):
        """

        :return:
        {'client_name':
            { 'b_last'    : 'date',
              'b_state'    : 'working/current',
              'b_phase' : 'phase1/phase2',
              'b_last' : 'date',
            }
        }
        """

        # Dictionary to use for translation
        data_t = {
            "b_phase": 'phase',
            "b_state": "state",
            "b_last": "last",
            "client_name": "name" }

        reports_clients = self.translate_clients_function(data_t=data_t)
        return reports_clients
