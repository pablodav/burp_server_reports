#!python3

import pytest
from ..lib.imap import ImapReceive
from ..defaults.default_config import set_defaults

config_default = set_defaults()
config_default['email_inventory']['imap_host'] = 'localhost'
config_default['email_inventory']['imap_password'] = 'pwd1'
config_default['email_inventory']['imap_user'] = 'test1'
config_default['email_inventory']['imap_port'] = '3993'
config_test = dict(config_default['email_inventory'])

class TestImap:

    def test_connection(self):
        conn = ImapReceive(config=config_test)
        conn_test = conn._connect_imap()
        assert conn_test.check()[0] == 'OK'
