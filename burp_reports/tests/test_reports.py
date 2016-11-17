#!python3

from .test_clients_dummy import test_dummy
from ..lib.configs import get_all_config
from ..reports.clients_reports import BurpReports


class TestReports:

    def test_burpreports(self):
        clients_dict = test_dummy()

        config = get_all_config()

        # Generate burp_reports object to use for reports.
        burp_reports = BurpReports(clients_dict,
                                   days_outdated=int(config['common']['days_outdated']),
                                   config=config)

        return burp_reports

    def test_basic_txt(self):
        reports = self.test_burpreports()
        reports.print_basic_txt()

    def test_get_outdated(self):
        reports = self.test_burpreports()
        outdated = reports._get_outdated()

        assert isinstance(outdated, dict)

    def test_outdated_ping(self):
        reports = self.test_burpreports()
        reports.report_outdated(ping=True)

    def test_burpreports_noconfig(self):
        clients_dict = test_dummy()

        # Generate burp_reports object to use for reports.
        burp_reports = BurpReports(clients_dict,
                                   )

        return burp_reports
