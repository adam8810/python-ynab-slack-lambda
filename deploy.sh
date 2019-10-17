#!/bin/bash

rm -rf dist

mkdir dist
source ./env/bin/activate

# Install deps according to requirements
pip install -r requirements.txt

# Copy source files into dist
cp -rf ./src/* ./dist

# Copy deps
cp -rf env/lib/python3.7/site-packages/* dist

cd dist; zip -r payload *  #> /dev/null 2>&1 
aws lambda update-function-code --function-name ynab-slack-hook --zip-file fileb://payload.zip #> /dev/null 2>&1
echo done $(date)
