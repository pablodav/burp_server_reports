from ..__main__ import parse_args
import pytest


class TestParser:

    def test_noargs(self):
        """
        User passes no args, should fail with SystemExit
        """
        with pytest.raises(SystemExit):
            options = parse_args([])

    def test_ui_dummy(self):
        """
        -ui dummy must be tested

        :return argparse dict with options and burpui_apiurl = dummy
        """
        options = parse_args(['-ui', 'dummy'])
        assert options.burpui_apiurl == 'dummy'

