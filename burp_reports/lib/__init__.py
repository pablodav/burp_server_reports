

def print_text(client, file=None, header=None, footer=None, detail=None, comments=None):
    """
    print only header once with client=None, header=True
    header to file:
    print_text(client=None, file=file, header=True)

    :param client: dict with clients (check burp_client_status())
    :param file: output file
    :param header: print header
    :param detail: adds detailed print of clients
    """
    jt = 11
    f = None
    if file:
        if header:
            f = open(file, 'w')
        else:
            f = open(file, 'a')
    if header:
        print('\n burp report'.ljust(jt*9), str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '\n', file=f)

        headers_text = str('Number'[:jt].center(jt)) + str('Date'[:jt].center(jt))
        headers_text += str('Time'[:jt].center(jt)) + str('Type'[:jt].center(jt)) + str('Status'[:jt].center(jt))

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

        client_text = str(clients_list[v].get('b_number', ''))[:jt].center(jt)
        client_text += str(clients_list[v].get('b_date', ''))[:jt].center(jt)
        client_text += str(clients_list[v].get('b_time', ''))[:jt].center(jt)
        client_text += clients_list[v].get('b_type', '')[:jt].center(jt)
        client_text += clients_list[v].get('b_status', '')[:jt].center(jt)

        if comments:
            client_text += comments[:jt].center(jt)

        if detail:
            s = int(clients_list[v].get('backup_stats', 0).get('time_taken', 0))
            time_taken = str('{:02}:{:02}:{:02}'.format(s//3600, s % 3600//60, s % 60))
            backup_size = int(clients_list[v].get('backup_stats', 0).get('bytes_in_backup', 0))
            bytes_received = int(clients_list[v].get('backup_stats', 0).get('bytes_received', 0))
            print(v[:jt].rjust(jt), client_text,
                  clients_list[v].get('exclude', '')[:jt].center(jt),
                  str(clients_list[v].get('b_phase', ''))[:jt].ljust(jt),
                  str(clients_list[v].get('b_phase_date', ''))[:jt].ljust(jt),
                  '', str(clients_list[v].get('b_phase_status', ''))[:jt].ljust(jt),
                  str(clients_list[v].get('b_log_date', ''))[:jt].ljust(jt),
                  str(clients_list[v].get('b_log_status', ''))[:jt].ljust(jt),
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