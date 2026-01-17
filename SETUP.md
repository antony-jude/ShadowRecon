# 📖 ShadowRecon Installation & Setup Guide

## System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.8 or higher |
| OS | Windows, macOS, or Linux |
| RAM | Minimum 256MB |
| Disk Space | ~100MB for dependencies |
| Network | Internet connection for API calls |

## Step-by-Step Installation

### Step 1: Install Python

#### Windows
```bash
# Download from https://www.python.org/downloads/
# Run installer and check "Add Python to PATH"
python --version  # Verify installation
```

#### macOS
```bash
brew install python3
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
python3 --version
```

### Step 2: Download ShadowRecon

```bash
# Clone or download the framework
cd your-projects-folder
unzip ShadowRecon.zip
cd ShadowRecon
```

### Step 3: Create Virtual Environment

**Why virtual environments?** They isolate project dependencies from your system Python.

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
# Prompt should show (venv) prefix
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
# Prompt should show (venv) prefix
```

### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected output should include:**
- aiohttp
- python-dotenv
- requests
- dnspython
- whois

### Step 5: Configure API Keys (Optional)

```bash
# Copy example configuration
cp .env.example .env

# Edit .env file with your editor
# Add API keys from services below
```

**Getting API Keys:**

1. **Shodan** (Open port detection)
   - Visit: https://www.shodan.io/
   - Sign up (free account)
   - Go to Account → API Key
   - Copy key to `.env`

2. **VirusTotal** (Malware scanning)
   - Visit: https://www.virustotal.com/
   - Sign up or login
   - Go to Settings → API Key
   - Copy key to `.env`

3. **HaveIBeenPwned** (Optional)
   - Visit: https://haveibeenpwned.com/API/v3
   - Register for API access
   - Copy key to `.env`

### Step 6: Run Framework

```bash
# Make sure venv is still activated
# (venv) should be in your prompt

# Start interactive menu
python main.py

# Follow on-screen prompts
```

## Configuration

### Environment Variables (.env)

```bash
# API Keys
SHODAN_API_KEY=your_key_here
VIRUSTOTAL_API_KEY=your_key_here
HIBP_API_KEY=your_key_here

# Feature Flags (true/false)
ENABLE_SHODAN=true
ENABLE_VIRUSTOTAL=true
ENABLE_HIBP=true

# Timeouts (seconds)
REQUEST_TIMEOUT=10
ASYNC_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
```

### Logging Configuration

Edit `config.py` to adjust logging:

```python
# Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Output file
LOG_FILE = "shadowrecon.log"
```

## Testing Installation

Run tests to verify everything works:

```bash
# Test imports
python -c "import aiohttp; print('✓ aiohttp OK')"
python -c "import dns.resolver; print('✓ dns OK')"
python -c "import whois; print('✓ whois OK')"
python -c "import requests; print('✓ requests OK')"

# Test framework
python -c "from modules import UsernameRecon; print('✓ Framework OK')"
```

## First Run

### Test Username Reconnaissance

```bash
python main.py

# Select option: 1
# Enter username: github
# Should find GitHub user
```

### Test Domain Reconnaissance

```bash
# Continue in menu
# Select option: 2
# Enter domain: google.com
# Should return WHOIS and DNS data
```

### Test IP Reconnaissance

```bash
# Select option: 3
# Enter IP: 8.8.8.8 (Google DNS)
# Should return geolocation data
```

## Troubleshooting

### "python: command not found"
- Python not installed or not in PATH
- **Solution**: Install Python and ensure "Add to PATH" is checked

### "ModuleNotFoundError: No module named 'aiohttp'"
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "Permission denied" on Linux/macOS
```bash
# Make script executable
chmod +x main.py

# Or use python explicitly
python3 main.py
```

### API keys not working
1. Verify `.env` file exists in main directory
2. Check API key format (no extra spaces)
3. Confirm API key is still valid on provider's site
4. Check API quotas/limits haven't been exceeded

### SSL certificate errors
```bash
# Windows: Update certificates
python -m certifi

# macOS: Run certificate installer
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Timeout errors
- Increase `REQUEST_TIMEOUT` in `.env`
- Check internet connection
- Try again (some APIs may be temporarily slow)

## Uninstalling

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment folder
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Or just delete the project folder
```

## Upgrading

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Run framework
python main.py
```

## Performance Optimization

### For Faster Username Checks
```python
# Increase async workers in config.py
CONCURRENT_TASKS = 15  # Default: 10
```

### For Faster DNS Queries
```python
# Use alternative DNS servers
# Add to .env
DNS_NAMESERVER=8.8.8.8  # Google
# or 1.1.1.1  # Cloudflare
```

## Advanced Setup

### Docker Installation (Optional)

```bash
# Build container
docker build -t shadowrecon .

# Run container
docker run -it -v $(pwd)/scans:/app/scans shadowrecon python main.py
```

### CI/CD Integration

```bash
# GitHub Actions example
name: OSINT Scan
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
```

## Best Practices

✅ **DO:**
- Keep `.env` file secure (add to `.gitignore`)
- Use virtual environments
- Review logs regularly
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Run in authorized environments only

❌ **DON'T:**
- Share `.env` file or API keys
- Run on systems without permission
- Commit `.env` to version control
- Leave credentials in code
- Ignore error logs

## Getting Help

### Documentation
- Check [README.md](README.md) for features and usage
- Review code comments for implementation details
- Check `shadowrecon.log` for error information

### Common Issues
1. **Framework won't start**: Check Python version (`python --version`)
2. **Import errors**: Verify all packages installed (`pip list`)
3. **API errors**: Check API keys and internet connection
4. **Slow performance**: Check internet speed and API rate limits

### Support Resources
- [Python Documentation](https://docs.python.org/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [VirusTotal API Docs](https://developers.virustotal.com/)
- [Shodan API Docs](https://developer.shodan.io/)

---

**Setup Complete!** 🎉

You're now ready to perform advanced OSINT reconnaissance.

Start with: `python main.py`

