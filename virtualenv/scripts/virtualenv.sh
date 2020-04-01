#! /bin/bash

echo "Create virtualenv for COVID scripts"

virtualenv ../covid -p python3.6
# create virtualenv called ansible with python3.6.

. ../covid/bin/activate
#activate the virtualenv.

pip install -r ../requirements.txt
# install needed packages inside the virtualenv.