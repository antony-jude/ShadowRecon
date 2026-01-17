"""
ShadowRecon - OSINT Framework v1.0
Complete Project Summary & Architecture

This file provides a comprehensive overview of the ShadowRecon framework.
"""

# ============================================================================
# PROJECT STRUCTURE
# ============================================================================

PROJECT_STRUCTURE = """
ShadowRecon/
│
├── 📄 Documentation Files
│   ├── README.md              - Complete feature documentation & usage guide
│   ├── SETUP.md               - Installation & configuration instructions  
│   ├── QUICKSTART.md          - Quick reference for common tasks
│   └── PROJECT_SUMMARY.md     - This file
│
├── 🔧 Core Configuration
│   ├── config.py              - Centralized configuration management
│   │   ├── API key management (Shodan, VirusTotal, HIBP)
│   │   ├── Feature flags (enable/disable modules)
│   │   ├── Timeout settings
│   │   ├── Platform list for username checks
│   │   └── Logging configuration
│   │
│   ├── .env.example           - Environment variable template (COPY AND EDIT)
│   │   ├── API keys
│   │   ├── Feature toggles
│   │   └── Timeout values
│   │
│   └── requirements.txt       - Python package dependencies
│       ├── aiohttp==3.9.1 (async HTTP)
│       ├── python-dotenv==1.0.0 (config)
│       ├── requests==2.31.0 (HTTP)
│       ├── dnspython==2.4.2 (DNS)
│       └── whois==0.9.7 (WHOIS)
│
├── 🛠️ Utility Module
│   └── utils.py               - Helper functions & utilities
│       ├── Email/domain/IP validation
│       ├── Risk scoring algorithm (0-100)
│       ├── Risk level classification (MINIMAL to CRITICAL)
│       ├── Timestamp formatting
│       ├── URL sanitization
│       ├── WHOIS parsing
│       ├── Result formatting
│       └── Analysis utilities
│
├── 📦 Core Modules (Intelligence Gathering)
│   │
│   └── modules/
│       │
│       ├── __init__.py        - Module imports & exports
│       │
│       ├── username.py        - Username Reconnaissance
│       │   ├── Async platform checking (GitHub, Twitter, Reddit, etc)
│       │   ├── 10+ platform support
│       │   ├── HTTP status interpretation
│       │   ├── Found/Not Found determination
│       │   ├── Summary statistics
│       │   └── Error handling per platform
│       │
│       ├── domain.py          - Domain Intelligence
│       │   ├── WHOIS lookup (registrar, dates, status)
│       │   ├── DNS resolution (A, MX, NS, TXT records)
│       │   ├── SSL certificate extraction
│       │   ├── Certificate validation
│       │   ├── Hosting IP identification
│       │   ├── Domain validation
│       │   └── Error handling
│       │
│       ├── ip.py              - IP Address Intelligence
│       │   ├── Geolocation lookup (country, city, ISP, timezone)
│       │   ├── Shodan integration (open ports, services, banners)
│       │   ├── ASN information extraction
│       │   ├── Organization lookup
│       │   ├── Service detection
│       │   ├── ISP/provider details
│       │   └── Optional API integration
│       │
│       ├── email.py           - Email Intelligence
│       │   ├── HaveIBeenPwned breach detection
│       │   ├── Breach database lookup
│       │   ├── Breach data classification
│       │   ├── Email domain validation
│       │   ├── MX record checking
│       │   ├── Clear breach status reporting
│       │   ├── Rate limiting awareness
│       │   └── Credential breach details
│       │
│       └── reputation.py      - Reputation & Threat Intelligence
│           ├── VirusTotal integration
│           ├── Malicious vendor detection
│           ├── Domain/IP reputation scoring
│           ├── URL analysis support
│           ├── Risk score calculation
│           ├── Threat level determination
│           ├── Threat recommendations
│           ├── Multi-vendor correlation
│           └── Categorization data extraction
│
├── 📊 Reporting Module
│   │
│   └── report/
│       │
│       └── __init__.py        - Report Generation & Analysis
│           ├── JSON report generation with metadata
│           ├── Timestamp tracking
│           ├── Findings analysis
│           ├── Risk indicator extraction
│           ├── Threat assessment
│           ├── HTML report generation
│           ├── Summary report creation
│           ├── Findings analysis per type (domain/IP/email/username)
│           ├── Risk assessment & recommendations
│           └── Extensible report formats
│
├── 🎯 Main Entry Point
│   │
│   └── main.py                - Interactive CLI Application
│       ├── Menu-driven interface
│       ├── User input validation
│       ├── Asynchronous operations handling
│       ├── Module orchestration
│       ├── Results display & formatting
│       ├── Report generation triggers
│       ├── Error handling & user feedback
│       ├── Logging integration
│       ├── Username reconnaissance (async)
│       ├── Domain reconnaissance
│       ├── IP reconnaissance
│       ├── Email reconnaissance
│       ├── Reputation checking
│       └── Graceful error handling
│
└── 📁 Output Directory (Auto-created)
    │
    └── scans/
        ├── username_*.json     - Username check reports
        ├── domain_*.json       - Domain intelligence reports
        ├── ip_*.json           - IP analysis reports
        ├── email_*.json        - Email breach reports
        ├── report_*.html       - HTML formatted reports
        └── *.log               - Execution logs
"""

