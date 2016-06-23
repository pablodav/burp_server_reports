

class Clients:
    """

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

    def get_clients_data():
        self.backend.get_all_clients()






        #  server.get_client(name='clientname')
        #  [{'received': 4025, 'end': 1466374965, 'encrypted': False, 'number': u'186', 'deletable': True, 'date': 1466374593, 'size': 2456396123}]


        #  server.get_all_clients()
        #  [{'state': 'idle', 'last': 'never', 'name': u'clientname'}]
