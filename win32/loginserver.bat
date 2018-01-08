@echo off
title login server

cd ../

:main
python -m login.StartLoginServer
pause
goto main
