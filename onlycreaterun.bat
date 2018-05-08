@echo off
SET PWD=%~dp0

echo @echo off > run.bat
echo activate.bat areasCBB ^&^& python.exe "%PWD%src\gui.py" ^&^& deactivate >> run.bat
echo PAUSE >> run.bat
