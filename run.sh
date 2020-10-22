#!bin/bash
source venv/bin/activate
uwsgi --http :8080 --home ~/Money-Disposer/venv --chdir disposer -w disposer.wsgi &
