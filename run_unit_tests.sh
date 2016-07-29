#! /bin/bash

# Simple shell script to run all the unit tests

# Exit on errors
set -e

# Test the field parsers first
./test_mtapi.py

# Then test the full command parsers
for i in test_*.py ; do
    if test "$i" != "test_mtapi.py" ; then
      ./$i
    fi
done

echo "PASSED"
