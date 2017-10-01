@echo off
SET PWD=%~dp0

conda create --name areasCBB -y -f --file requirements.txt 

IF errorlevel 1 (
echo.
echo.
echo --------------------------------------------------------------
echo ERROR: conda is not working or you have no internet connection
echo    * Maybe you need to install miniconda Python2.7:
echo           http://conda.pydata.org/miniconda.html 
echo --------------------------------------------------------------
echo.

PAUSE
EXIT
) 

echo @echo off > run.bat
echo activate.bat areasCBB ^&^& python.exe %PWD%src\gui.py ^&^& deactivate >> run.bat
echo PAUSE >> run.bat

echo.
echo.
echo -------------------------------------------------------------------------
echo INSTALATION COMPLETED !!!!  Execute the run.bat program in this directory
echo -------------------------------------------------------------------------
echo.
PAUSE