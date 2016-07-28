# encoding: utf-8
# http://www.magiksys.net/pyzmail/

import pyzmail
import email
import time


def send_email(config, text_msg=None, attachments=None):
    """

    :param text_msg: (str)
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
    filename this is the filename of the attachment, it must be a 'us-ascii' string or a tuple of the form (encoding,
    language, encoded_filename) following the RFC2231 requirement, for example ('iso-8859-1',
    'fr', u'r\xe9pertoir.png'.encode('iso-8859-1'))
    charset : if maintype is 'text', then data must be encoded using this charset. It can be None for non 'text'
    content.


    :return:
    """

    # Define variables to use
    fromaddr = config['email_from']
    toaddr = config['email_to'].split(',')
    smtp_host = config['smtp_server']
    smtp_port = int(config.get('smtp_port', 25))
    smtp_mode = config.get('smtp_mode')
    smtp_login = config.get('smtp_login')
    smtp_password = config.get('smtp_password')

    if not smtp_port:
        smtp_port = 25
    if not smtp_mode:
        smtp_mode = None
    if not smtp_login:
        smtp_login = None
    if not smtp_password:
        smtp_password = None

    sender = fromaddr
    recipients = toaddr
    subject = config.get('subject', 'the subject')
    text_content = text_msg
    preferred_encoding = 'iso-8859-1'
    text_encoding = 'iso-8859-1'
    # date = email.utils.formatdate(time.time(), localtime=True)

    # Compose the email in payload, mail_from, rcpt_to, msg_id
    payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail(
        sender,
        recipients,
        subject,
        preferred_encoding,
        (text_content, text_encoding),
        html=None,
        attachments=attachments)

    # Send the email:
    ret = pyzmail.send_mail(payload, mail_from, rcpt_to, smtp_host,
                            smtp_port=smtp_port, smtp_mode=smtp_mode,
                            smtp_login=smtp_login, smtp_password=smtp_password)

    if isinstance(ret, dict):
        if ret:
            print('failed recipients:', ', '.join(ret.keys()))
        else:
            print('success')
    else:
        print('error:', ret)



