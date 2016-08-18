#!python3

from ..dummy.burpui_dummy_api import Clients


class TestDummy:

    def test_dummy_api(self):
        clients_obj = Clients
        clients_dict = clients_obj.get_clients()

        assert clients_dict[0]['name'] == 'monitor'
