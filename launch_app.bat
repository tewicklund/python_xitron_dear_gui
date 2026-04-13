@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found.
    echo Run first_time_setup.bat first.
    echo.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" python_xitron_dearpygui.py

echo.
echo Exit code: %errorlevel%
pause