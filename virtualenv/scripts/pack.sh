! /bin/bash
mkdir artifacts
cd covid/lib/python3.6/site-packages/
zip -g -r ./../../package/covidlambda.zip . 
cd ../../../py
pwd && ls -al
zip -g ../artifacts/covidlambda.zip covidlambda.py
cd ..
ls -al artifacts