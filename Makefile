run:
	python3 -m thankful_server

install:
	pip3 install .

test:
	pytest thankful_server/*

lint:
	true

build:
	true
