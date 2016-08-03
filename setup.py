#! python3
# Help from: http://www.scotttorborg.com/python-packaging/minimal.html
# https://docs.python.org/3/distutils/commandref.html#sdist-cmd
# https://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
# https://docs.python.org/3.4/tutorial/modules.html
# Install it with python setup.py install
# Or use: python setup.py develop (changes to the source files will be immediately available)
# https://pypi.python.org/pypi?%3Aaction=list_classifiers

from setuptools import setup, find_packages
import os
from os import path

here = path.abspath(path.dirname(__file__))

# Get the version from VERSION file
mypackage_root_dir = 'burp_reports'
with open(os.path.join(mypackage_root_dir, 'VERSION')) as version_file:
    version = version_file.read().strip()

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

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
      license='GPLv3',
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
      install_requires=[
          'invpy_libs',
          'requests',
          'arrow',
          'requests-cache',
          'pyzmail',
          'validators'
      ],
      tests_require=['pytest'],
      zip_safe=False)
