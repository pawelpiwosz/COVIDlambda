#! /bin/bash
mkdir artifacts
ls -al
cd covid/lib/python3.6/site-packages/
pwd
ls ../../../../
zip -g -r ./../../../../artifacts/covidlambda.zip . 
cd ../../../../
ls -al artifacts/
cd py
pwd && ls -al
zip -g ../artifacts/covidlambda.zip covidlambda.py
cd ..
ls -al artifacts