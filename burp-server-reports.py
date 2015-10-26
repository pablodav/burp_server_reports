#!/usr/bin/python3
# This script will generate list of outdated
# Create folders /usr/local/share/burp-custom and /var/log/burp-custom
# chmod +x the py file
# Locate this file in  /usr/local/share/burp-custom/burp-custom-reports.py
# link to if desired ln -s /usr/local/share/burp-custom/burp-custom-reports.py /usr/local/bin/burp-custom-reports

""" Notes to add later:
http://staticjinja.readthedocs.org/en/latest/user/advanced.html
http://www.decalage.info/python/html
https://plot.ly/python/bar-charts-tutorial/
"""

# send_to={{ burp_server_send_to }}
# send_from={{ burp_server_send_from }}

import os
import re
import csv
# import sys
# import pprint
import json
import platform
# import pickle
from datetime import datetime, timedelta
from collections import deque

today_date = datetime.now().strftime('%Y-%m-%d')
log_timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
clients_list = {}


""" --- Creating empty dictionary:

"""


def get_file_m_date(file):
    """
    Return date of such file

    :param file:
    :return: YYYY-MM-DD
    """
    file_time = os.path.getmtime(file)
    file_time = datetime.fromtimestamp(file_time)
    file_time = file_time.strftime('%Y-%m-%d')
    return file_time


def date_check_status(backup_date):
    """
    Comares date YYYY-MM-DD with n_days_ago
    uses date_regexp to extract only YYYY-MM-DD

    :param backup_date:
    :return: ok / outdated
    """
    date_regexp = re.compile(r'''(
        \d{4}    #Year
        (-)?  #Separator
        \d{2}     #Month
        (-)?  #Separator
        \d{2}     #Day
    )''', re.VERBOSE)
    client_date = date_regexp.search(backup_date).group()
    if client_date >= n_days_ago:
        return 'ok'
    else:
        return 'outdated'


def get_time_stamp(client_path):
    """
    #  https://github.com/grke/burp/blob/master/docs/working_dir.txt
    #  http://burp.grke.org/docs/shuffling.html
    During backup phases 3 (manifest generation) and 4 (shuffling), the symlink
    will be renamed to 'finishing':

    /var/spool/burp/<client>/finishing -> 0000027 2015-04-12 01:24:29

    :param client_path:
    :return: reads timestamp file by status, expected file content:
    0000035 2015-07-16 03:08:08
    """
    burp_links = ('finishing', 'current')
    timestamp = ''
    time_stamp_file = os.path.join(client_path)
    for i in range(len(burp_links)):
        time_stamp_file = os.path.join(client_path, burp_links[i], 'timestamp')
        if os.path.isfile(time_stamp_file):  # only works on current or finishing
            timestamps = open(time_stamp_file)
            timestamp = timestamps.read()
            timestamps.close()
        if timestamp:
            return burp_links[i] + ' ' + timestamp
        else:
            continue
    print('WARNING: client timestamp file ', time_stamp_file,
          'exit get_time_stamp function without reading timestamp. ', timestamp)
    return None


def get_client_working_status(client_path):
    """
    #  https://github.com/grke/burp/blob/master/docs/working_dir.txt
    #  http://burp.grke.org/docs/shuffling.html

    During backup phases 1 (file system scan) and 2 (send actual data), there will
    be a symlink pointing to the directory called 'working':

    /var/spool/burp/<client>/working -> 0000027 2015-04-12 01:24:29

    burp_phase_dict = {
    }

    :param client_path:
    :return: burp_phase_dict
    """
    burp_phases = ('phase2', 'phase1')
    burp_phase_dict = {}
    burp_phase = ''
    for i in range(len(burp_phases)):
        # Set link name to use for each phase
        if burp_phases[i] == 'phase2' or burp_phases[i] == 'phase1':
            phase_link = 'working'
        # Use link to path to phase file
        phase_file = os.path.join(client_path, phase_link, burp_phases[i])
        # Get data from the phase
        if os.path.isfile(phase_file):
            burp_phase = burp_phases[i]
            burp_phase_date = get_file_m_date(phase_file)
            burp_phase_status = date_check_status(burp_phase_date)  # Will be ok or outdated
            # Create the dict with data collected
            burp_phase_dict.setdefault('b_phase', burp_phase)
            burp_phase_dict.setdefault('b_phase_date', burp_phase_date)
            burp_phase_dict.setdefault('b_phase_status', burp_phase_status)
            # Return with the first phase found
            return burp_phase_dict
        else:
            burp_phase = 'unknown'
    # Will return unknown phase if did not find any file known
    burp_phase_dict.setdefault('b_phase', burp_phase)
    return burp_phase_dict


