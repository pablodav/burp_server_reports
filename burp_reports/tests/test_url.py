import pytest
from ..lib.urlget import get_url_data
import requests


def test_wrongurl():
    """
    Raise ValueError when return wrong value
    """

    with pytest.raises(ValueError):
        get_url_data('https://admin:admin@demo.ziirish.me/api/demo1/c')

def test_wrongurl2():
    """
    Raise SystemExit
    """

    get_url_data('https://github.com/pablodav/cl')