# ============================================================================
# MODULE DESCRIPTIONS
# ============================================================================

MODULES_OVERVIEW = """
1. USERNAME RECONNAISSANCE (modules/username.py)
   ├─ Purpose: Identify username presence across social platforms
   ├─ Platforms: GitHub, Twitter, Reddit, Instagram, LinkedIn, YouTube, 
   │            TikTok, Medium, DeviantArt, Twitch
   ├─ Method: HTTP HEAD requests (async/concurrent)
   ├─ Output: Platform name, URL, status (FOUND/NOT FOUND), HTTP code
   ├─ Speed: Fast (async)
   ├─ API Required: No
   └─ Risk Score: Minimal (no direct threat)

2. DOMAIN RECONNAISSANCE (modules/domain.py)
   ├─ Purpose: Gather comprehensive domain intelligence
   ├─ Features:
   │  ├─ WHOIS: Registrar, creation/expiration dates, nameservers
   │  ├─ DNS: A records, MX records, NS records, TXT records
   │  ├─ SSL: Certificate issuer, subject, validity dates
   │  └─ Hosting: IP address, hosting provider
   ├─ Dependencies: whois, dnspython, ssl, socket
   ├─ Output: Structured domain intelligence
   ├─ Speed: Moderate (sequential)
   ├─ API Required: No
   └─ Risk Score: 0-50 points (based on SSL, open ports)

3. IP INTELLIGENCE (modules/ip.py)
   ├─ Purpose: Analyze IP addresses for threats & location
   ├─ Features:
   │  ├─ Geolocation: Country, city, ISP, timezone, coordinates
   │  ├─ Shodan: Open ports, services, banners, vulnerabilities
   │  ├─ ASN: Autonomous System Number, organization
   │  └─ Reputation: Organization details, provider info
   ├─ APIs: ip-api.com (free), Shodan (optional), ASNdb (optional)
   ├─ Output: Comprehensive IP threat profile
   ├─ Speed: Fast (parallel API calls)
   ├─ API Required: Shodan (optional, for port detection)
   └─ Risk Score: 0-100 (based on services, geolocation, reputation)

4. EMAIL RECONNAISSANCE (modules/email.py)
   ├─ Purpose: Detect if email has been in data breaches
   ├─ Features:
   │  ├─ HIBP: Known breach database lookup
   │  ├─ Breach Data: Breach name, date, affected data classes
   │  ├─ Credentials: Check for pwned passwords (optional)
   │  └─ Domain: Validate email domain & MX records
   ├─ API: HaveIBeenPwned (free tier)
   ├─ Output: Breach status, affected databases, risk level
   ├─ Speed: Fast (single API call)
   ├─ API Required: No (free tier available)
   └─ Risk Score: 0/30/75 (safe/unchecked/breached)

5. REPUTATION & THREAT INTEL (modules/reputation.py)
   ├─ Purpose: Determine if target is known malicious
   ├─ Features:
   │  ├─ VirusTotal: Malware detection, vendor consensus
   │  ├─ Reputation: Overall threat level
   │  ├─ Categories: Malware type, threat classification
   │  └─ Recommendations: Action items based on risk
   ├─ API: VirusTotal (requires API key)
   ├─ Output: Risk score, threat level, recommendations
   ├─ Speed: Fast (single API call)
   ├─ API Required: VirusTotal (critical for reputation)
   └─ Risk Score: 0-100 (based on vendor detections)
"""

# ============================================================================
# FEATURE MATRIX
# ============================================================================

