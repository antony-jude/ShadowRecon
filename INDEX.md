# 🔍 ShadowRecon - Complete OSINT Framework

## 📚 Documentation Index

Welcome to ShadowRecon! Here's where to find everything you need:

### 🚀 Getting Started (Start Here!)
1. **[README.md](README.md)** - Complete feature overview & examples
2. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick reference
3. **[SETUP.md](SETUP.md)** - Detailed installation & configuration

### 🔧 Technical Resources
4. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture & module descriptions
5. **[TESTING.md](TESTING.md)** - Testing procedures & validation
6. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide

### 📁 Core Files

#### Configuration
- **config.py** - Centralized settings (API keys, feature flags, platforms)
- **.env.example** - Environment variable template (copy to .env)
- **requirements.txt** - Python package dependencies

#### Main Application
- **main.py** - Interactive CLI entry point (450+ lines)
- **utils.py** - Helper functions & utilities (200+ lines)

#### Intelligence Modules
- **modules/username.py** - Social platform username checking (async)
- **modules/domain.py** - Domain intelligence (WHOIS, DNS, SSL)
- **modules/ip.py** - IP analysis (geolocation, Shodan, services)
- **modules/email.py** - Email breach detection (HaveIBeenPwned)
- **modules/reputation.py** - Threat scoring (VirusTotal)

#### Reporting
- **report/__init__.py** - Report generation & analysis

---

## 🎯 What ShadowRecon Does

### ✅ Supported Reconnaissance

| Type | Capabilities | Speed | API Required |
|------|-------------|-------|------------|
| **Username** | Check 10+ platforms for user existence | ⚡ Fast | No |
| **Domain** | WHOIS, DNS, SSL, hosting info | ⏱️ Moderate | No |
| **IP Address** | Geolocation, services, ISP, ASN | ⚡ Fast | Shodan (opt) |
| **Email** | Breach detection, domain validation | ⚡ Fast | No* |
| **Reputation** | Malware checks, risk scoring | ⚡ Fast | VirusTotal |

*Free tier available

---

## 🚀 Quick Start

### 1. Install (5 minutes)

```bash
cd ShadowRecon
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure (Optional)

```bash
cp .env.example .env
# Edit .env and add your API keys (optional)
```

### 3. Run

```bash
python main.py
```

---

## 📖 Documentation Guide

### For First-Time Users
1. Read **QUICKSTART.md** for 10-minute overview
2. Follow **SETUP.md** for installation
3. Run examples from **README.md**

### For Developers
1. Review **PROJECT_SUMMARY.md** for architecture
2. Study module code in **modules/**
3. Check **TESTING.md** for testing procedures

### For System Administrators
1. Follow **DEPLOYMENT.md** for production setup
2. Review **TESTING.md** for validation
3. Set up monitoring per **DEPLOYMENT.md**

### For Security Teams
1. Understand features in **README.md**
2. Review risk scoring in **PROJECT_SUMMARY.md**
3. Check ethics in **README.md** (Legal Compliance section)

---

## 🔑 API Keys (Optional)

### Enable Advanced Features

```bash
# Edit .env file:
SHODAN_API_KEY=your_key           # Open port detection
VIRUSTOTAL_API_KEY=your_key       # Malware scanning
HIBP_API_KEY=your_key             # Email breaches (optional)
```

### Get Free API Keys

- **Shodan**: https://www.shodan.io/ (free tier available)
- **VirusTotal**: https://www.virustotal.com/ (free tier available)
- **HIBP**: https://haveibeenpwned.com/ (free, no key needed)

---

## 📊 Features at a Glance

### 5 Core Modules

| Module | Purpose | Input | Output |
|--------|---------|-------|--------|
| **Username** | Find user accounts | username | Platforms where found |
| **Domain** | Domain intelligence | domain.com | WHOIS, DNS, SSL, IP |
| **IP** | Analyze IP address | 1.2.3.4 | Geolocation, services |
| **Email** | Check breaches | email@test.com | Breach status, database |
| **Reputation** | Threat assessment | target | Risk score, threats |

### 6 Key Features

✅ **Async Operations** - Fast parallel username checking  
✅ **Risk Scoring** - 0-100 threat assessment  
✅ **Clean Reporting** - JSON & HTML exports  
✅ **Comprehensive Logging** - Full audit trail  
✅ **Extensible Design** - Easy to add modules  
✅ **Production Quality** - Security best practices

---

## 🔐 Security & Ethics

### What It Does
- ✅ Collects **public** information only
- ✅ Respects Terms of Service
- ✅ Uses authorized APIs
- ✅ Maintains audit logs
- ✅ Enables ethical security research

### What It Doesn't Do
- ❌ Hacking or exploitation
- ❌ Private data scraping
- ❌ Password cracking
- ❌ Unauthorized access
- ❌ Malware creation

### Legal Use Cases
- Authorized penetration testing
- Due diligence investigations
- Threat intelligence gathering
- Security research (with permission)
- Brand/domain monitoring

---

## 📋 File Structure

```
ShadowRecon/
├── Documentation/
│   ├── README.md              ← Start here for features
│   ├── QUICKSTART.md          ← Quick reference
│   ├── SETUP.md               ← Installation guide
│   ├── TESTING.md             ← Testing procedures
│   ├── PROJECT_SUMMARY.md     ← Architecture
│   └── DEPLOYMENT.md          ← Production guide
│
├── Application/
│   ├── main.py                ← Run this: python main.py
│   ├── config.py              ← Settings & API keys
│   ├── utils.py               ← Helper functions
│   ├── requirements.txt       ← Dependencies
│   └── .env.example           ← Config template
│
├── Modules/
│   ├── modules/__init__.py
│   ├── modules/username.py
│   ├── modules/domain.py
│   ├── modules/ip.py
│   ├── modules/email.py
│   └── modules/reputation.py
│
├── Reporting/
│   └── report/__init__.py
│
└── Output/
    └── scans/                 ← Generated reports
