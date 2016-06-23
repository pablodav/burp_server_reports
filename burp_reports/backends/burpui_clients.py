

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

        if self.version == 1:
            from burpui.misc.backend.burp1 import Burp
        elif self.buiconf == 2:
            from burpui.misc.backend.burp2 import Burp

        self.backend = Burp(conf=self.buiconf)

    def get_client(self, client_name=None):
        """

        :param client_name: Name of the client to retrieve data.
        :return: [{'received': 4025, 'end': 1466374965, 'encrypted': False, 'number': u'186', 'deletable': True, 'date': 1466374593, 'size': 2456396123}]
        """
        self.backend.get_client(name=client_name)

    def get_clients(self):
        """
        #  server.get_all_clients()
        #
        :return: [{'state': 'idle', 'last': 'never', 'name': u'clientname'}]
        """
        all_clients = self.backend.get_all_clients()



