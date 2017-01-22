# -*- coding: utf8 -*-
import logging
from .burpui_api_translate import TranslateBurpuiAPI
from ..backends.burpui_api import Clients


class BUIClients:
    """"
    Get data from burp ui clients
    """

    def __init__(self, burpui_apiurl):
        """

        """

        # Define clients from Interface
        self.clientsobj = Clients(apiurl=burpui_apiurl)

    def translate_clients_stats(self, detail=None):
        """

        :return: clients translated
        """

        # Get the list of clients from the Interface
        if detail:
            clients = self.clientsobj.get_clients_reports()
        else:
            clients = self.clientsobj.get_clients_stats()

        logging.debug('clients: {}'.format(clients))

        # Set clients list from api interface to TranslateBurpuiAPI object
        clients_list_api = TranslateBurpuiAPI(clients=clients)
        # Translate with method translate_clients()
        clients_reports = clients_list_api.translate_clients()
        return clients_reports
