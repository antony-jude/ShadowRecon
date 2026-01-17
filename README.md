# 🔍 ShadowRecon - Advanced OSINT Framework

Professional-grade Open Source Intelligence (OSINT) framework for ethical cybersecurity research. Collects and analyzes publicly available information across multiple intelligence sources.

## ✨ Features

### 1. **Username Reconnaissance**
- Async checking across 10+ platforms (GitHub, Twitter, Reddit, Instagram, LinkedIn, YouTube, TikTok, Medium, DeviantArt, Twitch)
- Real-time platform status verification
- HTTP response code tracking
- Concurrent request handling for speed

### 2. **Domain Reconnaissance**
- **WHOIS lookups** - Registrar, creation date, expiration, name servers
- **DNS resolution** - A, MX, NS, TXT records
- **SSL certificate extraction** - Issuer, subject, validity dates
- **Hosting IP identification** - IP geolocation and ASN
- Security posture assessment

### 3. **IP Intelligence**
- **Geolocation** - Country, city, timezone, latitude/longitude
- **ISP/Organization** - Provider details, ASN information
- **Open ports & services** - Shodan integration (requires API key)
- **Service detection** - Banners, versions, products
- Threat scoring based on exposure

### 4. **Email Reconnaissance**
- **HaveIBeenPwned integration** - Breach detection
- Clear breach/no-breach distinction
- Data class identification from breaches
- Domain validity verification
- MX record checking

### 5. **Reputation & Threat Intelligence**
- **VirusTotal integration** - Malicious vendor counts
- **Risk scoring system** - 0-100 risk assessment
- **Threat categorization** - CRITICAL/HIGH/MEDIUM/LOW/MINIMAL
- Security recommendations
- Multi-vendor detection correlation

### 6. **Reporting & Analysis**
- Structured JSON exports with metadata
- Timestamp-tracked findings
- Risk assessment summaries
- Extensible architecture for future modules
- Professional logging and audit trails

## 🏗️ Project Structure

```
ShadowRecon/
├── main.py                 # Interactive CLI entry point
├── config.py              # Configuration & environment variables
├── utils.py               # Utility functions & helpers
├── requirements.txt       # Python dependencies
├── .env.example           # API keys template
│
├── modules/               # Core OSINT modules
│   ├── __init__.py
│   ├── username.py        # Username reconnaissance
│   ├── domain.py          # Domain intelligence
│   ├── ip.py              # IP address analysis
│   ├── email.py           # Email breach detection
│   └── reputation.py      # Threat intelligence
│
├── report/                # Report generation
│   └── __init__.py        # Report generator & analyzers
│
└── scans/                 # Output directory for reports
    ├── username_*.json
    ├── domain_*.json
    ├── ip_*.json
    ├── email_*.json
    └── *.html
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- (Optional) API keys for enhanced features

### Installation

```bash
# 1. Navigate to project directory
cd ShadowRecon

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and add your API keys (optional)
```

### Running the Framework

```bash
# Start interactive CLI
python main.py

# Or run specific reconnaissance from Python
python -c "
import asyncio
from modules import UsernameRecon
recon = UsernameRecon()
results = asyncio.run(recon.check_username('john_doe'))
print(results)
"
```

## 📋 API Keys Setup (Optional)

### Enable Enhanced Features

Edit `.env` file and add your API keys:

```bash
# Shodan - Service enumeration & port scanning
# Get free key at: https://www.shodan.io/
SHODAN_API_KEY=your_key_here

# VirusTotal - Malware & URL reputation
# Get free key at: https://www.virustotal.com/
VIRUSTOTAL_API_KEY=your_key_here

# HaveIBeenPwned - Breach detection (optional)
# API key for authenticated requests: https://haveibeenpwned.com/API/v3
HIBP_API_KEY=your_key_here
```

### Feature Flags

Enable/disable features in `.env`:

```bash
ENABLE_SHODAN=true           # Open port detection
ENABLE_VIRUSTOTAL=true       # Malicious vendor checks
ENABLE_HIBP=true             # Breach detection

