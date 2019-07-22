@echo off
set env=%1
call %env%/Scripts/activate.bat

:loop
shift
if [%1]==[] goto afterloop
set params=%params% %1
goto loop
:afterloop
echo %params%

py src/compute_areas.py %params%
call %env%/Scripts/deactivate.bat

