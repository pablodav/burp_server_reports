[![Build Status](https://travis-ci.org/pablodav/burp_server_reports.svg?branch=master)](https://travis-ci.org/pablodav/burp_server_reports)

burp_server_reports
===================

helpful reports for burp backup and restore

The new refactor doesnt use burp -a m, it uses burp-ui api to get data so you need burp-ui up and accessible.

The previous version is on tag 0.1 https://github.com/pablodav/burp_server_reports/tree/0.1 and it will not be maintained.

Version 1.0rc6

Requirements
===========

Python3.4+
pip install to install requirements listed in setup.py and also in requirements.txt

Recomendations
==============

burpui 0.3.0+ (to be released but with many improvements in api performance and stability)
burp 2.0.42+ (burp monitor has been improved a lot since this release)

Use protocol = 1  with burp2 server!!!!

Install
======

    sudo pip3 install burp_reports --upgrade

Also is possible to use:

    sudo python3 -m pip install burp_reports --upgrade

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
* `--report email_outdated`: Will send email with outdated clients, requires config.



Optional Configuration file
===========================

Configuration is required only to send emails. But allows you to customize the defaults used too.

    burp-reports -c /config/file/path.conf

Example config: `/etc/burp/burp-reports.conf `

Autogenerate a basic template: `--write_config`

Options to use in the file:

```
[common]
burpui_apiurl = http://user:pass@localhost:5000/api/
days_outdated = 31
csv_delimiter = ;
```

* burpui_apiurl is overwritten by cmd if you use --burpui_apiurl
* csv_delimiter, used for `-i` and `-o`

More possible options in config:

* **inventory_colums** and **inventory_status** is used in `--report inventory`
* **email_notification**: Config that makes possible send emails

```
[inventory_columns]
server = servidor
status = status
sub_status = status (detailed)
client_name = device name

[inventory_status]
not_inventory_in_burp = not in inventory
in_many_servers = duplicated
in_inventory_updated = ok
spare_not_in_burp = ignored spare
in_inventory_not_in_burp = absent
spare_in_burp = wrong spare in burp
inactive_in_burp = wrong not active
spare = spare
active = active

[email_notification]
email_to = root@localhost
smtp_password =
email_from = server@domain.com
smtp_server = localhost
smtp_login =
smtp_mode = normal
smtp_port = 25
foot_notes = a sample notes
```

* `email_to` you can add a list of comma separated values
* `smtp_mode` you can use normal/ssl/tls
* `spare` and `active` you can also specify a list of comma separated values as possible status.

To send email it uses pyzmail, so all options here are valid: http://www.magiksys.net/pyzmail/
I have successfully tested with smtp relay with no authentication and with gmail account, in my case I had to generate an "application password" in my account, logon of google.

TODO:

```
[common]
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

    --reports inventory -i input.csv -o output.csv


Data used by the script
=======================

Chec it on [Data notes](data/notes.md)