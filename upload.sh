#!/bin/bash
git rm -r dist
python3 setup.py bdist_wheel | grep defaults
python3 setup.py sdist | grep defaults
twine upload dist/*