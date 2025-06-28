@echo off
echo Activating virtual environment...
call .\myenv\Scripts\activate

echo Running processNSE.py...
py processNSE.py

echo Running plotIt.py...
py plotIt.py

echo Analysis complete.
pause