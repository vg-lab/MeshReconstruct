#!/usr/bin/env bash
python3 -m venv $1
source "$1/bin/activate"
python3 -m pip install vtk==8.1.2
python3 -m pip install numpy==1.16.4
deactivate

