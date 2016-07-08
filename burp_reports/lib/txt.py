
from datetime import datetime, timedelta
from .humanize import humanize_file_size
import os


class TxtReports:
    """
    Formats a dict of clients and prints to stdout or exports to file
    """
  
    def __init__(self, clients, file=None, detail=None, debug=None):
        """
        
        :param clients: dict of clients formated for burp reports.
        :param file: file to export the printed text
        :param detail: Use True when more detailed information is required
        """
        self.clients = clients
        self.file = file
        self.detail = detail
        self.debug = debug

    def format_client_text(self, client=None, header=None, footer=None,  comments=None):
        """
        print only header once with client=None, header=True
        header to file:
        print_text(client=None, file=file, header=True)
        Recommended doc: https://pyformat.info/

        :param client: client_name to report
        :param footer: True/None to report footer information
        :param comments: String text with Additional comments to add to the client
        :param header: True/None to report header formatted
        :param detail: adds detailed information of clients
        :return: client/footer/header str depending on the option choosen
        """

        jt = 11

        # List with dict {header: report_key to use from reports dict}
        client_details = [{'Date': 'b_date'},
                          {'Time': 'b_time'},
                          {'State': 'b_state'},
                          {'Phase': 'b_phase'}
                          ]

        if self.detail:
            # Extend more data to client_details list
            # Will be appended to both: header and data on report
            client_details.append({'exclude': 'exclude'})

        # Format basic header
        if header:
            headers_text = str('\n burp report'.ljust(jt * 9) + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

            # The clients name will be centered if there is detail, so the string starts different for client
            if self.detail:
                headers_text += ' {:>{}.{}} '.format('Name   ', jt, jt)
            else:
                headers_text += ' {:>{}.{}} '.format('Name   ', jt*3, jt)

            # Look on each item on client_details list
            for n in range(len(client_details)):
                detail_dict = client_details[n]
                for k in detail_dict.keys():
                    # Append header from clients_details
                    headers_text += ' {:{}.{}} '.format(k, jt, jt)

            if comments:
                headers_text += ' {:{}.{}} '.format('Comments', jt, jt)

        # Format basic client information for the basic header
        if client:
            # Dict of client only data
            client_data = self.clients[client]

            # The clients name will be centered if there is detail, so the string starts different for client
            if self.detail:
                client_text =  ' {:>{}.{}} '.format(client, jt, jt)
            else:
                client_text = ' {:>{}.{}} '.format(client, jt*3, jt)

            # Look on each item on client_details list
            for n in range(len(client_details)):
                detail_dict = client_details[n]
                for key, value in detail_dict.items():
                    # Add client data to the string client_text using client_details list to fetch keys
                    item_value = client_data.get(value, '')
                    # Check if item value is valid to be a string, if not add empty str value.
                    if not item_value:
                        item_value = ''
                    # Add the value of the item from client dictionary to client_text
                    # :Will put left , .Will truncate
                    client_text += ' {:{}.{}} '.format(item_value, jt, jt)

            if comments:
                client_text += ' {:{}.{}} '.format(comments, jt, jt)

        # Additional details to add on headers and clients to the end of the strings
        if self.detail:

            if header:
                # Additional calculated added data
                headers_text += ' {:{}.{}} '.format('time taken', jt, jt)
                headers_text += ' {:{}.{}} '.format('backup size', jt, jt)
                headers_text += ' {:{}.{}} '.format('bytes received', jt, jt)

            if client:
                # Look into client_data['backup_stats']['time_taken']
                s = int(client_data.get('backup_stats', 0).get('time_taken', 0))
                time_taken = str('{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
                # Look into client_data['backup_stats']['bytes_in_backup']
                backup_size = int(client_data.get('backup_stats', 0).get('bytes_in_backup', 0))
                # Look into client_data['backup_stats']['bytes_received']
                bytes_received = int(client_data.get('backup_stats', 0).get('bytes_received', 0))

                # Additional calculated added data
                client_text += ' {:{}.{}} '.format(time_taken, jt, jt)
                client_text += ' {:{}.{}} '.format(backup_size, jt, jt)
                client_text += ' {:{}.{}} '.format(bytes_received, jt, jt)

        if footer:
            if self.detail:
                footer_text = '\n\n {:{}} \n'.format(footer, jt)
            else:
                footer_text = str(footer)

        # Return formated text
        if header:
            return headers_text
        if client:
            return client_text
        if footer:
            return footer_text

    def print_text(self, client=None, header=None, footer=None):
        """
        print only header once with client=None, header=True
        header to file:
        print_text(client=None, file=file, header=True)

        :param client:
        :param footer:
        :param comments:
        :param header: print header
        """

        jt = 11
        f = None

        if self.file:
            if header:
                f = open(self.file, 'w')
            else:
                f = open(self.file, 'a')

        if header:
            header_text = self.format_client_text(client=None, header=True)
            print(header_text, file=f)

        if client:
            client_text = self.format_client_text(client, header=None)
            print(client_text, file=f)

        if footer:
            footer_text = self.format_client_text(client=None, footer=True)
            print(footer_text, file=f)

    def report_to_txt(self):
        """

        """

        total_taken = 0
        bytes_in_backup = 0
        total_clients = 0
        self.print_text(client=None, header=True)
        
        for client, v in sorted(self.clients.items()):
            client_data = self.clients[client]
            self.print_text(client)
            
            if self.detail:
                total_taken += int(client_data.get('backup_stats', 0).get('time_taken', 0))
                bytes_in_backup += int((client_data.get('backup_stats', 0).get('bytes_in_backup', 0)))
                total_clients += 1
                
        if self.detail:
            s = total_taken
            foot_notes = str('total time backups taken: {:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
            foot_notes += str('\ntotal size in backup: ')
            foot_notes += str(humanize_file_size(bytes_in_backup))
            foot_notes += str('\nTotal clients: {}'.format(total_clients))
            self.print_text(client=None, footer=foot_notes)
        
        if self.file:
            if os.path.isfile(self.file):
                print('exported to', self.file)
