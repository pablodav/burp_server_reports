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

    def get_clients_stats(self):
        """
        #  server.get_all_clients()
        #
        :return example: [{
            "phase": 'null',
            "percent": 0,
            "state": "idle",
            "last": "2016-06-23 14:33:06-03:00",
            "name": "monitor"},
            {
                "last": "2015-05-17 11:40:02",
                "name": "client1",
                "state": "idle",
                "phase": "phase1",
                "percent": 12,
            },
            {
                "last": "never",
                "name": "client2",
                "state": "idle",
                "phase": "phase2",
                "percent": 42,
            }
        ]
        """

        if self.debug:
            print("Url received: {}".format(self.apiurl))

        serviceurl = self.apiurl + 'clients/stats'
        clients_stats = get_url_data(serviceurl=serviceurl)

        return clients_stats
