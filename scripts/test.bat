@echo off
setlocal

cd /d "%~dp0\.."

if not exist ".venv\" (
    python3 -m venv .venv
)

.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip.exe install -r requirements-dev.txt
.venv\Scripts\pytest.exe -v

exit /b %ERRORLEVEL%
