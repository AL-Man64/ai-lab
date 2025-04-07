#!/bin/sh

# If already exists, remove it
rm -f 0036541258.zip

# Create the submission
zip -r 0036541258.zip lab2py \
	-x lab2py/.venv/**\* \
	-x lab2py/autograder.log
