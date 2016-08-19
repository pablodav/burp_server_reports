from ..__main__ import parse_args, cli_execution
import pytest
import os


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

    def test_demo_ui_outdated(self):
        """
        """
        options = parse_args(['-ui', 'https://admin:admin@demo.ziirish.me/api/', '--report', 'outdated', '--detail'])

        cli_execution(options)

    def test_demo_ui_outdated_debug(self):
        """
        """
        options = parse_args(['-ui', 'https://admin:admin@demo.ziirish.me/api/',
                              '--report', 'outdated',
                              '--detail',
                              '--debug'])

        cli_execution(options)

    def test_demo_ui_debug(self):
        """
        """
        options = parse_args(['-ui', 'https://admin:admin@demo.ziirish.me/api/',
                              '--detail',
                              '--debug'])

        cli_execution(options)






