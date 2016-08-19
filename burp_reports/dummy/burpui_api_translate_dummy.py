# -*- coding: utf8 -*-

from ..interfaces.burpui_api_translate import TranslateBurpuiAPI
from ..dummy.burpui_dummy_api import Clients


class BUIClients:
    """"
    Get data from burp ui clients
    """

    def __init__(self):
        """

        """
        # Define clients from Interface
        self.clientsobj = Clients
        # Get the list of clients from the Interface
        self.clients = self.clientsobj.get_clients()

    def translate_clients_stats(self):
        """

        :return: clients translated
        """

        # Set clients list from api interface to TranslateBurpuiAPI object
        clients_list_api = TranslateBurpuiAPI(clients=self.clients)
        # Translate with method translate_clients()
        clients_reports = clients_list_api.translate_clients()

        return clients_reports

