#!/bin/sh
export FLASK_APP=./server.py
pipenv run python setup.py
pipenv run flask --debug run -h 0.0.0.0 -p 5123