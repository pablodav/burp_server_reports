
class TranslateAPI:
    """
    Translate data from burpui_api to burp_reports
    """

    def __init__(self, clients):
        """
        Initialize vars
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

        client_translate = {
            "b_phase": 'phase',
            "b_state": "state",
            "b_last": "last",
            "client_name": "name" }