REQUEST_TIMEOUT=10           # API request timeout (seconds)
ASYNC_TIMEOUT=30             # Async operation timeout
```

## 💻 Usage Examples

### Command Line Interface

```
🔍 ShadowRecon - Advanced OSINT Framework
======================================================================

[1] Username Reconnaissance
[2] Domain Reconnaissance
[3] IP Address Reconnaissance
[4] Email Reconnaissance
[5] Reputation & Threat Intel
[0] Exit

Select option (0-5): _
```

### Example 1: Username Reconnaissance

```bash
Select option (0-5): 1
👤 Enter username: john_doe
⏳ Checking platforms (async)...

======================================================================
  Username Reconnaissance: john_doe
======================================================================

GitHub: FOUND (200)
Twitter: NOT FOUND (404)
Reddit: FOUND (200)
LinkedIn: NOT FOUND (403)
...

📊 Found on 4 platform(s)
```

### Example 2: Domain Reconnaissance

```bash
Select option (0-5): 2
🌐 Enter domain: example.com
⏳ Gathering domain intelligence...

======================================================================
  Domain Reconnaissance: example.com
======================================================================

WHOIS Information:
  registrar: Example Registrar Inc.
  creation_date: 2010-03-10
  expiration_date: 2025-03-10
  status: ['ok', 'active']

DNS Resolution:
  a_records: ['93.184.216.34']
  mx_records: ['10 mail.example.com.']
  ns_records: ['ns1.example.com.', 'ns2.example.com.']

SSL Certificate:
  has_ssl: True
  issuer: Let's Encrypt Authority X3
  subject: example.com
  valid_from: 2024-01-15
  valid_until: 2025-01-15

────────────────────────────────────────────────────────────────────
RISK ASSESSMENT
────────────────────────────────────────────────────────────────────
Risk Score:  15/100
Risk Level:  LOW
```

### Example 3: Email Breach Detection

```bash
Select option (0-5): 4
📧 Enter email address: user@example.com
⏳ Checking email security databases...

======================================================================
  Email Reconnaissance: user@example.com
======================================================================

breach_status: NO BREACHES
breach_count: 0

domain_valid:
  domain: example.com
  valid: True
  has_mx_records: True

🚨 ALERT: Email found in 0 breach(es)
✅ No breaches detected in HaveIBeenPwned database
```

## 🔧 Advanced Usage

### Using as Python Module

```python
from modules import DomainRecon, ReputationRecon
from utils import Utils

# Domain intelligence
domain_recon = DomainRecon("example.com")
findings = domain_recon.recon()

# Check domain reputation
reputation = ReputationRecon("example.com", "domain")
threat_data = reputation.recon()

# Calculate risk
risk_score = Utils.calculate_risk_score(findings)
risk_level = Utils.get_risk_level(risk_score)

print(f"Risk Score: {risk_score}/100")
print(f"Risk Level: {risk_level}")
```

### Batch Processing

```python
import asyncio
from modules import UsernameRecon

async def check_multiple_users(usernames):
    recon = UsernameRecon()
    for username in usernames:
        results = await recon.check_username(username)
        print(f"{username}: {results}")

# Check multiple usernames
asyncio.run(check_multiple_users([
    'alice_smith',
    'bob_jones',
    'charlie_brown'
]))
```

### Saving Reports

```python
from report import ReportGenerator

# Generate JSON report
reporter = ReportGenerator(output_dir="scans")
reporter.save_report("example.com", findings, "domain")

