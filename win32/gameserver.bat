@echo off
title game server

cd ../

:main
python -m game.StartGameServer
pause
goto main
