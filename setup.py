#! python3
# Help from: http://www.scotttorborg.com/python-packaging/minimal.html
# https://docs.python.org/3.4/tutorial/modules.html
# Install it with python setup.py install
# Or use: python setup.py develop (changes to the source files will be immediately available)

from setuptools import setup

setup(name='burp_reports',
    version='1.0rc1',
    description='Burp reports package',
    classifiers=[
      'Development Status :: 1 - release candidate 1',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.4',
    ],
    url='https://github.com/pablodav/burp_server_reports',
    author='Pablo Estigarribia',
    author_email='pablodav@gmail.com',
    license='MIT',
    packages=['burp_reports'],
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
        'pyzmail'
    ],
    zip_safe=False)
