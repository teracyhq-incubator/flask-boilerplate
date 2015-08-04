#!/bin/bash

find . -name "*.pyc" -exec rm -rf {} \;
make resolve

# style report
flake8 --max-complexity 12 .
pep8 . --exclude=migrations,docs > pep8_report.txt


coverage erase
rm -rf coverage*.xml
rm -rf nosetests*.xml

coverage run --branch --source=. `which nosetests` -v --exe -a 'unit' --with-xunit --xunit-file=nosetests-unit.xml
coverage xml --omit=tests/* -o coverage-unit.xml

coverage erase
coverage run --branch --source=. `which nosetests` -v --exe -a 'intg' --with-xunit --xunit-file=nosetests-intg.xml
coverage xml --omit=tests/* -o coverage-intg.xml

# must be the last command to exit 0, otherwise, the next command will not be executed.
pylint --rcfile .pylintrc -f parseable *.py **/*.py **/**/*.py **/**/**/*.py > pylint_report.txt || exit 0
