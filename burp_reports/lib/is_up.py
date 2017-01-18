import os
import platform
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor as Executor


@lru_cache(None)
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
def check_isup(k, return_client=None):
    """
    Checks ping and returns status
    Used with concurrent decorator for parallel checks

    :param k: name to ping
    :param return_client: to change return format as '{k: {'comments': comments}}'
    :return(str): ping ok / -
    """
    if is_up(k):
        comments = 'ping ok'
    else:
        comments = ' - '

    if return_client:
        comments = {k: {'comments': comments}}

    return comments


def outdated_pings(outdated_clients: dict):
    """
    Appends comments to clients if pings or not.
    Used with synchronized decorator for parallel checks (required def with concurrent decorator)

    :param outdated_clients: dict formatted with clients as keys
    :return: dict with appended comments
    """
    outdated = outdated_clients

    with Executor(max_workers=10) as exe:
        # jobs are executed in parallel with exe.submit
        # params passed to exe.submit are: (function, args, args)
        # in this case we pass client, True. True is to get a return as dict with key as client and new comments
        # we use one are from a list appending a for in the list
        jobs = [exe.submit(check_isup, k, True) for k in outdated.keys()]
        # results are generated from jobs
        results = [job.result() for job in jobs]

    for n in range(len(results)):

        # Append ping information to outdated_clients
        # as we have same format in results as the original dict, we just update the values.
        # dict returned by results is {k: {'comments': comments}}
        outdated.update(results[n])

    return outdated
