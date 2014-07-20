resolve:
	pip install -r requirements/dev.txt

check-style:
	flake8 --max-complexity 12 . || exit 0
	pylint --rcfile .pylintrc *.py **/*.py **/**/*.py || exit 0

test:
	coverage erase
	coverage run --branch --source=. `which nosetests` -v tests/**/*.py tests/**/**/*.py

report-coverage:
	coverage report --omit=tests/*

.DEFAULT_GOAL := resolve

.PHONY: resolve, check-style, report-coverage
