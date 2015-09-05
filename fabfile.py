from fabric.api import local


def install_requirements(env='dev'):
    """Install requirements.txt packages using pip"""
    local('pip install -r requirements/{env}.txt --upgrade'.format(env=env))


def check_style():
    local('flake8 --max-complexity 12 . || exit 0')
    local('pylint --rcfile .pylintrc *.py **/*.py **/**/*.py **/**/**/*.py || exit 0')


def test_clean():
    local('coverage erase')


def test_unit():
    local("coverage run --branch --source=. `which nosetests` -v --exe -a 'unit'")


def test_intg():
    local("coverage run --branch --source=. `which nosetests` -v --exe -a 'intg'")


def test():
    test_clean()
    test_unit()
    test_intg()


def report_coverage():
    local('coverage report --omit=tests/*,migrations/*')
