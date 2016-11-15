from ..lib.is_up import is_up
from ..lib.is_up import outdated_pings


def test_isupok():
    assert is_up('localhost')


def test_isupfail():
    assert not is_up('nohost')


def test_isupfeedbackok():
    assert is_up('localhost', give_feedback=True)


def test_isupfeedbackfail():
    assert not is_up('nohost', give_feedback=True)


def test_outdated_pings():
    clients = {'localhost': {}}
    result = outdated_pings(clients)
    assert isinstance(result['localhost']['comments'], str)

