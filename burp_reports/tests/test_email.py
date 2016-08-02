#!python3

from burp_reports.dummy.burpui_api_translate_dummy import BUIClients
from burp_reports.lib.configs import get_all_config
from burp_reports.reports.clients_reports import BurpReports
from burp_reports.lib.email import EmailNotifications


class TestClass:

    def test_compose(self):
        clients_obj = BUIClients()
        clients_dict = clients_obj.translate_clients_stats()

        config = get_all_config()

        # Generate burp_reports object to use for reports.
        burp_reports = BurpReports(clients_dict,
                                   days_outdated=int(config['common']['days_outdated']),
                                   config=config)

        email = burp_reports._compose_email('outdated')

        assert isinstance(email, EmailNotifications)
