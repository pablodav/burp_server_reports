# -*- coding: utf8 -*-
import json
import time
from datetime import timedelta

import requests
import requests_cache
from urllib3.util import parse_url
import urllib3

from .files import temp_file

cache_file = 'burp_reports_cache'
expire_after = timedelta(minutes=30)
cache_path = temp_file(cache_file)
# Disable warning about not using certificate verification
urllib3.disable_warnings()

requests_cache.install_cache(cache_path, backend='sqlite', expire_after=expire_after)


def get_url_data(serviceurl: 'url to retrieve data',
                 params: "python requests params in url" = None,
                 ignore_empty: "returned [] value will be ignored" = False,
                 timeout: "how much time to wait for a response" = 30,
                 check_multi: "check if response has data or not" = False):

    """

    :param serviceurl: url to retrieve data
    :param params: http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    :param ignore_empty: returned [] value will be ignored, so it will allow return [] from url
    :param timeout: how much time to wait for a response
    :return: json url_data
    """

    # Get data from the url
    # Support https without verification of certificate
    # req = requests.get(serviceurl, verify=False, params=params)
    retry_times = 0
    max_retry = 3
    retry_sleep_seconds = 5
    purl = parse_url(serviceurl)
    message = ''
    req = []

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
    
    s = requests.Session()
    a = requests.adapters.HTTPAdapter(max_retries=max_retry)
    s.verify = False
    s.params = params
    s.timeout = timeout
    if username and password:
        s.auth = (username, password)
    # Add the adapter with retries to http and https
    s.mount('http://', a)
    s.mount('https://', a)

    while retry_times < max_retry:

        message = ''
        if retry_times >= 1:
            time.sleep(retry_sleep_seconds)
            retry_sleep_seconds += 15
        retry_times += 1

        try:
            req = s.get(burl)
            if check_multi:
                if not req.json():
                    return []

            req.json()

            if req.json():

                if isinstance(req.json(), dict):
                    message = req.json().get('message', '')

                elif isinstance(req.json(), list):

                    if isinstance(req.json()[0], dict):
                        message = req.json()[0].get('message', '')

                if message in ['timed out']:
                    # next try
                    requests_cache.clear()
                    continue

                # Don't try again
                break

            # If you want to ignore empty list
            elif ignore_empty:
                continue

            elif req.from_cache:
                # Clear cache to retry again
                # Added in urlget module test if it's [] retry n times due to issue:
                # https://git.ziirish.me/ziirish/burp-ui/issues/148
                # As now issue is fixed, let's see how it goes for future try
                # requests_cache.clear()
                # next try
                continue

            else:
                # Raise a custom exception
                raise ValueError('No data from response')

        except requests.exceptions.RequestException as e:

            print('request failed to {} \n retry Nº: {}'.format(burl, retry_times))

            if retry_times >= max_retry:
                raise e

        except ValueError as e:

            print('request failed to get {}'.format(burl))
            raise e

        except Exception as e:

            print('request failed to {} \n with exception'.format(burl))
            raise e

    data = req.json()

    return data
