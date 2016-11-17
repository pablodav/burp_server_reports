#!python3

from .test_clients_dummy import test_dummy
from ..lib.configs import get_all_config
from ..reports.clients_reports import BurpReports
from ..lib.email import EmailNotifications
import pytest

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

    def test_compose_noconfig(self):
        clients_dict = test_dummy()

        # Generate burp_reports object to use for reports.
        burp_reports = BurpReports(clients_dict)

        with pytest.raises(SystemExit):
            burp_reports._compose_email('text')

    def test_send_email(self):
        clients_dict = test_dummy()
        config = get_all_config()

        # Generate burp_reports object to use for reports.
        burp_reports = BurpReports(clients_dict,
                                   days_outdated=int(config['common']['days_outdated']),
                                   config=config)

        send_email = burp_reports.email_outdated()

        assert send_email[0] or not send_email[0]


