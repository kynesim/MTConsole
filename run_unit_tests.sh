#! /bin/bash

# Simple shell script to run all the unit tests

# Exit on errors
set -e

# Test the field parsers first
./test_mtapi.py
./test_mtapi_tokenparse.py

# Then test the full command parsers
for i in test_*.py ; do
    if [ "$i" != "test_mtapi.py" -a "$i" != "test_mtapi_tokenparse.py" ] ; then
      ./$i
    fi
done

echo "PASSED"