FEATURE_MATRIX = """
╔════════════════════════╦═════════╦════════════╦═════════════════╗
║ Feature                ║ Status  ║ Requires   ║ Speed           ║
║                        ║         ║ API?       ║                 ║
╠════════════════════════╬═════════╬════════════╬═════════════════╣
║ Username Checks        ║ ✅      ║ No         ║ Fast (async)    ║
║ Domain WHOIS          ║ ✅      ║ No         ║ Moderate        ║
║ DNS Resolution        ║ ✅      ║ No         ║ Fast            ║
║ SSL Certificates      ║ ✅      ║ No         ║ Fast            ║
║ IP Geolocation        ║ ✅      ║ No         ║ Fast            ║
║ Email Breach Check    ║ ✅      ║ No*        ║ Fast            ║
║ Port Detection        ║ ✅      ║ Shodan     ║ Moderate        ║
║ Malware Scanning      ║ ✅      ║ VirusTotal ║ Fast            ║
║ Risk Scoring          ║ ✅      ║ No         ║ Instant         ║
║ Report Generation     ║ ✅      ║ No         ║ Instant         ║
║ HTML Reports          ║ ✅      ║ No         ║ Instant         ║
║ JSON Exports          ║ ✅      ║ No         ║ Instant         ║
║ Logging & Auditing    ║ ✅      ║ No         ║ Automatic       ║
╚════════════════════════╩═════════╩════════════╩═════════════════╝

* Free tier available for HaveIBeenPwned
"""

# ============================================================================
# RISK SCORING ALGORITHM
# ============================================================================

RISK_SCORING = """
Risk Score Calculation (0-100 scale):

1. SSL CERTIFICATE ASSESSMENT
   ├─ No SSL certificate found: +15 points
   ├─ Expired certificate: +10 points
   └─ Valid certificate: +0 points

2. OPEN PORTS & SERVICES (per port)
   ├─ Each open port detected: +3 points
   ├─ Known vulnerable service: +5 points
   └─ Maximum from ports: +20 points

3. DOMAIN/IP REPUTATION
   ├─ Per VirusTotal malicious vendor: +5 points
   ├─ Suspicious category flag: +10 points
   └─ Maximum from reputation: +50 points

4. EMAIL BREACH STATUS
   ├─ Email in breach database: +30 points
   ├─ Multiple breaches: +5 per breach (capped)
   └─ No breaches: +0 points

5. HIBP DETECTIONS
   ├─ Email found in HIBP: +25 points
   ├─ Multiple services: +5 per service
   └─ No detections: +0 points

FINAL SCORE = Sum of all factors (capped at 100)

Risk Levels:
├─ 0-19   = MINIMAL   (🟢 Safe)
├─ 20-39  = LOW       (🟢 Minor concerns)
├─ 40-59  = MEDIUM    (🟡 Monitor)
├─ 60-79  = HIGH      (🔴 Exercise caution)
└─ 80-100 = CRITICAL  (🔴 Block immediately)
"""

# ============================================================================
# API INTEGRATION GUIDE
# ============================================================================

API_INTEGRATION = """
OPTIONAL API KEYS FOR ENHANCED FEATURES

1. SHODAN (Open Port Detection)
   ├─ URL: https://www.shodan.io/
   ├─ Free Tier: Yes (limited)
   ├─ What it does: Finds open ports, services, vulnerabilities
   ├─ Setup: Add to .env: SHODAN_API_KEY=your_key
   ├─ Usage: Automatic in IP reconnaissance
   └─ Example output:
      {
        "open_ports": [22, 80, 443],
        "services": ["SSH", "HTTP", "HTTPS"]
      }

2. VIRUSTOTAL (Malware Detection)
   ├─ URL: https://www.virustotal.com/
   ├─ Free Tier: Yes (limited)
   ├─ What it does: Scans domains/IPs for malware
   ├─ Setup: Add to .env: VIRUSTOTAL_API_KEY=your_key
   ├─ Usage: Automatic in reputation checks
   └─ Example output:
      {
        "malicious_count": 5,
        "undetected_count": 65,
        "suspicious_count": 2
      }

3. HAVEIBEENPWNED (Breach Database)
   ├─ URL: https://haveibeenpwned.com/
   ├─ Free Tier: Yes (limited - no API key needed)
   ├─ What it does: Checks if email in known breaches
   ├─ Setup: Optional - Add to .env: HIBP_API_KEY=your_key
   ├─ Usage: Automatic in email reconnaissance
   └─ Example output:
      {
        "breach_status": "BREACHED",
        "breach_count": 3,
        "breaches": ["FirstDataBreach", "SecondBreach"]
      }

ALTERNATIVE/FALLBACK SERVICES:
├─ IP Geolocation: ip-api.com (free)
├─ WHOIS Lookup: whois.net (free)
├─ DNS Resolution: Google DNS (8.8.8.8)
└─ ASN Information: ASNdb.net (free)
"""

