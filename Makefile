run:
	pipenv run -m thankful_server

install:
	pip3 show pipenv || pip3 install pipenv
	pipenv install
	pipenv run pip install pipenv .

test:
	pipenv run pytest thankful_server/main.py

lint:
	pipenv run pylint thankful_server/

lintfix:
	pipenv run autopep8 --in-place **.py

typecheck:
	pipenv run mypy thankful_server --ignore-missing-imports

vulnerabilities:
	pipenv check

precommit:
	make typecheck || true
	make lint || true
	make vulnerabilities
	make test

build:
	true
