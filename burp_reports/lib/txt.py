
def report_to_txt(clients, file=None, detail=None):

    if detail:
        detail = True
    total_taken = 0
    bytes_in_backup = 0
    total_clients = 0
    print_text(client=None, file=file, header=True, detail=detail)
    for k, v in sorted(clients_list.items()):
        client = k
        print_text(client, file, detail=detail)
        if detail:
            total_taken += int(clients_list.get(k).get('backup_stats', 0).get('time_taken', 0))
            bytes_in_backup += int((clients_list.get(k).get('backup_stats', 0).get('bytes_in_backup', 0)))
            total_clients += 1
    if detail:
        s = total_taken
        foot_notes = str('total time backups taken: {:02}:{:02}:{:02}'.format(s // 3600, s % 3600 // 60, s % 60))
        foot_notes += str('\ntotal size in backup: ')
        foot_notes += str(humanize_file_size(bytes_in_backup))
        foot_notes += str('\nTotal clients: {}'.format(total_clients))
        print_text(client=None, file=file, footer=foot_notes, detail=detail)
    if file:
        if os.path.isfile(file):
            print('exported to', file)
