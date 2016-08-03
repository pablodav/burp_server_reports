import restructuredtext_lint as rst_lint


def check_readme(file='README.rst'):
    """
    Checks readme rst file, to ensure it will upload to pypi and be formatted correctly.
    :param file:
    :return:
    """
    errors = rst_lint.lint_file(file)
    if errors:
        msg = 'There are errors in {}, errors \n {}'.format(file, errors[0].message)
        raise SystemExit(msg)
    else:
        msg = 'No errors in {}'.format(file)
        print(msg)

