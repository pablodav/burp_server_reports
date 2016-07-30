#!python3

from burp_reports.dummy.burpui_api_translate_dummy import BUIClients


class TestClass:

    def test_clients(self):
        clients_obj = BUIClients()
        clients_dict = clients_obj.translate_clients_stats()

        assert isinstance(clients_dict, dict)