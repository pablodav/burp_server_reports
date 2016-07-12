Requirements notes:
==================
arrow: will manage all datetime functionality
requests: will be used to fetch data from rest urls.


Expected format:
==============

Usable by reports scripts:

        {'client_name':
            { 'b_last'    : 'YYYY-MM-DD HH:mm:ssZZ',
              'b_state'    : 'working/current',
              'b_phase' : 'phase1/phase2',
              'b_date' : 'date'
              'b_time' : 'time'
            }
        }

*b_last:* will use http://crsmithdev.com/arrow/ - As described in https://git.ziirish.me/ziirish/burp-ui/issues/146#note_1306
*b_date and b_time* will be converted to local time always. (It simplifies the txt module)

More information that will be processed later:

{'client_name':
        { 'b_number'  : 'number',
          'b_date'    : 'date',
          'b_status'  : 'outdated/ok',
          # 'b_type'    : 'finishing/working/current',
          'quota'   : 'ok/soft/hard',
          'warnings': 'warnings',
          'exclude' : 'yes/no',
          'b_phase' : 'phase1/phase2',
          'b_phase_date' : 'date',
          'b_phase_status' : 'outdated/ok',
          'b_log_date' : 'date of log file',
          'b_log_status' : 'outdated/ok',
          'b_curr_taken' : 'seconds',
          'backup_stats' : {'contents': 'all contents of backup_stats file for the client', some example:
                            'time_taken': 'seconds', 'bytes_in_backup': 'bytes', bytes_received: 'bytes'}
        }
}