# Generate HTML report
reporter.generate_html_report(findings)
```

## 📊 Risk Scoring System

ShadowRecon calculates risk scores (0-100) based on multiple factors:

| Risk Level | Score Range | Description | Action |
|-----------|-----------|-----------|---------|
| 🟢 MINIMAL | 0-19 | Safe, minimal concerns | Continue normally |
| 🟢 LOW | 20-39 | Minor issues detected | Standard precautions |
| 🟡 MEDIUM | 40-59 | Moderate concerns | Monitor activity |
| 🔴 HIGH | 60-79 | Significant risks | Exercise caution |
| 🔴 CRITICAL | 80-100 | Severe threats | Block immediately |

### Risk Factors

- **SSL Certificate**: Missing SSL = +15 points
- **Open Ports**: Each open port = +3 points (max +20)
- **Domain Reputation**: Each VirusTotal detection = +5 points (max +50)
- **Email Breaches**: Confirmed breach = +30 points
- **HIBP Detections**: Data in breach database = +25 points

## 🔐 Security & Ethics

### ✅ What ShadowRecon Does
- Collects **publicly available** information only
- Respects `robots.txt` and rate limiting
- Uses public APIs with proper authentication
- Maintains comprehensive audit logs
- Implements responsible disclosure practices

### ❌ What ShadowRecon Does NOT Do
- ✗ Private data scraping or hacking
- ✗ Malware creation or exploitation
- ✗ Password cracking or brute force
- ✗ Unauthorized system access
- ✗ Spam or phishing campaigns

### Legal Compliance
- Only OSINT - open source intelligence
- Complies with Terms of Service of all integrated services
- Respects GDPR, CCPA, and similar regulations
- Follow local laws regarding data collection
- Use for authorized security research only

## 📝 Logging & Auditing

All operations are logged for audit trails:

```bash
# View logs
tail -f shadowrecon.log

# Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Configure in .env: LOG_LEVEL=DEBUG
```

## 🤝 Extensibility

### Adding New Modules

```python
# Create new module: modules/blockchain.py

from utils import Utils
import logging

logger = logging.getLogger("ShadowRecon")

class BlockchainRecon:
    def __init__(self, address):
        self.address = address
    
    def recon(self):
        """Execute blockchain reconnaissance"""
        return {
            "address": self.address,
            "timestamp": Utils.format_timestamp(),
            "blockchain_data": self._fetch_data()
        }
```

### Custom Risk Scoring

Override `calculate_risk_score()` in `utils.py` to implement custom algorithms.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'aiohttp'"
```bash
pip install -r requirements.txt
```

### "API key invalid" for VirusTotal/Shodan
- Verify API key in `.env` file
- Check API key hasn't expired
- Confirm proper formatting (no extra spaces)

### DNS resolution errors
```bash
pip install dnspython
```

### SSL certificate errors
```bash
# On Windows, may need to run:
python -m certifi
```

## 📚 Resources

### OSINT Learning
- [OSINT Framework](https://osintframework.com/)
- [GreyHat Warfare OSINT Guide](https://greyhathacker.com/)
- [SANS OSINT Course](https://www.sans.org/course-search)

### APIs Used
- [Shodan](https://www.shodan.io/) - Internet search engine
- [VirusTotal](https://www.virustotal.com/) - Malware scanner
- [HaveIBeenPwned](https://haveibeenpwned.com/) - Breach database
- [ip-api.com](https://ip-api.com/) - IP geolocation

## 📋 Requirements

```
aiohttp==3.9.1              # Async HTTP client
python-dotenv==1.0.0        # Environment variables
requests==2.31.0            # HTTP library
dnspython==2.4.2            # DNS queries
whois==0.9.7                # WHOIS lookups
```

## 📄 License

Educational and authorized cybersecurity use only.

## ⚖️ Disclaimer

ShadowRecon is designed for **authorized** cybersecurity research and OSINT only. Users are responsible for:
- Complying with all applicable laws
- Obtaining proper authorization before scanning
- Respecting privacy and terms of service
- Using responsibly and ethically

Unauthorized access to computer systems is illegal. Use ShadowRecon only on systems you own or have explicit permission to test.

## 👨‍💻 Author

ShadowRecon Framework v1.0
Built for professional security researchers and ethical hackers.

---

**Last Updated**: January 2026
**Python Version**: 3.8+
**Status**: Production Ready ✅
