import os

# Read version from VERSION file
__version__ = open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')
).read().rstrip()

