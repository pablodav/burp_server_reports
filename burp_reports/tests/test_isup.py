from ..lib.is_up import is_up
from ..lib.is_up import outdated_pings


class TestIsUP(object):

    def test_isup_ok(self):
        assert is_up('localhost')

    def test_isup_fail(self):
        assert not is_up('nohost')

    def test_isup_feedback_ok(self):
        assert is_up('localhost', give_feedback=True)

    def test_isup_feedback_fail(self):
        assert not is_up('nohost', give_feedback=True)

    def test_outdated_pings(self):
        clients = {'localhost': {}}
        result = outdated_pings(clients)
        assert isinstance(result['localhost']['comments'], str)