def burp_client_status():
    """
    Version 1 of burp only supported for this function
    It doesn't use burp -a s, it looks into directory structure of burp 1 and also uses files:
        log, timestamp and backup_stats.

    This is the most important function, it creates a dictionary with the status of all clients and collects
    many information about them, also collects backup_statistics file and puts it on the dictionary.
    At the moment it is done for burp 1.x
    Format that will be used:
    clients_list = {'client_name':
        { 'b_number'  : 'number',
          'b_date'    : 'date',
          'b_status'  : 'outdated/ok',
          'b_type'    : 'finishing/working/current',
          'quota'   : 'ok/soft/hard',
          'warnings': 'warnings',
          'exclude' : 'yes/no',
          'b_phase' : 'phase1/phase2',
          'b_phase_date' : 'date',
          'b_phase_status' : 'outdated/ok',
          'b_log_date' : 'date of log file',
          'b_log_status' : 'outdated/ok',
          'b_curr_taken' : 'seconds',
          'backup_stats' : {'contents': 'all contents of backup_stats file for the client'}
        }
    }
    Example of a complete dict:
        backup_stats comes from client/current/backups_stats file

    {"client_x": {"b_phase": null, "b_time": "14:06:08", "b_log_status": "ok", "exclude": "no",

    "backup_stats": {"special_files_deleted": "0", "total": "0", "vss_headers_changed": "0",
    "vss_headers_encrypted": "0", "vss_footers_changed": "0", "files_encrypted_total": "0", "files_changed": "18",
    "files_encrypted_deleted": "0", "files_deleted": "0", "efs_files": "0", "soft_links_changed": "0",
    "hard_links_same": "0", "efs_files_same": "0", "files_encrypted_scanned": "0", "meta_data_scanned": "0",
    "directories_total": "0", "soft_links_deleted": "0", "vss_footers_deleted": "0", "special_files_total": "0",
    "files": "0", "server_version": "1.4.34", "vss_headers_encrypted_total": "0", "total_total": "4238",
    "meta_data_encrypted_same": "0", "time_start": "1434387966", "directories": "0", "vss_footers_encrypted_same":
    "0", "total_changed": "18", "vss_headers_encrypted_deleted": "0", "bytes_in_backup": "2565998015",
    "vss_headers_encrypted_changed": "0", "meta_data_encrypted_total": "0", "total_scanned": "4238", "meta_data": "0",
    "meta_data_same": "0", "meta_data_encrypted_scanned": "0", "hard_links_scanned": "0", "files_encrypted_same": "0",
    "files_encrypted": "0", "files_encrypted_changed": "0", "vss_headers": "0", "efs_files_total": "0",
    "directories_same": "0", "efs_files_changed": "0", "meta_data_encrypted_changed": "0", "directories_scanned": "0",
    "vss_headers_total": "0", "meta_data_changed": "0", "bytes_sent": "0", "meta_data_total": "0", "vss_headers_same":
    "0", "files_same": "4220", "soft_links": "0", "vss_footers": "0", "efs_files_deleted": "0",
    "special_files_scanned": "0", "vss_footers_encrypted_deleted": "0", "bytes_received": "6607775",
    "directories_deleted": "0", "total_deleted": "0", "special_files": "0", "total_same": "4220",
    "files_total": "4238", "vss_headers_encrypted_same": "0", "vss_headers_scanned": "0",
    "vss_footers_encrypted": "0", "vss_headers_deleted": "0", "soft_links_same": "0", "vss_footers_same": "0",
    "warnings": "60", "vss_footers_encrypted_total": "0", "special_files_same": "0", "meta_data_encrypted": "0",
    "efs_files_scanned": "0", "client": "client_x", "meta_data_deleted": "0", "hard_links": "0", "time_taken": "174",
    "vss_footers_encrypted_changed": "0", "hard_links_deleted": "0", "vss_footers_scanned": "0",
    "vss_headers_encrypted_scanned": "0", "files_scanned": "4238", "soft_links_scanned": "0",
    "vss_footers_encrypted_scanned": "0", "hard_links_changed": "0", "vss_footers_total": "0",
    "special_files_changed": "0", "client_is_windows": "1", "directories_changed": "0", "hard_links_total": "0",
    "bytes_estimated": "2564874175", "meta_data_encrypted_deleted": "0", "soft_links_total": "0",
    "time_end": "1434388140"},

    "b_status": "ok", "b_type": "current", "b_phase_date": null,
    "b_date": "2015-06-15", "b_log_date": "2015-06-15", "b_phase_status": null, "b_number": "0000005"},
    :rtype : dict
    """
    burp_clients = []
    l_clients_list = {}
    try:
        burp_clients = os.listdir(burp_client_confdir)  # Get list of clients from ls in clientconfdir
    except PermissionError:
        print('Permission denied in' + burp_client_confdir)
        exit()
    except:
        print('Could not list folders in' + burp_client_confdir)
        exit()
    for c in burp_clients:
        b_status = ''
        b_date = ''
        b_number = 0
        b_time = ''
        client = c
        b_phase = ''
        b_type = ''
        b_phase_date = ''
        b_phase_status = ''
        b_log_date = ''
        b_log_status = ''
        stats_dict = {}
        if (client == 'incexc') or (client == 'profiles'):  # Ignore incexc and profiles folders
            continue
        client_path = os.path.join(burp_directory, client)
        if os.path.isdir(client_path):
            timestamp = get_time_stamp(client_path)  # call function to get data from timestamp
            # It will get timestamp from finishing or current. and gives working status if there is working
            if timestamp:
                timestamp = timestamp.split()  # Set list timestamp example:
                # ['current', '0000008', '2015-05-18', '05:49:01' ]
                b_type = timestamp[0]
                b_date = timestamp[2]
                b_status = date_check_status(b_date)
                b_time = timestamp[3]
                b_number = timestamp[1]
            else:
                print('WARNING: client', client_path, ' exit without timestamp')

            stats_links = ('current', 'finishing')
            for i in range(len(stats_links)):
                if os.path.isfile(os.path.join(client_path, stats_links[i], 'backup_stats')):
                    # Creates dict of backup_stats file for each client
                    stats_file = os.path.join(client_path, stats_links[i], 'backup_stats')
                    stats_dict = parse_config(filename=stats_file, stats=True)

            #  Get data status of client when working status
            working_link = os.path.join(client_path, 'working')
            if os.path.islink(working_link):
                b_type = 'working'
                burp_phase_status = get_client_working_status(client_path)  # get client working phase
                b_phase = burp_phase_status.get('b_phase', '')  #
                b_phase_date = burp_phase_status.get('b_phase_date', '')
                b_phase_status = burp_phase_status.get('b_phase_status', '')

            if os.path.isfile(os.path.join(client_path, 'current', 'log.gz')):
                b_log_date = get_file_m_date(os.path.join(client_path, 'current', 'log.gz'))
                b_log_status = date_check_status(b_log_date)

            # Get some details from working/log file and set b_log_status
            working_log = os.path.join(client_path, 'working', 'log')
            if os.path.isfile(working_log):
                with open(working_log, 'r') as f:
                    tail_content = deque(f, 10)
                    content_full = f.read()
                content = ''.join(tail_content)
                resume_errors = ["/working/unchanged: No such file or directory",
                                 "working/phase1.gz: No such file or directory",
                                 "gzwrite failed: 0!=-1"]
                client_reset_error = 'SSL read problem: 5, errno=104 (Connection reset by peer)'
                if 'working_dir_recovery_method: resume' in content:
                    b_log_status = "Resume started"
                if 'Resume previously resumed' in content:
                    b_log_status = "In resume"
                if 'soft quota exceeded' in content_full:
                    b_log_status = 'soft quota excee'
                # DETECTING: Generic error in log
                if 'error in backup phase 2' in content:
                    b_log_status = 'with err'
                    if 'Connection timed out' in content:
                        b_log_status = 'dis timeout'
                # DETECTING: Resume errors
                for msg in resume_errors:
                    if msg in content:
                        b_log_status = 'Resume err'
                # DETECTING: client reset
                if 'error in backup phase 2' in content:
                    if client_reset_error in content:
                        b_log_status = "cli reset"
                # DETECTING: Quota exceeded
                if 'hard quota exceeded' in content_full:
                    b_log_status = 'hard quota excee'
                    b_status = 'outdated'
            else:
                # If not log file on working
                b_log_status = ''

        else:
            # If there is no client folder in storage/burp backup
            # Verifies the date and status of added client to client_confdir
            b_number = "None"
            b_date = "None"
            client_conf_dir = os.path.join(burp_client_confdir, client)
            file_time = get_file_m_date(client_conf_dir)
            file_status = date_check_status(file_time)
            if file_status == 'ok':
                b_status = 'new'
                b_type = 'not started'
            else:
                b_status = 'UNKNOWN'
                b_type = "never"

        if b_status == 'outdated':
            if is_up(client):
                b_phase_status = "ping ok"

        if client in config_excluded_clients:
            excluded = 'yes'
        else:
            excluded = 'no'

        # Setup dictionary values based on processed information of the client

        l_clients_list.setdefault(client, {})['b_status'] = b_status
        l_clients_list.setdefault(client, {})['b_date'] = b_date
        l_clients_list.setdefault(client, {})['b_time'] = b_time
        l_clients_list.setdefault(client, {})['b_number'] = b_number
        l_clients_list.setdefault(client, {})['b_type'] = b_type
        l_clients_list.setdefault(client, {})['exclude'] = excluded
        l_clients_list.setdefault(client, {})['b_phase'] = b_phase
        l_clients_list.setdefault(client, {})['b_phase_date'] = b_phase_date
        l_clients_list.setdefault(client, {})['b_phase_status'] = b_phase_status
        l_clients_list.setdefault(client, {})['b_log_date'] = b_log_date
        l_clients_list.setdefault(client, {})['b_log_status'] = b_log_status
        l_clients_list[client].update({'backup_stats': stats_dict})
    return l_clients_list


