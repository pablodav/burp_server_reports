# -*- coding: utf8 -*-
import requests
# Doc from http://docs.python-requests.org/en/master/user/quickstart/
import socket
# https://requests-cache.readthedocs.io/en/latest/user_guide.html#usage
import requests_cache
import os
from sys import platform
from datetime import timedelta

cache_file = 'burp_reports_cache'
expire_after = timedelta(hours=1)
cache_path = 'file_cache.sqlite'

if platform in ['linux', 'darwin', 'linux2']:
    # linux/osx
    cache_path = os.path.join(os.sep, 'tmp', cache_file)
elif platform == "win32":
    cache_path = os.path.join(os.sep, 'temp', cache_file)

# timeout in seconds
timeout = 60
socket.setdefaulttimeout(timeout)

requests_cache.install_cache(cache_path, backend='sqlite', expire_after=expire_after)


def get_url_data(serviceurl, params=None):
    """

    :param serviceurl: url to retrieve data
    :param params: http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    :return: json url_data
    """

    # Get data from the url
    # Support https without verification of certificate
    req = requests.get(serviceurl, verify=False, params=params)

    data = req.json()

    return data
