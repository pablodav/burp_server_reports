from ..lib.is_up import is_up
from ..lib.is_up import outdated_pings


class TestIsUP(object):

    def test_isupok(self):
        assert is_up('localhost')


    def test_isupfail(self):
        assert not is_up('nohost')


    def test_isupfeedbackok(self):
        assert is_up('localhost', give_feedback=True)


    def test_isupfeedbackfail(self):
        assert not is_up('nohost', give_feedback=True)


    def test_outdated_pings(self):
        clients = {'localhost': {}}
        result = outdated_pings(clients)
        assert isinstance(result['localhost']['comments'], str)

