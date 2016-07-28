# -*- coding: utf8 -*-


class Clients:
    """
    Get clients information.

    """

    def __init__(self, conf=None):
        """

        :param conf: burp_ui configuration to use.
        """

        self.buiconf = conf

    @staticmethod
    def get_client(client='monitor'):
        """

        :param client: Name of the client to retrieve data.
        :return: [{'received': 326753806, 'end': 1466714070, 'encrypted': False, 'number': 1,
        'deletable': True, 'date': 1466713986, 'size': 572911431}]
        """
        
        client_data = [{'received': 326753806, 'end': 1466714070, 'encrypted': False, 'number': 1,
                        'deletable': True, 'date': 1466713986, 'size': 572911431}]
        return client_data 

    @staticmethod
    def get_clients():
        """
        #  server.get_all_clients()
        #
        :return: [{'state': u'idle', 'last': 1466703186, 'name': u'monitor'}]
        """
                
        all_clients = [{'state': u'idle', 'last': 1466703186, 'name': u'monitor'}]

        return all_clients


