# -*- coding: utf8 -*-


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
        "last": "2016-06-23 14:33:06-03:00",
        "name": "monitor"}]
        """

        clients_stats = [{
            "phase": 'null',
            "percent": 0,
            "state": "idle",
            "last": "2016-06-23 14:33:06-03:00",
            "name": "monitor"}]

        return clients_stats




