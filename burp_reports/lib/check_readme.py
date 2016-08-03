import rstcheck


def check_readme(file='README.rst'):
    """
    Checks readme rst file, to ensure it will upload to pypi and be formatted correctly.
    :param file:
    :return:
    """
    # Get the long description from the relevant file
    with open(file, encoding='utf-8') as f:
        long_description = f.read()

    errors = list(rstcheck.check(long_description))
    if errors:
        msg = 'There are errors in {}, errors \n {}'.format(file, errors[0].message)
        raise SystemExit(msg)
    else:
        msg = 'No errors in {}'.format(file)
        print(msg)

