#!python3

from ..interfaces.burpui_api_interface import BUIClients


def test_bui_demo():
    clients_obj = BUIClients(burpui_apiurl='https://admin:admin@demo.ziirish.me/api/')
    clients_dict = clients_obj.translate_clients_stats()

    assert isinstance(clients_dict, dict)

    return clients_dict

def test_bui_demo_detail():
    clients_obj = BUIClients(burpui_apiurl='https://admin:admin@demo.ziirish.me/api/')
    clients_dict = clients_obj.translate_clients_stats(detail=True)

    assert isinstance(clients_dict, dict)

    return clients_dict