```

---

## 🎓 Learning Path

### Beginner (Day 1)
- [ ] Read README.md
- [ ] Follow QUICKSTART.md
- [ ] Run python main.py
- [ ] Test with examples

### Intermediate (Day 2-3)
- [ ] Complete SETUP.md
- [ ] Add API keys
- [ ] Run each module
- [ ] Check generated reports

### Advanced (Week 1)
- [ ] Review PROJECT_SUMMARY.md
- [ ] Study module code
- [ ] Follow TESTING.md
- [ ] Customize/extend framework

### Production (Week 2+)
- [ ] Follow DEPLOYMENT.md
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Plan maintenance

---

## ⚡ Performance

| Operation | Time | Method |
|-----------|------|--------|
| Username search (10 platforms) | < 15s | Async/parallel |
| Domain check | 10-30s | Sequential |
| IP geolocation | < 5s | Single API |
| Email breach check | < 5s | Single API |
| Reputation check | < 5s | Single API |

---

## 📞 Common Questions

### Q: Do I need API keys?
**A:** No! Framework works without them. Add keys for enhanced features (Shodan, VirusTotal).

### Q: Is this legal?
**A:** Yes! Only collects public data. Follow local laws and get proper authorization.

### Q: What's the risk score?
**A:** 0-100 scale based on multiple threat indicators. See PROJECT_SUMMARY.md for details.

### Q: Can I integrate with other tools?
**A:** Yes! Check DEPLOYMENT.md for SIEM, ticketing, and Slack integration guides.

### Q: How do I update?
**A:** `pip install -r requirements.txt --upgrade`

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Issue: "API key invalid"
- Check .env file format (no spaces)
- Verify API key is still valid
- Check at provider's website

### Issue: "Connection timeout"
- Check internet connection
- Increase REQUEST_TIMEOUT in .env
- Try different network/VPN

### For More Help
See **TROUBLESHOOTING** section in [SETUP.md](SETUP.md)

---

## 🚀 Next Steps

1. **Start Here**: [QUICKSTART.md](QUICKSTART.md)
2. **Then Setup**: [SETUP.md](SETUP.md)
3. **Then Run**: `python main.py`
4. **Then Learn**: [README.md](README.md)
5. **Then Explore**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 📊 Quick Stats

- **Lines of Code**: 2,000+
- **Python Files**: 14
- **Documentation Pages**: 6
- **API Integrations**: 3 (optional)
- **Platforms Checked**: 10+
- **Core Features**: 5 modules
- **Advanced Features**: 10+

---

## ✅ Status

- **Version**: 1.0
- **Status**: ✅ Production Ready
- **Python**: 3.8+
- **License**: Educational/Security Research
- **Last Updated**: January 2026

---

## 📄 Quick Links

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Complete features & examples |
| [QUICKSTART.md](QUICKSTART.md) | Quick reference (10 min) |
| [SETUP.md](SETUP.md) | Installation guide |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Architecture & design |
| [TESTING.md](TESTING.md) | Testing procedures |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment |

---

## 🎯 Start Your OSINT Journey

**Ready to begin?** → Read [QUICKSTART.md](QUICKSTART.md)

**Want full details?** → Read [README.md](README.md)

**Need to install?** → Follow [SETUP.md](SETUP.md)

**Need to deploy?** → Check [DEPLOYMENT.md](DEPLOYMENT.md)

---

**ShadowRecon v1.0** | Advanced OSINT Framework | Ethical Intelligence Gathering

*Remember: Always use responsibly and legally. Unauthorized access is a crime.*

---

**Need help?** Check the documentation above or review the code comments for detailed explanations.

**Ready to start?** Run: `python main.py`

✅ Framework initialized and ready for deployment!
