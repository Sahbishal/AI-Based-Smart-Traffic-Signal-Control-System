@echo off
title AI Traffic Management - Frontend Dashboard
color 0A
echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║          Frontend Dashboard - http://localhost:8000               ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

cd Frontend
python -m http.server 8000
start http://localhost:8000

pause
