resolve:
	pip install -r requirements/dev.txt --upgrade

check-style:
	flake8 --max-complexity 12 . || exit 0
	pylint --rcfile .pylintrc *.py **/*.py **/**/*.py **/**/**/*.py || exit 0

test-clean:
	coverage erase

test-unit:
	coverage run --branch --source=. `which nosetests` -v --exe -a 'unit'

test-intg:
	coverage run --branch --source=. `which nosetests` -v --exe -a 'intg'

test: | test-clean test-unit test-intg

report-coverage:
	coverage report --omit=tests/*,migrations/*

.DEFAULT_GOAL := resolve

.PHONY: resolve, check-style, report-coverage, test-clean, test-unit, test-intg, test
