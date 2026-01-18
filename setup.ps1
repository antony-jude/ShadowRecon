# ShadowRecon Automated Setup Script for Windows PowerShell
# Run this script immediately after cloning: .\setup.ps1

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        ShadowRecon - Automated Setup Script (Windows)      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Git installation
Write-Host "[0/6] Checking Git installation..." -ForegroundColor Yellow
$gitCheck = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ Git not found! Please install Git from https://git-scm.com/download/win" -ForegroundColor Yellow
} else {
    Write-Host "✓ Git found: $gitCheck" -ForegroundColor Green
    
    # Initialize git repo if not already initialized
    if (-not (Test-Path ".git")) {
        Write-Host "  → Initializing git repository..." -ForegroundColor Cyan
        git init | Out-Null
        git config user.email "shadowrecon@local" | Out-Null
        git config user.name "ShadowRecon User" | Out-Null
    }
    
    # Setup git hooks
    Write-Host "  → Setting up git hooks..." -ForegroundColor Cyan
    $hooksDir = ".git\hooks"
    if (-not (Test-Path $hooksDir)) {
        New-Item -ItemType Directory -Path $hooksDir -Force | Out-Null
    }
}
Write-Host ""

# Check Python installation
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Python not found! Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python found: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  → Virtual environment already exists, skipping..." -ForegroundColor Cyan
} else {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip and install dependencies
Write-Host "[4/5] Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip --no-cache-dir > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to upgrade pip" -ForegroundColor Red
    exit 1
}

pip install -r requirements.txt --no-cache-dir
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies from requirements.txt" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
Write-Host ""

# Create .env file if it doesn't exist
Write-Host "[5/5] Setting up configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    @"
# ShadowRecon Configuration File
# Add your API keys here (get them from service websites)

# Shodan API Key (optional)
# Get from: https://www.shodan.io/account/api
SHODAN_API_KEY=

# VirusTotal API Key (optional)
# Get from: https://www.virustotal.com/gui/my-apikey
VIRUSTOTAL_API_KEY=

# Have I Been Pwned API Key (optional)
# Get from: https://haveibeenpwned.com/API/v3
HIBP_API_KEY=

# Feature flags
ENABLE_SHODAN=true
ENABLE_VIRUSTOTAL=true
ENABLE_HIBP=true

# Request timeout settings (seconds)
REQUEST_TIMEOUT=10
ASYNC_TIMEOUT=30

# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✓ Configuration file created (.env)" -ForegroundColor Green
} else {
    Write-Host "  → Configuration file already exists (.env), skipping..." -ForegroundColor Cyan
}
Write-Host ""

# Verification & Git Status
Write-Host "[✓] SETUP COMPLETE!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan

# Show git status if repo exists
if (Test-Path ".git") {
    Write-Host ""
    Write-Host "Git Repository Status:" -ForegroundColor Cyan
    git status --short
    Write-Host ""
}

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Edit .env file to add your API keys (optional)"
Write-Host "  2. (Git) Run: git add . && git commit -m 'Initial setup'" -ForegroundColor Cyan
Write-Host "  3. Run: python main.py" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
