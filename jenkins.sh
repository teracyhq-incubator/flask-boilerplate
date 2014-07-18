#!/bin/bash

make resolve

# style report
flake8 --max-complexity 12 .
pep8 . > pep8_report.txt


coverage erase
coverage run --branch --source=. `which nosetests` -v --with-xunit -v tests tests/**/**
coverage xml --omit=tests/*

# must be the last command to exit 0, otherwise, the next command will not be executed.
pylint --rcfile .pylintrc -f parseable **/*.py > pylint_report.txt || exit 0
