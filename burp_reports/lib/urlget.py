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
from urllib3.util import parse_url

cache_file = 'burp_reports_cache'
expire_after = timedelta(minutes=30)
cache_path = temp_file(cache_file)

requests_cache.install_cache(cache_path, backend='sqlite', expire_after=expire_after)


def get_url_data(serviceurl, params=None, ignore_empty=False):
    """

    :param serviceurl: url to retrieve data
    :param params: http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    :return: json url_data
    """

    # Get data from the url
    # Support https without verification of certificate
    # req = requests.get(serviceurl, verify=False, params=params)
    timeout = 90
    cnt = 1
    max_retry = 4
    purl = parse_url(serviceurl)

    if purl.auth:
        username = purl.auth.split(':')[0]
        password = purl.auth.split(':')[1]
    else:
        username = None
        password = None
    # Add url like http://host
    burl = '{}://{}'.format(purl.scheme, purl.host)
    if purl.port:
        # Add port like: http://host:8080
        burl += ':{}'.format(purl.port)
    if purl.request_uri:
        # Add path and query like: http://host:8080/path/uri?query
        burl += '{}'.format(purl.request_uri)

    while cnt < max_retry:

        message = ''

        try:
            req = requests.get(burl, verify=False, params=params, timeout=timeout, auth=(username, password))

            if req.json():

                if isinstance(req.json(), dict):
                    message =  req.json().get('message', '')

                elif isinstance(req.json(), list):

                    if isinstance(req.json()[0], dict):
                        message = req.json()[0].get('message', '')

                if message == 'timed out':
                    # next try
                    cnt += 1
                    requests_cache.clear()
                    continue

                # Don't try again
                break

            elif ignore_empty:
                continue

            elif req.from_cache:
                # Clear cache to retry again
                # Added in urlget module test if it's [] retry n times due to issue:
                # https://git.ziirish.me/ziirish/burp-ui/issues/148
                requests_cache.clear()
                # next try
                cnt += 1
                continue

            else:
                # Raise a custom exception
                raise ValueError('No data from response')

            time.sleep(2 ** cnt)

        except requests.exceptions.RequestException as e:
            time.sleep(2 ** cnt)
            cnt += 1
            print('request failed to {} \n retry Nº: {}'.format(burl, cnt))
            if cnt >= max_retry:
                raise e

    if message == 'timed out':
        raise TimeoutError('request timed out')

    data = req.json()

    return data
