@echo off
setlocal
cd /d "%~dp0"

echo ===================================================
echo   AI Candidate Screener - MCP Server Launcher
echo ===================================================

set PYTHON_EXE=
py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=py -3
    goto :RUN
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=python
    goto :RUN
)

if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
    goto :RUN
)

if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    goto :RUN
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :RUN
)

echo [ERROR] Python was not found in PATH or standard installation directories.
pause
exit /b 1

:RUN
if "%~1"=="" (
    echo Starting MCP Server in Remote SSE mode on http://0.0.0.0:8000/sse ...
    %PYTHON_EXE% mcp_server.py --transport sse --host 0.0.0.0 --port 8000
) else (
    %PYTHON_EXE% mcp_server.py %*
)
