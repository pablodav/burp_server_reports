# -*- coding: utf8 -*-
from ..defaults.default_data_structure import default_client_backup_report
import arrow
import random


class Clients:
    """
    Get clients from burpui api url.

    """

    def __init__(self):
        """

        """

    @staticmethod
    def get_clients():
        """
        #  server.get_all_clients()
        #
        :return: [{
        "phase": null,
        "percent": 0,
        "state": "idle",
        "last": "2016-06-23T14:33:06-03:00",
        "name": "monitor"}]
        """
        actual_time = arrow.get()

        default_backup_report = default_client_backup_report()

        clients_stats = [{
            "phase": 'null',
            "percent": 0,
            "state": "idle",
            "last": "2016-06-23T14:33:06-03:00",
            "name": "monitor",
            'backup_report': default_backup_report},
            {
            "last": "now",
            "name": "client1",
            "state": "idle",
            "phase": "phase1",
            "percent": 12,
            'backup_report': default_backup_report},
            {
            "last": "never",
            "name": "client2",
            "state": "idle",
            "phase": "phase2",
            "percent": 42,
            'backup_report': default_backup_report},
            {
                "last": 'now',
                "name": "cli30",
                "state": "idle",
                "phase": "null",
                "percent": 42,
                "server": 'server1',
                'backup_report': default_backup_report},
            {
                "last": actual_time.isoformat('T'),
                "name": "cli30",
                "state": "idle",
                "phase": "phase2",
                "percent": 0,
                "server": 'server2',
                'backup_report': default_backup_report}
        ]

        server = 'server1'
        # Add clients with random last in a range of 100
        for num in range(1, 101):
                    client_time = actual_time.replace(days=-random.randrange(5, 200))
                    client_last = client_time.isoformat(sep='T')
                    client_name = "client_{:03d}".format(num)
                    client_state = random.choice(['idle', 'working'])
                    client_phase = 'null'
                    client_percent = 0
                    if client_state == 'working':
                        client_phase = 'phase2'
                        client_percent = random.randrange(30, 90)
                    if num > 50:
                        server = 'server2'
                    
                    empty_backup_report = default_client_backup_report()
                    totsize = random.randrange(0, 10)
                    empty_backup_report['totsize'] = totsize

                    clients_stats.append({
                        "last": client_last,
                        "name": client_name,
                        "state": client_state,
                        "phase": client_phase,
                        "percent": client_percent,
                        "server": server,
                        'backup_report': empty_backup_report
                    })


        clients_stats[1]['backup_report']['totsize'] = 2048

        return clients_stats

    # @staticmethod
    # def get_backup_report():
    #     """
    #     dummy data example
    #     GET /api/client/(server)/report/(name)/(int: backup)
    #     GET /api/client/report/(name)/(int: backup)
    #
    #     :return:
    #     """
    #
    #     backup_report = [
    #         {"received": 326753806,
    #          "number": 1,
    #          "totsize": 572911431,
    #          "duration": 84
    #          }]
