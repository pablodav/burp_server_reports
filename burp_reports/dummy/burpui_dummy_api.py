# -*- coding: utf8 -*-
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

        clients_stats = [{
            "phase": 'null',
            "percent": 0,
            "state": "idle",
            "last": "2016-06-23T14:33:06-03:00",
            "name": "monitor"},
            {
            "last": "now",
            "name": "client1",
            "state": "idle",
            "phase": "phase1",
            "percent": 12},
            {
            "last": "never",
            "name": "client2",
            "state": "idle",
            "phase": "phase2",
            "percent": 42},
            {
                "last": 'now',
                "name": "cli30",
                "state": "idle",
                "phase": "null",
                "percent": 42,
                "server": 'server1'},
            {
                "last": actual_time.isoformat('T'),
                "name": "cli30",
                "state": "idle",
                "phase": "phase2",
                "percent": 0,
                "server": 'server2'}
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

                    clients_stats.append({
                        "last": client_last,
                        "name": client_name,
                        "state": client_state,
                        "phase": client_phase,
                        "percent": client_percent,
                        "server": server,
                    })

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
