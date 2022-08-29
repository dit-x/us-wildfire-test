setup:
	# Create python virtualenv & source it
	# python3 -m venv .venv
	# source .venv/bin/activate

install:
	# This should be run from inside a virtualenv
	pip install --upgrade pip &&\
		pip install -r requirements.txt

download_file:
	bash ./download_file.sh

test:
	pytest test.py


lint:
	pylint --disable=R,C,W1203,W1202 app.py

run:
	streamlit run app.py

all: install download_file test lint run