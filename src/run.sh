#!/usr/bin/env bash
source "$1/bin/activate"
python3 compute_areas.py -a test.csv -v test.vrml -s None
source "$1/bin/deacticate"
