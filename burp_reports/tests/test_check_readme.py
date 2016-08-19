from ..lib.check_readme import check_readme
import os

__readme__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'README.rst')


def test_check_readme():
    check_readme(__readme__)
