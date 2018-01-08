@echo off
title cpl gs

cd ../

:main
python -m game.StartGameServer
pause
goto main
