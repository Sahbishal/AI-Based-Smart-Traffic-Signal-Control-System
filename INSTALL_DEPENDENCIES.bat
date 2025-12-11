@echo off
title Installing AI Traffic Management System Dependencies
color 0A
echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║          Installing Dependencies...                                ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

python -m pip install -r requirements.txt

echo.
echo ✅ Installation completed!
echo.
pause
