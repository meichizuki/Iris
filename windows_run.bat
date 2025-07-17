@echo off
color 0E

:: Create venv if not exists
if not exist venv (
    echo [setup] Virtual environment does not exist, creating...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate.bat

:: First-time setup
if not exist ".setup_done" (
    echo [setup] Installing dependencies...
    pip install -r requirements.txt
    type nul > .setup_done
    echo [setup] Complete.
)

:: run app
echo [Iris] Do not close this window to keep the bot running.
timeout /t 3 /nobreak >nul
python main.py
