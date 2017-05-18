import tempfile
import os
import getpass


def temp_file(file='temporal'):
    """
    return: str with tempfilename
    """
    # Append uid to end of filename
    file += '_{}'.format(getpass.getuser())
    # Simplified and reutilized core funtionally from python
    cache_path = os.path.join(tempfile.gettempdir(), file)

    return cache_path
