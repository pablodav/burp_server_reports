#!python3

from .test_clients_dummy import test_dummy
from burp_reports.lib.configs import get_all_config
from burp_reports.reports.clients_reports import BurpReports
import os
from ..lib.files import temp_file
from invpy_libs import csv_as_dict

# Read version from VERSION file
__inventory__ = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..',
                                              'data', 'test_inventory.csv'))

__output__ = temp_file('inventory_test.csv')


class TestInventory:

    def test_file(self):
        assert (__inventory__, os.path.isfile(__inventory__))

    def test_inventory(self):
        clients_dict = test_dummy()

        config = get_all_config()

        # Generate burp_reports object to use for reports.
        burp_reports = BurpReports(clients_dict,
                                   days_outdated=int(config['common']['days_outdated']),
                                   config=config)

        burp_reports.save_compared_inventory(__inventory__, __output__)
        compared_clients = csv_as_dict(__output__, config['inventory_columns']['client_name'],
                                       delimiter=config['common']['csv_delimiter'])

        return compared_clients

    def test_inventory_result(self):

        report = self.test_inventory()
        config = get_all_config()

        status_dict = dict(config['inventory_status'])
        status = config['inventory_columns']['status']

        assert (report['cli10'][status], status_dict['in_inventory_not_in_burp'])
        assert (report['cli10'][status], not status_dict['in_many_servers'])
        assert (report['cli20'][status], status_dict['spare_not_in_burp'])
        assert (report['cli30'][status], status_dict['in_many_servers'])
        assert (report['client_001'][status], status_dict['in_inventory_updated'] or 'outdated')
        assert (report['client_002'][status], status_dict['spare_in_burp'])
        assert (report['client_003'][status], status_dict['inactive_in_burp'])




