# encoding: utf-8
# http://www.magiksys.net/pyzmail/

import pyzmail


# import email
# import time


class EmailNotifications:
    def __init__(self, config, msg, attachments=None):
        """
        :param msg: (str)
        :param config: (dict) dict with configurations

        {   'email_to': 'root@localhost',
            'smtp_password': '',
            'email_from': 'server@domain.com',
            'smtp_server': 'localhost',
            'smtp_login': '',
            'smtp_mode': 'normal',
            'smtp_port': '25',
        }
        :param attachments: [] files to attach attachments (list) - the list of attachments to include into the mail,
        in the form [(data, maintype, subtype, filename, charset), ..] where :

        data : is the raw data, or a charset encoded string for 'text' content.
        maintype : is a MIME main type like : 'text', 'image', 'application' ....
        subtype : is a MIME sub type of the above maintype for example : 'plain', 'png', 'msword' for respectively
        'text/plain', 'image/png', 'application/msword'.
        filename this is the filename of the attachment, it must be a 'us-ascii' string or a tuple of the form
        (encoding, language, encoded_filename) following the RFC2231 requirement, for example ('iso-8859-1',
        'fr', u'r\xe9pertoir.png'.encode('iso-8859-1'))
        charset : if maintype is 'text', then data must be encoded using this charset. It can be None for non 'text'
        content.
        """

        self.fromaddr = config['email_from']
        self.toaddr = config['email_to'].split(',')
        self.smtp_host = config['smtp_server']
        self.smtp_port = int(config.get('smtp_port', 25))
        self.smtp_mode = config.get('smtp_mode', None)
        self.smtp_login = config.get('smtp_login', None)
        self.smtp_password = config.get('smtp_password', None)

        self.sender = self.fromaddr
        self.recipients = self.toaddr
        self.subject = config.get('subject', 'the subject')

        self.attachments = attachments
        self.msg = msg

    def send_email(self):
        """

        :return: tuple, True/False, details
        """

        payload, mail_from, rcpt_to, msg_id = self.compose_email()

        # Send the email:
        ret = pyzmail.send_mail(payload, mail_from, rcpt_to,
                                smtp_host=self.smtp_host,
                                smtp_port=self.smtp_port,
                                smtp_mode=self.smtp_mode,
                                smtp_login=self.smtp_login,
                                smtp_password=self.smtp_password)

        if isinstance(ret, dict):
            if ret:
                return False, 'failed recipients:', ', '.join(ret.keys())
            else:
                return True, 'success'
        else:
            return False, 'error:', ret

    def compose_email(self):
        # Define variables to use

        text_content = self.msg
        preferred_encoding = 'iso-8859-1'
        text_encoding = 'iso-8859-1'
        # date = email.utils.formatdate(time.time(), localtime=True)
        # Compose the email in payload, mail_from, rcpt_to, msg_id

        payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail(
            self.sender,
            self.recipients,
            self.subject,
            preferred_encoding,
            (text_content, text_encoding),
            html=None,
            attachments=self.attachments)

        return payload, mail_from, rcpt_to, msg_id
