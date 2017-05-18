from ..lib.check_readme import check_readme
import os
import pytest


__readme__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'README.rst')


def test_check_readme():
    check_readme(__readme__)


def test_check_readme_error():
    __readmef__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Readme.rst')
    with pytest.raises(SystemExit):
        check_readme(__readmef__)
