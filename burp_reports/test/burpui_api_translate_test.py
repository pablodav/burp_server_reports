# -*- coding: utf8 -*-

from .burpui_api_translate import TranslateBurpuiAPI
from ..dummy.burpui_dummy_api import Clients

class BUIClients:
    """"
    Get data from burp ui clients
    """

    def __init__(self):
        """

        """
        self.clientes = Clients

