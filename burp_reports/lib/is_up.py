import os
import platform
from deco import concurrent, synchronized

def is_up(hostname, give_feedback=False):
    """

    :param hostname: hostname/ip to ping
    :param give_feedback: just print up or down to stdout
    :return: True/False
    """

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


# Functions to add parallel ping:
@concurrent
def check_isup(k):
    """
    Checks ping and returns status
    Used with concurrent decorator for parallel checks

    :param k: name to ping
    :return(str): ping ok / -
    """
    if is_up(k):
        comments = 'ping ok'
    else:
        comments = ' - '
    return comments


@synchronized
def outdated_pings(outdated_clients):
    """
    Appends comments to clients if pings or not.
    Used with synchronized decorator for parallel checks (required def with concurrent decorator)

    :param outdated: dict formatted with clients as keys
    :return: dict with appended comments
    """
    outdated = outdated_clients

    for k in outdated.keys():
        # Append ping information to outdated_clients
        outdated[k]['comments'] = check_isup(k)
    return outdated
