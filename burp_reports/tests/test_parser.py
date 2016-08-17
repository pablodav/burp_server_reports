from burp_reports.__main__ import create_parser
import pytest


class TestParser:

    def test_noargs(self):
        """
        User passes no args, should fail with SystemExit
        """
        parser = create_parser()
        parser.parse_args([])

    def test_ui_dummy(self):
        parser = create_parser()
        args = parser.parse_args(['-ui', 'dummy'])

