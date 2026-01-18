#!/bin/bash
# ShadowRecon Automated Setup Script for macOS/Linux
# Run this script immediately after cloning: bash setup.sh

echo "╔════════════════════════════════════════════════════════════╗"
echo "║      ShadowRecon - Automated Setup Script (Unix/Linux)     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Git installation
echo "[0/6] Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo "⚠ Git not found! Please install Git"
    echo "  macOS: brew install git"
    echo "  Ubuntu/Debian: sudo apt-get install git"
else
    GIT_VERSION=$(git --version)
    echo "✓ Git found: $GIT_VERSION"
    
    # Initialize git repo if not already initialized
    if [ ! -d ".git" ]; then
        echo "  → Initializing git repository..."
        git init
        git config user.email "shadowrecon@local"
        git config user.name "ShadowRecon User"
    fi
    
    # Setup git hooks
    echo "  → Setting up git hooks..."
    mkdir -p .git/hooks
fi
echo ""

# Check Python installation
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python3 not found! Please install Python 3.8+"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✓ Python found: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "  → Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "✗ Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "✗ Failed to activate virtual environment"
    exit 1
fi
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip and install dependencies
echo "[4/5] Installing dependencies..."
pip install --upgrade pip --no-cache-dir > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "✗ Failed to upgrade pip"
    exit 1
fi

pip install -r requirements.txt --no-cache-dir
if [ $? -ne 0 ]; then
    echo "✗ Failed to install dependencies from requirements.txt"
    exit 1
fi
echo "✓ Dependencies installed successfully"
echo ""

# Create .env file if it doesn't exist
echo "[5/5] Setting up configuration..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
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
EOF
    echo "✓ Configuration file created (.env)"
else
    echo "  → Configuration file already exists (.env), skipping..."
fi
echo ""

# Verification & Git Status
echo "[✓] SETUP COMPLETE!"
echo "════════════════════════════════════════════════════════════"

# Show git status if repo exists
if [ -d ".git" ]; then
    echo ""
    echo "Git Repository Status:"
    git status --short
    echo ""
fi

echo "Next steps:"
echo "  1. Edit .env file to add your API keys (optional)"
echo "  2. (Git) Run: git add . && git commit -m 'Initial setup'"
echo "  3. Run: python main.py"
echo "════════════════════════════════════════════════════════════"
echo ""
