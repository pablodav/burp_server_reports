#!python3
# https://gist.github.com/rdempsey/22afd43f8d777b78ef22
# https://stackoverflow.com/questions/3362600/how-to-send-email-attachments

import pytest
from ..lib.imap import ImapReceive
from ..defaults.default_config import set_defaults
import imaplib
import time
import email.message

config_default = set_defaults()
config_default['email_inventory']['imap_host'] = 'localhost'
config_default['email_inventory']['imap_password'] = 'pwd1'
config_default['email_inventory']['imap_user'] = 'test1'
config_default['email_inventory']['imap_port'] = '3993'
config_test = dict(config_default['email_inventory'])

config_default['email_notification']['smtp_port'] = '3025'
config_default['email_notification']['subject'] = 'inventory'
config_smtp = dict(config_default['email_notification'])
# new_smtp_email = EmailNotifications(config=config_smtp, msg="test", attachments=[('utf-8', 'text', 'plain', 'burp_reports/data/test_inventory.csv', 'utf-8')])
# new_smtp_email.send_email()

class TestImap:

    def test_connection(self):
        conn = ImapReceive(config=config_test)
        conn_test = conn._connect_imap()
        assert conn_test.check()[0] == 'OK'

    def test_attachment(self):
        conn = ImapReceive(config=config_test)
        c = conn._connect_imap()
        new_message = email.message.Message()
        new_message["From"] = "hello@itsme.com"
        new_message["Subject"] = "inventory"
        new_message.set_payload("This is test message.")
        c.append('INBOX', '',
                 imaplib.Time2Internaldate(time.time()),
                 str(new_message).encode('utf-8'))
