#!python3
# 

# Default dict for 

def default_client_backup_report():
    empty_backup_report = dict()
    empty_backup_report = {'totsize': 0,
                       'efs': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'vssheader_enc': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'start': '0', 'encrypted': False,
                       'hardlink': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'windows': 'Unknown',
                       'vssheader': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                        'softlink': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'files': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'end': '0',
                       'meta_enc': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'duration': 0, 'number': 0,
                       'meta': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'special': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'dir': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'vssfooter_enc': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'received': 0,
                       'vssfooter': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0},
                       'files_enc': {'total': 0, 'deleted': 0, 'unchanged': 0, 'scanned': 0, 'changed': 0, 'new': 0}
                       }
    
    return empty_backup_report
