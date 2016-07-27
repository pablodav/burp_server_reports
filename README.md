# burp_server_reports
helpful reports for burp backup and restore


It doesnt use burp -a m, it uses burp-ui api to get data so you need burp-ui up and accessible.

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
* `--report inventory`: Will compare with `-i input.csv` and will export to `-o output.csv`
* `-c config.conf`: Ini file to use
* `--write_config`: will write all default settings on config file not ovewrites any existing, requires `-c`



Optional Configuration file
===========================

    burp-reports -c /config/file/path.conf

Example config: `/etc/burp/burp-reports.conf `

Options to use in the file:

```
[common]
burpui_apiurl = http://user:pass@localhost:5000/api/
days_outdated = 31
csv_delimiter = ;
```

More possible options in config:

```
[inventory_columns]
server = servidor
status = status
sub_status = status (detailed)
client_name = device name

[inventory_status]
not_inventory_in_burp = not in inventory
active = ['active']
in_many_servers = duplicated
in_inventory_updated = ok
spare_not_in_burp = ignored spare
in_inventory_not_in_burp = absent
spare_in_burp = wrong spare in burp
spare = ['spare']
inactive_in_burp = wrong not active
```

TODO:

```
[email_notification]
outdated_notes = This is useful comment that will be added to the foot of emails of outdated clients
# burp_www_reports, is output place for example files:
# /var/www/html/inventory_status.csv /var/www/html/clients_status.txt
email_to = emaildest@example.net
email_from = sendingfrom@example.net
smtp_server = addres.or.name
excluded_clients = list,of,clients,that,will,not,be,added,to,outdated,reports
```

By default it reads burp config from /etc/burp/burp-reports.conf



## Inventory: Compare your clients with external inventory

Default columns is described in the configuration section above, you don't need to specify it but you can change if
required.

An example (you can also add any more columns as you desire, it will be automatically appended on output, like notes):
```
device name;status;Status (detailed);notes
demo1; active;;should be ok
demo2; active; spare; should be wrong spare
cli10; active;;
cli20; active; spare;
```

As the example, it will give you details only on "active" assets and will compare if it is spare or not also. 

You can use it to compare with your list of clients (useful to see if all your inventory is in burp or not).
It can also tell you if you have clients not in the inventory

Command line:

`--reports inventory -i input.csv -o output.csv


Data used by the script
=======================

Chec it on [Data notes](data/notes.md)