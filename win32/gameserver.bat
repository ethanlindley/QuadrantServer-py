@echo off
title cpl gs

cd ../

:main
python -m base.StartGameServer
pause
goto main
