# -*- coding: utf8 -*-
import requests
# Doc from http://docs.python-requests.org/en/master/user/quickstart/
import socket
# https://requests-cache.readthedocs.io/en/latest/user_guide.html#usage
import requests_cache
from datetime import timedelta
from . files import temp_file
# http://stackoverflow.com/questions/27062099/python-requests-retrying-until-a-valid-response-is-received
import time

cache_file = 'burp_reports_cache'
expire_after = timedelta(hours=1)
cache_path = temp_file(cache_file)

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
    # req = requests.get(serviceurl, verify=False, params=params)

    cnt = 0
    max_retry = 3
    while cnt < max_retry:
        try:
            req = requests.get(serviceurl, verify=False, params=params)
            if req.json():
                return req.json()
            else:
                # Raise a custom exception
                raise ValueError('No data from response')

        except requests.exceptions.RequestException as e:
            time.sleep(2 ** cnt)
            cnt += 1
            if cnt >= max_retry:
                raise e

    data = req.json()

    return data
