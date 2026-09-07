@echo off
setlocal enabledelayedexpansion
title AI Candidate Screener Portal
echo =======================================================
echo   Launching AI Candidate Screener Web Portal...
echo =======================================================
echo.

:: Detect Python executable
set "PY_CMD="

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=py"
    goto :found
)

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=python"
    goto :found
)

for /d %%I in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%I\python.exe" (
        set "PY_CMD=%%I\python.exe"
        goto :found
    )
)

for /d %%I in ("%ProgramFiles%\Python*") do (
    if exist "%%I\python.exe" (
        set "PY_CMD=%%I\python.exe"
        goto :found
    )
)

:found
if "%PY_CMD%"=="" (
    echo [ERROR] Python was not found on this system.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python environment detected: %PY_CMD%
echo Opening web portal in browser (http://localhost:8080) ...
start http://localhost:8080
"%PY_CMD%" app.py
pause
