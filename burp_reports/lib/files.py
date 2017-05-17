import tempfile
import os


def temp_file(file='temporal'):
    """
    return: str with tempfilename
    """
    # Append uid to end of filename
    file += '_{}'.format(os.getlogin())
    # Simplified and reutilized core funtionally from python
    cache_path = os.path.join(tempfile.gettempdir(), file)

    return cache_path

