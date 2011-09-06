@echo off
call %~dp0\setpypath.bat
python %~dp0\%~n0 %*
