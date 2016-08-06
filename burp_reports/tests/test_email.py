#!python3

from .test_clients_dummy import test_dummy
from burp_reports.lib.configs import get_all_config
from burp_reports.reports.clients_reports import BurpReports
from burp_reports.lib.email import EmailNotifications


class TestEmail:

    def test_compose(self):
        clients_dict = test_dummy()

        config = get_all_config()

        # Generate burp_reports object to use for reports.
        burp_reports = BurpReports(clients_dict,
                                   days_outdated=int(config['common']['days_outdated']),
                                   config=config)

        email = burp_reports._compose_email('outdated')

        assert isinstance(email, EmailNotifications)
