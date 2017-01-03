# -*- coding: utf8 -*-
import arrow
from collections import defaultdict
from functools import lru_cache


class TranslateBurpuiAPI:
    """
    Translate data from burpui_api to burp_reports
    """

    def __init__(self, clients):
        """
        Initialize vars
        :param: clients list of clients coming from burp_api
        """
        self.clients = clients

    def translate_clients_function(self, data_t):
        """

        :param data_t: list of clients dicts to use for translation
        :return: d_clients dictionary of clients translated to use in burp_reports
        example from clients stats:

        {'client_name':
            { 'b_last'    : 'YYYY-MM-DDTHH:mm:ssZZ',
              'b_state'    : 'working/current',
              'b_phase' : 'phase1/phase2',
              'b_date' : 'date(local)',
              'b_time' : 'time(local)',
              'server': 'server in multi-agent mode'
            }
        }
        """
        d_clients = defaultdict(dict)

        for cli in range(len(self.clients)):
            # Get the client dict data from list of clients
            client_data = self.clients[cli]
            client_name = client_data.get(data_t['client_name'], None)

            # Go to next item in client_data if there is not 'client_name'
            if not client_name:
                continue

            # Translate and define variables:
            # Define a dict with data to clients
            for k, v in data_t.items():

                if k is not 'client_name':
                    # similar and simplified to: d_clients.setdefault(client_name, {})['b_phase'] = b_phase
                    d_clients[client_name][k] = client_data.get(v, None)

                # Add b_date and b_time from b_last information
                # if k is b_last and b_last has data and is not never, add the keys.
                if k is 'b_last':
                    last_backup = client_data.get(v, None)
                    if last_backup and last_backup not in 'never':
                        if last_backup == 'now':
                            date_and_time = arrow.get()
                            d_clients[client_name]['b_last'] = date_and_time.isoformat(sep='T')
                        else:
                            date_and_time = arrow.get(last_backup)
                        # Convert date_and_time to local time
                        date_and_time = date_and_time.to('local')
                        d_clients[client_name]['b_date'] = date_and_time.format('YYYY-MM-DD')
                        d_clients[client_name]['b_time'] = date_and_time.format('HH:mm:ss')

            # Add server list if not exists
            if not d_clients[client_name].get('server', None):
                d_clients[client_name]['server'] = []
            # Append servers if exist
            if client_data.get('server', None):
                d_clients[client_name]['server'].append(client_data['server'])

        # Return dictionary of clients expected to use in burp_reports
        return d_clients

    def translate_clients(self):
        """

        :return:
        {'client_name':
            { 'b_last'    : '2016-06-23T14:33:06-03:00',
              'b_state'    : 'working/current',
              'b_phase' : 'phase1/phase2'
              'b_date' : 'local time date'
              'b_time' : 'local time'
              'backup_report' : 'dict with backup report, data like duration, totsize, received'
            }
        }
        """

        # Dictionary to use for translation
        data_t = {
            "b_phase": 'phase',
            "b_state": "state",
            "b_last": "last",
            "client_name": "name"}

        # Check if key backup_report exists in clients
        if 'backup_report' in self.clients[0]:
            # Add to dictionary of client
            data_t['backup_report'] = 'backup_report'

        reports_clients = self.translate_clients_function(data_t=data_t)
        return reports_clients
