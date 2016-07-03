# -*- coding: utf8 -*-
import urllib
import json


# -*- coding: utf8 -*-

class Clients:
    """
    Get clients from burpui api url.

    """

    def __init__(self, apiurl):
        """
        should be the api to connect
        like: http:/user:password@server:port/api/

        :param apiurl
        """

        self.apiurl = apiurl

    @staticmethod
    def get_url_data(serviceurl):
        """

        :param url: url to retrieve data
        :return: json url_data
        """
        uh = urllib.urlopen(serviceurl)
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

        serviceurl = self.apiurl + 'clients/stats'
        clients_stats = self.get_url_data(serviceurl=serviceurl)

        return clients_stats




