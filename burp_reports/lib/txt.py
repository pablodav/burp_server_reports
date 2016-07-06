
from datetime import datetime, timedelta
from ..lib.humanize import humanize_file_size

class TxtReports:
  
    def __init__(self, clients, file=None):
        """
        
        :param clients: dict of clients formated for burp reports.
        """
        self.clients = clients
        self.file = file

    def print_text(self, client=None, header=None, footer=None, detail=None, comments=None):
        """
        print only header once with client=None, header=True
        header to file:
        print_text(client=None, file=file, header=True)

        :param header: print header
        :param detail: adds detailed print of clients
        """

        jt = 11
        f = None
        
        if self.file:
            if header:
                f = open(self.file, 'w')
            else:
                f = open(self.file, 'a')
                
        if header:
            print('\n burp report'.ljust(jt*9), str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '\n', file=f)

            headers_text = str('Number'[:jt].center(jt)) + str('LastDate'[:jt].center(jt))
            headers_text += str('Time'[:jt].center(jt)) + str('Phase'[:jt].center(jt)) + str('State'[:jt].center(jt))

            if comments:
                headers_text += str('Comments'[:jt].center(jt))

            if detail:
                print('clients'[:jt].rjust(jt), headers_text, 'exclude'[:jt].center(jt),
                      'phase'[:jt].ljust(jt),
                      'phase date  '[:jt].ljust(jt), 'phase status'[:jt].ljust(jt), 'curr log'[:jt].ljust(jt),
                      'log status'[:jt].ljust(jt), 'time taken'[:jt].ljust(jt), 'backup size'[:jt].ljust(jt),
                      'bytes received'[:jt].ljust(jt), '\n', file=f)
            else:
                print(str('Clients'[:jt].rjust(jt+jt+jt)), headers_text, '\n', file=f)

        if client:
            v = client

            client_text = str(self.clients[v].get('b_number', ''))[:jt].center(jt)
            client_text += str(self.clients[v].get('b_last', ''))[:jt].center(jt)
            client_text += str(self.clients[v].get('b_time', ''))[:jt].center(jt)
            client_text += self.clients[v].get('b_phase', '')[:jt].center(jt)
            client_text += self.clients[v].get('b_state', '')[:jt].center(jt)

            if comments:
                client_text += comments[:jt].center(jt)

            if detail:
                s = int(self.clients[v].get('backup_stats', 0).get('time_taken', 0))
                time_taken = str('{:02}:{:02}:{:02}'.format(s//3600, s % 3600//60, s % 60))
                backup_size = int(self.clients[v].get('backup_stats', 0).get('bytes_in_backup', 0))
                bytes_received = int(self.clients[v].get('backup_stats', 0).get('bytes_received', 0))
                print(v[:jt].rjust(jt), client_text,
                      self.clients[v].get('exclude', '')[:jt].center(jt),
                      str(self.clients[v].get('b_phase', ''))[:jt].ljust(jt),
                      str(self.clients[v].get('b_phase_date', ''))[:jt].ljust(jt),
                      '', str(self.clients[v].get('b_phase_status', ''))[:jt].ljust(jt),
                      str(self.clients[v].get('b_log_date', ''))[:jt].ljust(jt),
                      str(self.clients[v].get('b_log_status', ''))[:jt].ljust(jt),
                      str(time_taken)[:jt].ljust(jt),
                      str(humanize_file_size(backup_size))[:jt].ljust(jt),
                      str(humanize_file_size(bytes_received))[:jt].ljust(jt),
                      file=f
                      )
            else:
                print(v.rjust(jt+jt+jt), client_text,
                      file=f
                      )
        if footer:
            if detail:
                print('\n\n'.rjust(jt), ''.center(jt), ''.center(jt), ''.center(jt),
                      ''.center(jt), ''.center(jt), ''.center(jt), ''.ljust(jt),
                      '  '.ljust(jt), ''.ljust(jt), ''.ljust(jt), footer.ljust(jt), '\n', file=f)
            else:
                print(footer, file=f)

    def report_to_txt(self, detail=None):
        """

        :param clients: clients dict with format for burp_reports
        """

        if detail:
            detail = True
        total_taken = 0
        bytes_in_backup = 0
        total_clients = 0
        self.print_text(client=None, header=True, detail=detail)
        
        for k, v in sorted(self.clients.items()):
            client = k
            self.print_text(client, detail=detail)
            
            if detail:
                total_taken += int(self.clients.get(k).get('backup_stats', 0).get('time_taken', 0))
                bytes_in_backup += int((self.clients.get(k).get('backup_stats', 0).get('bytes_in_backup', 0)))
                total_clients += 1
                
        if detail:
            s = total_taken
            foot_notes = str('total time backups taken: {:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
            foot_notes += str('\ntotal size in backup: ')
            foot_notes += str(humanize_file_size(bytes_in_backup))
            foot_notes += str('\nTotal clients: {}'.format(total_clients))
            self.print_text(client=None, footer=foot_notes, detail=detail)
        
        if self.file:
            if os.path.isfile(self.file):
                print('exported to', self.file)
