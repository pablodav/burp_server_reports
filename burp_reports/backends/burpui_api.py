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
        It will define the url to connect to the api
        like: http:/user:password@server:port/api/

        :param user: User to connect the api url
        :param password: Password to connect the api url
        :param server: server to connect api url
        :param port: port to connect api url
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




