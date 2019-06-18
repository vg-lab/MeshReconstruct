#!/usr/bin/env bash
source "$1/bin/activate"
shift
python3 src/compute_areas.py $*
deactivate
