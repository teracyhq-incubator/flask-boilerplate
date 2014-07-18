resolve:
	pip install -r requirements/dev.txt

check-style:
	flake8 --max-complexity 12 .
	pylint --rcfile .pylintrc *.py || exit 0

test:
	coverage erase
	coverage run --branch --source=. `which nosetests` -v tests tests/**/**

report-coverage:
	coverage report --omit=tests/*

.DEFAULT_GOAL := resolve

.PHONY: resolve, check-style, report-coverage