def report_outdated(file=None, detail=None, email=None):
    """

    :param file: file to export outdated
    :param detail: export / or send email with details
    :param email: send email with outdated
    :return:
    """
    if file == 'print':
        file = None
    if detail:
        detail = True
    # fix missing file parameter when sending emails without file
    if email and not file:
        import socket
        server_name = socket.gethostname()
        file_name = server_name + '_burp_outdated.txt'
        file = os.path.join(os.sep, 'tmp', file_name)

    reports_config = parse_config(burp_custom_file)
    outdated_notes = reports_config.get('outdated_notes', None)

    print('reporting outdated for clients_list: \n', file)
    print_text(client=None, file=file, header=True, detail=detail, comments=True)

    outd_count = 0
    for v in sorted(clients_list.keys()):
        client = v
        if clients_list[v]['exclude'] == 'yes':  # Do not report excluded
            continue
        if clients_list[v]['b_status'] != 'ok':
            outd_count += 1
            if "hard quota" in clients_list[v]['b_log_status']:
                print_text(client, file, detail=detail, comments='Hard quota')
            else:
                print_text(client, file, detail=detail, comments=' - ')
        elif "soft quota" in clients_list[v]['b_log_status']:
            print_text(client, file, detail=detail, comments='Soft quota')

    if outd_count != 0:
        if file:
            if os.path.isfile(file):
                print('exported to', file)
                foot_notes = str('\n\nTotal clients outdated: {} '.format(outd_count))
                if outdated_notes:
                    foot_notes = foot_notes + "\n\n" + str(outdated_notes)
                print_text(client=None, file=file, footer=foot_notes, detail=None)
        if email:
            send_email(text_file=file)
    else:
        print('Not outdated clients found, does nothing')


