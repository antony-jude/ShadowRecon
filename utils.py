"""
ShadowRecon Utilities Module
Helper functions for OSINT operations and data processing
"""

import re
import logging
from urllib.parse import urlparse, quote
from datetime import datetime

logger = logging.getLogger("ShadowRecon")

class Utils:
    """Utility functions for OSINT framework"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_domain(domain):
        """Validate domain format"""
        pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$'
        return re.match(pattern, domain.lower()) is not None
    
    @staticmethod
    def validate_ip(ip):
        """Validate IPv4 address format"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_url(url):
        """Check if string is valid URL"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def calculate_risk_score(findings):
        """
        Calculate risk score (0-100) based on findings
        Higher score = higher risk
        """
        score = 0
        
        # Domain/IP reputation
        if findings.get("virustotal"):
            vt = findings["virustotal"]
            malicious_count = vt.get("malicious_count", 0)
            if malicious_count > 0:
                score += min(malicious_count * 5, 50)
        
        # Security indicators
        if not findings.get("ssl_certificate"):
            score += 15  # No SSL = higher risk
        
        if findings.get("open_ports"):
            open_port_count = len(findings["open_ports"])
            score += min(open_port_count * 3, 20)
        
        # Email breach
        if findings.get("breach_status") == "BREACHED":
            score += 30
        
        # HIBP found
        if findings.get("hibp_found"):
            score += 25
        
        # Cap at 100
        return min(score, 100)
    
    @staticmethod
    def get_risk_level(score):
        """Convert numeric risk score to human-readable level"""
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        elif score >= 20:
            return "LOW"
        else:
            return "MINIMAL"
    
    @staticmethod
    def format_timestamp():
        """Return formatted current timestamp"""
        return datetime.now().isoformat()
    
    @staticmethod
    def sanitize_username(username):
        """Remove special characters from username for URL encoding"""
        return quote(username, safe='')
    
    @staticmethod
    def parse_whois_output(whois_text):
        """Parse WHOIS output into key-value pairs"""
        if not whois_text:
            return {}
        
        data = {}
        for line in whois_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        
        return data
    
    @staticmethod
    def extract_domain_from_url(url):
        """Extract domain from full URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            # Remove 'www.' prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return url
    
    @staticmethod
    def format_results(data, title=None):
        """Pretty print results"""
        if title:
            logger.info(f"\n{'='*60}")
            logger.info(f"  {title}")
            logger.info(f"{'='*60}\n")
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    logger.info(f"{key}: {str(value)[:100]}...")
                else:
                    logger.info(f"{key}: {value}")
        else:
            logger.info(data)
