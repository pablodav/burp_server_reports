# -*- coding: utf8 -*-
from burp_reports.lib.urlget import get_url_data
from collections import defaultdict


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

        if self.debug:
            print('burpui_servers: {}'.format(burpui_servers))

        clients_stats = []

        for i in range(len(burpui_servers)):

            # Do not get data from servers offline
            if not burpui_servers[i]['alive']:
                continue

            server = burpui_servers[i]['name']
            # Not used now: burpui_api_params = {'server': server}

            serviceurl = self.apiurl + 'clients/{}/stats'.format(server)

            if self.debug:
                print('serviceurl: {}'.format(serviceurl))

            server_clients_stats = get_url_data(serviceurl=serviceurl)
            if self.debug:
                print('server_clients_stats: {}'.format(server_clients_stats))

            # Append client to clients_stats
            for cli in range(len(server_clients_stats)):
                client_stats = server_clients_stats[cli]
                client_stats['server'] = server
                clients_stats.append(client_stats)

        return clients_stats

    def _get_backup_report_stats(self, client, number, server=None):
        """
        GET /api/client/(server)/report/(name)/(int: backup)
        GET /api/client/report/(name)/(int: backup)
        will be used: totsize, received, duration.
        """

        serviceurl = self.apiurl + 'client/report/{}/{}'.format(client, number)

        if server:
            serviceurl = self.apiurl + 'client/{}/report/{}/{}'.format(server, client, number)

        if self.debug:
            print('apiurl: {}'.format(serviceurl))

        backup_report = get_url_data(serviceurl)

        return backup_report

    def _get_client_report_stats(self, client, server=None):
        """
        https://burp-ui.readthedocs.io/en/latest/api.html#get--api-client-stats-(name)
        GET  /api/client/stats/(name)
        GET /api/client/(server)/stats/(name)

        :return:
        [
          {
            "date": "2015-01-25 13:32:00",
            "deletable": true,
            "encrypted": true,
            "received": 123,
            "size": 1234,
            "number": 1
          },
        ]
        """

        serviceurl = self.apiurl + 'client/stats/{}'.format(client)

        if server:
            serviceurl = self.apiurl + 'client/{}/stats/{}'.format(server, client)

        if self.debug:
            print('apiurl: {}'.format(serviceurl))

        client_report = get_url_data(serviceurl)

        return client_report

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

    def get_clients_reports(self):
        """
        Clients reports method
        :return: [client_report_dict, ]
        """

        # Get a list of clients to use
        clients_stats = self.get_clients_stats()

        if self.debug:
            print('clients_stats: {}'.format(clients_stats))

        # Create a new list to return
        clients_report = []

        for cli in range(len(clients_stats)):

            # Server, client is required to fetch report_stats
            server = clients_stats[cli].get('server', None)
            if self.debug:
                print('server: {}'.format(server))
            client = clients_stats[cli].get('name', None)

            # Create dict with all data of the client's dict
            client_report_dict = defaultdict(dict)
            client_report_dict.update(clients_stats[cli])
            # Create new list to use a list of numbers of backups only
            backups = []

            if not client:
                continue

            if clients_stats[cli].get('last', 'None') not in ['None', 'never']:

                # Get client_report_stats ;
                # Needs to add test if it's [] retry n times due to issue:
                # https://git.ziirish.me/ziirish/burp-ui/issues/148
                cr_stats = self._get_client_report_stats(client, server=server)
                # and create a list of backups numbers only
                for n in range(len(cr_stats)):
                    backups.append(cr_stats[n].get('number'))
                # Get the maximum number of backup to use
                number = max(backups)

                # Add the backup_report to the dict of the client
                client_report_dict['backup_report'] = self._get_backup_report_stats(client, number, server=server)
            else:
                client_report_dict['backup_report'] = {}

            # if self.debug: print('backup_report: {}'.format(client_report_dict))

            clients_report.append(client_report_dict)

        return clients_report
