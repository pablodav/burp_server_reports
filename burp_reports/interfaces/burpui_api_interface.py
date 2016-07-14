# -*- coding: utf8 -*-

from .burpui_api_translate import TranslateBurpuiAPI
from ..backends.burpui_api import Clients


class BUIClients:
    """"
    Get data from burp ui clients
    """

    def __init__(self, burpui_apiurl, debug=None):
        """

        """

        # Define clients from Interface
        self.clientsobj = Clients(apiurl=burpui_apiurl,
                                  debug=debug)
        self.debug = debug

    def translate_clients_stats(self):
        """

        :return: clients translated
        """

        # Get the list of clients from the Interface
        clients = self.clientsobj.get_clients_stats()

        if self.debug:
            print('clients: {}'.format(clients))

        # Set clients list from api interface to TranslateBurpuiAPI object
        clients_list_api = TranslateBurpuiAPI(clients=clients)
        # Translate with method translate_clients()
        clients_reports = clients_list_api.translate_clients()

        return clients_reports


