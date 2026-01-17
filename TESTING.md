# 🧪 ShadowRecon - Testing & Validation Guide

## Pre-Deployment Testing Checklist

### Environment Verification

```bash
# 1. Verify Python version
python --version
# Expected: Python 3.8.0 or higher

# 2. Verify virtual environment is active
# Expected: (venv) prefix in prompt

# 3. Verify all packages installed
pip list
# Expected: aiohttp, requests, dnspython, whois, python-dotenv

# 4. Verify .env file exists
ls -la .env
# If missing: cp .env.example .env
```

## Module Testing

### Test 1: Username Reconnaissance

```bash
python -c "
import asyncio
from modules import UsernameRecon

async def test():
    recon = UsernameRecon()
    results = await recon.check_username('github')
    print('✓ GitHub check:', results.get('GitHub', {}).get('status'))
    
    summary = recon.get_summary()
    print(f'✓ Found on {summary[\"found_count\"]} platform(s)')
    return len(results) > 0

result = asyncio.run(test())
print('✓ Username module working' if result else '✗ Username module failed')
"
```

**Expected Output:**
```
✓ GitHub check: FOUND
✓ Found on 3 platform(s)
✓ Username module working
```

### Test 2: Domain Reconnaissance

```bash
python -c "
from modules import DomainRecon

try:
    recon = DomainRecon('google.com')
    results = recon.recon()
    
    print('✓ Domain:', results['domain'])
    print('✓ WHOIS:', 'Data' if results['whois'] else 'None')
    print('✓ DNS A Records:', results['dns']['a_records'])
    print('✓ SSL Certificate:', results['ssl']['has_ssl'])
    print('✓ Hosting IP:', results['hosting_ip']['ip'])
    print('✓ Domain module working')
except Exception as e:
    print(f'✗ Domain module failed: {e}')
"
```

**Expected Output:**
```
✓ Domain: google.com
✓ WHOIS: Data
✓ DNS A Records: ['142.251.41.14']
✓ SSL Certificate: True
✓ Hosting IP: 142.251.41.14
✓ Domain module working
```

### Test 3: IP Reconnaissance

```bash
python -c "
from modules import IPRecon

try:
    recon = IPRecon('8.8.8.8')  # Google DNS
    results = recon.recon()
    
    print('✓ IP:', results['ip'])
    print('✓ Country:', results['geolocation']['country'])
    print('✓ ISP:', results['geolocation']['isp'])
    print('✓ IP module working')
except Exception as e:
    print(f'✗ IP module failed: {e}')
"
```

**Expected Output:**
```
✓ IP: 8.8.8.8
✓ Country: United States
✓ ISP: Google LLC
✓ IP module working
```

### Test 4: Email Reconnaissance

```bash
python -c "
from modules import EmailRecon

try:
    recon = EmailRecon('test@gmail.com')
    results = recon.recon()
    
    print('✓ Email:', results['email'])
    print('✓ Breach Status:', results['hibp']['breach_status'])
    print('✓ Domain Valid:', results['domain_valid']['valid'])
    print('✓ Email module working')
except Exception as e:
    print(f'✗ Email module failed: {e}')
"
```

**Expected Output:**
```
✓ Email: test@gmail.com
✓ Breach Status: [NO BREACHES, BREACHED, or SAFE]
✓ Domain Valid: True
✓ Email module working
```

### Test 5: Reputation Check (Without API Key)

```bash
python -c "
from modules import ReputationRecon

try:
    recon = ReputationRecon('google.com', 'domain')
    results = recon.recon()
    
    print('✓ Target:', results['target'])
    print('✓ Risk Score:', results['risk_score'])
    print('✓ Risk Level:', results['risk_level'])
    print('✓ Reputation module working')
except Exception as e:
    print(f'✗ Reputation module failed: {e}')
"
```

**Expected Output:**
```
✓ Target: google.com
✓ Risk Score: 0-100
✓ Risk Level: [MINIMAL, LOW, MEDIUM, HIGH, CRITICAL]
✓ Reputation module working
```

## Integration Testing

### Test Report Generation

```bash
python -c "
from modules import DomainRecon
from report import ReportGenerator
import json

# 1. Run reconnaissance
recon = DomainRecon('example.com')
findings = recon.recon()

# 2. Generate report
reporter = ReportGenerator('scans')
filepath = reporter.save_report('example.com', findings, 'test')

# 3. Verify report
with open(filepath, 'r') as f:
    report = json.load(f)
    print(f'✓ Report saved: {filepath}')
    print(f'✓ Report contains {len(report)} fields')
"
```

