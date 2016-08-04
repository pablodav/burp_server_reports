#!/bin/bash
# requires pip3 install wheel
rm -r dist/*
python3 setup.py sdist | grep defaults
python3 setup.py bdist_wheel | grep defaults
twine upload dist/*