def send_email(text_file):
    import smtplib
    # Import modules need for mime text
    from email.mime.text import MIMEText

    # Get configuration from burp_custom_file
    reports_config = parse_config(burp_custom_file)
    fromaddr = reports_config.get('emails_from', None)
    toaddr = reports_config.get('emails_to', None)
    if not toaddr or not fromaddr:
        print('Not defined emails_from or not defined emails_to in:', burp_custom_file)
        exit()
    smtp_server = reports_config.get('smtp_server', None)
    if not smtp_server:
        print('smtp_server not defined in:', burp_custom_file)
        exit()

    # Add the From: and To: headers at the start
    # msg = ("From: %s\r\nTo: %s\r\n\r\n"
    #        % (fromaddr, ", ".join(toaddr)))
    # body = "This is a body test"
    with open(text_file) as fp:
        # Create a text/plain message
        msg = MIMEText(fp.read())
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['subject'] = 'Sending content of file %s' % text_file
    server = smtplib.SMTP('10.196.81.38')
    server.set_debuglevel(1)
    server.send_message(msg)
    server.quit()


def report_to_txt(file=None, detail=None):
    if not file or file == 'default':
        file = txt_clients_status
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
        foot_notes = str('total time backups taken: {:02}:{:02}:{:02}'.format(s//3600, s % 3600//60, s % 60))
        foot_notes += str('\ntotal size in backup: ')
        foot_notes += str(humanize_file_size(bytes_in_backup))
        foot_notes += str('\nTotal clients: {}'.format(total_clients))
        print_text(client=None, file=file, footer=foot_notes, detail=detail)
    if file:
        if os.path.isfile(file):
            print('exported to', file)


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


def automation_fixes():
    for k, v in sorted(clients_list.items()):
        client = k
        # Delete working symlink and dir if there is resume error
        if clients_list[client].get('b_log_status') == 'Resume err':
            working_symlink = os.path.join(burp_directory, client, 'working')
            if os.path.exists(working_symlink):
                rm_command = 'rm -rfv "$(readlink -f ' + working_symlink + ')"'
                os.system(rm_command)
                os.remove(working_symlink)
                clients_list.setdefault(client, {})['b_log_status'] = 'fixed_res1'


def load_csv_data(csv_filename=None):
    if not csv_filename:
        csv_filename = csv_file_data
    if os.path.isfile(csv_filename):
        print('Loading', csv_filename, 'and ignoring first row')
    else:
        return str('we could not read the source csv:', csv_filename)
    csv_rows = []
    csv_file_obj = open(csv_filename)
    reader_obj = csv.reader(csv_file_obj, delimiter=';')
    for row in reader_obj:
        if reader_obj.line_num == 1:
            continue  # skip first row
        csv_rows.append(row)
    return csv_rows


def save_csv_data(csv_rows=None, csv_filename=None):
    if not csv_filename or csv_filename == "default":
        csv_filename = csv_file_data_export
    if not csv_rows:
        return 'There are no csv rows to write'
    print('saving to csv file:', csv_filename)
    csv_file_obj = open(csv_filename, 'w', newline='')
    csv_writer = csv.writer(csv_file_obj, delimiter=';')
    for row in csv_rows:
        csv_writer.writerow(row)
    csv_file_obj.close()
    if csv_filename:
        if os.path.isfile(csv_filename):
            print('exported to:', csv_filename)


def inventory_compare(csv_filename=None):
    import socket
    server_name = socket.gethostname()
    if not csv_filename or csv_filename == "default":
        inventory = load_csv_data()
    else:
        inventory = load_csv_data(csv_filename)
    csv_rows_inventory_status = [['client', 'status', 'server' 'inv_status', 'sub_status']]
    for i in range(len(inventory)):
        client, status, det_status = inventory[i][0:3]
        if client in clients_list:
            if det_status.lower() == 'spare':
                burp_status = 'wrong spare in burp'
            elif status.lower() != 'active':
                burp_status = 'wrong not active'
            else:
                burp_status = clients_list[client]['b_status']
        elif det_status.lower() == 'spare':
            burp_status = 'ignored spare'
        else:
            burp_status = 'absent'
        row = inventory[i]
        row.insert(1, burp_status)
        row.insert(2, server_name)
        csv_rows_inventory_status.append(row)
    return csv_rows_inventory_status

def parse_config(filename, stats=None):
    """

    :param filename: file name to parse config
    :param stats: only use it to stats file with separator :
    :return: dict with options
    """
    options = {}
    comment_char = '#'
    option_char = '='
    stats_char = ':'
    f = open(filename)
    for line in f:
        # First, remove comments:
        if comment_char in line:
            # split on comment char, keep only the part before
            line, comment = line.split(comment_char, 1)
        # Second, find lines with an option=value:
        if option_char in line and not stats:
            # split on option char:
            option, value = line.split(option_char, 1)
        elif stats_char in line and stats:
            option, value = line.split(stats_char, 1)
        else:
            continue
        if option and value:
            # strip spaces:
            option = option.strip()
            value = value.strip()
            # store in dictionary:
            options[option] = value
    f.close()
    return options


def reports_config_global(burp_custom=None, example=None):
    """
    Creates global variables to use by the script

    if exist /etc/burp/burp-custom-reports.conf uses parameters from that file

    Example config file:
    burp_automation_folder = /storage/samba/automation
    # csv_file_to compare with external inventory:
    csv_file_data = /storage/samba/automation/inventory.csv
    days_outdated = 31
    outedated_notes = "some notes for your emails"
    burp_www_reports = /var/www/html
    # burp_www_reports, is output place for example files:
    # /var/www/html/inventory_status.csv /var/www/html/clients_status.txt
    json_clients_file = /var/spool/burp/clients_status.json

    If emails will be sent:
    emails_to = email@domain.x
    emails_from = email@domain.x
    smtp_server = ip/name


    :param burp_custom: path to use for config of this script
    :param example: prints an example to create your own burp-custom-reports.conf file
    :return:
    """
    global burp_automation_folder
    global n_days_ago
    global csv_file_data_export
    global txt_clients_status
    global csv_file_data
    global json_clients_status
    global burp_www_reports
    global config_excluded_clients
    # Global to parse to help TODO:change it to return and try to use classes if possible and there is time for it :)
    global burp_custom_file
    if not burp_custom:
        burp_custom_file = os.path.join(os.sep, 'etc', 'burp', 'burp-custom-reports.conf')
    else:
        burp_custom_file = burp_custom
    # ###### ------------ BURP custom reports variables -------------------- #########
    if os.path.isfile(burp_custom_file):
        if not example:
            print('Loading configuration: ', burp_custom_file)
        # GET FROM burp_custom_file:
        reports_config = parse_config(burp_custom_file)
        # burp automation folder for files in use with list of clients and other with automation tasks.
        # - option: burp_automation_folder = default = /storage/samba/automation
        burp_automation_folder = reports_config.get('burp_automation_folder', '/storage/samba/automation')
        days_outdated = reports_config.get('days_outdated', 31)
        days_outdated = int(str(days_outdated))
        burp_www_reports = reports_config.get('burp_www_reports', '/var/www/html')
        json_clients_status = reports_config.get('json_clients_file', '/var/spool/burp/clients_status.json')
        csv_file_data = reports_config.get('csv_file_data', '/storage/samba/automation/inventory.csv')
        config_excluded_clients = reports_config.get('excluded_clients', '')
    else:
        # if not burp custom file SET DEFAULT VALUES:
        burp_automation_folder = os.path.join(os.sep, 'storage', 'samba', 'automation')
        days_outdated = 31
        burp_www_reports = os.path.join(os.sep, 'var', 'www', 'html')
        json_clients_status = os.path.join(os.sep, 'var', 'spool', 'burp', 'clients_status.json')
        csv_file_data = os.path.join(burp_automation_folder, 'inventory.csv')
        config_excluded_clients = ''
    # SET OTHER GLOBAL Variables to use around the script:
    n_days_ago = datetime.now() - timedelta(days=days_outdated)
    n_days_ago = n_days_ago.strftime('%Y-%m-%d')
    csv_file_data_export = os.path.join(burp_www_reports, 'inventory_status.csv')
    txt_clients_status = os.path.join(burp_www_reports, 'clients_status.txt')
    if example:
        print('    Example config for burp custom config file', burp_custom_file,
              '\n        burp_automation_folder =', burp_automation_folder,
              '\n        # csv_file_to compare with external inventory:'
              '\n        csv_file_data =', csv_file_data,
              '\n        days_outdated =', days_outdated,
              '\n        days_outdated = "some notes for your emails"',
              '\n        burp_www_reports =', burp_www_reports,
              '\n        # burp_www_reports, is output place for example files:',
              '\n            #', csv_file_data_export, txt_clients_status,
              '\n        json_clients_file =', json_clients_status,
              '\n\n      # if you will send emails, these must be defined:',
              '\n        smtp_server = ip/or name',
              '\n        emails_from = email@address.x',
              '\n        emails_to = email@address.x'
              '\n        # Clients to exclude in outdated reports:'
              '\n\n        excluded_clients = clients,list,to,exclude,in,outdated,report')


def burp_config_global(burp_conf=None):
    global burp_conf_file
    global burp_directory
    global burp_client_confdir
    # ###### ------------ BURP Main config variables ----------------------- #########
    if not burp_conf:
        burp_conf_file = os.path.join(os.sep, 'etc', 'burp', 'burp-server.conf')
    else:
        burp_conf_file = burp_conf
    if os.path.isfile(burp_conf_file):
        print('Loading variables from: ', burp_conf_file)
        burp_config = parse_config(burp_conf_file)
        burp_directory = burp_config.get('directory') # storage backup directory
        burp_client_confdir = burp_config.get('clientconfdir')
    else:
        burp_directory = 'UNKNOWN'
        burp_client_confdir = 'UNKNOWN'


def is_up(hostname):
    # import os
    # import platform

    give_feedback = False

    if platform.system() == "Windows":
        response = os.system("ping "+hostname+" -n 1")
    else:
        response = os.system("ping -c 1 " + hostname)

    is_up_bool = False
    if response == 0:
        if give_feedback:
            print(hostname, 'is up!')
        is_up_bool = True
    else:
        if give_feedback:
            print(hostname, 'is down!')

    return is_up_bool


def export_json(file=None):
    if not file or file == "default":
        file = json_clients_status
    with open(file, 'w') as fp:
        json.dump(clients_list, fp, indent=4)


def import_json(file=None):
    if not file:
        file = json_clients_status
    with open(file, 'r') as fp:
        l_clients_list = json.load(fp)
    return l_clients_list


def humanize_file_size(size):
    # It will be used on some prints of text for size representation.
    import math
    size = abs(size)
    if size == 0:
        return "0B"
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    p = math.floor(math.log(size, 2)/10)
    return "%.3f%s" % (size/math.pow(1024, p), units[int(p)])


# TODO: enhance help
def print_usage():
    print('\n'
          '    Import clients_list from json: --i --import_json=file/path\n'
          '        -i runs with default file\n'
          '        --import=/path/to/file does the same as -i but allows you to specify the .json file to import\n'
          '        It is useful to work without scanning the status (like debugging the script)\n'
          '        Default file: ', json_clients_status)
    print('\n'
          '    Export clients_list from json: --export_json=file/path\n'
          '        It is useful to work without scanning the status in other environment\n'
          '        (like debugging the script or working with inventory)\n'
          '        Default file: ', json_clients_status)
    print('\n\n'
          '    Report outdated --o --outdated\n'
          '        Will print a list of outdated clients\n')
    print('\n'
          '    Report clients to text file json: --t --text=file/path\n'
          '        -t runs with default file\n'
          '        --text=/path/to/file does the same as -i but allows you to specify the file to export\n'
          '        Default file: ', txt_clients_status)
    print('\n\n'
          '    You can use a combination of parameters, examples: \n'
          ' --text --detail  (for Text and details)\n'
          ' --outdated --detail --email (For a combined outdated with emails and details for the clients)\n'
          ' -o --email  (for simple outdated email)\n'
          ' -o (To only report outdated)\n'
          ' -o /path/file (To report outdated to a file)\n'
          '\n\n')
    print('\n\n'
          '    Compare with inventory from file csv: --compare=file\n'
          '    csv file must have at least 3 columns with this order and separator ;:\n'
          '        The purpose is to compare and check from external inventory:\n'
          '        client; status; det_status\n'
          '        Status must be: active if not: will ignore the client (is case insensitive).\n'
          '        det_status (sub status), could be empty but should be there at least empty.\n'
          '        If spare the reported status will be: ignored spare\n'
          '        if client is not in burp and does not meet previous conditions, it will be: absent.\n'
          '        --compare --csv_output to export the compared inventory to another csv.\n'
          '        Default file: ', csv_file_data)
    print('\n\n'
          '    you must also specify output csv: --csv_output=file\n'
          '    Default output:', csv_file_data_export)
    print('\n\n\n'
          '    Specify burp-config=file\n'
          '    Default:', burp_conf_file)
    print('\n\n'
          '    Specify burp-reports-config=file\n'
          '    Default:', burp_custom_file)
    print(reports_config_global(burp_custom=None, example=True))
    print('\n\n'
          '    For all --option you can use --option or --option=arg\n'
          '        If you use --option it will use default value\n')


def parser_commandline():
    """
    Information extracted from: https://mkaz.com/2014/07/26/python-argparse-cookbook/
    :return:
    """
    import argparse
    global clients_list
    compare_result = []
    parser = argparse.ArgumentParser()
    parser.add_argument('--burp_conf', nargs='?', const=os.path.join(os.sep, 'etc', 'burp', 'burp-server.conf'),
                        help='burp-server.conf file')
    parser.add_argument('--reports_conf', const=os.path.join(os.sep, 'etc', 'burp', 'burp-custom-reports.conf'),
                        nargs='?', help='burp-custom-server.conf file')
    parser.add_argument('--import_json', nargs='?',
                        help='clients_status.json file')
    parser.add_argument('--outdated', '-o', nargs='?', const='print',
                        help='Report outdated or --outdated=file')
    parser.add_argument('--text', '-t', nargs='?', const='default',
                        help='Report to default text file or --text=file')
    parser.add_argument('--detail', default=False, action='store_true',
                        help='Report details on text reports')
    parser.add_argument('--email', default=False, action='store_true',
                        help='Send email on text reports')
    parser.add_argument('--compare', '-co', nargs='?', default=None, const='default',
                        help='Compare inventory --compare=file')
    parser.add_argument('--csv_output', nargs='?', default=None, const='default',
                        help='export compare to --csv_output=file')
    parser.add_argument('--export_json', nargs='?', default=None, const='default',
                        help='export clients_list to file')
    parser.add_argument('--print_usage', nargs='?', default=None, const='Print', help='print usage')
    parser.add_argument('--auto_fixes', default=False, action='store_true',
                        help='Execute automation fixes')
    args = parser.parse_args()
    # Always load some config with or without --burp_conf
    burp_config_global(burp_conf=args.burp_conf)
    # Always set reports config with or without --reports_conf
    reports_config_global(burp_custom=args.reports_conf)
    # Configure options:
    if args.import_json:
        clients_list = import_json(args.import_json)
    else:
        clients_list = burp_client_status()
    if args.outdated:
        report_outdated(file=args.outdated, detail=args.detail, email=args.email)
    if args.text:
        report_to_txt(file=args.text, detail=args.detail)
    if args.compare:
        compare_result = inventory_compare(args.compare)
    if args.csv_output:
        save_csv_data(compare_result, args.csv_output)
    if args.export_json:
        export_json(args.export_json)
    if args.print_usage == 'Print':
        print_usage()
    if args.auto_fixes:
        automation_fixes()


if __name__ == "__main__":
    parser_commandline()


# #### ---- tests ---- #####
# set global clients_list
# clients_list = {}
# clients_list = burp_client_status() or # clients_list = import_json(file) - file or json_clients_status
# pprint.pprint(clients_list)
# report_to_txt(txt_clients_status)
# report_outdated()
# export_json(file) - file or json_clients_status
# inventory_compare()
