@echo off
rd /s /q build
rd /s /q dist
python py2exe_setup.py py2exe
rd /s /q build
pause
@echo on
