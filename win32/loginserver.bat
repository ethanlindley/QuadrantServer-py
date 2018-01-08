@echo off
title cpl ls

cd ../

:main
python -m login.StartLoginServer
pause
goto main
