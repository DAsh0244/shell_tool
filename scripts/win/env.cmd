@echo off

set version=0.0.2 - 'Silly Name Here'
title DAQ shell tool %version%

pushd ..\..
SET home=%cd%
popd
cd %home%
rem SET PYTHONSTARTUP="%home%\\scripts\startup.py"

REM echo 'p' for python
REM echo 'pip' for pip
doskey p=python.exe $*
doskey pip=python.exe -m pip $*

REM echo 'act' for activate
REM echo 'dct' for deactivate
doskey act="%home%\venv\Scripts\activate.bat $*"
doskey dct="%home%\venv\Scripts\deactivate.bat $*"

echo 'shell' to start shell
echo 'shell FAKE' to start shell in simulated daq mode
doskey shell=python src\shell.py $*

echo 'q' or 'exit' for quit
doskey q=exit $*



