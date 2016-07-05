# -*- coding: utf8 -*-
import requests
# Doc from http://docs.python-requests.org/en/master/user/quickstart/
import socket

# timeout in seconds
timeout = 60
socket.setdefaulttimeout(timeout)


def get_url_data(serviceurl):
    """

    :param serviceurl: url to retrieve data
    :return: json url_data
    """

    # Get data from the url
    # Support https without verification of certificate
    req = requests.get(serviceurl, verify=False)

    data = req.json()

    return data
