#!/bin/bash

python3 test.py

status=$?

if [ "$status" -eq 0 ]
then
  python3 app.py
  exit 0
else
  echo "something wrong"
  exit 1
fi