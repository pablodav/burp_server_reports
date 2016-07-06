
from datetime import datetime, timedelta
from ..lib.humanize import humanize_file_size
import os

class TxtReports:
    """
    Formats a dict of clients and prints to stdout or exports to file
    """
  
    def __init__(self, clients, file=None, detail=None):
        """
        
        :param clients: dict of clients formated for burp reports.
        :param file: file to export the printed text
        :param detail: Use True when more detailed information is required
        """
        self.clients = clients
        self.file = file
        self.detail = detail

    def format_client_text(self, client=None, header=None, footer=None,  comments=None):
        """
        print only header once with client=None, header=True
        header to file:
        print_text(client=None, file=file, header=True)

        :param client: client_name to report
        :param footer: True/None to report footer information
        :param comments: String text with Additional comments to add to the client
        :param header: True/None to report header formatted
        :param detail: adds detailed information of clients
        :return: client/footer/header depending on the option choosen
        """

        jt = 11
        
        detail = self.detail

        # List with dict {header: report_key to use from reports dict}
        client_details = [{'LastDate': 'b_last'},
                          {'Phase': 'b_phase'},
                          {'State': 'b_state'}
                          ]

        if detail:
            # Extend more data to client_details list
            # Will be appended to both: header and data on report
            client_details.append({'exclude': 'exclude'})

        # Format basic header
        if header:
            headers_text = str('\n burp report'.ljust(jt * 9) + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

            # The clients name will be centered if there is detail, so the string starts different for client
            if detail:
                headers_text += str('Name'[:jt].rjust(jt))
            else:
                headers_text += str('Name'[:jt].rjust(jt+jt+jt))

            # Look on each item on client_details list
            for n in range(len(client_details)):
                detail_dict = client_details[n]
                for k in detail_dict.keys():
                    # Append header from clients_details
                    headers_text += str(k)[:jt].center(jt)

            if comments:
                headers_text += str('Comments'[:jt].center(jt))

        # Format basic client information for the basic header
        if client:
            # Dict of client only data
            client_data = self.clients[client]

            # The clients name will be centered if there is detail, so the string starts different for client
            if detail:
                client_text =  str(client[:jt].rjust(jt))
            else:
                client_text = str(client[:jt].rjust(jt + jt + jt))

            # Look on each item on client_details list
            for n in range(len(client_details)):
                detail_dict = client_details[n]
                for key, value in detail_dict.items():
                    # Add client data to the string client_text using client_details list to fetch keys
                    client_text += str(self.client_data.get(value, '')[:jt].center(jt))

            if comments:
                client_text += comments[:jt].center(jt)

        # Additional details to add on headers and clients to the end of the strings
        if detail:

            if header:
                # Additional calculated added data
                headers_text += str('time taken'[:jt].ljust(jt))
                headers_text += str('backup size'[:jt].ljust(jt) + 'bytes received'[:jt].ljust(jt))

            if client:
                # Look into client_data['backup_stats']['time_taken']
                s = int(self.client_data.get('backup_stats', 0).get('time_taken', 0))
                time_taken = str('{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
                # Look into client_data['backup_stats']['bytes_in_backup']
                backup_size = int(self.client_data.get('backup_stats', 0).get('bytes_in_backup', 0))
                # Look into client_data['backup_stats']['bytes_received']
                bytes_received = int(self.client_data.get('backup_stats', 0).get('bytes_received', 0))

                # Additional calculated added data
                client_text += str(time_taken)[:jt].ljust(jt)
                client_text += str(humanize_file_size(backup_size))[:jt].ljust(jt)
                client_text += str(humanize_file_size(bytes_received))[:jt].ljust(jt)

        if footer:
            if detail:
                footer_text = str('\n\n'.rjust(jt) + ''.center(jt) + ''.center(jt) + ''.center(jt))
                footer_text += str(''.center(jt) + ''.center(jt) + ''.center(jt) + ''.ljust(jt))
                footer_text += str('  '.ljust(jt) + ''.ljust(jt) + ''.ljust(jt), footer.ljust(jt) + '\n')
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

        if self.detail:
            detail = True
            
        total_taken = 0
        bytes_in_backup = 0
        total_clients = 0
        self.print_text(client=None, header=True)
        
        for client, v in sorted(self.clients.items()):
            client_data = self.clients[client]
            self.print_text(client)
            
            if detail:
                total_taken += int(client_data.get('backup_stats', 0).get('time_taken', 0))
                bytes_in_backup += int((client_data.get('backup_stats', 0).get('bytes_in_backup', 0)))
                total_clients += 1
                
        if detail:
            s = total_taken
            foot_notes = str('total time backups taken: {:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
            foot_notes += str('\ntotal size in backup: ')
            foot_notes += str(humanize_file_size(bytes_in_backup))
            foot_notes += str('\nTotal clients: {}'.format(total_clients))
            self.print_text(client=None, footer=foot_notes)
        
        if self.file:
            if os.path.isfile(self.file):
                print('exported to', self.file)