# ============================================================================
# USAGE WORKFLOWS
# ============================================================================

WORKFLOWS = """
COMMON OSINT WORKFLOWS

Workflow 1: PERSON INVESTIGATION
├─ Step 1: Username search
│  └─ Find all platforms where person has accounts
├─ Step 2: Email reconnaissance
│  ├─ Check if email is in breaches
│  └─ Validate email domain
├─ Step 3: Reputation check
│  └─ Determine overall risk profile
└─ Output: Comprehensive person profile with risk score

Workflow 2: DOMAIN INVESTIGATION
├─ Step 1: Domain reconnaissance
│  ├─ WHOIS data (registrar, dates, ownership)
│  ├─ DNS records (mail servers, nameservers)
│  ├─ SSL certificate (validity, issuer)
│  └─ Hosting information (IP, provider)
├─ Step 2: IP reconnaissance
│  ├─ Geolocation (country, city, ISP)
│  ├─ Open ports (requires Shodan API)
│  └─ Services (versions, vulnerabilities)
├─ Step 3: Reputation check
│  ├─ VirusTotal score
│  ├─ Known malware associations
│  └─ Threat categorization
└─ Output: Complete domain security assessment

Workflow 3: IP ADDRESS INVESTIGATION
├─ Step 1: IP reconnaissance
│  ├─ Geolocation (coordinates, timezone)
│  ├─ ISP/Organization (provider details)
│  ├─ Open ports and services
│  └─ Hosting provider identification
├─ Step 2: Reverse IP lookup
│  └─ Find domains hosted on same IP
├─ Step 3: Reputation assessment
│  ├─ Malware detection
│  ├─ Spam/phishing associations
│  └─ Risk scoring
└─ Output: IP threat assessment & related infrastructure

Workflow 4: SECURITY INCIDENT RESPONSE
├─ Step 1: Initial reconnaissance
│  ├─ Identify target (domain/IP/email)
│  └─ Gather basic intel
├─ Step 2: Detailed analysis
│  ├─ Infrastructure mapping
│  ├─ Service enumeration
│  └─ Breach history check
├─ Step 3: Risk assessment
│  ├─ Threat scoring
│  ├─ Recommendation generation
│  └─ Report generation
└─ Output: Incident investigation report
"""

# ============================================================================
# ETHICAL GUIDELINES
# ============================================================================

ETHICS = """
ETHICAL FRAMEWORK & LEGAL COMPLIANCE

✅ WHAT SHADOWRECON DOES (Ethical OSINT):
├─ Collects PUBLICLY AVAILABLE information only
├─ Uses authorized public APIs
├─ Respects Terms of Service
├─ Maintains audit logs of all activities
├─ Provides transparent reporting
└─ Enables responsible security research

❌ WHAT SHADOWRECON DOES NOT DO:
├─ Create malware or exploit code
├─ Perform unauthorized hacking
├─ Scrape private data
├─ Brute force passwords
├─ Launch attacks or scans
├─ Violate terms of service
└─ Access restricted systems

🔐 RESPONSIBLE DISCLOSURE:
├─ Only use on authorized targets
├─ Obtain written permission before testing
├─ Report findings through proper channels
├─ Allow time for remediation before disclosure
├─ Never publicly disclose vulnerabilities without permission
└─ Follow coordinated disclosure practices

⚖️ LEGAL COMPLIANCE:
├─ Comply with GDPR (EU privacy law)
├─ Comply with CCPA (California privacy law)
├─ Follow CFAA (US Computer Fraud Act)
├─ Respect local data protection laws
├─ Obtain proper authorization
└─ Document all activities for audit trail

📋 ACCEPTABLE USE CASES:
├─ Authorized security research
├─ Penetration testing (with permission)
├─ Competitive intelligence (public info only)
├─ Due diligence investigations
├─ Brand monitoring
├─ Threat intelligence gathering
└─ Educational/training purposes

❌ UNACCEPTABLE USE CASES:
├─ Unauthorized system access
├─ Privacy violations
├─ Competitive espionage
├─ Stalking or harassment
├─ Fraud or deception
├─ Malware creation
└─ Unauthorized network penetration
"""

# ============================================================================
# DEPLOYMENT & PRODUCTION CONSIDERATIONS
# ============================================================================

