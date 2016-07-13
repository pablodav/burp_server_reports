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

        self.IsMultiAgent = self._is_multi_agent()

    def _is_multi_agent(self):
        """

        :param self:
        :return: True/None
        """
        # Notes for future detection of multi-agent mode:
        # url /api/servers/report
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
        serviceurl = self.apiurl + 'servers/stats'
        burpui_servers = get_url_data(serviceurl)

        if burpui_servers:
            return True
        else:
            return None

    def _get_clients_stats_multi(self):
        """

        :return: return a complete list of clients for each alive server in multi-agent server.
        """

        serviceurl = self.apiurl + 'servers/stats'
        burpui_servers = get_url_data(serviceurl)
        clients_stats = []

        for i in range(len(burpui_servers)):

            # Do not get data from servers offline
            if not burpui_servers[i]['alive']:
                continue

            server = burpui_servers[i]['name']
            burpui_api_params = {'server': server}

            serviceurl = self.apiurl + 'clients/stats'
            server_clients_stats = get_url_data(serviceurl=serviceurl, params=burpui_api_params)

            for cli in range(len(server_clients_stats)):
                client_stats = server_clients_stats[cli]
                clients_stats['server'] = server
                clients_stats.append(client_stats)

        return clients_stats

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
                "last": "2015-05-17 11:40:02-03:00",
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

        if self.IsMultiAgent:
            clients_stats = self._get_clients_stats_multi()
        else:
            serviceurl = self.apiurl + 'clients/stats'
            clients_stats = get_url_data(serviceurl=serviceurl)

        return clients_stats
