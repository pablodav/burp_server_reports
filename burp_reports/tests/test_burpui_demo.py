#!python3

from ..interfaces.burpui_api_interface import BUIClients
from ..backends.burpui_api import Clients

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

def test_burpui_api_multi():
    bui_api_obj = Clients(apiurl=burpui_demo)
    clients = bui_api_obj._get_clients_report_multi()

    assert isinstance(clients, list)

def test_burpui_api_brief():
    bui_api_obj = Clients(apiurl=burpui_demo)
    clients = bui_api_obj.get_clients_reports_brief()

    assert isinstance(clients, list)