PRODUCTION = """
PRODUCTION DEPLOYMENT CHECKLIST

SECURITY:
├─ [ ] Use .env file for all credentials (never hardcode)
├─ [ ] Add .env to .gitignore
├─ [ ] Implement API rate limiting
├─ [ ] Use HTTPS for all external calls
├─ [ ] Validate/sanitize all user inputs
├─ [ ] Implement authentication for multi-user deployment
├─ [ ] Encrypt sensitive report data
└─ [ ] Regular security audits

PERFORMANCE:
├─ [ ] Use connection pooling for API calls
├─ [ ] Implement caching for repeated queries
├─ [ ] Monitor timeout settings
├─ [ ] Batch process large target lists
├─ [ ] Use async for parallel operations
├─ [ ] Monitor API rate limits
└─ [ ] Implement request queuing

RELIABILITY:
├─ [ ] Comprehensive error handling
├─ [ ] Graceful degradation (fallback APIs)
├─ [ ] API health checks
├─ [ ] Automatic retry logic with exponential backoff
├─ [ ] Data persistence/database backup
├─ [ ] Service monitoring/alerting
└─ [ ] Regular testing of critical functions

COMPLIANCE & AUDIT:
├─ [ ] Comprehensive logging of all activities
├─ [ ] Log retention policy (90+ days)
├─ [ ] Audit trail for all data access
├─ [ ] Terms of Service compliance
├─ [ ] Data retention policies
├─ [ ] Privacy policy alignment
└─ [ ] Regular compliance reviews

SCALABILITY:
├─ [ ] Consider microservices architecture
├─ [ ] Database for result storage
├─ [ ] Queue system for large batches
├─ [ ] Load balancing for API calls
├─ [ ] Distributed processing capability
└─ [ ] Monitoring and metrics collection
"""

# ============================================================================
# TROUBLESHOOTING & MAINTENANCE
# ============================================================================

MAINTENANCE = """
TROUBLESHOOTING & MAINTENANCE GUIDE

COMMON ISSUES & SOLUTIONS:

1. API Connection Errors
   Problem: "Connection refused" or "Timeout"
   Solutions:
   ├─ Check internet connectivity
   ├─ Verify API endpoint URLs are correct
   ├─ Check firewall/proxy settings
   ├─ Increase ASYNC_TIMEOUT in .env
   ├─ Try alternative API (fallback)
   └─ Check API service status

2. Invalid API Key Errors
   Problem: "401 Unauthorized" or "Invalid API key"
   Solutions:
   ├─ Verify key in .env file (no extra spaces)
   ├─ Check API key hasn't expired
   ├─ Regenerate key from service provider
   ├─ Verify correct API endpoint for key type
   └─ Check API key has required permissions

3. Rate Limiting
   Problem: "429 Too Many Requests"
   Solutions:
   ├─ Increase delay between requests
   ├─ Reduce concurrent requests
   ├─ Check API quota usage
   ├─ Upgrade API tier if available
   └─ Implement request queue

4. DNS Resolution Failures
   Problem: "Could not resolve domain"
   Solutions:
   ├─ Check domain spelling/validity
   ├─ Verify DNS connectivity
   ├─ Try different DNS server (8.8.8.8)
   ├─ Check if domain exists
   └─ Wait for DNS propagation

5. Memory Issues
   Problem: "Memory error" on large datasets
   Solutions:
   ├─ Process targets in smaller batches
   ├─ Reduce concurrent operations
   ├─ Clear old reports from scans/
   ├─ Increase system RAM
   └─ Implement pagination for results

MAINTENANCE TASKS:

Weekly:
├─ Review logs for errors
├─ Check API rate limits
├─ Verify API key still valid
└─ Test core functionality

Monthly:
├─ Update dependencies (pip install -r requirements.txt -U)
├─ Clean old reports (scans/ older than 90 days)
├─ Review security logs
├─ Test disaster recovery
└─ Update documentation

Quarterly:
├─ Security audit
├─ Performance optimization review
├─ API alternative evaluation
├─ Compliance review
└─ User access audit

Annual:
├─ Full penetration test
├─ Architecture review
├─ Dependency audit
├─ Capacity planning
└─ Security certifications update
"""

if __name__ == "__main__":
    print("ShadowRecon - OSINT Framework v1.0")
    print("Project Architecture & Documentation")
    print("\nRefer to individual markdown files for details:")
    print("- README.md: Complete feature documentation")
    print("- SETUP.md: Installation & configuration")
    print("- QUICKSTART.md: Quick reference guide")
