@echo off
title cpl ls

cd ../

:main
python -m base.StartLoginServer
pause
goto main
