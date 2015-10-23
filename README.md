# burp_server_reports
helpful reports for burp backup and restore

Version 1 of burp only supported for now
It doesn't use burp -a s, it looks into directory structure of burp 1 and also uses files:
log, timestamp and backup_stats.

Code is more detailed about how it uses the files, like working funcion: 

```
get_client_working_status(client_path):
    """
    #  https://github.com/grke/burp/blob/master/docs/working_dir.txt
    #  http://burp.grke.org/docs/shuffling.html

    During backup phases 1 (file system scan) and 2 (send actual data), there will
    be a symlink pointing to the directory called 'working':

    /var/spool/burp/<client>/working -> 0000027 2015-04-12 01:24:29

    burp_phase_dict = {
    }
```

But I will not explain all these details here, because most of them are already commented in the code. 

# Prepare the script for daily usage

clone the repo or copy the file. 

I would recommend to copy to something like: /usr/local/share/burp-custom
Then create a symbolik link to that with something like: 

`ln -s /usr/local/share/burp-custom/burp-server-reports.py /usr/local/bin/burp-server-reports`

With this done you will be able to call burp-server-reports command anywhere

Create a file with config desired for most of the functions: `/etc/burp/burp-custom-reports.conf `
You will be able to use `--reports_conf /file/path` if you want to use different place for this file.

File must contain: 

`
burp_automation_folder = /storage/samba/automation
# csv_file_to compare with external inventory:
csv_file_data = /storage/samba/automation/inventory.csv
days_outdated = 10
outdated_notes = This is useful comment that will be added to the foot of emails of outdated clients
burp_www_reports = /var/www/html
# burp_www_reports, is output place for example files:
# /var/www/html/inventory_status.csv /var/www/html/clients_status.txt
json_clients_file = /var/spool/burp/clients_status.json
emails_to = emaildest@example.net
emails_from = sendingfrom@example.net
smtp_server = addres.or.name
excluded_clients = list,of,clients,that,will,not,be,added,to,outdated,reports
`

By default it reads burp config from /etc/burp/burp-server.conf to locate the clients dir.
You can use `--burp_conf /path/file` to specify which config to use

# Usage of burp-server-reports.py

## The script has bultin help, so I would recommend to use those options first:

(Every option should precedes with burp-server-reports command first, example: burp-server-reports --help)
`
--help
--print_usage
`

## Print list text of clients

`--text`

You can also use `--detail`

`--text --detail`

And also specify output file:

`--text /path/to/file --detail` or without --detail 

## --detail 

As previous example, it adds more detail on list of commands, so it will be possible to use this option on most of the reports.
You can use it combined with --text, --outdated (or -o), --email

## Report outdated

Use: 

`-o --text` or `--outdated --text`

You can also use `-o --email`

Also output to a file `-o /path/to/file`

## Compare your list of clients with external inventory

If you specify in configuration a list of inventory like:
`csv_file_data = /storage/samba/automation/inventory.csv`
It must have: 

`
name,status,det_status,whatever,else
client1,active,,,
client2,active,spare,,othercomments irrelevant for compare but will not be a problem
`
As the example, it will give you details only on "active" assets and will compare if it is spare or not also. 

You can use it to compare with your list of clients (useful to see if all your inventory is in burp or not). 

Option: 

`--compare --csv_output`


