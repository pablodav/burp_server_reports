# -*- coding: utf8 -*-
import urllib
import json


# -*- coding: utf8 -*-

class Clients:
    """
    Get clients from burpui api url.

    """

    def __init__(self, user, password, server, port):
        """

        :param burp_version: version of burp backend to work with 1/2
        :param conf: burp_ui configuration to use.
        :param dummy: if true all functions will return only examples outputs.
        """

        self.serviceurl = 'http://' + user + ':' + password + '@' + server + ':' + port + '/api/'

    @staticmethod
    def get_url_data(url):
        """

        :param url: url to retrieve data
        :return: json url_data
        """
        uh = urllib.urlopen(url)
        data = uh.read()

        try:
            js = json.loads(str(data))
        except:
            js = None

        return js

    def get_clients(self):
        """
        #  server.get_all_clients()
        #
        :return: [{
        "phase": null,
        "percent": 0,
        "state": "idle",
        "last": "2016-06-23 14:33:06-03:00",
        "name": "monitor"}]
        """

        url = self.serviceurl + 'clients/stats'
        clients_stats = self.get_url_data(url=url)

        return clients_stats




