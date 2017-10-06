from datetime import datetime
from .humanize import humanize_file_size
from ..defaults.default_data_structure import default_client_backup_report
import os


class TxtReports:
    """
    Formats a dict of clients and prints to stdout or exports to file
    """

    def __init__(self, clients,
                 file=None,
                 detail=None,
                 additional_columns=None,
                 foot_notes='',
                 format_text=None):
        """
        :param clients: dict of clients formatted for burp reports.
        :param file: file to export the printed text
        :param detail: Use True when more detailed information is required
        :param additional_columns: Add more column in format: {'Column name': 'key'}
                Where 'key' is the key to search in, example: clients['key']
        :param foot_notes: str with more notes in the foot of the text
        :param format_text: dict with some settings for format text like: 
               { 'name_length': '15', 'all_column_length': '11' }
        """
        self.clients = clients
        self.file = file
        self.detail = detail
        self.additional_columns = additional_columns
        self.foot_notes = foot_notes
        self.empty_backup_report = default_client_backup_report()

        # set the format_text dict:
        default_format_text = {
            'name_length': '15',
            'all_column_length': '11'
        }
        
        self.format_text = format_text or default_format_text

    def format_client_text(self, client=None, header=None):
        """
        print only header once with client=None, header=True
        header to file:
        print_text(client=None, file=file, header=True)
        Recommended doc: https://pyformat.info/

        :param client: client_name to report
        :param header: True/None to report header formatted
        :return: client/header str depending on the option chosen
        """

        nlength = int(self.format_text.get('name_length')) # column length for name
        clength = int(self.format_text.get('all_column_length')) # column length for all columns except name
        headers_text = ''
        client_text = ''

        # List with dict {header: report_key to use from reports dict}
        client_details = [{'Date(local)': 'b_date'},
                          {'Time(local)': 'b_time'},
                          {'State': 'b_state'},
                          {'Phase': 'b_phase'}]

        empty_values = ('null', 'Null', 'None')

        if self.additional_columns:
            client_details.append(self.additional_columns)

            # if self.detail:
            # Extend more data to client_details list
            # Will be appended to both: header and data on report
            # client_details.append({'exclude': 'exclude'})

        # Format basic header
        if header:
            headers_text = str('\n burp report'.ljust(clength * 9) + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

            # The clients name will be centered if there is detail, so the string starts different for client
            if self.detail:
                headers_text += ' {:>{}.{}} '.format('Name   ', nlength, nlength)
            else:
                headers_text += ' {:>{}.{}} '.format('Name   ', nlength * 2, nlength)

            # Look on each item on client_details list
            for n in range(len(client_details)):
                detail_dict = client_details[n]
                for k in detail_dict.keys():
                    # Append header from clients_details
                    headers_text += ' {:{}.{}} '.format(k, clength, clength)

            # Add more details from static method
            if self.detail:
                headers_text += self._txt_header_details(clength)

        # Format basic client information for the basic header
        if client:
            # Dict of client only data
            client_data = self.clients[client]

            # The clients name will be centered if there is detail, so the string
            # starts different for client
            if self.detail:
                client_text = ' {:>{}.{}} '.format(client, nlength, nlength)
            else:
                client_text = ' {:>{}.{}} '.format(client, nlength * 2, nlength)

            # Look on each item on client_details list
            for n in range(len(client_details)):
                detail_dict = client_details[n]
                for key, value in detail_dict.items():
                    # Add client data to the string client_text using client_details
                    # list to fetch keys
                    item_value = client_data.get(value, ' --- ')
                    # Check if item value is valid to be a string, if not add empty str value.
                    if not item_value or item_value in empty_values:
                        item_value = ' --- '
                    # Add the value of the item from client dictionary to client_text
                    # :Will put left , .Will truncate
                    client_text += ' {:{}.{}} '.format(item_value, clength, clength)

            # Add more details from static method
            if self.detail:
                client_text += self._txt_client_details(client_data=client_data, clength=clength)

        # Return formatted text
        if header:
            return headers_text
        if client:
            return client_text

    def _foot_notes(self, footer):
        """

        :param footer: (str) to add in foot notes
        :return: str formatted to be in foot_notes
        """
        footer_text = ''

        if self.detail:
            footer_text = '\n\n{}\n'.format(footer)

        if self.foot_notes:
            footer_text += '\n\n{}\n'.format(self.foot_notes)

        return footer_text

    @staticmethod
    def _txt_header_details(clength):
        """

        :param clength: number of spaces to use to justify and format columns
        :return:
        """
        # Additional details to add on headers and clients to the end of the strings
        headers_text = ' {:{}.{}} '.format('Duration', clength, clength)
        headers_text += ' {:{}.{}} '.format('Size', clength, clength)
        headers_text += ' {:{}.{}} '.format('Received', clength, clength)

        return headers_text

    def _txt_client_details(self, client_data, clength):
        """

        :param client_data: dict in burp reports format only for the client you want to get additional details
        :param clength: number of spaces to use to justify and format columns
        :return:
        """
        # Additional details to add on headers and clients to the end of the strings
        # Additional calculated added data
        # Look into client_data['backup_report']['duration']
        s = int(client_data.get('backup_report', self.empty_backup_report).get('duration', 0))
        duration = str('{:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
        # Look into client_data['backup_report']['totsize']
        totsize = int(client_data.get('backup_report', self.empty_backup_report).get('totsize', 0))

        # Look into client_data['backup_report']['received']
        received = int(client_data.get('backup_report', self.empty_backup_report).get('received', 0))

        # Additional calculated added data
        client_text = ' {:^{}} '.format(duration, clength, clength)
        client_text += ' {:<{}} '.format(humanize_file_size(totsize), clength)
        client_text += ' {:<{}} '.format(humanize_file_size(received), clength)

        return client_text

    def __print_text__(self, client=None, header=None, footer=None, print_text=True):
        """
        print only header once with client=None, header=True
        header to file:
        print_text(client=None, file=file, header=True)

        :param client:
        :param footer:
        :param header: print header
        :param print_text: to print or return
        :return: text line if no print_text
        """

        file_obj = None

        if self.file:
            if header:
                file_obj = open(self.file, 'w')
            else:
                file_obj = open(self.file, 'a')

        if header:
            header_text = self.format_client_text(client=None, header=True)
            if print_text:
                print(header_text, file=file_obj)
            else:
                return header_text

        if client:
            client_text = self.format_client_text(client, header=None)
            if print_text:
                print(client_text, file=file_obj)
            else:
                return client_text

        if footer:
            footer_text = self._foot_notes(footer=footer)
            if print_text:
                print(footer_text, file=file_obj)
            else:
                return footer_text

    def report_to_txt(self, print_text=True):
        """
        Method used to format the clients to text in stdout

        """

        total_taken = 0
        totsize = 0
        total_clients = 0
        text_body = ''
        foot_notes = ''

        if print_text:
            self.__print_text__(client=None, header=True)
        else:
            text_body += self.__print_text__(client=None, header=True, print_text=False)
            text_body += '\n'

        for client, v in sorted(self.clients.items()):
            client_data = self.clients[client]

            if print_text:
                self.__print_text__(client)
            else:
                text_body += self.__print_text__(client, print_text=False)
                text_body += '\n'

            if self.detail:
                total_taken += int(client_data.get('backup_report', {}).get('duration', 0))
                totsize += int((client_data.get('backup_report', {}).get('totsize', 0)))
                total_clients += 1

        if self.detail:
            foot_notes = '\n{:>30}  {:02}:{:02}:{:02}'.format('total duration backups taken:',
                                                              total_taken // 3600,
                                                              total_taken % 3600 // 60,
                                                              total_taken % 60)

            foot_notes += "\n{:>30}  {}".format('total size in backup:',
                                                humanize_file_size(totsize))

            foot_notes += '\n{:>30}  {}'.format('Total clients:',
                                                total_clients)

        if foot_notes:

            if print_text:
                self.__print_text__(client=None, footer=foot_notes)
            else:
                text_body += self.__print_text__(client=None, footer=foot_notes, print_text=False)
                text_body += '\n'

        if self.file:
            if os.path.isfile(self.file):
                print('exported to', self.file)

        if not print_text:
            return text_body
