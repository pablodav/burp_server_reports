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

        return clients_stats

    @staticmethod
    def get_client_report():
        """
        dummy data example using api/client/report/monitor

        :return:
        """

        client_report = [
            {"files": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 9082, "new": 9082, "total": 9082},
             "softlink": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0},
             "vssheader_enc": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0},
             "end": 1466714070,
             "meta_enc": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0},
             "received": 326753806,
             "vssfooter": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0},
             "encrypted": false,
             "efs": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0},
             "number": 1,
             "totsize": 572911431,
             "start": 1466713986,
             "windows": true,
             "hardlink": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 33, "new": 33, "total": 33},
             "meta": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0},
             "dir": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 2040, "new": 2040, "total": 2040},
             "files_enc": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0},
             "duration": 84,
             "vssfooter_enc": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0},
             "vssheader": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0},
             "special": {"deleted": 0, "unchanged": 0, "changed": 0, "scanned": 0, "new": 0, "total": 0}}]




