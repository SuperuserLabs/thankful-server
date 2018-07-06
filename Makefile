run:
	python3 -m thankful_server

install:
	pip3 install .

test:
	pipenv run pytest thankful_server/main.py

lint:
	pipenv run pylint thankful_server/

typecheck:
	pipenv run mypy thankful_server --ignore-missing-imports

precommit:
	make typecheck || true
	make lint || true
	make test

build:
	true
