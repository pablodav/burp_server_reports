# -*- coding: utf8 -*-

g_burpbin = u'/usr/sbin/burp'

class Clients:
    """
    Get clients information.

    :param burp_version: version of burp backend to work with 1/2
    :param conf: burp client configuration to use.
    """

    def __init__(self, burp_version=2, burpconfcli='/etc/burp/burp-monitor.conf'):

        global g_burpbin

        self.version = burp_version
        self.burpconfcli = burpconfcli
        self.burpbin = g_burpbin


