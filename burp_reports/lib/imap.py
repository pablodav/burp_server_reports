# encoding: utf-8
# https://docs.python.org/3.5/library/imaplib.html#imap4-example
# https://gist.github.com/jasonrdsouza/1674794

import imaplib
import email
import os
import arrow


class ImapReceive:
    def __init__(self, config):
        """
        :param msg: (str)
        :param config: (dict) dict with configurations

        {   'imap_host': 'hostname',
            'imap_password': 'password',
            'imap_user': 'username', # You can use 'domain\\user'
            'imap_folder': 'INBOX',
            'email_subject': 'inventory',
            'imap_search': 'TODAY', # TODAY will set today date in
            format: "SENTON 23-Sep-2017 Subject \"inventory\""
            # you could filter using the IMAP rules here (check
            # http://www.example-code.com/csharp/imap-search-critera.asp)
            'imap_port': '993',
            'attachment_save_directory': '/tmp',
            'attachment_filename': 'inventory.csv'
        }

        """

        self.host = config['imap_host']
        self.user = config['imap_user']
        self.password = config['imap_password']
        self.imap_folder = config['imap_folder'] or 'INBOX'
        self.email_subject = config['email_subject'] or 'inventory'
        self.imap_search = config['imap_search'] or 'TODAY'
        self.imap_port = config['imap_port'] or '993'
        self.save_directory = config['attachment_save_directory'] or '.'
        self.filename = config['attachment_filename'] or 'inventory.csv'
        self.save_file = os.path.join(self.save_directory, self.filename)

        if config['imap_search'] == 'TODAY':
            today_string = arrow.now().format('DD-MMM-YYYY')
            self.imap_search = "SENTON {} Subject \"{}\"".format(today_string, self.email_subject)

    def _connect_imap(self):

        conn = imaplib.IMAP4_SSL(self.host, self.imap_port)
        conn.login(self.user, self.password)
        conn.select(self.imap_folder)

        return conn

    def download_attachment(self):

        conn = self._connect_imap()

        # results,data = conn.search(None,'ALL')
        # resp, data = conn.search(None, "ALL") # you could filter using the IMAP rules here
        # (check http://www.example-code.com/csharp/imap-search-critera.asp)
        resp, data = conn.search(None, self.imap_search)

        msg_ids = data[0]
        msg_id_list = msg_ids.split()

        for emailid in msg_id_list:
            # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for
            # headers only, etc
            resp, data = conn.fetch(emailid, "(RFC822)")
            email_body = data[0][1] # getting the mail content
            # mail = email.message_from_string(email_body) # parsing the mail content to get a
            # mail object
            mail = email.message_from_bytes(email_body)  # parsing the mail content to
            # get a mail object python3
            # https://docs.python.org/3.5/library/email.html

            #Check if any attachments at all
            if mail.get_content_maintype() != 'multipart':
                continue

            #    print ("["+mail["From"]+"] :" + mail["Subject"])

            # we use walk to create a generator so we can iterate on the parts and forget
            # about the recursive headach
            for part in mail.walk():
                # multipart are just containers, so we skip them
                if part.get_content_maintype() == 'multipart':
                    continue

                # is this part an attachment ?
                if part.get('Content-Disposition') is None:
                    continue

                #filename = part.get_filename()
                #filename = mail["From"] + "_hw1answer"

                att_path = self.save_file

                #Check if its already there
                #if not os.path.isfile(att_path):

                # finally write the stuff
                with open(att_path, 'wb') as file_open:
                    file_open.write(part.get_payload(decode=True))
                # Save the attachment only for one file
                break

        conn.close()
