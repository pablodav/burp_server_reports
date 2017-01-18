import pytest
from ..lib.urlget import get_url_data
import requests
import json


def test_wrong_url():
    """
    Raise ValueError when return wrong value
    """

    with pytest.raises(ValueError):
        get_url_data('https://admin:admin@demo.ziirish.me/api/demo1/c')


def test_wrong_url2():
    """
    Raise SystemExit
    """

    with pytest.raises(json.decoder.JSONDecodeError):
        get_url_data('https://github.com/pablodav/cl')


def test_wrong_url3():
    """
    Raise SystemExit
    """

    with pytest.raises(json.decoder.JSONDecodeError):
        get_url_data('https://github.com:443/pablodav/cl')
