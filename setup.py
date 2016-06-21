#! python3
# Help from: http://www.scotttorborg.com/python-packaging/minimal.html
# https://docs.python.org/3.4/tutorial/modules.html
# Install it with python setup.py install
# Or use: python setup.py develop (changes to the source files will be immediately available)

from setuptools import setup

setup(name='burp_reports',
      version='0.0.1',
      description='Burp reports package',
      classifiers=[
            'Development Status :: 1 - Not usable yet',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.4',
      ],
      url='https://github.com/pablodav/burp_server_reports',
      author='Pablo Estigarribia',
      author_email='pablodav@gmail.com',
      license='MIT',
      packages=['burp_reports'],
      install_requires=[
            'invpy_libs',
      ],
      zip_safe=False)

