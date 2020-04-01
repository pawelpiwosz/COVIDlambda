#! /bin/bash

echo "Create virtualenv for COVID scripts"

pip install virtualenv

virtualenv covid -p python3.6
# create virtualenv called ansible with python3.6.

ls -al
. covid/bin/activate
#activate the virtualenv.

ls -al
pip install -r ./virtualenv/scripts/requirements.txt
# install needed packages inside the virtualenv.