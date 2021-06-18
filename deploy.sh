#!/usr/bin/env bash
rm lambda.zip
rm -rf build
mkdir build
cp .tool-versions build
cp progress.py build
cp lambda_function.py build
cp -r templates build
pip3 install -r requirements.txt -t build/
cd build
zip -r ../lambda.zip *
cd ..
