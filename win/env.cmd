@echo off
rem title "aliased things for python command line and venv"
SET home=%cd ..%
cd %home%
rem SET PYTHONSTARTUP="%home%\\scripts\startup.py"

echo 'p' for python
doskey p=python.exe $*

echo 'pip' for pip
doskey pip=python.exe -m pip $*

echo 'act' for activate
doskey act="%home%\venv\Scripts\activate.bat $*"

echo 'dct' for deactivate
doskey dct="%home%\venv\Scripts\deactivate.bat $*"

echo 'q' for quit
doskey q=exit $*


