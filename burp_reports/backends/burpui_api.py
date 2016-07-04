# -*- coding: utf8 -*-
import urllib.request
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

        # Only python3 compatible functionality
        # Get data from the url
        print("Try to open url", serviceurl )

        with urllib.request.urlopen(serviceurl) as response:
            data = response.read()

        # Convert data on string and load with json file
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
        print("Url received: {}".format(self.apiurl))

        serviceurl = self.apiurl + 'clients/stats'
        clients_stats = self.get_url_data(serviceurl=serviceurl)

        return clients_stats




