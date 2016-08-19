#!python3

from ..dummy.burpui_api_translate_dummy import BUIClients


def test_dummy():
    clients_obj = BUIClients()
    clients_dict = clients_obj.translate_clients_stats()

    assert isinstance(clients_dict, dict)

    return clients_dict
