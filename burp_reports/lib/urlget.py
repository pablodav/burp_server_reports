# -*- coding: utf8 -*-
import requests
# Doc from http://docs.python-requests.org/en/master/user/quickstart/
import socket

# timeout in seconds
timeout = 60
socket.setdefaulttimeout(timeout)


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
