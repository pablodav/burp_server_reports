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

    # Notes for future detection of multi-agent mode:
    # url to check /api/servers/report
    # If not {"servers": {"name": null}}
    # Then we should look on the list of servers with their names.
    # https://burp-ui.readthedocs.io/en/latest/api.html#get--api-servers-report
    # And use:
    # Parameters:
    # server (str)  Which server to collect data from when in multi-agent mode

    # Comments from Ziirish:
    # You'd better test /api/servers/stats
    # It returns an empty list ([]) when there are no agents and then switch back to
    # the "standalone" mode.
    # Now if the list is not empty, you'll have something like:

    # [
    # {
    #   'alive': true,
    #   'clients': 2,
    #   'name': 'burp1',
    # },
    #  {
    #   'alive': false,
    #   'clients': 0,
    #   'name': 'burp2',
    #   },
    #  ]


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
