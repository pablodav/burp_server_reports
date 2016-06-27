
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
        d_clients = {}

        # Dictionary to use for translation
        data_t = {
            "b_phase": 'phase',
            "b_state": "state",
            "b_last": "last",
            "client_name": "name" }

        for clin in range(len(self.clients)):
            # Get the client data from list of clients
            client_data = self.clients[clin]

            # Translate and define variables:
            b_phase = client_data.get(data_t['b_phase'])
            b_state = client_data.get(data_t['b_state'])
            b_last = client_data.get(data_t['b_last'])
            client_name = client_data.get(data_t['client_name'])

            # Define a dict for all clients
            d_clients.setdefault(client_name, {})['b_phase'] = b_phase
            d_clients.setdefault(client_name, {})['b_state'] = b_state
            d_clients.setdefault(client_name, {})['b_last'] = b_last

        # Return dictionary of clients expected to use in burp_reports
        return d_clients