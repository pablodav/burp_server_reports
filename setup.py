#! python3
# pylint: disable=invalid-name
"""
 Setup file to package burp_reports
 Help from: http://www.scotttorborg.com/python-packaging/minimal.html
 https://docs.python.org/3/distutils/commandref.html#sdist-cmd
 https://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
 https://docs.python.org/3.4/tutorial/modules.html
 Install it with python setup.py install
 Or use: python setup.py develop (changes to the source files will be
 immediately available)
 https://pypi.python.org/pypi?%3Aaction=list_classifiers
"""
import os
from os import path
from setuptools import setup, find_packages
import rstcheck

here_path = path.abspath(path.dirname(__file__))

with open(os.path.join(here_path, 'requirements.txt')) as f:
    requires = [x.strip() for x in f if x.strip()]


def check_readme(file='README.rst'):
    """
    Checks readme rst file, to ensure it will upload to pypi and be formatted
    correctly.
    :param file:
    :return:
    """
    # Get the long description from the relevant file
    with open(file, encoding='utf-8') as f_object:
        readme_content = f_object.read()

    errors = list(rstcheck.check(readme_content))
    if errors:
        msg = 'There_path are errors in {}, errors \n {}'.format(file,
                                                            errors[0].message)
        raise SystemExit(msg)
    else:
        msg = 'No errors in {}'.format(file)
        print(msg)

readme_path = path.join(here_path, 'README.rst')

# Get the version from VERSION file
mypackage_root_dir = 'burp_reports'
with open(os.path.join(mypackage_root_dir, 'VERSION')) as version_file:
    version = version_file.read().strip()

# Get the long description from the relevant file
with open(readme_path, encoding='utf-8') as f:
    long_description = f.read()

check_readme(readme_path)

# Define setuptools specifications
setup(name='burp_reports',
      version=version,
      description='Burp reports package',
      long_description=long_description,  # this is the file README.rst
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: System :: Archiving :: Backup',
      ],
      url='https://github.com/pablodav/burp_server_reports',
      author='Pablo Estigarribia',
      author_email='pablodav@gmail.com',
      license='BSD3',
      packages=find_packages(),
      include_package_data=True,
      package_data={
          'data': 'burp_reports/data/*',
      },
      data_files=[('VERSION', ['burp_reports/VERSION'])],
      entry_points={
          'console_scripts': [
              'burp-reports = burp_reports.__main__:main'
          ]
      },
      install_requires=requires,
      tests_require=['pytest',
                     'pytest-cov'],
      zip_safe=False)
