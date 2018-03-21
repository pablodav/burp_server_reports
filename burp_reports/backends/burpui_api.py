# -*- coding: utf8 -*-
import logging
from ..lib.urlget import get_url_data
from ..defaults.default_data_structure import default_client_backup_report
from collections import defaultdict
from functools import lru_cache
import requests


class Clients:
    """
    Get clients from burpui api url.

    """

    def __init__(self, apiurl, check_idle=True):
        """
        should be the api to connect
        like: http:/user:password@server:port/api/

        Use get_clients_stats to get the default list of clients

        :param apiurl
        :param check_idle: Will enable on function like get_clients_stats to verify each client for those without idle state and 
        a latest date of backup.
        """

        self.apiurl = apiurl

        self.IsMultiAgent = self._is_multi_agent()
        self.empty_backup_report = default_client_backup_report()
        self.check_idle = check_idle

    @lru_cache(maxsize=32)
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
        burpui_servers = get_url_data(serviceurl, check_multi=True)
        return_bool = None

        if burpui_servers:
            return_bool = True

        return return_bool

    @lru_cache(maxsize=32)
    def _get_clients_stats_multi(self):
        """

        :return: return a complete list of clients for each alive server in multi-agent server.
        """

        serviceurl = self.apiurl + 'servers/stats'
        burpui_servers = get_url_data(serviceurl)

        logging.debug('burpui_servers: {}'.format(burpui_servers))

        clients_stats = []

        for i in range(len(burpui_servers)):

            # Do not get data from servers offline
            if not burpui_servers[i]['alive']:
                continue

            server = burpui_servers[i]['name']
            # Not used now: burpui_api_params = {'server': server}
            # Use http://burp-ui.readthedocs.io/en/latest/api.html#get--api-clients-(server)-stats
            # The JSON returned is:
            # {
            #   [
            #     {
            #       "last": "2015-05-17 11:40:02",
            #       "name": "client1",
            #       "state": "idle",
            #       "phase": "phase1",
            #       "percent": 12,
            #     },
            #     {
            #       "last": "never",
            #       "name": "client2",
            #       "state": "idle",
            #       "phase": "phase2",
            #       "percent": 42,
            #     }
            #   ]
            # }
            serviceurl = self.apiurl + 'clients/{}/stats'.format(server)

            logging.debug('serviceurl: {}'.format(serviceurl))

            server_clients_stats = get_url_data(serviceurl=serviceurl)
            logging.debug('server_clients_stats: {}'.format(server_clients_stats))

            # Append client to clients_stats
            for cli in range(len(server_clients_stats)):
                client_stats = server_clients_stats[cli]
                client_stats['server'] = server
                clients_stats.append(client_stats)

        return clients_stats

    @lru_cache(maxsize=32)
    def _get_clients_report_multi(self):
        """
        doc: https://burp-ui.readthedocs.io/en/latest/api.html#get--api-clients-(server)-report
        GET /api/clients/(server)/report
        Returns a global report about all the clients of a given server

        :return: return a complete list of clients for each alive server in multi-agent server.
        """
        # Get burpui servers:
        serviceurl = self.apiurl + 'servers/stats'
        burpui_servers = get_url_data(serviceurl)

        logging.debug('burpui_servers: {}'.format(burpui_servers))

        clients_reports = []

        for i in range(len(burpui_servers)):

            # Do not get data from servers offline
            if not burpui_servers[i]['alive']:
                continue

            server = burpui_servers[i]['name']
            # Not used now: burpui_api_params = {'server': server}
            # Use http://burp-ui.readthedocs.io/en/latest/api.html#get--api-clients-(server)-stats
            # GET /api/clients/(server)/report
            serviceurl = self.apiurl + 'clients/{}/report'.format(server)

            logging.debug('serviceurl: {}'.format(serviceurl))

            server_clients_reports = get_url_data(serviceurl=serviceurl)
            # From demo: {'backups': [{'number': 11, 'name': 'demo3'}, {'number': 11, 'name': 'demo4'}],
            # 'clients': [{'name': 'demo3', 'stats': {'windows': 'unknown', 'totsize': 8317913635, 'total': 540904}},
            # {'name': 'demo4', 'stats': {'windows': 'unknown', 'totsize': 8317913635, 'total': 540904}}]}

            logging.debug('server_clients_reports: {}'.format(server_clients_reports))

            # Append client to clients_reports
            for cli in range(len(server_clients_reports['clients'])):
                client_stats = server_clients_reports['clients'][cli]
                client_stats['server'] = server
                clients_reports.append(client_stats)

        return clients_reports

    @lru_cache(maxsize=32)
    def _get_backup_report_stats(self, client, number, server=None):
        """
        GET /api/client/(server)/report/(name)/(int: backup)
        GET /api/client/report/(name)/(int: backup)
        will be used: totsize, received, duration.
        """

        serviceurl = self.apiurl + 'client/report/{}/{}'.format(client, number)

        if server:
            serviceurl = self.apiurl + 'client/{}/report/{}/{}'.format(server, client, number)

        logging.debug('apiurl: {}'.format(serviceurl))

        backup_report = get_url_data(serviceurl)

        return backup_report

    @lru_cache(maxsize=32)
    def _get_client_report_stats(self, client, server=None):
        """
        https://burp-ui.readthedocs.io/en/latest/api.html#get--api-client-stats-(name)
        GET  /api/client/stats/(name)
        GET /api/client/(server)/stats/(name)

        :return list:
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

        logging.debug('apiurl: {}'.format(serviceurl))

        client_report = get_url_data(serviceurl, ignore_empty=True)

        return client_report

    def _check_idle_state_clients_stats(self, clients_stats):
        """
        Receive list generated by api client, like get_clients_stats returns.
        Verifies each client state and last not never
        Then get get_client_report information to have totsize in backup_report nested dict
        :param clients_stats exmple:
        [{
            "phase": 'null',
            "percent": 0,
            "state": "idle",
            "last": "2016-06-23 14:33:06-03:00",
            "name": "monitor"},
            {
                "last": "never",
                "name": "client2",
                "state": "idle",
                "phase": "phase2",
                "percent": 42,
            }
        ]
        """
        # Create a new list to return
        clients_report = []

        for i, values in enumerate(clients_stats):
            client_state = clients_stats[i].get('state', None)
            client_last = clients_stats[i].get('last', None)   
            # Create dict with all data of the client's dict
            client_report_dict = defaultdict(dict)
            client_report_dict.update(values)

            if client_state not in ['idle', 'running'] and client_last not in ['never', None]:

                client = client_report_dict.get('name', None)
                logging.info("client {} has no clean status, getting totsize, status: {}".format(client, client_state))
                if not client:
                    continue
                server = client_report_dict.get('server', None)
                # running clients on server
                server_running = self.get_clients_running(server)
                # Omit getting stats for clients running a backup
                # burpui doesn't return data when client is running.
                if client in server_running:
                    continue
            
                client_report_dict = self._get_client_report_backups(client_report_dict)

            clients_report.append(client_report_dict)

        return clients_report

    @lru_cache(maxsize=32)
    def get_clients_stats(self):
        """
        # Default function used to get a list of clients with fastest as possible.
        # Now adding a verification of status: idle to identify clients without backup
        # Will be slower but could be disabled
        #  server.get_all_clients()
        #
        :return list: example: [{
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

        logging.debug("get_clients_stats: Url received: {}".format(self.apiurl))

        if self.IsMultiAgent:
            clients_stats = self._get_clients_stats_multi()
        else:
            serviceurl = self.apiurl + 'clients/stats'
            clients_stats = get_url_data(serviceurl=serviceurl)

        if self.check_idle:
            clients_stats = self._check_idle_state_clients_stats(clients_stats)

        return clients_stats

    @lru_cache(maxsize=32)
    def get_clients_reports_brief(self) -> list:

        # For multi server:
        # https://burp-ui.readthedocs.io/en/stable/api.html#get--api-clients-(server)-report
        # For single server:
        # https://burp-ui.readthedocs.io/en/latest/api.html#get--api-clients-report
        # GET /api/clients/report
        logging.debug("get_clients_reports_brief: Url received: {}".format(self.apiurl))

        if self.IsMultiAgent:
            clients_report = self._get_clients_report_multi()
        else:
            serviceurl = self.apiurl + 'clients/report'
            clients_report = get_url_data(serviceurl=serviceurl)

        return clients_report

    @lru_cache(maxsize=32)
    def get_clients_running(self, server=None) -> list:
        """
        http://burp-ui.readthedocs.io/en/latest/api.html#get--api-clients-(server)-running
        :return: list of clients
        """

        if self.IsMultiAgent:
            serviceurl = '{}clients/{}/running'.format(self.apiurl, server)

        else:
            serviceurl = '{}clients/running'.format(self.apiurl)

        logging.debug("get_clients_running: get info")

        clients_running = get_url_data(serviceurl, ignore_empty=True)

        return clients_running

    @lru_cache(maxsize=32)
    def get_clients_reports(self):
        """
        Clients reports method
        :return list: [client_report_dict, ]
        example client:
        [ {'state': 'idle', 'human': '24 minutes ago', 'last': '2016-11-18T10:17:02+01:00', 'percent': 0,
            'server': 'Burp1', 'name': 'demo2',
        'backup_report': {'totsize': 8280079447,
            'efs': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
            'vssheader_enc': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
            'start': '2016-11-18T09:17:02+01:00', 'encrypted': False,
            'hardlink': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
            'windows': True,
            'vssheader': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
            'softlink': {'total': 102, 'deleted': 0, 'unchanged': 102, 'scanned': 102, 'changed': 0, 'new': 0},
            'files': {'total': 506894, 'deleted': 4, 'unchanged': 506882, 'scanned': 506894, 'changed': 10, 'new': 2},
            'end': '2016-11-18T09:19:49+01:00',
            'meta_enc': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
            'duration': 167, 'number': 2066,
            'meta': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
            'special': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
            'dir': {'total': 33094, 'deleted': 0, 'unchanged': 33087, 'scanned': 33094, 'changed': 0, 'new': 7},
            'vssfooter_enc': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
            'received': 1257441,
            'vssfooter': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
            'files_enc': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0}},
        'phase': None}]
        """

        # Get a list of clients to use
        clients_stats = self.get_clients_stats()

        logging.debug('clients_stats: {}'.format(clients_stats))

        # Create a new list to return
        clients_report = []
        
        for cli in range(len(clients_stats)):

            # Create dict with all data of the client's dict
            client_report_dict = defaultdict(dict)
            client_report_dict.update(clients_stats[cli])
            client = client_report_dict.get('name', None)
            if not client:
                continue
            server = client_report_dict.get('server', None)
            # running clients on server
            server_running = self.get_clients_running(server)
            # Omit getting stats for clients running a backup
            # burpui doesn't return data when client is running.
            if client in server_running:
                continue

            client_report_dict = self._get_client_report_backups(client_report_dict)

            clients_report.append(client_report_dict)

        return clients_report

    def _get_client_report_backups(self, client_report_dict):
        """

        :param client_report_dict: should be in format of default dict, with the data of clients_stats dict for
        one client.
        Generate it with:
            # Create dict with all data of the client's dict
            client_report_dict = defaultdict(dict)
            client_report_dict.update(clients_stats[cli])
        :return: same dict with appended 'backup_report' as nested dict with totsize, received, duration, etc.
        """
        # Create new list to use a list of numbers of backups only
        backups = []
        # Server, client is required to fetch report_stats
        server = client_report_dict.get('server', None)
        logging.debug('_get_client_report_backups: server: {}'.format(server))
        client = client_report_dict.get('name', None)

        if client_report_dict.get('last', 'None') not in ['None', 'never']:

            # Get client_report_stats ;
            # It is a list of all backups stats
            cr_stats = self._get_client_report_stats(client, server=server)
            # and create a list of backups numbers only
            for n in range(len(cr_stats)):
                backups.append(cr_stats[n].get('number'))

            if backups:
                # Get the maximum number of backup to use
                # The first backup could have date but not being reported with number, so no statistics.
                # For that reason I add this if backups:
                number = max(backups)

                # Add the backup_report to the dict of the client
                client_report_dict['backup_report'] = self._get_backup_report_stats(client, number, server=server)
            else:
                client_report_dict['backup_report'] = self.empty_backup_report
        else:
            client_report_dict['backup_report'] = self.empty_backup_report

        if not client_report_dict['backup_report'].get('totsize'):
            client_report_dict['backup_report']['totsize'] = 0
        if not client_report_dict['backup_report'].get('received'):
            client_report_dict['backup_report']['received'] = 0
        if not client_report_dict['backup_report'].get('duration'):
            client_report_dict['backup_report']['duration'] = 0
        
        return client_report_dict
