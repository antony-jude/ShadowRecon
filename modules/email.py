"""
ShadowRecon Email Reconnaissance Module
HaveIBeenPwned breach detection
"""

import requests
import logging
import time
from config import Config
from utils import Utils

logger = logging.getLogger("ShadowRecon")

class EmailRecon:
    """Email address reconnaissance and breach detection"""
    
    def __init__(self, email):
        if not Utils.validate_email(email):
            raise ValueError(f"Invalid email format: {email}")
        
        self.email = email.lower()
        self.results = {}
    
    def recon(self):
        """Execute full email reconnaissance"""
        logger.info(f"Starting email reconnaissance for: {self.email}")
        
        self.results = {
            "email": self.email,
            "timestamp": Utils.format_timestamp(),
            "hibp": self._check_hibp(),
            "domain_valid": self._validate_email_domain()
        }
        
        return self.results
    
    def _check_hibp(self):
        """Check HaveIBeenPwned for email breaches"""
        hibp_data = {
            "breach_status": "SAFE",  # Default to safe
            "breaches": [],
            "breach_count": 0,
            "pwned_passwords": False,
            "error": None
        }
        
        try:
            logger.debug(f"Checking HaveIBeenPwned for {self.email}")
            
            # HIBP API requires User-Agent header
            headers = {
                'User-Agent': 'ShadowRecon-OSINT/1.0 (Educational Purpose)'
            }
            
            # Check for account breaches
            response = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{self.email}",
                headers=headers,
                timeout=Config.REQUEST_TIMEOUT
            )
            
            # Rate limiting
            time.sleep(1.5)
            
            if response.status_code == 200:
                breaches = response.json()
                hibp_data["breaches"] = [
                    {
                        "name": b.get("Name"),
                        "title": b.get("Title"),
                        "date": b.get("BreachDate"),
                        "data_classes": b.get("DataClasses", []),
                        "pwned_count": b.get("PwnCount")
                    }
                    for b in breaches
                ]
                hibp_data["breach_count"] = len(breaches)
                
                if hibp_data["breach_count"] > 0:
                    hibp_data["breach_status"] = "BREACHED"
                    logger.warning(f"Email {self.email} found in {hibp_data['breach_count']} breach(es)")
                else:
                    hibp_data["breach_status"] = "NO BREACHES"
            
            elif response.status_code == 404:
                hibp_data["breach_status"] = "NO BREACHES"
                logger.debug(f"No breaches found for {self.email}")
            
            elif response.status_code == 429:
                hibp_data["error"] = "Rate limited by HIBP API"
                logger.warning("HIBP rate limit reached")
            
            elif response.status_code == 401:
                hibp_data["error"] = "HIBP API key invalid or not configured"
            
            else:
                hibp_data["error"] = f"HTTP {response.status_code}"
            
            # Check for pwned passwords (requires User-Agent)
            if hibp_data["breach_status"] != "ERROR":
                try:
                    pwd_response = requests.get(
                        f"https://haveibeenpwned.com/api/v3/pwnedpassword/{self.email}",
                        headers=headers,
                        timeout=Config.REQUEST_TIMEOUT
                    )
                    
                    if pwd_response.status_code == 200:
                        hibp_data["pwned_passwords"] = True
                except:
                    pass  # Optional check
        
        except requests.Timeout:
            hibp_data["error"] = "HIBP request timeout"
            logger.warning(f"HIBP timeout for {self.email}")
        
        except Exception as e:
            hibp_data["error"] = str(e)
            logger.warning(f"HIBP lookup error: {str(e)}")
        
        return hibp_data
    
    def _validate_email_domain(self):
        """Validate if email domain exists and has MX records"""
        domain_data = {
            "domain": self.email.split('@')[1],
            "valid": False,
            "has_mx_records": False,
            "error": None
        }
        
        try:
            import dns.resolver
            
            domain = domain_data["domain"]
            mx_records = dns.resolver.resolve(domain, 'MX')
            
            if mx_records:
                domain_data["valid"] = True
                domain_data["has_mx_records"] = True
                logger.debug(f"Email domain {domain} is valid")
        
        except ImportError:
            logger.debug("DNS module not available for domain validation")
        
        except Exception as e:
            domain_data["error"] = str(e)
            logger.debug(f"Domain validation error: {str(e)}")
        
        return domain_data
