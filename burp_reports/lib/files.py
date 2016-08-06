from sys import platform
import os


def temp_file(file='temporal'):

    if platform in ['linux', 'darwin', 'linux2']:
        # linux/osx
        cache_path = os.path.join(os.sep, 'tmp', file)
    elif platform == "win32":
        cache_path = os.path.join(os.sep, 'temp', file)

    return cache_path


