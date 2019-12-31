#!/bin/bash
echo "Clearing directories"
rm dist/*
echo "Directory cleared"
echo "Running sdist"
python setup.py sdist
echo "Completed sdist"
echo "Running bdist_wheel"
python setup.py bdist_wheel
echo "Completed bdist_wheel"
