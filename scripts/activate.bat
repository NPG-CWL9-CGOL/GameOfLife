@echo off
if not exist ".venv\" (
    python3 -m venv .venv
)

call .venv\Scripts\activate.bat
pip install -r requirements.txt
