@echo off
REM ShadowRecon Automated Setup Script for Windows Command Prompt
REM Run this script immediately after cloning: setup.bat

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║        ShadowRecon - Automated Setup Script (Windows)      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Git installation
echo [0/6] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo ⚠ Git not found! Please install Git from https://git-scm.com/download/win
) else (
    for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
    echo ✓ Git found: !GIT_VERSION!
    
    REM Initialize git repo if not already initialized
    if not exist .git (
        echo   ^→ Initializing git repository...
        git init >nul
        git config user.email "shadowrecon@local" >nul
        git config user.name "ShadowRecon User" >nul
    )
    
    REM Setup git hooks
    echo   ^→ Setting up git hooks...
    if not exist .git\hooks mkdir .git\hooks
)
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found! Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python found: !PYTHON_VERSION!
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo   ^→ Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ✗ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ✗ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

REM Upgrade pip and install dependencies
echo [4/5] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
if errorlevel 1 (
    echo ✗ Failed to upgrade pip
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install dependencies from requirements.txt
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully
echo.

REM Create .env file if it doesn't exist
echo [5/5] Setting up configuration...
if not exist .env (
    (
        echo # ShadowRecon Configuration File
        echo # Add your API keys here (get them from service websites)
        echo.
        echo # Shodan API Key (optional)
        echo # Get from: https://www.shodan.io/account/api
        echo SHODAN_API_KEY=
        echo.
        echo # VirusTotal API Key (optional)
        echo # Get from: https://www.virustotal.com/gui/my-apikey
        echo VIRUSTOTAL_API_KEY=
        echo.
        echo # Have I Been Pwned API Key (optional)
        echo # Get from: https://haveibeenpwned.com/API/v3
        echo HIBP_API_KEY=
        echo.
        echo # Feature flags
        echo ENABLE_SHODAN=true
        echo ENABLE_VIRUSTOTAL=true
        echo ENABLE_HIBP=true
        echo.
        echo # Request timeout settings (seconds)
        echo REQUEST_TIMEOUT=10
        echo ASYNC_TIMEOUT=30
        echo.
        echo # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        echo LOG_LEVEL=INFO
    ) > .env
    echo ✓ Configuration file created (.env)
) else (
    echo   ^→ Configuration file already exists (.env), skipping...
)
echo.

REM Verification & Git Status
echo [✓] SETUP COMPLETE!
echo ════════════════════════════════════════════════════════════

REM Show git status if repo exists
if exist .git (
    echo.
    echo Git Repository Status:
    git status --short
    echo.
)

echo Next steps:
echo   1. Edit .env file to add your API keys (optional)
echo   2. (Git) Run: git add . ^&^& git commit -m "Initial setup"
echo   3. Run: python main.py
echo ════════════════════════════════════════════════════════════
echo.
pause
