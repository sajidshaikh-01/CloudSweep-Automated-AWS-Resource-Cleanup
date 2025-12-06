#!/bin/bash

cd ../lambda

pip install -r requirements.txt -t package

cp cronda.py package/

cd package
zip -r ../cronda.zip .
cd ..
rm -rf package
