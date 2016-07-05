# -*- coding: utf8 -*-
from ..lib.urlget import get_url_data


class Clients:
    """
    Get clients from burpui api url.

    """

    def __init__(self, apiurl, debug=False):
        """
        should be the api to connect
        like: http:/user:password@server:port/api/

        :param apiurl
        """

        self.apiurl = apiurl
        self.debug = debug

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

        if self.debug:
            print("Url received: {}".format(self.apiurl))

        serviceurl = self.apiurl + 'clients/stats'
        clients_stats = get_url_data(serviceurl=serviceurl)

        return clients_stats
