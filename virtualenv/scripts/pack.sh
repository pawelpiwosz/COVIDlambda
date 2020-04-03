#! /bin/bash
mkdir artifacts
ls -al
cd covid/lib/python3.6/site-packages/
pwd
ls ../../../../
zip -g -r ./../../../../artifacts/covidlambda.zip . 
cd ../../../../
cd lambdafunction
zip -g ../artifacts/covidlambda.zip covidlambda.py
cd ..