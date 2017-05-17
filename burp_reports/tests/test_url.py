import pytest
from ..lib.urlget import get_url_data


def test_wrong_url():
    """
    Raise ValueError when return wrong value
    """

    with pytest.raises(ValueError):
        get_url_data('https://admin:admin@demo.burp-ui.org/api/demo1/c')


def test_wrong_url2():
    """
    Raise SystemExit
    """

    with pytest.raises(Exception):
        get_url_data('https://github.com/pablodav/cl')


def test_wrong_url_timeout():
    """
    Raise SystemExit
    """

    with pytest.raises(Exception):
        get_url_data('https://httpbin.org/delay/10', timeout=1)
