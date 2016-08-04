.. image:: https://travis-ci.org/pablodav/burp_server_reports.svg?branch=master
    :target: https://travis-ci.org/pablodav/burp_server_reports

burp_server_reports
===================

helpful reports for burp backup and restore

The new refactor doesnt use burp -a m, it uses burp-ui api to get data so you need burp-ui up and accessible.

The previous version is on tag 0.1 https://github.com/pablodav/burp_server_reports/tree/0.1 and it will not be maintained.

`VERSION  <burp_reports/VERSION>`__


Intro
=====

I'm trying to create some extra feature to the burp and burp-ui ecosystem, with burp you have everything that's required
to backup/restore your systems, but like burp-ui is created by a sysadmin that loves Burp and would like to help Burp
adoption with it's nice interface, I'm a sysadmin that loves burp and burp-ui and would like to help Burp adoption
by providing nice reports.

I have started with those reports that I think are more critical in large deployments, but also are good for every
deployment.

I have also create lot of flexibility in the configuration of those reports, so you will notice that you could change
almost every behaviour of them from the config file.


Requirements
============

Python3.4+    
pip install to install requirements listed in setup.py and also in requirements.txt    

Recommendations
===============

burpui 0.3.0+ (to be released but with many improvements in api performance and stability)    
burp 2.0.42+ (burp monitor has been improved a lot since this release)    

Use protocol = 1  with burp2 server!!!!

Install
=======

Linux::

    sudo pip3 install burp_reports --upgrade

Also is possible to use::

    sudo python3 -m pip install burp_reports --upgrade

On windows with python3.4::

    \python34\scripts\pip install burp_reports --upgrade

For proxies add::

    --proxy='http://user:passw@server:port'

*IMPORTANT NOTE FOR UBUNTU 14.04 and maybe others*
I have problems on the first try, it said `No distributions matching  the version`, and fixed it with::

    pip3 install pip --upgrade

Consideration
=============

It caches the data of burp-ui for 1h , if you need to refresh the data just remove /tmp/burp_reports_cache.sqlite

Usage
=====

Use the command line::

    burp-reports --help

Windows env::

    \python34\scripts\burp-reports.exe --help


* ``--detail`` it adds more detail on list of commands, so it will be possible to use this option on most of the reports.
* ``--report`` multiple report options.
* ``--report outdated``: will report outdated clients
* ``--report inventory``: Will compare with `-i input.csv` and will export to `-o output.csv`
* ``-c config.conf``: Ini file to use
* ``--write_config``: will write all default settings on config file not overwrites any existing, requires `-c`
* ``--report email_outdated``: Will send email with outdated clients, requires config.

* ``-i`` (also can be an url, the program will recognize the url and download the file from it)


Optional Configuration file
===========================

Configuration is required only to send emails. But allows you to customize the defaults used too::

    burp-reports -c /config/file/path.conf

Recommended location: ``/etc/burp/burp-reports.conf``

Auto generate a basic template: ``--write_config``

Options to use in the file:

.. code-block:: ini

    [common]
    burpui_apiurl = http://user:pass@localhost:5000/api/
    days_outdated = 31
    csv_delimiter = ;
    excluded_clients = list,of,clients,that,will,not,be,added,to,outdated,reports


* burpui_apiurl is overwritten by cmd if you use ``--burpui_apiurl``
* csv_delimiter, used for ``-i`` and ``-o``

More possible options in config:

* **inventory_columns** and **inventory_status** is used in ``--report inventory``
* **email_notification**: Config that makes possible send emails

.. code-block:: ini

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
        foot_notes = a sample notes in the end of your email


* ``email_to`` you can add a list of comma separated values without spaces.
* ``smtp_mode`` you can use normal/ssl/tls
* ``spare`` and ``active`` you can also specify a list of comma separated values without spaces as possible status.

To send email it uses pyzmail, so all options here are valid: http://www.magiksys.net/pyzmail/
I have successfully tested with smtp relay with no authentication and with gmail account,
in my case I had to generate an "application password" in my account, logon of google.

By default it does not reads any config file and tries to use the defaults in the program. (the easiest way to see the defaults is to write a config with ``--write_config``)



Inventory: Compare your clients with external inventory
-------------------------------------------------------

Default columns is described in the configuration section above, you don't need to specify it but you can change if
required.

An example (you can also add many more columns as you desire, it will be automatically appended on output, like notes):

::

        device name;statsu;Status (detailed);notes
        demo1; active;;should be ok
        demo2; active; spare; should be wrong spare
        cli10; active;;
        cli20; active; spare;

As the example, it will give you details only on "active" assets and will compare if it is spare or not also. 

You can use it to compare with your list of clients (useful to see if all your inventory is in burp or not).    
It can also tell you if you have clients not in the inventory

Command line::

    ``--reports inventory -i input.csv -o output.csv``


Data used by the script
=======================

Check it on `Data notes  <burp_reports/data/notes.md>`__

Bugs and requests
=================

Just report on github issues: https://github.com/pablodav/burp_server_reports/issues 

TODO:

* Add cron examples
* Add more introduction
* Add features section?

Thanks
======

Thanks you for your feedbacks and bug reports.

Thanks to Graham Keeling for making `Burp <http://burp.grke.org/>`__, it's a great backup software system.

Thanks to Benjamin Sans (ziirish) for making `Burp-ui <https://git.ziirish.me/ziirish/burp-ui>`__

Thanks to all those that collaborate in those projects (sorry for those that I didn't mention here).

