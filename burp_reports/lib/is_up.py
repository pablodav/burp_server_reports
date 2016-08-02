import os
import platform


def is_up(hostname):
    """

    :param hostname: hostname/ip to ping
    :return: True/False
    """
    give_feedback = False

    if platform.system() == "Windows":
        response = os.system("ping " + hostname + " -n 1")
    else:
        response = os.system("ping -c 1 " + hostname)

    is_up_bool = False

    # If ping responds
    if response == 0:
        if give_feedback:
            print(hostname, 'is up!')
        is_up_bool = True
    else:
        if give_feedback:
            print(hostname, 'is down!')

    return is_up_bool
