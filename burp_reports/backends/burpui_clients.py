

class Clients:
    """
    Get clients information.

    """

    def __init__(self, burp_version=1, conf=None):
        """

        :param burp_version: version of burp backend to work with 1/2
        :param conf: burp_ui configuration to use.
        """

        self.version = burp_version
        self.buiconf = conf

        # Use burpui backend for specified burp version

        if self.version == 1:
            from burpui.misc.backend.burp1 import Burp
        elif self.version == 2:
            from burpui.misc.backend.burp2 import Burp

        self.backend = Burp(conf=self.buiconf)

    def get_client(self, client):
        """

        :param client: Name of the client to retrieve data.
        :return: [{'received': 326753806, 'end': 1466714070, 'encrypted': False, 'number': 1, 'deletable': True, 'date': 1466713986, 'size': 572911431}]
        """
        client_data = self.backend.get_client(name=client)
        return client_data

    def get_clients(self):
        """
        #  server.get_all_clients()
        #
        :return: [{'state': u'idle', 'last': 1466703186, 'name': u'monitor'}]
        """
        all_clients = self.backend.get_all_clients()
        return all_clients

    def get_b_logs(self, number, client):
        """

        :param number: backup number
        :param client: name of the client
        :return:
        """

        backup_data = self.backend.get_backup_logs(self, number, client)
        return backup_data



