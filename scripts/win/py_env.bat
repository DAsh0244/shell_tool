@echo off
rem -noexit option
powershell.exe  -ExecutionPolicy ByPass  "& "".\update.ps1"""
cmd.exe /K env.cmd
exit