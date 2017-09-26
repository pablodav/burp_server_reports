#!python3
# https://gist.github.com/rdempsey/22afd43f8d777b78ef22
# https://stackoverflow.com/questions/3362600/how-to-send-email-attachments

import imaplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
# from email.utils import COMMASPACE, formatdate
from email.utils import formatdate
from email import encoders
from burp_reports.lib.imap import ImapReceive
from burp_reports.defaults.default_config import set_defaults

__inventory__ = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..',
                                              'data', 'test_inventory.csv'))

defaults_settings = set_defaults()
defaults_settings['email_inventory']['imap_host'] = 'localhost'
defaults_settings['email_inventory']['imap_password'] = 'pwd1'
defaults_settings['email_inventory']['imap_user'] = 'test1'
defaults_settings['email_inventory']['imap_port'] = '3993'
defaults_settings['email_inventory']['imap_search'] = 'ALL'
config_test = dict(defaults_settings['email_inventory'])

defaults_settings['email_notification']['smtp_port'] = '3025'
defaults_settings['email_notification']['subject'] = 'inventory'
config_smtp = dict(defaults_settings['email_notification'])
# new_smtp_email = EmailNotifications(config=config_smtp, msg="test", attachments=[('utf-8', 'text', 'plain', 'burp_reports/data/test_inventory.csv', 'utf-8')])
# new_smtp_email.send_email()


def send_email():
    msg = MIMEMultipart()
    msg['From'] = "hello@itsme.com"
    msg['Subject'] = 'inventory'
    msg['Date'] = formatdate(localtime=True)
    files = [__inventory__]
    msg.attach(MIMEText("test message"))

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(
            os.path.basename(file)))
        msg.attach(part)

    conn = ImapReceive(config=config_test)
    conn_imap = conn._connect_imap()
    conn_imap.append('INBOX', '',
                     imaplib.Time2Internaldate(time.time()),
                     str(msg.as_string()).encode('utf-8'))

class TestImap:

    def test_connection(self):
        conn = ImapReceive(config=config_test)
        conn_test = conn._connect_imap()
        assert conn_test.check()[0] == 'OK'

    def test_attachment(self):
        send_email()
        imap_receive = ImapReceive(config=config_test)
        if os.path.isfile(imap_receive.save_file):
            os.remove(imap_receive.save_file)

        imap_receive.download_attachment()
        assert os.path.isfile("/tmp/inventory.csv")
