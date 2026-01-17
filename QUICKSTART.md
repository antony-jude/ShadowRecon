# 🚀 ShadowRecon - Quick Start Reference

## Installation (5 minutes)

```bash
# 1. Navigate to project
cd ShadowRecon

# 2. Create environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install packages
pip install -r requirements.txt

# 4. Run framework
python main.py
```

## Quick Usage

### Menu Options

```
[1] Username Reconnaissance      → Check if username exists on platforms
[2] Domain Reconnaissance        → WHOIS, DNS, SSL, hosting details
[3] IP Address Reconnaissance    → Geolocation, services, threat intel
[4] Email Reconnaissance         → Breach detection via HaveIBeenPwned
[5] Reputation & Threat Intel    → VirusTotal scores & risk assessment
[0] Exit                         → Quit framework
```

## Example Workflows

### Workflow 1: Investigate a Person

```
1. Enter username
   → Finds all platforms where username exists
   → Links to all social media profiles

2. Check email address
   → Sees if email is in data breaches
   → Checks email domain validity

3. Check reputation
   → Determines risk level
   → Shows threat indicators
```

### Workflow 2: Investigate a Domain

```
1. Domain reconnaissance
   → Gets WHOIS info (registrar, dates)
   → Checks SSL certificate validity
   → Resolves DNS records
   → Identifies hosting IP

2. Check IP reputation
   → Geolocation (country, city, ISP)
   → VirusTotal score
   → Risk assessment

3. Check domain reputation
   → Malicious vendor detections
   → Known threat categories
   → Recommendation (safe/risky)
```

### Workflow 3: Security Assessment

```
1. IP reconnaissance
   → Geolocation and ISP info
   → Open ports (requires Shodan API)
   → Services and versions

2. Reputation check
   → VirusTotal detections
   → Risk score calculation
   → Threat indicators

3. Report generation
   → Auto-saved to scans/ folder
   → JSON format with full details
```

## API Keys Setup

### Quick Setup (Optional)

```bash
# 1. Copy template
cp .env.example .env

# 2. Add your API keys
SHODAN_API_KEY=your_key
VIRUSTOTAL_API_KEY=your_key

# 3. Run framework
python main.py
```

### Get Free API Keys

| Service | URL | Features |
|---------|-----|----------|
| VirusTotal | virustotal.com | Malware scanning (free tier) |
| Shodan | shodan.io | Open port detection (free tier) |
| HaveIBeenPwned | haveibeenpwned.com | Breach database (free) |

## Output Files

```
scans/
├── username_github_20260117_120530.json
├── domain_example.com_20260117_120535.json
├── ip_8.8.8.8_20260117_120540.json
├── email_test@example.com_20260117_120545.json
└── report_20260117_120550.html
```

## Risk Levels

| Level | Score | Meaning |
|-------|-------|---------|
| 🟢 MINIMAL | 0-19 | Safe |
| 🟢 LOW | 20-39 | Minor issues |
| 🟡 MEDIUM | 40-59 | Moderate risk |
| 🔴 HIGH | 60-79 | Significant risk |
| 🔴 CRITICAL | 80-100 | Severe threat |

## Common Commands (Python API)

```python
# Username check (async)
from modules import UsernameRecon
import asyncio

recon = UsernameRecon()
results = asyncio.run(recon.check_username("john_doe"))
print(results)

# Domain check
from modules import DomainRecon

recon = DomainRecon("example.com")
results = recon.recon()
print(results)

# IP check
from modules import IPRecon

recon = IPRecon("8.8.8.8")
results = recon.recon()
print(results)

# Email check
from modules import EmailRecon

recon = EmailRecon("user@example.com")
results = recon.recon()
print(results)

# Reputation check
from modules import ReputationRecon

recon = ReputationRecon("example.com", "domain")
results = recon.recon()
print(results)

# Save report
from report import ReportGenerator

reporter = ReportGenerator()
reporter.save_report("example.com", results, "domain")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `API key invalid` | Check `.env` file format, no spaces |
| `Connection timeout` | Check internet, increase timeout in `.env` |
| `Permission denied` | Run with: `python main.py` (not `./main.py`) |
| `Port already in use` | Kill process or restart terminal |

## Features Checklist

| Feature | Status | Requires API |
|---------|--------|-------------|
| Username check (async) | ✅ | No |
| Domain WHOIS lookup | ✅ | No |
| DNS resolution | ✅ | No |
| SSL certificate | ✅ | No |
| IP geolocation | ✅ | No |
| Email breach check | ✅ | No* |
| Open port detection | ✅ | Yes (Shodan) |
| Malware scanning | ✅ | Yes (VirusTotal) |
| Risk scoring | ✅ | No |
| Report generation | ✅ | No |

*Free tier available

## Best Practices

✅ **Do This:**
- Run only on authorized targets
- Keep API keys in `.env` (never in code)
- Use virtual environments
- Monitor logs: `tail -f shadowrecon.log`
- Review reports before sharing

❌ **Don't Do This:**
- Access unauthorized systems
- Share API keys
- Perform OSINT without authorization
- Ignore error messages
- Leave credentials in git

## File Structure Reference

```
ShadowRecon/
├── main.py              ← Run this: python main.py
├── config.py            ← API keys & settings
├── utils.py             ← Helper functions
├── .env                 ← Your API keys (don't share)
├── .env.example         ← Template
│
├── modules/
│   ├── username.py      ← Platform checking
│   ├── domain.py        ← Domain intelligence
│   ├── ip.py            ← IP analysis
│   ├── email.py         ← Breach detection
│   └── reputation.py    ← Threat scoring
│
└── scans/               ← Output reports (auto-created)
```

## Logging

```bash
# View live logs
tail -f shadowrecon.log

# Adjust log level in .env
LOG_LEVEL=DEBUG         # Most verbose
LOG_LEVEL=INFO          # Default
LOG_LEVEL=WARNING       # Errors only
```

## Performance Tips

- Username checks are **async** (fast, parallel)
- Domain checks are **sequential** (normal)
- Use Shodan API for faster port scans
- Cache results to avoid re-checking
- Batch process multiple targets

## Getting Help

1. **Check README.md** - Full documentation
2. **Check SETUP.md** - Installation help
3. **Review logs** - `shadowrecon.log`
4. **Check code comments** - Implementation details
5. **Test with examples** - Use known targets

## Example Targets for Testing

```
Username:       github, john_doe, admin
Domain:         google.com, github.com, example.com
IP:             8.8.8.8, 1.1.1.1, 142.251.41.14
Email:          test@gmail.com, admin@github.com
```

## Next Steps

1. ✅ Installation complete? Run `python main.py`
2. ✅ Test with example targets
3. ✅ Add API keys to `.env` for enhanced features
4. ✅ Review generated reports in `scans/` folder
5. ✅ Check logs: `tail -f shadowrecon.log`
6. ✅ Read full documentation: `README.md`

---

**Version**: 1.0  
**Status**: Production Ready ✅  
**Python**: 3.8+  
**Last Updated**: January 2026

**Remember**: Always use ethically and legally.
