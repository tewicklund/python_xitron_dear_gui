@echo off
setlocal

REM Move to the folder this script lives in
cd /d "%~dp0"

echo ========================================
echo DearPyGui App First-Time Setup
echo ========================================
echo.

REM Check for Python launcher first
where py >nul 2>nul
if %errorlevel%==0 (
    set "PY_CMD=py"
    goto :python_found
)

REM Fallback: check for python
where python >nul 2>nul
if %errorlevel%==0 (
    set "PY_CMD=python"
    goto :python_found
)

echo ERROR: Python was not found on PATH.
echo Install Python from python.org and make sure "Add Python to PATH" is enabled.
echo.
pause
exit /b 1

:python_found
echo Found Python command: %PY_CMD%
echo.

REM Verify Python actually runs
%PY_CMD% --version
if errorlevel 1 (
    echo ERROR: Python command exists but failed to run.
    echo.
    pause
    exit /b 1
)
echo.

REM Check whether pip works
%PY_CMD% -m pip --version >nul 2>nul
if errorlevel 1 (
    echo pip is missing or broken. Attempting ensurepip...
    %PY_CMD% -m ensurepip --upgrade
    if errorlevel 1 (
        echo ERROR: Could not install/repair pip.
        echo.
        pause
        exit /b 1
    )
)
echo pip is available.
echo.

REM Create venv if missing
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Creating .venv...
    %PY_CMD% -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        echo.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)
echo.

REM Upgrade pip inside the venv
echo Upgrading pip in virtual environment...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip in virtual environment.
    echo.
    pause
    exit /b 1
)
echo.

REM Install requirements if present
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements.
        echo.
        pause
        exit /b 1
    )
) else (
    echo WARNING: requirements.txt not found. Skipping dependency install.
)
echo.

echo ========================================
echo Setup complete.
echo ========================================
echo.
pause
exit /b 0