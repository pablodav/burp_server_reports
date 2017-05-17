from ..__main__ import parse_args, cli_execution
import pytest
import os
from ..lib.files import temp_file


class TestCli:

    def test_write_nofile(self):
        """
        Raise SystemExit when no -c option is given

        """
        options = parse_args(['-ui', 'dummy', '--write_config'])

        with pytest.raises(SystemExit):
            cli_execution(options)

    def test_write_config(self):
        """
        Check if config file is written correctly

        """
        options = parse_args(['-ui', 'dummy', '-c', 'test_write_config.conf', '--write_config'])

        cli_execution(options)

        assert os.path.isfile(options.reports_conf)

    def test_report_outdated_withconfig(self):
        """
        """
        options = parse_args(['-ui', 'dummy', '-c', 'test_write_config.conf', '--report', 'outdated'])

        cli_execution(options)

    def test_report_outdated(self):
        """
        """
        options = parse_args(['-ui', 'dummy', '--report', 'outdated'])

        cli_execution(options)

    def test_report_outdated_detail(self):
        """
        """
        options = parse_args(['-ui', 'dummy', '--report', 'outdated', '--detail'])

        cli_execution(options)

    def test_report_outdated_detail_ping(self):
        """
        """
        options = parse_args(['-ui', 'dummy', '--report', 'outdated', '--detail', '--ping'])

        cli_execution(options)

    def test_report_email_outdated(self):
        """
        """
        options = parse_args(['-ui', 'dummy', '--report', 'email_outdated'])

        cli_execution(options)

    def test_report_inventory(self):
        """
        """
        # Read inventory file from data dir
        inventory = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data',
                                                  'test_inventory.csv'))

        output = temp_file('inventory_test.csv')

        options = parse_args(['-ui', 'dummy', '--report', 'inventory', '-i', inventory, '-o', output])

        cli_execution(options)

    def test_report_inventoryurl(self):
        """
        """
        # Read inventory file from data dir
        inventory = 'https://raw.githubusercontent.com/pablodav/burp_server_reports/master/burp_reports/data/test_inventory.csv'
        output = temp_file('inventory_test.csv')

        options = parse_args(['-ui', 'dummy', '--report', 'inventory', '-i', inventory, '-o', output])

        cli_execution(options)

    def test_demo_ui_outdated_detail(self):
        """
        """
        options = parse_args(['-ui', 'https://admin:admin@demo.burp-ui.org/api/', '--report', 'outdated', '--detail'])

        cli_execution(options)

    def test_demo_ui_outdated(self):
        """
        """
        options = parse_args(['-ui', 'https://admin:admin@demo.burp-ui.org/api/', '--report', 'outdated'])

        cli_execution(options)

    def test_demo_ui_outdated_debug(self):
        """
        """
        options = parse_args(['-ui', 'https://admin:admin@demo.burp-ui.org/api/',
                              '--report', 'outdated',
                              '--detail',
                              '--debug'])

        cli_execution(options)

    def test_demo_ui_debug(self):
        """
        """
        options = parse_args(['-ui', 'https://admin:admin@demo.burp-ui.org/api/',
                              '--detail',
                              '--debug'])

        cli_execution(options)

    def test_version(self):
        """
        """
        options = parse_args(['--version'])

        with pytest.raises(SystemExit):
            cli_execution(options)

    def test_noapi(self):
        """
        Raise SystemExit when no burpui_apiurl option is given
        """
        options = parse_args(['--report', 'print'])

        with pytest.raises(SystemExit):
            cli_execution(options)

