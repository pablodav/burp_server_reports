#!python3

from ..interfaces.burpui_api_interface import BUIClients

burpui_demo='https://admin:admin@demo.burp-ui.org/api/'
burpui_standalone='http://admin:admin@172.17.0.2:8080/api/'

def test_bui_demo():
    clients_obj = BUIClients(burpui_apiurl=burpui_demo)
    clients_dict = clients_obj.translate_clients_stats()

    assert isinstance(clients_dict, dict)

    return clients_dict

def test_bui_demo_detail():
    clients_obj = BUIClients(burpui_apiurl=burpui_demo)
    clients_dict = clients_obj.translate_clients_stats(detail=True)

    assert isinstance(clients_dict, dict)

    return clients_dict
