@echo off
py -m venv %1
call %1/Scripts/activate.bat
py -m pip install vtk==8.1.2
py -m pip install numpy==1.16.4
call %1/Scripts/deactivate.bat

