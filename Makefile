install: bin/python

bin/python:
	python3 -m venv .
	bin/pip install wheel
	bin/pip install -r requirements.txt

migrate: bin/python
	bin/python teknologr/manage.py migrate

checkmigrations: bin/python
	bin/python teknologr/manage.py makemigrations --check --dry-run

serve: bin/python
	bin/python teknologr/manage.py runserver 8888

deploy: bin/python
	bin/python teknologr/manage.py collectstatic -v0 --noinput
	touch teknologr/teknologr/wsgi.py

clean:
	rm -rf bin/ lib/ build/ dist/ *.egg-info/ include/ local/
