@echo off
title Python Environment Setup
echo [1/3] Checking Python installation...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.12 and check "Add to PATH".
    pause
    exit
)

echo [2/3] Upgrading pip...
python -m pip install --upgrade pip

echo [3/3] Installing dependencies from requirements.txt...
:: The -r flag tells pip to read the file list
python -m pip install -r requirements.txt

:: If you use playwright, uncomment the line below
:: python -m playwright install

echo.
echo ==========================================
echo Setup Complete! Your environment is ready.
echo ==========================================
pause