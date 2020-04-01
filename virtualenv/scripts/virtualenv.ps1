Write-Host "Create virtualenv for COVID scripts"

virtualenv covid -p python3.8
# create virtualenv called ansible with python3.6.

covid\Scripts\activate
# activate the virtualenv.

pip install -r requirements.txt
# install needed packages inside the virtualenv.