**Expected Output:**
```
✓ Report saved: scans/example.com_test_YYYYMMDD_HHMMSS.json
✓ Report contains X fields
```

### Test Utilities

```bash
python -c "
from utils import Utils

# Test validation functions
print('Testing validation:')
print('✓ Valid email:', Utils.validate_email('test@example.com'))
print('✓ Invalid email:', not Utils.validate_email('invalid'))
print('✓ Valid domain:', Utils.validate_domain('example.com'))
print('✓ Invalid domain:', not Utils.validate_domain('invalid'))
print('✓ Valid IP:', Utils.validate_ip('8.8.8.8'))
print('✓ Invalid IP:', not Utils.validate_ip('999.999.999.999'))

# Test risk scoring
findings = {'risk_indicators': True}
score = Utils.calculate_risk_score(findings)
level = Utils.get_risk_level(score)
print(f'✓ Risk Score: {score}/100')
print(f'✓ Risk Level: {level}')
"
```

**Expected Output:**
```
Testing validation:
✓ Valid email: True
✓ Invalid email: True
✓ Valid domain: True
✓ Invalid domain: True
✓ Valid IP: True
✓ Invalid IP: True
✓ Risk Score: [0-100]/100
✓ Risk Level: [MINIMAL|LOW|MEDIUM|HIGH|CRITICAL]
```

## UI/CLI Testing

### Test Interactive Menu

```bash
# Run the framework
python main.py

# Test each menu option:
# 1. Try option 1 (Username) with: github
# 2. Try option 2 (Domain) with: google.com
# 3. Try option 3 (IP) with: 8.8.8.8
# 4. Try option 4 (Email) with: test@gmail.com
# 5. Try option 5 (Reputation) with: google.com
# 0. Exit
```

**Expected Behavior:**
- Menu displays correctly
- Input validation works
- Results display without errors
- Reports save to scans/ folder
- Framework exits cleanly with option 0

## Performance Testing

### Test Execution Speed

```python
import time
import asyncio
from modules import UsernameRecon

# Measure username check speed (should be fast due to async)
start = time.time()
recon = UsernameRecon()
results = asyncio.run(recon.check_username('john_doe'))
duration = time.time() - start

print(f"Username check: {duration:.2f} seconds")
print("✓ PASS" if duration < 15 else "✗ FAIL (too slow)")

# Measure domain check speed
from modules import DomainRecon
start = time.time()
recon = DomainRecon('google.com')
results = recon.recon()
duration = time.time() - start

print(f"Domain check: {duration:.2f} seconds")
print("✓ PASS" if duration < 30 else "✗ FAIL (too slow)")
```

## Error Handling Testing

### Test Invalid Inputs

```bash
python -c "
from modules import DomainRecon, IPRecon, EmailRecon
from utils import Utils

# Test domain validation
try:
    recon = DomainRecon('invalid!!domain')
    print('✗ Domain validation failed')
except ValueError:
    print('✓ Domain validation working')

# Test IP validation
try:
    recon = IPRecon('999.999.999.999')
    print('✗ IP validation failed')
except ValueError:
    print('✓ IP validation working')

# Test email validation
try:
    recon = EmailRecon('notanemail')
    print('✗ Email validation failed')
except ValueError:
    print('✓ Email validation working')

# Test util functions
print('✓ All validation functions working')
"
```

## API Integration Testing

### Without API Keys (Free Tier)

```bash
# These should work without API keys:
python main.py
# Option 1: Username ✓ (no API needed)
# Option 2: Domain ✓ (no API needed)
# Option 3: IP ✓ (partial - geolocation works, Shodan will be skipped)
# Option 4: Email ✓ (HIBP free tier)
# Option 5: Reputation ✓ (will show API key warning)
```

### With API Keys (Enhanced Features)

```bash
# 1. Set API keys in .env
SHODAN_API_KEY=your_key
VIRUSTOTAL_API_KEY=your_key

# 2. Test with API keys
python main.py
# Option 3: IP (now includes Shodan data)
# Option 5: Reputation (now includes VirusTotal data)
```

## Logging & Audit Testing

### Check Logs

```bash
# View recent logs
tail -50 shadowrecon.log

# Check for errors
grep ERROR shadowrecon.log

# Check all activity
cat shadowrecon.log | tail -100
```

