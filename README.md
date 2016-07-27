# burp_server_reports
helpful reports for burp backup and restore


It doesn't use burp -a m, it uses burp-ui api to get data so you need burp-ui up and accessible.

Requirements
===========

Python3.4+
pip install to install requirements listed in setup.py and also in requirements.exe

Install
======

    pip3 install burp_reports --upgrade

Also is possible to use:

    python3 -m pip install burp_reports --upgrade

On windows with python3.4:

    \python34\scripts\pip install burp_reports --upgrade

For proxies add:

    --proxy='http://user:passw@server:port'

To keep in mind
==============

It caches the data of burp-ui for 1h , if you need to refresh the data just remove /tmp/burp_reports_cache.sqlite

Usage
====

Use the command line:

    burp-reports --help

Windows env:

    \python34\scripts\burp-reports.exe --help


* `--detail` it adds more detail on list of commands, so it will be possible to use this option on most of the reports.
* `--report` multile report options.
* `--report outdated`: will report outdated clients



Optional Configuration file
===========================

    burp-reports -c /config/file/path.conf

Example config: `/etc/burp/burp-reports.conf `

Options to use in the file:

```
[common]
burpui_apiurl = http://admin:burpui@localhost:5000/api/
days_outdated = 31
```

TODO:

```
# csv_file_to compare with external inventory:
csv_file_data = /storage/samba/automation/inventory.csv
outdated_notes = This is useful comment that will be added to the foot of emails of outdated clients
# burp_www_reports, is output place for example files:
# /var/www/html/inventory_status.csv /var/www/html/clients_status.txt
emails_to = emaildest@example.net
emails_from = sendingfrom@example.net
smtp_server = addres.or.name
excluded_clients = list,of,clients,that,will,not,be,added,to,outdated,reports
```

By default it reads burp config from /etc/burp/burp-reports.conf



## Compare your list of clients with external inventory (TODO)

If you specify in configuration a list of inventory like:
`csv_file_data = /storage/samba/automation/inventory.csv`
It must have: 

```
name,status,det_status,whatever,else
client1,active,,,
client2,active,spare,,othercomments irrelevant for compare but will not be a problem
```
As the example, it will give you details only on "active" assets and will compare if it is spare or not also. 

You can use it to compare with your list of clients (useful to see if all your inventory is in burp or not). 

Option: 

`--reports inventory -i input.csv -o output.csv


Data used by the script
=======================

Chec it on [Data notes](data/notes.md)