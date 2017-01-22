#!/bin/bash
# requires pip3 install wheel
# for future simplicity evaluate flit
sudo python3 -m pip install wheel twine
rm -r dist/*
python3 setup.py sdist | grep defaults
python3 setup.py bdist_wheel | grep defaults
twine upload dist/*