**Expected Content:**
- INFO: Framework started
- INFO: Module operations logged
- DEBUG: Detailed execution info
- WARNING: API issues
- ERROR: Failed operations

## Output Validation

### Check Generated Reports

```bash
# List generated reports
ls -la scans/

# Check JSON report format
cat scans/example.com_domain_*.json | python -m json.tool

# Verify all required fields
python -c "
import json
import glob

for report in glob.glob('scans/*.json')[:1]:
    with open(report) as f:
        data = json.load(f)
        required = ['timestamp', 'domain'] or ['ip'] or ['email']
        print(f'✓ Report: {report}')
        print(f'  Fields: {list(data.keys())}')
"
```

## Security Testing

### Test Credential Protection

```bash
# Verify .env is not tracked
cat .gitignore | grep .env
# Should output: .env

# Verify no credentials in code
grep -r "SHODAN_API_KEY" *.py --exclude=config.py
# Should output: (nothing)

# Verify no credentials in logs
grep -i "apikey\|api_key\|password" shadowrecon.log
# Should output: (nothing)
```

## Compatibility Testing

### Python Version

```bash
# Test on Python 3.8+
python --version
python -c "import sys; print(f'✓ Python {sys.version_info.major}.{sys.version_info.minor}')"
```

### Operating Systems

**Windows:**
```cmd
python main.py
# Should display menu and work normally
```

**macOS/Linux:**
```bash
python3 main.py
# Should display menu and work normally
```

### Package Versions

```bash
pip show aiohttp dnspython whois requests python-dotenv
# Verify minimum versions are installed
```

## Load Testing

### Batch Processing

```python
import asyncio
from modules import UsernameRecon

async def batch_username_check():
    usernames = ['admin', 'user', 'test', 'demo', 'support']
    recon = UsernameRecon()
    
    for username in usernames:
        print(f"Checking {username}...")
        results = await recon.check_username(username)
        print(f"  Result: Found on {results.get('summary', {}).get('found_count', 0)} platforms")

asyncio.run(batch_username_check())
```

## Test Results Template

```markdown
# ShadowRecon Test Results

## Date: YYYY-MM-DD
## Tester: [Name]
## Environment: [OS] Python [Version]

### Module Tests
- [ ] Username Module: PASS/FAIL
- [ ] Domain Module: PASS/FAIL
- [ ] IP Module: PASS/FAIL
- [ ] Email Module: PASS/FAIL
- [ ] Reputation Module: PASS/FAIL

### Integration Tests
- [ ] Report Generation: PASS/FAIL
- [ ] Logging: PASS/FAIL
- [ ] Configuration: PASS/FAIL

### CLI Tests
- [ ] Menu Display: PASS/FAIL
- [ ] User Input Validation: PASS/FAIL
- [ ] Result Display: PASS/FAIL
- [ ] Error Handling: PASS/FAIL

### Performance Tests
- [ ] Username Check: <15s
- [ ] Domain Check: <30s
- [ ] IP Check: <10s
- [ ] Email Check: <5s

### Security Tests
- [ ] Credentials Protected: PASS/FAIL
- [ ] Logs Clean: PASS/FAIL
- [ ] Input Validation: PASS/FAIL

### Overall Result: ✓ PASS / ✗ FAIL

### Issues Found:
1. [Issue description]
2. [Issue description]

### Recommendations:
1. [Recommendation]
2. [Recommendation]
```

## Continuous Integration Testing

### GitHub Actions Example

```yaml
name: Test ShadowRecon

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Test imports
      run: |
        python -c "from modules import *; print('Imports OK')"
    
    - name: Test validation functions
      run: |
        python -c "from utils import Utils; print('Utils OK')"
```

## Regression Testing

Test these scenarios to ensure nothing is broken:

- [ ] Can start framework
- [ ] Username search works
- [ ] Domain lookup works
- [ ] IP geolocation works
- [ ] Email breach check works
- [ ] Reports save correctly
- [ ] Logs are created
- [ ] Error messages are helpful
- [ ] Menu navigation works
- [ ] Input validation works

## Sign-Off

```
Testing completed: _______________
Tester name: _____________________
Date: ___________________________

Framework Status: [ ] Production Ready [ ] Needs Fixes

Approval: ________________________
```

---

**Testing Guide Version**: 1.0  
**Last Updated**: January 2026
