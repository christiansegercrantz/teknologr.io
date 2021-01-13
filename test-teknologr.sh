#!/bin/bash
# test-teknologr.sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
WORK_DIR=$DIR/teknologr
TEST_DIR=$DIR/testenv/local

cleanup() {
	docker-compose -f $TEST_DIR/docker-compose.yml down
	deactivate
}

trap cleanup SIGINT

docker-compose -f $TEST_DIR/docker-compose.yml up -d 
sleep 5
virtualenv -p /usr/bin/python3 $TEST_DIR/venv
pip install -r $DIR/requirements.txt
source $TEST_DIR/venv/bin/activate

set -a; source $TEST_DIR/local.env; set +a

python $WORK_DIR/manage.py makemigrations
python $WORK_DIR/manage.py migrate
python $WORK_DIR/manage.py runserver
