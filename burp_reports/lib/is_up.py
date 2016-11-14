import pyping


def is_up(hostname, give_feedback=False):
    """

    :param hostname: hostname/ip to ping
    :param give_feedback: just print if it is up or down
    :return: True/False
    """

    response = pyping.ping(hostname)

    is_up_bool = False

    # If ping responds
    if response.ret_code == 0:
        if give_feedback:
            print(hostname, 'is up!')
        is_up_bool = True
    else:
        if give_feedback:
            print(hostname, 'is down!')

    return is_up_bool
